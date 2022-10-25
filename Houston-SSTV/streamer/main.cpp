#include <opencv2/opencv.hpp>

#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <cstdint>
#include <cstring>
#include <vector>

#include <nadjieb/mjpeg_streamer.hpp>

// for convenience
using MJPEGStreamer = nadjieb::MJPEGStreamer;

int main()
{
    int Width = 0;
    int Height = 0;
    int Bpp = 0;
    std::vector<std::uint8_t> Pixels;
    std::vector<int> params = {cv::IMWRITE_JPEG_QUALITY, 90};

    // Create streamer
    MJPEGStreamer streamer;

    // Open display
    Display *display = XOpenDisplay(":60");
    if (display == NULL)
    {
        std::cerr << "Error opening display!\n";
        exit(EXIT_FAILURE);
    }
    Window root = DefaultRootWindow(display);

    // Get atributes
    XWindowAttributes attributes = {0};
    XGetWindowAttributes(display, root, &attributes);

    Width = attributes.width;
    Height = attributes.height;

    // Start the streamer
    streamer.start(8888);

    // Visit /shutdown or another defined target to stop the loop and graceful shutdown
    while (streamer.isRunning())
    {
        XImage *img = XGetImage(display, root, 0, 0, Width, Height, AllPlanes, ZPixmap);
        Bpp = img->bits_per_pixel;
        Pixels.resize(Width * Height * 4);

        if (img != NULL)
        {
            memcpy(&Pixels[0], img->data, Pixels.size());

            cv::Mat frame = cv::Mat(Height, Width, Bpp > 24 ? CV_8UC4 : CV_8UC3, &Pixels[0]);

            if (frame.empty())
            {
                std::cerr << "frame not grabbed\n";
                exit(EXIT_FAILURE);
            }

            // http://localhost:8080/bgr
            std::vector<uchar> buff_bgr;
            cv::imencode(".jpg", frame, buff_bgr, params);
            streamer.publish("/bgr", std::string(buff_bgr.begin(), buff_bgr.end()));

            cv::Mat hsv;
            cv::cvtColor(frame, hsv, cv::COLOR_BGR2HSV);

            // http://localhost:8080/hsv
            std::vector<uchar> buff_hsv;
            cv::imencode(".jpg", hsv, buff_hsv, params);
            streamer.publish("/hsv", std::string(buff_hsv.begin(), buff_hsv.end()));

            std::this_thread::sleep_for(std::chrono::milliseconds(10));
        }
    }

    // XDestroyImage(img);
    XCloseDisplay(display);

    streamer.stop();
}
