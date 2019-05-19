import os
from flask import Flask
import settings as SETTINGS
from flask import render_template
import sys
sys.path.append("..")
from flask import request

import labeler as lr

import pandas as pd
import logging

app = Flask(__name__)

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.ERROR)

datasets_path = SETTINGS.PATHS["datasets"]

Lr = lr.Labeler(datasets_path, 1)

@app.route("/")
@app.route("/info")
def info():
    return render_template('info.html', datasets=Lr.datasets)

@app.route("/labeler")
def labeler():

    Lr.cursor_size = 1
    #Lr.current_position = 0
    Lr.cursor_next(True)

    context = {
        "datasets": Lr.datasets,
        "dataset": Lr.dataset,
        "cursor_current": Lr.current_position,
        "cursor": Lr.cursor_render()
    }

    return render_template('labeler.html', **context)


@app.route("/labeler/change_dataset")
def action_change_dataset():
    print(request.args)
    dataset = request.args.get('dataset')
    Lr.select_dataset(dataset)
    return ""

@app.route("/labeler/cursor_prev")
def action_cursor_prev():
    Lr.cursor_prev()
    return ""

@app.route("/labeler/cursor_next")
def action_cursor_next():
    Lr.cursor_next()
    return ""


@app.route("/viewer")
def viewer():

    Lr.cursor_size = 100
    #Lr.current_position = 0
    Lr.cursor_next(True)

    context = {
        "datasets": Lr.datasets,
        "dataset": Lr.dataset,
        "cursor_current": Lr.current_position,
        "cursor": Lr.cursor_render()
    }

    print(Lr.dataset.Y)

    return render_template('viewer.html', **context)