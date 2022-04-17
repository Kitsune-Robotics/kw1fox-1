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

        # ffmpeg command

        # ffmpeg  --stream_loop -1 -re -i ~/INPUT_FILE -vcodec libx264 -profile:v main -preset:v medium -r 20 -g 60 -keyint_min 60 -sc_threshold 0 -b:v 2500k -maxrate 2500k -bufsize 2500k  -sws_flags lanczos+accurate_rnd -acodec aac -b:a 96k -ar 48000 -ac 2 -f flv rtmp://rtmp.robotstreamer.com/live/123?key=123"
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
        self.font = ImageFont.truetype(r"../../Resources/RadioFont.ttf", 20)

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

    def drawGraphics(self, image):
        """
        Draws graphics and sprites over
        a frame
        """

        frame = Image.new(mode="RGB", size=(1280, 720))

        # Scale and paste
        scaledSSTV = image[0].resize((960, 720), Image.ANTIALIAS)
        frame.paste(scaledSSTV)

        scaledWaveform = image[1].resize((1280 - 720, self.scrHeight), Image.ANTIALIAS)
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
        draw.text((970, 200), info, font=self.font, align="left", fill=(255, 0, 0, 255))

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

    # myStreamer.drawGraphics(Image.open("../../Resources/KW1FOX-1_320x240.png")).show()
    myStreamer.stream()

    # imgs = myStreamer.cropFrame(Image.open("../../Resources/screenshot.png"))
    # myStreamer.drawGraphics(imgs).show()
