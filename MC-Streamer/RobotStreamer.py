import os
import sys
import time
import ffmpeg
import logging
import subprocess as sp
import utils.rsUtils as rsutil

# import importlib.util
# spec = importlib.util.spec_from_file_location(
#     "robot_util", "resources/robotstreamer/robot_util.py"
# )
# robot_util = importlib.util.module_from_spec(spec)

sys.path.append("utils/robotstreamer/")
import robot_util as robot_util

from subprocess import DEVNULL, PIPE, STDOUT
from PIL import Image, ImageFont, ImageDraw, ImageChops
from datetime import datetime

# from utils.controller import rsController


class Streamer:
    def __init__(self):
        # Stream/graphics
        self.streamWidth, self.streamHeight = 1280, 720

        # Logging/debug
        logging.basicConfig(level=logging.DEBUG)
        self.testImage = Image.open("resources/testPattern.jpg")

        # This holds the logs shown by the LogBox
        self.streamLog = []
        self.addLog("Houston-Streamer rebooted. Welcome to the stream!")
        self.lastLog = int(time.time())

        # Api data
        self.camera_id = "5505"
        self.api_server = "https://api.robotstreamer.com"
        endpointData = rsutil.getVideoEndpoint(self.api_server, self.camera_id)
        print(endpointData)

        # ffmpeg
        videoHost = endpointData["host"]
        videoPort = endpointData["port"]
        self.stream_key = os.environ.get("STREAMKEY")

        # Send camera alive
        robot_util.sendCameraAliveMessage(
            self.api_server, self.camera_id, self.stream_key
        )

        ffmpegSettings = [
            "ffmpeg",
            "-f",
            "image2pipe",
            "-vcodec",
            "png",
            "-r",
            "25",
            "-i",
            "-",  # Inject pil images here
            "-f",
            "mpegts",
            "-codec:v",
            "mpeg1video",
            "-b:v",
            "2500K",
            "-bf",
            "0",
            "-muxdelay",
            "0.001",
            f"http://{videoHost}:{videoPort}/{self.stream_key}/{self.streamWidth}/{self.streamHeight}/",
        ]

        print(
            f"http://{videoHost}:{videoPort}/***/{self.streamWidth}/{self.streamHeight}/"
        )

        # This is the ffmpeg pipe streamer!
        self.ffmpeg = sp.Popen(
            ffmpegSettings, stdin=PIPE, stderr=STDOUT, stdout=DEVNULL
        )

        # self.ffmpeg = (
        #     ffmpeg.input(
        #         filename="pipe:",
        #         format="rawvideo",
        #         pixel_format="bgr24",
        #         s="1080x720",
        #         framerate=25,
        #     )
        #     .output(
        #         f"http://{videoHost}:{videoPort}/{self.stream_key}/{self.streamWidth}/{self.streamHeight}/",
        #         format="mpegts",
        #         vcodec="mpeg1video",
        #     )
        #     .run_async(pipe_stdin=True)
        # )

        # Graphics and resources
        self.fontSize = 20  # This is easer than getting a tuple from ImageFont.getsize
        self.font = ImageFont.truetype(r"resources/RadioFont.ttf", self.fontSize)
        self.currentFrame = Image.new(
            mode="RGB", size=(self.streamWidth, self.streamHeight)
        )  # The currently displayed frame
        self.redrawFrame = True

        self.deleteme = int(time.time())

    def refreshStream(self):
        """
        Sets the redraw frame flag
        to tell the computer to redo
        the current frame.
        """

        self.redrawFrame = True

    def getFrame(self):
        """
        Returns a single full frame.
        """

        return self.testImage

    def addLog(self, newLog):
        # Add timestamp
        logTime = datetime.now().strftime("[%H:%M:%S] ")
        newLog = logTime + newLog

        self.streamLog.append(newLog)
        self.lastLog = int(time.time())

        if len(self.streamLog) > 12:
            self.streamLog.pop(0)

        self.refreshStream()

    def getLogBox(self):
        logboxWidth = 1000
        logboxHeight = len(self.streamLog) * self.fontSize + 20

        # Create a new logbox image
        logBox = Image.new(mode="RGBA", size=(logboxWidth, logboxHeight))

        # Draw on the logbox
        draw = ImageDraw.Draw(logBox)

        # Black background
        draw.rectangle([(0, 0), logBox.size], fill=(200, 200, 200))

        # Log text
        for log_index in range(len(self.streamLog)):
            draw.text(
                (0, log_index * self.fontSize),
                self.streamLog[log_index],
                font=self.font,
                align="left",
                fill=(255, 0, 0, 255),
            )

        drawLog = int(time.time()) - self.lastLog < 20

        return drawLog, logBox

    def drawGraphics(self, image):
        """
        Draws graphics and sprites over
        a frame
        """

        frame = Image.new(mode="RGB", size=(self.streamWidth, self.streamHeight))

        # Scale and paste the SSTV image
        scaledSSTV = image[0].resize((960, self.streamHeight), Image.Resampling.LANCZOS)
        frame.paste(scaledSSTV)

        # Scale and paste the waveform image
        scaledWaveform = image[1].resize(
            (self.streamWidth - 720, self.scrHeight), Image.Resampling.LANCZOS
        )
        frame.paste(scaledWaveform, (self.scrWidth - 65, 0))

        # Populate text, normally this should poll or use shared vars!
        info = f"""
KW1FOX-1
Online!
Volt: N/A
Last comm: {datetime.now().strftime("[%H:%M:%S]")}

KW1FOX-2
Offline.
Volt: N/A
Last comm: N/A

KW1FOX-3
Offline.
Volt: N/A
Last comm: {time.strftime("[%H:%M:%S]", time.localtime(self.lastLog))}

Currently Showing:
KW1FOX-1
NOCOM
NOMETA
"""

        # Draw text
        draw = ImageDraw.Draw(frame)
        draw.text(
            (970, 200),
            info,
            font=self.font,
            align="left",
            fill=(255, 0, 0, 255),
        )

        # Scale and paste the alerts/log window
        drawLogbox, scaledLogbox = self.getLogBox()
        if drawLogbox:
            logboxCenter = int(self.streamWidth / 2) - int(scaledLogbox.size[0] / 2)
            frame.paste(scaledLogbox, (logboxCenter, 200))

        return frame

    def stream(self):
        """
        Actually streams!
        """

        # Construct the robot controller, constructing it will autostart its run routine
        # self.controller = rsController(self)

        logging.info("Entering stream loop")

        while True:
            if self.redrawFrame:
                # Redraw frame if required
                self.currentFrame = self.getFrame()

            # Draw a frame into the ffmpeg pipe
            self.currentFrame.save(self.ffmpeg.stdin, "JPEG")
            # TODO: This could be optimized with some multithreading

            # Junk, delete me lol
            if int(time.time()) - self.deleteme > 10:
                """
                First off this should be a async scheduled function
                secondly, robot_util prints to stio witch is really annoying and dosent use logging!
                """
                self.deleteme = int(time.time())

                # Send camera alive
                robot_util.sendCameraAliveMessage(
                    self.api_server, self.camera_id, self.stream_key
                )

    # def __del__(self):
    #     self.pipe.stdin.close()
    #     self.pipe.wait()


if __name__ == "__main__":
    robotStreamer = Streamer()

    robotStreamer.stream()
