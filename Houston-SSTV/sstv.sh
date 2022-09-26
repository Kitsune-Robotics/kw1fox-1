#!/bin/bash

# Runs all the required fluff for spawning qsstv with notifing and stuff.

# Make tempdirs
mkdir -p /tmp/sstv_images

# Copy config file
cp /opt/radio/kw1fox-1/sstv/qsstv_9.0.conf ~/.config/ON4QZ/qsstv_9.0.conf

# Spawn qsstv
xinit -geometry =1280x960+0+0 -fn 8x13 -j -fg white -bg black qsstv -- -nocursor
