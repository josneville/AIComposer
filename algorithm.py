import neo4j
import random
import numpy
from math import floor, ceil
from rhythms import rhythms, correlation
connection = neo4j.connect("http://localhost:7474")
cursor = connection.cursor()

class Composition:
  def __init__(self, seedNote):
    self.seedNote = seedNote
    self.tab = []
    self.rhythm = -1
    self.count = 0
    self.mainChord = []
    self.prevHalf = False

  def createRhythm(self):
    note = self.seedNote
    noteText = correlation[note % 12]
    newRhythm = []
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

    banana = False #its' the variable to add a bar at the end of two halves
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
      if (duration == 11 or duration == 13 or duration == 15 or duration == "|"):
        rest = ""
        keys = "b/4"
        if (duration == 11):
          rest = "8"
        if (duration == 13):
          rest = "q"
        if (duration == 15):
          rest = "h"
        if (duration == "|"):
          keys = "bar"
          rest = "|"
        newRhythm.append({"keys": keys, "duration": rest})
        continue

      newRhythm.append({"keys": note, "duration": duration})
      #Next note based weight
      newNotes = []
      for notes in cursor.execute("MATCH (b:Chord {name: '"+self.mainChord+"'})-[:CONTAINS]->a RETURN a.name"):
        newNotes.append(notes[0])
      change = (numpy.random.normal(0, 4, 1))[0]
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
        if octave != 2:
          octave = octave + 1
      else:
        octave = octave
      note = int(correlation.index(newNoteText) + octave * 12)
    if (self.prevHalf):
      newRhythm.append({"keys": "bar", "duration": "|"})
      self.prevHalf = False
    elif (mainRhythm['bar'] == "h"):
      self.prevHalf = True

    self.seedNote = note
    self.tab.append(newRhythm)

  def compose(self, numRhythms):
    for x in range(0, numRhythms):
      self.createRhythm()

  def convertToString(self):
    text = "options space=20"
    counter = 0
    for rhythm in self.tab:
      for note in rhythm:
        if (counter % 5 == 0):
          text = text + "\ntabstave notation=true tablature=false time=4/4\nnotes"
          counter += 1
        if (note['keys'] == "b/4"):
          text = text + ":" + note['duration'] + " ## "
          continue
        if (note['keys'] == "bar"):
          text = text + " | "
          counter += 1
          continue
        text = text + ":" + note['duration'] + " " + str(note['keys']) + "/" + str(int(floor(note['keys']/ 12)) + 3) + " "
    return text

if __name__ == "__main__":
  comp = Composition(17)
  comp.compose(50)
  print comp.convertToString()
