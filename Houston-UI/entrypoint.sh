#!/bin/bash

cd MissionController && gunicorn -b 0.0.0.0:8000 main:app
