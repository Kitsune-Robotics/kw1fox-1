#!/bin/sh
set -e

# export FLASK_APP="~/app/app.py"



# flask db upgrade

cd app && gunicorn --bind 0.0.0.0:5000 app:app
