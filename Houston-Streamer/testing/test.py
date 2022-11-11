import ffmpeg
import numpy as np
import cv2 as cv

cam = cv.VideoCapture(0)

process = (
    ffmpeg.input(
        filename="pipe:",
        format="rawvideo",
        pixel_format="bgr24",
        s="1080x720",
        framerate=25,
    )
    .output("out.mp4")
    .overwrite_output()
    .run_async(pipe_stdin=True)
)

for i in range(100):
    # retval, image = cam.read()
    image = np.full((1080, 720, 3), 60, np.uint8)
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
