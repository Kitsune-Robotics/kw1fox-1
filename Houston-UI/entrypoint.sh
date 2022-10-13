#!/bin/sh

export FLASK_APP="~/src/run.py"

set -e

flask db upgrade

gunicorn -c gunicorn.config.py wsgi:app
