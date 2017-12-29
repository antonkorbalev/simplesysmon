#!/usr/bin/python3

from flask import *
from conf import config as cfg
from lib import timemon as tm
from lib import info
import psutil
import datetime
import platform


# server health monitoring tool

app = Flask(cfg.server_name)


@app.route('/')
def index():
    active_since = datetime.datetime.fromtimestamp(psutil.boot_time())
    return render_template("index.html",
                           script_version=cfg.version,
                           active_since=active_since,
                           days_active=(datetime.datetime.now() - active_since).days,
                           system=platform.system(),
                           release=platform.release(),
                           version=platform.version(),
                           blocks=info.get_blocks())

print("Starting time monitor for", cfg.time_step, "s period")
tm.start()

print("Starting web server", cfg.server_name, "at", cfg.server_host, ":", cfg.server_port)
app.run(port=cfg.server_port, host=cfg.server_host)
