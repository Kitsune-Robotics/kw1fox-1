# RS Connector, replaces Houston-Streamer

import os
import sys
import time
import logging
import subprocess as sp

from PIL import Image

from subprocess import DEVNULL, PIPE, STDOUT
from PIL import Image, ImageFont, ImageDraw, ImageChops
from datetime import datetime

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
    "flv",
    "-flvflags",
    "no_duration_filesize",
    "rtmp://rtmp.robotstreamer.com/live/4619?key=UsXwgej5mtjyZJe",
]


# This is the ffmpeg pipe streamer!
ffmpeg = sp.Popen(ffmpegSettings, stdin=PIPE, stderr=STDOUT)

testImage = Image.open("testPattern.png")

while True:
    testImage.save(ffmpeg.stdin, "PNG")
