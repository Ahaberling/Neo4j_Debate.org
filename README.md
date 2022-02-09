# Neo4j_Debate.org
MMDS Individual Project 2020/2021

* Objective: Creating a *Neo4j* Graph Database containing a data sample of the online discourse platform *debate.org*. Additionally, conducting a brief Assortativity analysis of the collected user data. 
* Data used: http://www.cs.cornell.edu/~esindurmus/ddo.html
* Graph Database used: https://neo4j.com Version 4.1.1
* Network Analysis tool used: https://graph-tool.skewed.de
* Python version used: 3.7
* Further details: *\'Alexander_Haberling_Individual_Project.pdf\'*

## Instructions

1. debateDB_Creation.py \
	Extractes data from the Jsons provided by http://www.cs.cornell.edu/~esindurmus/ddo.html

2. Install APOC-Plugin for Neo4j https://neo4j.com/developer/neo4j-apoc/ (4.1.0.2 used in *\'debateDB_Exportation.py\'*)

3. debateDB_Exportation.py \
	Exports data as *GraphML*

4. Add the following two lines to the beginning of the resulting *GraphML*. This ensures a successful GraphTool import \
		\<key id="labels" for="node" attr.name="labels" attr.type="string"/> \
		\<key id="label" for="edge" attr.name="label" attr.type="string"/>

5. For Windows: Access *GraphTool* library via *Docker* https://graph-tool.skewed.de \
		docker pull tiagopeixoto/graph-tool

6. GraphTool_Preprocessing.py \
	Prepares data for further analysis

7. GraphTool_Descriptives.py \
	Provides a descriptive overview

8. GraphTool_Assortativity.py \
	Provides a brief assortativity analysis


