FROM debian:latest

# Setup home
ARG HOME="/app"
ENV HOME=${HOME}

# Set the working directory to app home
WORKDIR ${HOME}

# Install virt frame buffer and qsstv deps
RUN apt update \
    && apt install -y xvfb qsstv pulseaudio

# For debugging
RUN apt install -y x11vnc
EXPOSE 5920

# Copy config files
# QSSTV
RUN mkdir -p .config/ON4QZ
COPY qsstv_9.0.conf .config/ON4QZ/qsstv_9.0.conf
# Pulse
COPY pulse-client.conf /etc/pulse/client.conf

# Copy in entrypoint
COPY entrypoint.sh entrypoint.sh

# Start!
ENTRYPOINT ./entrypoint.sh
