from RobotStreamer import Streamer

from PIL import Image, ImageFont, ImageDraw, ImageChops


def test_graphics():
    robotStreamer = Streamer()

    scrshot = Image.open("../resources/screenshot.png")

    robotStreamer.drawGraphics(robotStreamer.cropFrame(scrshot)).save("_test/frame.png")

    assert 2 == 2
