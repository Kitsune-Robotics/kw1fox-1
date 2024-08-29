FROM debian:12

# Setup home directory
ARG HOME="/app"
ENV HOME=${HOME}

# Set the working directory to app home
WORKDIR ${HOME}

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Python, PostgreSQL development headers, and other dependencies
RUN apt update && \
    apt install -y python3 python3-venv python3-dev libpq-dev build-essential curl

# Create a virtual environment
RUN python3 -m venv venv

# Activate the virtual environment and upgrade pip
RUN . venv/bin/activate && pip install --upgrade pip

# Copy the requirements file and install Python dependencies in the virtual environment
COPY requirements.txt requirements.txt
RUN . venv/bin/activate && pip install -r requirements.txt

# Copy application code
COPY . .

# Expose the api port
EXPOSE 8501

# Healthcheck the server with a quick curl command
HEALTHCHECK CMD curl --fail http://localhost:8501/health || exit 1

# Entrypoint to activate the virtual environment and run the application
ENTRYPOINT ["/bin/bash", "-c", ". venv/bin/activate && python -u main.py"]
