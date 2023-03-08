import sys
import time
import random
import threading

from flask import Flask, render_template
from turbo_flask import Turbo

from datetime import datetime, timedelta

import consts

app = Flask(__name__)
turbo = Turbo(app)


@app.context_processor
def inject_load():
    if sys.platform.startswith("linux"):
        with open("/proc/loadavg", "rt") as f:
            load = f.read().split()[0:3]
    else:
        load = [int(random.random() * 100) / 100 for _ in range(3)]
    return {"load1": load[0], "load5": load[1], "load15": load[2]}


@app.context_processor
def inject_status():
    now = datetime.now()
    epoch = datetime.fromtimestamp(consts.MISSION_EPOCH)

    missionTime = now - epoch

    return {
        "missionTime": f"T {str(missionTime).split('.')[0]}"
    }  # Clunky but trims off the microseconds


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/page2")
def page2():
    return render_template("page2.html")


@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()


def update_load():
    with app.app_context():
        while True:
            time.sleep(0.5)
            turbo.push(turbo.replace(render_template("loadavg.html"), "load"))
            turbo.push(
                turbo.replace(render_template("windows/statusbar.html"), "status")
            )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
