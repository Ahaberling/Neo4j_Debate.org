# Neo4j_Debates.org
MMDS Individual Project 2020

Data used: 		"http://www.cs.cornell.edu/~esindurmus/ddo.html"
Graph Database used: 	"https://neo4j.com


1. debateDB_Creation.py
	Extractes data from the Jsons provided by "http://www.cs.cornell.edu/~esindurmus/ddo.html"

2. debateDB_Exportation.py
	Exports data as graphml

3. Add following to the resulting graphml (by hand). This ensures a successful GraphTool import
		<key id="labels" for="node" attr.name="labels" attr.type="string"/>
		<key id="label" for="edge" attr.name="label" attr.type="string"/>

4. For Windows: Access GraphTool library via Docker "https://graph-tool.skewed.de"
		docker pull tiagopeixoto/graph-tool

5. GraphTool_Preprocessing.py
	Prepares data for further analysis

6. GraphTool_Descriptives.py
	Provides a descriptive overview

7. GraphTool_Assortativity.py
	Provides a brief assortativity analysis


