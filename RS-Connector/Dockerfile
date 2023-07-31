FROM debian:latest

# Setup home
ARG HOME="/app"
ENV HOME=${HOME}

# Set the working directory to app home
WORKDIR ${HOME}

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install deps
RUN apt update \
    && apt install -y gcc python3-dev python3-pip ffmpeg

# Python deps
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

ENTRYPOINT ./entrypoint.sh
