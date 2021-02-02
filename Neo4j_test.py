from neo4j import GraphDatabase
import json

driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "123"))

def add_user(tx):
    tx.run("MERGE (a:User {username: \"test_node\"})")

with driver.session() as session:
    session.write_transaction(add_user)