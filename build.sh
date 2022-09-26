#!/bin/bash

SHORT_REV=$(git rev-parse --short HEAD) docker-compose build
