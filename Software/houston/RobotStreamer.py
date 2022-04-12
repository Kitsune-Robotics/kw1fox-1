import time
import subprocess as sp

from Xlib import display, X
from PIL import Image, ImageFont, ImageDraw


class Streamer:
    def __init__(self):
        self.x1, self.y1 = 580, 620

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
            "60",
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
        Returns a single cropped sstv video frame
        """

        raw = self.root.get_image(0, 0, self.x1, self.y1, X.ZPixmap, 0xFFFFFFFF)
        image = Image.frombytes("RGB", (self.x1, self.y1), raw.data, "raw", "BGRX")

        image = image.crop((0, 182, self.x1, self.y1))

        return image

    def drawGraphics(self, image: Image):
        """
        Draws graphics and sprites over
        a frame
        """

        frame = Image.new(mode="RGB", size=(1280, 720))

        # Scale and paste
        image = image.resize((960, 720), Image.ANTIALIAS)
        frame.paste(image)

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
        draw.text((960 + 10, 10), info, font=self.font, align="left")

        return frame

    def stream(self):
        """
        Actually streams!
        """

        while True:
            self.drawGraphics(self.getFrame()).save(self.pipe.stdin, "PNG")

    def __del__(self):
        self.dsp.close()

        self.pipe.stdin.close()
        self.pipe.wait()


if __name__ == "__main__":
    myStreamer = Streamer()

    # myStreamer.drawGraphics(Image.open("../../Resources/KW1FOX-1_320x240.png")).show()
    myStreamer.stream()
