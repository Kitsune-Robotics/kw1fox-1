#!/bin/bash

# Start audio
# export "PULSE_SERVER=unix:/tmp/pulsesocket" && pulseaudio --system &
direwolf &

# Wait for any process to exit
wait -n
  
# Exit with status of process that exited first
exit $?
