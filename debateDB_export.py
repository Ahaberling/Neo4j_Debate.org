from neo4j import GraphDatabase


driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "123"))

def extrac_complete(tx):
    tx.run("""CALL apoc.export.graphml.all('debate.org_full.graphml', {})""")

def extrac_friends(tx):
    #tx.run("""MATCH (a:User) WITH a AS users MATCH (n:User)-[r:FRIENDS_WITH]-(m:User) WITH r AS friends CALL apoc.export.graphml.data(users, friends, 'debate.org_friends.graphml', {}) YIELD file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data RETURN file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data""")
    #tx.run("""MATCH (a:User) WITH collect(a) AS users CALL apoc.export.graphml.data(users, [], 'debate.org_friends.graphml', {}) YIELD file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data RETURN file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data""")
    #tx.run("""MATCH (n:User)-[r:FRIENDS_WITH]-(m:User) WITH collect(n) AS users, collect(r) AS friendships CALL apoc.export.graphml.data(users + , friendships, 'debate.org_friends.graphml', {useTypes:true}) YIELD file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data RETURN file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data""")
    #tx.run("""MATCH (n: User) OPTIONAL MATCH (n: User)-[r:FRIENDS_WITH]-(m) With collect(n) as uuser, collect(r) as friendships CALL apoc.export.graphml.data(uuser, friendships, 'debate.org_test.graphml', {useTypes:true}) YIELD file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data RETURN file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data""")
    #tx.run("""MATCH (n: User) OPTIONAL MATCH (n:User)-[r:FRIENDS_WITH]-() WITH COLLECT(n) AS vertices, COLLECT(r) AS edges CALL apoc.export.graphml.data(vertices, edges, 'debate.org_test.graphml', {useTypes:true}) YIELD file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data RETURN file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data""")
    tx.run("""MATCH (n: User)-[r1:GIVES_ISSUES]-(m:Issues) OPTIONAL MATCH (n:User)-[r2:FRIENDS_WITH]-() WITH COLLECT(DISTINCT n) AS users, COLLECT(DISTINCT m) AS issues, COLLECT(r1) AS gives_issues, COLLECT(r2) AS firends_with CALL apoc.export.graphml.data(users + issues, gives_issues + firends_with, 'debate.org_with_issues.graphml', {useTypes:true}) YIELD file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data RETURN file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data""")
    #tx.run("""MATCH (n:User)-[r:FRIENDS_WITH]-(m:User) WITH collect(n)[..1000] AS users, collect(r)[..1000] AS friendships CALL apoc.export.graphml.data(users, friendships, 'debate.org_friends_withType_limit.graphml', {useTypes:true}) YIELD file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data RETURN file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data""")


with driver.session() as session:

    session.write_transaction(extrac_friends)