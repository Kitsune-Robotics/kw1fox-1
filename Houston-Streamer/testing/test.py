import ffmpeg
import numpy as np
import cv2 as cv

cam = cv.VideoCapture(0)

width = 1080
height = 720

process = (
    ffmpeg.input(
        filename="pipe:",
        format="rawvideo",
        pixel_format="bgr24",
        s=f"{width}x{height}",
        framerate=25,
    )
    .output("out.mp4")
    .overwrite_output()
    .run_async(pipe_stdin=True)
)

for i in range(100):
    # retval, image = cam.read()
    image = np.full((width, height, 3), 60, np.uint8)
    ret, snap = cam.read()

    x_offset = y_offset = 50
    image[
        y_offset : y_offset + snap.shape[0], x_offset : x_offset + snap.shape[1]
    ] = snap
    cv.putText(
        image,
        "TEXT ON VIDEO " + str(i),
        (20, 50),
        cv.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2,
        cv.LINE_4,
    )  # Put a frame counter for showing progress.
    process.stdin.write(image.tobytes())
