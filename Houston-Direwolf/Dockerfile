FROM debian:latest

# Setup home
ARG HOME="/app"
ENV HOME=${HOME}

# Set the working directory to app home
WORKDIR ${HOME}

# Install deps to build direwolf
RUN apt update \
    && apt install -y git gcc g++ build-essential make cmake libasound2-dev libudev-dev

# Clone, build and install direwolf
RUN cd /tmp && \
    git clone https://www.github.com/wb2osz/direwolf && \
    cd direwolf && \
    git checkout dev && \
    mkdir build && cd build && \
    cmake .. && \
    make -j4 && \
    make install && \
    make install-conf

# Copy in config files
COPY direwolf.conf direwolf.conf

# Copy in entrypoint
COPY entrypoint.sh entrypoint.sh

# Start!
ENTRYPOINT ./entrypoint.sh
