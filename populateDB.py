import neo4j
connection = neo4j.connect("http://localhost:7474")
cursor = connection.cursor()
#chords

c = {
  "chords" : [
    { "name" : "CMaj" },
    { "name" : "GMaj" },
    { "name" : "DMaj" },
    { "name" : "AMaj" },
    { "name" : "A13"}
  ]
}

cursor.execute("CREATE (n:Chord {chords}) ", **c)
connection.commit()

#Notes
n = {
  "notes" : [
    { "name" : "G" },
    { "name" : "G#" },
    { "name" : "A" },
    { "name" : "B" },
    { "name" : "B@" },
    { "name" : "C" },
    { "name" : "C#" },
    { "name" : "D" },
    { "name" : "E@" },
    { "name" : "E" },
    { "name" : "F" },
    { "name" : "F#" }
  ]
}

cursor.execute("CREATE (n:Note {notes}) ", **n)
connection.commit()

cursor.execute("MATCH (a:Note), (b:Chord {name: 'CMaj'}) WHERE a.name IN ['G', 'A', 'B', 'C', 'D', 'E', 'F'] CREATE (b)-[:CONTAINS]->(a)")
cursor.execute("MATCH (a:Note), (b:Chord {name: 'GMaj'}) WHERE a.name IN ['G', 'A', 'B', 'C', 'D', 'E', 'F#'] CREATE (b)-[:CONTAINS]->(a)")
cursor.execute("MATCH (a:Note), (b:Chord {name: 'DMaj'}) WHERE a.name IN ['G', 'A', 'B', 'C#', 'D', 'E', 'F#'] CREATE (b)-[:CONTAINS]->(a)")
cursor.execute("MATCH (a:Note), (b:Chord {name: 'AMaj'}) WHERE a.name IN ['G#', 'A', 'B', 'C#', 'D', 'E', 'F#'] CREATE (b)-[:CONTAINS]->(a)")
cursor.execute("MATCH (a:Note), (b:Chord {name: 'A13'}) WHERE a.name IN ['G', 'A', 'C', 'E', 'F'] CREATE (b)-[:CONTAINS]->(a)")
connection.commit()
