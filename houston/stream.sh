#!/bin/bash

# Runs the robotstream
cd /opt/radio/kw1fox-1/houston/ && STREAMURL="rtmp://rtmp.robotstreamer.com/live/4619?key=jEquBubjizYDMQNe8nKjLdu88iqFpNe3sVQmGRJ2tzbxd4QJrkSSEZBQhi9UTL3k" pipenv run python RobotStreamer.py

