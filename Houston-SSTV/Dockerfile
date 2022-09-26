FROM debian:latest

# Install and update python + pip
# RUN pip install --upgrade pip

# Install other deps
RUN apt update \
    && apt install -y xvfb qsstv

# For debugging
RUN apt install -y x11vnc
EXPOSE 5920

# Setup home
ARG HOME="/app"
ENV HOME=${HOME}

# Set the working directory to app home
WORKDIR ${HOME}

# Copy config files
RUN mkdir -p .config/ON4QZ
COPY qsstv_9.0.conf .config/ON4QZ/qsstv_9.0.conf

# Copy in entrypoint
COPY entrypoint.sh entrypoint.sh

# Start!
ENTRYPOINT ./entrypoint.sh
