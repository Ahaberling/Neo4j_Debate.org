from neo4j import GraphDatabase

driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "123"))

def extrac_complete(tx):
    tx.run("""CALL apoc.export.graphml.all('debate.org_full.graphml', {})""")

def extrac_friends(tx):
    tx.run("""MATCH (n: User)-[r1:GIVES_ISSUES]-(m:Issues) OPTIONAL MATCH (n:User)-[r2:FRIENDS_WITH]-() WITH COLLECT(DISTINCT n) AS users, COLLECT(DISTINCT m) AS issues, COLLECT(r1) AS gives_issues, COLLECT(r2) AS firends_with CALL apoc.export.graphml.data(users + issues, gives_issues + firends_with, 'debate.org_with_issues.graphml', {useTypes:true}) YIELD file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data RETURN file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data""")

with driver.session() as session:

    #session.write_transaction(extrac_complete)
    session.write_transaction(extrac_friends)