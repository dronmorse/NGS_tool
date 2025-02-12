#!/usr/bin/env python3

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():

    if request.method == "GET":

        x = "HOW ABOUT NOW"

        return render_template("index.html", x=x)