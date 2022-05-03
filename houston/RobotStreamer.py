import os
import time
import json
import logging
import subprocess as sp
import utils.rsUtils as rsutil
import utils.robot_utils as robot_util

from subprocess import DEVNULL, PIPE, STDOUT
from Xlib import display, X
from PIL import Image, ImageFont, ImageDraw, ImageChops


class Streamer:
    def __init__(self):
        # Display settings
        self.scrWidth, self.scrHeight = 1024, 768

        # Stream/graphics
        self.streamWidth, self.streamHeight = 1280, 720

        # Logging
        logging.basicConfig(level=logging.DEBUG)

        # Create display
        self.dsp = display.Display(":0")

        # This is the root of the screen
        self.root = self.dsp.screen().root

        # This holds the logs shown by the LogBox
        self.streamLog = ["Stream just started!", "Welcome!"]
        self.lastLog = int(time.time())

        # Api data
        self.camera_id = 5505
        self.api_server = "http://api.robotstreamer.com:8080"
        endpointData = rsutil.getVideoEndpoint(self.api_server, self.camera_id)

        # ffmpeg
        videoHost = endpointData["host"]
        videoPort = endpointData["port"]
        self.stream_key = os.environ.get("STREAMKEY")

        ffmpegSettings = f"ffmpeg -f image2pipe -vcodec png -r 25 -i - -f mpegts -codec:v mpeg1video -b:v 2500K -bf 0 -muxdelay 0.001 http://{videoHost}:{videoPort}/{self.stream_key}/{self.streamWidth}/{self.streamHeight}/"

        # This is the ffmpeg pipe streamer!
        self.pipe = sp.Popen(ffmpegSettings.split(), stdin=PIPE, stderr=STDOUT)

        # Send camera alive
        robot_util.sendCameraAliveMessage(
            self.api_server, self.camera_id, self.stream_key
        )

        # Graphics and resources
        self.fontSize = 20  # This is easer than getting a tuple from ImageFont.getsize
        self.font = ImageFont.truetype(r"../resources/RadioFont.ttf", self.fontSize)

        self.deleteme = int(time.time())

    def getFrame(self):
        """
        Returns a single full frame from the xorg display server.
        """

        raw = self.root.get_image(
            0, 0, self.scrWidth, self.scrHeight, X.ZPixmap, 0xFFFFFFFF
        )
        image = Image.frombytes(
            "RGB", (self.scrWidth, self.scrHeight), raw.data, "raw", "BGRX"
        )

        return image

    def cropFrame(self, image: Image):
        """
        Crops the full frame image into a waveform and an image display
        """

        sstvImage = image.crop((0, 182, 580, 620))

        waveformImage = image.crop((865, 30, self.scrWidth - 2, self.scrHeight - 74))

        return sstvImage, waveformImage

    def addLog(self, newLog):
        self.streamLog.append(newLog)
        self.lastLog = int(time.time())

        if len(self.streamLog) > 12:
            self.streamLog.pop(0)

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
        scaledSSTV = image[0].resize((960, self.streamHeight), Image.LANCZOS)
        frame.paste(scaledSSTV)

        # Scale and paste the waveform image
        scaledWaveform = image[1].resize(
            (self.streamWidth - 720, self.scrHeight), Image.LANCZOS
        )
        frame.paste(scaledWaveform, (self.scrWidth - 65, 0))

        # Populate text, normally this should poll or use shared vars!
        info = f"""
KW1FOX-1
Online!
Volt: N/A
Last comm: {int(time.time())}

KW1FOX-2
Offline.
Volt: N/A
Last comm: N/A

KW1FOX-3
Offline.
Volt: N/A
Last comm: {self.lastLog}

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

        while True:
            # Draw a frame into the ffmpeg pipe
            self.drawGraphics(self.cropFrame(self.getFrame())).save(
                self.pipe.stdin, "PNG"
            )

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

    def __del__(self):
        self.dsp.close()

        self.pipe.stdin.close()
        self.pipe.wait()


if __name__ == "__main__":
    robotStreamer = Streamer()

    robotStreamer.stream()

    # imgs = robotStreamer.cropFrame(Image.open("../../Resources/screenshot.png"))
    # robotStreamer.getLogs().show()
    # robotStreamer.drawGraphics(imgs).show()
