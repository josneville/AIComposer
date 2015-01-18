from flask import Flask, render_template, request, jsonify
import sys
import os
from algorithmv2 import Composition
import logging
from logging.handlers import RotatingFileHandler

comp = Composition()
app = Flask(__name__)

@app.route("/")
def main():
  return render_template("index.html")

@app.route("/compose/<note>")
def rhythm(note):
  intNote = int(note)
  comp.compose(intNote)
  return comp.convertToString()

@app.route("/delete/<location>")
def delete(location):
  comp.deleteAndRestart(int(location))
  return comp.convertToString()


if __name__ == "__main__":
  handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
  handler.setLevel(logging.INFO)
  app.logger.addHandler(handler)
  app.run()
