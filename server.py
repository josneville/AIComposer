from flask import Flask, render_template, request, jsonify
import sys
import os
from algorithmv2 import Composition
import logging
from logging.handlers import RotatingFileHandler

comp = Composition()
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = './static/images'

@app.route("/")
def main():
  return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    print request.files
    file = request.files['image']
    # Check if the file is one of the allowed types/extensions
    if file:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], "image.png"))
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], "image.png"))
        return "yes", 200

@app.route("/compose/<note>")
def rhythm(note):
  intNote = int(note)
  comp.compose(intNote)
  print comp.convertToString()
  return jsonify(vex=comp.convertToString(), tab=comp.tab)

@app.route("/restart", methods=['POST'])
def restart():
  if 'note' in request.json:
    note = request.json['note']
  else:
    return "Oh Nyo - Note", 400
  if 'index' in request.json:
    index = request.json['index']
  else:
    return "Oh Nyo - Index", 400

  comp.deleteAndRestart(int(index), int(note))
  return jsonify(vex=comp.convertToString(), tab=comp.tab)

@app.route("/arpeggio", methods=['POST'])
def arpeggio():
  comp.customArpeggio()
  print comp.convertToString()
  return jsonify(vex=comp.convertToString(), tab=comp.tab)

if __name__ == "__main__":
  handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
  handler.setLevel(logging.INFO)
  app.logger.addHandler(handler)
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)
