FROM python:3.11

LABEL maintainer="kenwood364@gmail.com"

WORKDIR /app

# Install python requirements
COPY requirements.txt /app
RUN pip install -r requirements.txt

# Copy the rest
COPY . /app

# Git commit
ARG GIT_COMMIT
ENV GIT_COMMIT=$GIT_COMMIT

EXPOSE 8080

ENTRYPOINT ["./entrypoint.sh"]
