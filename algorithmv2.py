from __future__ import division
import neo4j
import random
import numpy
from math import floor, ceil
from rhythms import *
connection = neo4j.connect("http://localhost:7474")
cursor = connection.cursor()

class Composition:
  def __init__(self):
    self.tab = []
    self.rhythm = -1
    self.count = 0
    self.mainChord = []
    self.prevHalf = False
    self.max = 8
    self.currentMeasurement = []
    random.seed()

  def createRhythm(self):
    note = self.seedNote
    noteText = correlation[note % 12]
    #Use neo4j to find all chords nearby
    possibleChords = []
    for chord in cursor.execute("MATCH (a:Note {name: '"+noteText+"'})<-[:CONTAINS]-b RETURN b.name"):
      possibleChords.append(chord[0])

    #Pick one of them randomly and set as current cord
    if self.count == 0:
      self.mainChord = random.choice(possibleChords)
      self.count = self.count + 1
    elif self.count == 3:
      self.count = 0
    else:
      self.count = self.count + 1

    #Pick random rhythm
    if (self.rhythm == -1):
      mainRhythm = random.choice(rhythms)
      self.rhythm = rhythms.index(mainRhythm)
    else:
      if random.random() > 0.50 :
        if (self.prevHalf == True):
          mainRhythm = random.choice(rhythms[0:6])
          self.rhythm = rhythms.index(mainRhythm)
        else:
          mainRhythm = random.choice(rhythms)
          self.rhythm = rhythms.index(mainRhythm)
      else:
        mainRhythm = rhythms[self.rhythm]
    #Set first note as seedNote
    for duration in mainRhythm['notes']:
      ## For rests for bars
      noteText = correlation[note % 12]
      if (duration == 11 or duration == 13 or duration == 15):
        rest = ""
        keys = "b/4"
        if (duration == 11):
          rest = "8"
        if (duration == 13):
          rest = "q"
        if (duration == 15):
          rest = "h"
        self.currentMeasurement.append({"keys": keys, "duration": rest})
        continue

      if (duration == "|"):
        self.tab.append(self.currentMeasurement)
        self.currentMeasurement = []
        continue

      self.currentMeasurement.append({"keys": noteText, "duration": duration, "note": note})

      #Next note based weight
      newNotes = []
      for notes in cursor.execute("MATCH (b:Chord {name: '"+self.mainChord+"'})-[:CONTAINS]->a RETURN a.name"):
        newNotes.append(notes[0])
      change = (numpy.random.normal(0, 1.5, 1))[0]
      if (change < 0):
        change = int(ceil(change))
      else:
        change = int(floor(change))
      octave = floor(note / 12)
      newIndex = (newNotes.index(noteText) + change) % len(newNotes)
      newNoteText = newNotes[newIndex]
      if (newNotes.index(noteText) < newNotes.index(newNoteText) and change < 0):
        if octave != 0:
          octave = octave - 1
      elif (newNotes.index(noteText) > newNotes.index(newNoteText) and change > 0):
        if octave != 1:
          octave = octave + 1
      else:
        octave = octave
      note = int(correlation.index(newNoteText) + octave * 12)

    if (self.prevHalf):
      self.tab.append(self.currentMeasurement)
      self.currentMeasurement = []
      self.prevHalf = False
      self.seedNote = note
      if (len(self.tab) >= self.max):
        return
      self.arpeggio()
      return
    elif (mainRhythm['bar'] == "h"):
      self.prevHalf = True

    self.seedNote = note


  def arpeggio(self):
    if (random.random() > 0.25):
      return
    print "arpeggio: " + self.mainChord
    current = arpeggio[self.mainChord]
    for note in current:
      noteText = correlation[note % 12]
      self.currentMeasurement.append({"keys": noteText, "duration": "16", "note": note})
    self.tab.append(self.currentMeasurement)
    self.currentMeasurement = []

  def compose(self, seed):
    self.seedNote = seed
    while (len(self.tab) < self.max):
      self.createRhythm()

  def convertToString(self):
    text = ""
    counter = 0
    maxCounter = 0
    for measurement in self.tab:
      if (maxCounter >= self.max):
        break
      if (counter % 4 == 0):
        text = text + "\noptions space=20\ntabstave notation=true tablature=false time=4/4\nnotes"

      for note in measurement:
        if (note['keys'] == "b/4"):
          text = text + ":" + note['duration'] + " ## "
          continue
        if (note['note'] < 7):
          note['note']+=12
        text = text + ":" + note['duration'] + " " + note['keys'] + "/" + str(int(floor(note['note']/ 12)) + 3) + " "

      maxCounter += 1
      counter += 1
      text = text + " | "
    extraPadding = ""
    if (self.max % 4 != 0 and text != ""):
      extraPadding = ":w ## |" * (4 - (self.max%4))
    return text + extraPadding

  def deleteAndRestart(self, location, note):
    self.seedNote = note
    index = location - 1
    if (index == -1):
      self.tab = []
    else:
      self.tab = self.tab[:index]
    self.currentMeasurement = []
    self.max = int(ceil( (index + 8) / 8 )) * 8
    print self.max
    self.compose(self.seedNote)

if __name__ == "__main__":
  comp = Composition(10)
  comp.compose()
  comp.deleteAndRestart(5, 14)
