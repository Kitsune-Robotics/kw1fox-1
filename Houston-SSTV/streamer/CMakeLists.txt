cmake_minimum_required(VERSION 3.8)
project(HoustonSSTV-Streamer LANGUAGES CXX)

add_subdirectory(external/cpp-mjpeg-streamer)

find_package(OpenCV 4.2 REQUIRED)
find_package(X11 COMPONENTS X11 Xft)

add_executable(main ./main.cpp)
target_compile_features(main PRIVATE cxx_std_17)
target_link_libraries(main
    PRIVATE
    nadjieb_mjpeg_streamer::nadjieb_mjpeg_streamer
    ${OpenCV_LIBS}
    ${X11_LIBRARIES}
)
