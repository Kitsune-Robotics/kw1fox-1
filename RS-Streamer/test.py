import ffmpeg

(
    ffmpeg.input("../resources/testPattern.jpg", pattern_type="glob", framerate=25)
    .output("movie.mp4")
    .run()
)
