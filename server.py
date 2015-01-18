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
  return jsonify(vex=comp.convertToString(), tab=comp.tab)

@app.route("/restart", methods=['POST'])
def restart():
  if 'note' in request.form:
    note = request.form['note']
  else:
    return "Oh Nyo", 400
  if 'index' in request.form:
    index = request.form['index']
  else:
    return "Oh Nyo", 400

  comp.deleteAndRestart(int(index), int(note))
  return jsonify(vex=comp.convertToString(), tab=comp.tab)


if __name__ == "__main__":
  handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
  handler.setLevel(logging.INFO)
  app.logger.addHandler(handler)
  app.run()
