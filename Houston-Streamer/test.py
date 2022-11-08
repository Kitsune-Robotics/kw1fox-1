import os
import io
import sys
import time
import json
import logging
import subprocess as sp


from subprocess import DEVNULL, PIPE, STDOUT
from PIL import Image, ImageFont, ImageDraw, ImageChops
from datetime import datetime


testImage = Image.open("resources/testPattern.jpg")
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
    "out.mp4",
]

pipe = sp.Popen(ffmpegSettings, stdin=PIPE, stderr=STDOUT, stdout=DEVNULL)

for i in range(200):
    print(f"frame {i} out of 200")
    testImage.save(pipe.stdin, "JPEG")
    time.sleep(0.2)
