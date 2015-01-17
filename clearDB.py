import neo4j
connection = neo4j.connect("http://localhost:7474")
cursor = connection.cursor()
cursor.execute("MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r")
connection.commit()

