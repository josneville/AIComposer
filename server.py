from flask import Flask, render_template, request, jsonify
import sys
import os
from algorithm import Composition
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

@app.route("/")
def main():
  return render_template("index.html")

@app.route("/rhythm/<note>")
def rhythm(note):
  intNote = int(note)
  comp = Composition(intNote)
  comp.compose(100)
  return comp.convertToString()


if __name__ == "__main__":
  handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
  handler.setLevel(logging.INFO)
  app.logger.addHandler(handler)
  app.run()
