"""Minimal flask app"""
from flask import Flask

"""Make the minimal application"""

app = FLASK(__name__)


"""Make the route--the decorator"""
@app.route("/")

"""define the function"""
def hello():
    return "Hello beautiful world!"

""" This file list constitutes the minimum viable app
    LICENSE  Pipfile  Pipfile.lock  README.md  hello.py
    """

"""Creating additional routes"""

@app.route("/about")
def preds():
    return "This is my about page!"