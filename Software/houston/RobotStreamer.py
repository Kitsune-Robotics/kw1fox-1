import time
import subprocess as sp

from Xlib import display, X
from PIL import Image, ImageFont, ImageDraw, ImageChops


class Streamer:
    def __init__(self):
        # Display settings
        self.scrWidth, self.scrHeight = 1024, 768

        # Create display
        self.dsp = display.Display(":0")

        # This is the root of the screen
        self.root = self.dsp.screen().root

        # This holds the logs shown by the LogBox
        self.streamLog = ["Stream just started!", "Welcome!"]
        self.lastLog = int(time.time())

        # ffmpeg
        cmd_out = [
            "ffmpeg",
            "-f",
            "image2pipe",
            "-vcodec",
            "png",
            "-r",
            "5",  # FPS
            "-i",
            "-",  # Indicated input comes from pipe
            "-vcodec",
            "libx264",
            "-profile:v",
            "main",
            "-pix_fmt",
            "yuv420p",
            "-preset:v",
            "medium",
            "-r",
            "30",
            "-g",
            "10",
            "-keyint_min",
            "60",
            "-sc_threshold",
            "0",
            "-b:v",
            "2500k",
            "-maxrate",
            "1500k",
            "-bufsize",
            "1500k",
            "-sws_flags",
            "lanczos+accurate_rnd",
            "-acodec",
            "aac",
            "-b:a",
            "96k",
            "-r",
            "6",
            "-ar",
            "48000",
            "-ac",
            "2",
            "-f",
            "flv",
            "rtmp://rtmp.robotstreamer.com/live/topkek",
        ]

        # This is the ffmpeg pipe streamer!
        self.pipe = sp.Popen(cmd_out, stdin=sp.PIPE)

        # Graphics and resources
        self.fontSize = 20  # This is easer than getting a tuple from ImageFont.getsize
        self.font = ImageFont.truetype(r"../../Resources/RadioFont.ttf", self.fontSize)

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

        if len(self.streamLog) > 10:
            self.streamLog.pop()

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
        streamWidth, streamHeight = 1280, 720

        frame = Image.new(mode="RGB", size=(streamWidth, streamHeight))

        # Scale and paste the SSTV image
        scaledSSTV = image[0].resize((960, streamHeight), Image.LANCZOS)
        frame.paste(scaledSSTV)

        # Scale and paste the waveform image
        scaledWaveform = image[1].resize(
            (streamWidth - 720, self.scrHeight), Image.LANCZOS
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
Last comm: N/A

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
            logboxCenter = int(streamWidth / 2) - int(scaledLogbox.size[0] / 2)
            frame.paste(scaledLogbox, (logboxCenter, 200))

        return frame

    def stream(self):
        """
        Actually streams!
        """

        while True:
            self.drawGraphics(self.cropFrame(self.getFrame())).save(
                self.pipe.stdin, "PNG"
            )

    def __del__(self):
        self.dsp.close()

        self.pipe.stdin.close()
        self.pipe.wait()


if __name__ == "__main__":
    myStreamer = Streamer()

    myStreamer.stream()

    # imgs = myStreamer.cropFrame(Image.open("../../Resources/screenshot.png"))
    # myStreamer.getLogs().show()
    # myStreamer.drawGraphics(imgs).show()
