import neo4j
connection = neo4j.connect("http://localhost:7474")
cursor = connection.cursor()
#chords

c = {
  "chords" : [
    { "name" : "CMaj" },
    { "name" : "GMaj" },
    { "name" : "DMaj" },
    { "name" : "GMin" },
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
    { "name" : "Gs" },
    { "name" : "A" },
    { "name" : "B" },
    { "name" : "Bf" },
    { "name" : "C" },
    { "name" : "Cs" },
    { "name" : "D" },
    { "name" : "Ef" },
    { "name" : "E" },
    { "name" : "F" },
    { "name" : "Fs" }
  ]
}

cursor.execute("CREATE (n:Note {notes}) ", **n)
connection.commit()

cursor.execute("MATCH (a:Note), (b:Chord {name: 'CMaj'}) WHERE a.name IN ['G', 'A', 'B', 'C', 'D', 'E', 'F'] CREATE (b)-[:CONTAINS]->(a)")
cursor.execute("MATCH (a:Note), (b:Chord {name: 'GMaj'}) WHERE a.name IN ['G', 'A', 'B', 'C', 'D', 'E', 'Fs'] CREATE (b)-[:CONTAINS]->(a)")
cursor.execute("MATCH (a:Note), (b:Chord {name: 'DMaj'}) WHERE a.name IN ['G', 'A', 'B', 'Cs', 'D', 'E', 'Fs'] CREATE (b)-[:CONTAINS]->(a)")
cursor.execute("MATCH (a:Note), (b:Chord {name: 'GMin'}) WHERE a.name IN ['G', 'A', 'Bf', 'C', 'D', 'Ef', 'F'] CREATE (b)-[:CONTAINS]->(a)")
cursor.execute("MATCH (a:Note), (b:Chord {name: 'AMaj'}) WHERE a.name IN ['Gs', 'A', 'B', 'Cs', 'D', 'E', 'Fs'] CREATE (b)-[:CONTAINS]->(a)")
cursor.execute("MATCH (a:Note), (b:Chord {name: 'A13'}) WHERE a.name IN ['G', 'A', 'C', 'E', 'F'] CREATE (b)-[:CONTAINS]->(a)")
connection.commit()
