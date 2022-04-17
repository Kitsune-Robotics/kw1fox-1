from Xlib import display, X
from PIL import Image

scrHeight = 1024
scrWidth = 768

dsp = display.Display(":0")
root = dsp.screen().root


raw = root.get_image(0, 0, scrHeight, scrWidth, X.ZPixmap, 0xFFFFFFFF)
image = Image.frombytes("RGB", (scrHeight, scrWidth), raw.data, "raw", "BGRX")
image.save("screenshot.png")
