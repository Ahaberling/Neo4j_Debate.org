from neo4j import GraphDatabase


driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "123"))

def extrac_complete(tx):
    tx.run("""CALL apoc.export.graphml.all('debate.org_full.graphml', {})""")

def extrac_friends(tx):
    #tx.run("""MATCH (a:User) WITH a AS users MATCH (n:User)-[r:FRIENDS_WITH]-(m:User) WITH r AS friends CALL apoc.export.graphml.data(users, friends, 'debate.org_friends.graphml', {}) YIELD file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data RETURN file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data""")
    #tx.run("""MATCH (a:User) WITH collect(a) AS users CALL apoc.export.graphml.data(users, [], 'debate.org_friends.graphml', {}) YIELD file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data RETURN file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data""")
    tx.run("""MATCH (n:User)-[r:FRIENDS_WITH]-(m:User) WITH collect(n) AS users, collect(r) AS friendships CALL apoc.export.graphml.data(users, friendships, 'debate.org_friends.graphml', {}) YIELD file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data RETURN file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data""")


with driver.session() as session:

    session.write_transaction(extrac_friends)