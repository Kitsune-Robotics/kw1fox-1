#!/bin/bash

# Start xfvb
Xvfb :60 -screen 0 1920x1080x24 &

# Start audio
# export "PULSE_SERVER=unix:/tmp/pulsesocket" && pulseaudio --system &

# Start qsstv
export DISPLAY=:60 && qsstv &

# Start videostreamer
./streamer_binary &

# For testing
# x11vnc -passwd iamnotacrook -display :60 -N -forever &

# Wait for any process to exit
wait -n
  
# Exit with status of process that exited first
exit $?
