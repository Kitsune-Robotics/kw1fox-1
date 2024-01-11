"""
Leverages robotstreamer to deliver control input to the robot
"""

import time
import json
import _thread
import asyncio
import logging
import traceback
import threading
import websockets

from robotstreamer_utils.controller import getControlHost

from enum import Enum


class Command(Enum):
    STBY = 0  # Standby
    FWD = 1  # Forward
    BACK = 2  # Backward
    STAR = 3  # Starboard (right of screen)
    PORT = 4  # Port (left of screen)
    META = 5  # Send metadata
    IMGB = 6  # Black and white image
    IMGC = 7  # Color image


class rsController:
    def __init__(self, streamer):
        """
        rsController will produce one command and one only at a time.
        Its up to the robotstreamer application to find the time to read it,
        and then 'excecute it' (whatever that means depending on the command)

        This method should take care of the 'voting' system
        """

        self.streamer = streamer

        self.cmd = Command.STBY
        self.isDone = True

        self.streamer.addLog("rsController Connected.")

        # Start her up!
        _thread.start_new_thread(self.run, ())

    def getCommand(self):
        """
        Returns the command currently scheduled to be excecuted
        """
        return (self.cmd, self.isDone)

    def finishCommand(self):
        """
        Updates the status of the audience requested command
        """
        self.isDone = True

    def run(self):
        """
        Run!
        """

        logging.debug("Pausing for a second")
        time.sleep(2)

        while True:
            logging.info("Control loop started")

            try:
                asyncio.new_event_loop().run_until_complete(
                    self.handleControlMessages()
                )
            except:
                print("CONTROL: error")
                traceback.print_exc()

            logging.warn("Event loop handler died!")

            time.sleep(2)  # Dont rapid reconnect

    async def handleControlMessages(self):
        """
        From:
        https://github.com/robotstreamer/robotstreamer/blob/2f89d9acbca949ab0a9e2f8229da8c2cc1ffb26b/controller.py#L380
        """

        host = getControlHost(camera_id=self.streamer.camera_id)

        url = "%s://%s:%s/echo" % (
            host["protocol"],
            host["host"],
            host["port"],
        )  # TODO: Clean me!
        # logging.debug("control url:", url)

        async with websockets.connect(url) as websocket:
            # logging.debug("control websocket object:", websocket)

            if host["protocol"] == "wss":
                # validation handshake new
                await websocket.send(
                    json.dumps(
                        {
                            "type": "robot_connect",
                            "robot_id": self.streamer.camera_id,
                            "stream_key": self.streamer.stream_key,
                        }
                    )
                )
                logging.info("Validated with the new handshake")
                self.streamer.addLog("Controller reconnected.")
            else:
                # validation handshake old
                await websocket.send(json.dumps({"command": self.streamer.stream_key}))
                logging.info("Validated with the old handshake")

            while True:
                logging.debug("awaiting control message")

                message = await websocket.recv()
                logging.debug(f"Got a new message: {message}")

                j = json.loads(message)
                print("Control message: ", j)

                if j.get("command") == "RS_PONG":
                    print("PONG")
                if j.get("type") == "RS_PING":
                    print("PING")
