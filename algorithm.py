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

  def createRhythm(self):
    note = self.seedNote
    noteText = correlation[note % 12]
    #Use neo4j to find all chords nearby
    possibleChords = []
    for chord in cursor.execute("MATCH (a:Note {name: '"+noteText+"'})<-[:CONTAINS]-b RETURN b.name"):
      possibleChords.append(chord[0])

    #Pick one of them randomly and set as current cord
    mainChord = random.choice(possibleChords)

    #Pick random rhythm
    mainRhythm = random.choice(rhythms)

    #Set first note as seedNote
    for duration in mainRhythm:
      if (duration == 11 or duration == 13 or duration == 15):
        rest = ""
        if (duration == 11):
          rest = "8"
        if (duration == 13):
          rest = "q"
        if (duration == 15):
          rest = "h"
        self.tab.append({"keys": "b/4", "duration": rest})
        continue

      self.tab.append({"keys": note, "duration": duration})
      #Next note based weight
      newNotes = []
      for notes in cursor.execute("MATCH (b:Chord {name: '"+mainChord+"'})-[:CONTAINS]->a RETURN a.name"):
        newNotes.append(notes[0])
      change = (numpy.random.normal(0, 2, 1))[0]
      if (change < 0):
        change = int(ceil(change))
      else:
        change = int(floor(change))
      octave = floor(note / 12)
      newIndex = (newNotes.index(noteText) + change) % 7
      newNoteText = newNotes[newIndex]
      if (newNotes.index(noteText) < newNotes.index(newNoteText) and change < 0):
        if octave != 0:
          octave = octave - 1
      elif (newNotes.index(noteText) > newNotes.index(newNoteText) and change > 0):
        if octave != 2:
          octave = octave + 1
      else:
        octave = octave
      note = int(newIndex + octave * 12)

    return self.tab

  def convertToString(self):
    tab = self.tab
    print tab
    notes = "options space=20\ntabstave notation=true tablature=false time=4/4\nnotes "
    for note in tab:
      if (note['keys'] == "b/4"):
        notes += ":" + note['duration'] + " ## "
        continue
      notes = notes + ":" + note['duration'] + " " + str(note['keys']) + "/" + str(int(floor(note['keys']/ 12)) + 3) + " "
    return notes
if __name__ == "__main__":
  comp = Composition(17)
  comp.createRhythm()
  print comp.convertToString()
