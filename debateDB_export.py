from neo4j import GraphDatabase


driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "123"))

def extrac_complete(tx):
    tx.run("""CALL apoc.export.graphml.all('debate.org_full.graphml', {})""")

def extrac_friends(tx):
    tx.run("""MATCH (a:User) MATCH (n:User)-[r:FRIENDS_WITH]-(m:User) WITH n AS nodes, r AS relations CALL apoc.export.graphml.data(nodes, relations, 'debate.org_friends.graphml', {})""")


with driver.session() as session:

    session.write_transaction(extrac_friends)