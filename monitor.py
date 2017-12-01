#!/usr/bin/python3

from flask import Flask
from conf import config as cfg
from lib import pagegenerator as pg
from lib import  timemon as tm

# server health monitoring tool

app = Flask(cfg.server_name)


@app.route('/')
def index():
    return pg.get_index()

print("Starting time monitor for", cfg.time_step, "s period")
tm.start()

print("Starting web server", cfg.server_name, "at", cfg.server_host, ":", cfg.server_port)
app.run(port=cfg.server_port, host=cfg.server_host)
