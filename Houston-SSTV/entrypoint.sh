#!/bin/bash

# Start xfvb
Xvfb :60 -screen 0 1920x1080x16 &

# Start qsstv
export DISPLAY=:60 && qsstv &

# For testing
x11vnc -passwd iamnotacrook -display :60 -N -forever &

# Wait for any process to exit
wait -n
  
# Exit with status of process that exited first
exit $?
