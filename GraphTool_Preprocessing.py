import graph_tool.all as gt
import numpy as np
import sys


######################
### Initialization ###
######################

np.set_printoptions(threshold=sys.maxsize)

g_raw = gt.load_graph('debate.org_with_issues_mod.graphml', fmt='graphml')
# DO NOT USE g_raw FOR ASSORTATIVITY ANALYSIS! It contains uni- and bilateral FRIENDS_WITH relations.
# This is intentional due to the optional privacy setting of friendships in debate.org. See report for details.
# g_raw contains nodes: User, Issues
# g_raw contains edges: FRIENDS_WITH, GIVES_ISSUES

approach1_bool = True
approach2_bool = True
approach3_bool = True
summary_bool = True


###########################
### Graph Preprocessing ###
###########################

# There are 3 kind of User nodes that are handled differently by each of the following approaches. Kind of User nodes in focus:
#A: User nodes with friendship visibility setting on PRIVATE AND     being nominated as friend by any other User node (jusitfied unidirectional edge)
#B: User nodes with friendship visibility setting on PRIVATE AND NOT being nominated as friend by any other User node (isolated)
#C: User nodes with friendship visibility setting on PUBLIC  AND     being nominated as friend by any other User node
#   AND and empty friends list (UNjusitfied unidirectional edge - faulty. These 331 edges must not exist. I assume this is caused by faulty data crawling/scraping)

g_raw_friend = gt.GraphView(g_raw, vfilt=lambda v: g_raw.vp.userID[v] != "")
# g_raw_friend contains nodes: Users; edges: FRIENDS_WITH

g_raw_issues = gt.GraphView(g_raw, vfilt=lambda v: g_raw.vp.issuesID[v] != "")
# g_raw_issues contains nodes: Users, Issues; edges: GIVES_ISSUES


#--- Approach 1: Keep all User nodes AND make A & C bidirectional ---#

if approach1_bool == True:

    print("Approach 1 - Keep all User nodes AND make A & C bidirectional")

    g_ap1 = g_raw
    tuplelist = list(map(tuple, g_raw_friend.get_edges()))

    no_e_before = len(g_ap1.get_edges())

    c = 0
    c_newE = 0
    c_max = len(g_raw_friend.get_edges())

    for e in g_raw_friend.get_edges():
        c = c + 1
        source = e[0]
        target = e[1]

        if (target, source) not in tuplelist: # target and source switched to create the missing edge in the opposite direction
            c_newE = c_newE + 1
            g_ap1.add_edge(target, source)

        if c % 10000 == 0:
            print(c, "/", c_max)

    print(c_max, "/", c_max)

    print("Unidirectional friend edges made bidirectional:", c_newE)
    print("Number of edges (Friendship & Issues) before making A & C bidirectional: ", no_e_before)
    print("Number of edges (Friendship & Issues) after making A & C bidirectional: ", len(g_ap1.get_edges()))

    g_ap1.save("Graph_Preprocessed_Approach1.graphml")

    g_ap1_friend = gt.GraphView(g_ap1, vfilt=lambda v: g_ap1.vp.userID[v] != "")
    g_ap1_issues = gt.GraphView(g_ap1, vfilt=lambda v: g_ap1.vp.issuesID[v] != "")



#--- Approach 2: Remove B AND make A & C bidirectional ---#

if approach2_bool == True:

    print("Approach 2 - Remove B AND make A & C bidirectional")

    g_ap2 = g_ap1

    vprop_approach2 = g_ap2.new_vertex_property("bool")
    g_ap2.vp.approach2 = vprop_approach2

    for v in g_ap2.get_vertices():
        g_ap2.vp.approach2[v] = True

    c = 0
    c_max = len(g_ap1_friend.get_vertices())

    for v in g_ap1_friend.get_vertices():
        c = c + 1
        if len(g_ap1_friend.get_all_neighbors(v)) <= 0:         # or "==False"
            if g_ap1_friend.vp.friend_privacy[v] == True:
                g_ap2.vp.approach2[v] = False

        if c % 10000 == 0:
            print(c, "/", c_max)

    print(c_max, "/", c_max)

    no_v_before = len(g_ap2.get_vertices())
    no_e_before = len(g_ap2.get_edges())

    g_ap2 = gt.GraphView(g_ap2, vfilt=lambda v: g_ap2.vp.approach2[v] == True)

    print("Number of nodes removed: ", no_v_before - len(g_ap2.get_vertices()))
    print("Number of edges removed: ", no_e_before - len(g_ap2.get_edges()))
    print("Number of nodes (User & Issues)       before removing B: ", no_v_before)
    print("Number of edges (Friendship & Issues) before removing B: ", no_e_before)
    print("Number of nodes (User & Issues)       after removing B: ", len(g_ap2.get_vertices()))
    print("Number of edges (Friendship & Issues) after removing B: ", len(g_ap2.get_edges()))

    g_ap2.save("Graph_Preprocessed_Approach2.graphml")

    g_ap2_friend = gt.GraphView(g_ap2, vfilt=lambda v: g_ap2.vp.userID[v] != "")
    g_ap2_issues = gt.GraphView(g_ap2, vfilt=lambda v: g_ap2.vp.issuesID[v] != "")


#--- Approach 3: Remove B & C AND make A bidirectional ---#

if approach3_bool == True:

    print("Approach 3 - Remove B & C AND make A bidirectional")

    g_ap3 = g_ap2

    vprop_approach3 = g_ap3.new_vertex_property("bool")
    g_ap3.vp.approach3 = vprop_approach3

    for v in g_ap3.get_vertices():
        g_ap3.vp.approach3[v] = True

    g_raw_friend_noPriv = gt.GraphView(g_raw_friend, vfilt=lambda v: g_raw.vp.friend_privacy[v] == False)  # 311 edges regarding C
    tuplelist = list(map(tuple, g_raw_friend_noPriv.get_edges()))

    c = 0
    c_newE = 0
    c_max = len(g_raw_friend_noPriv.get_edges())
    new_edges = []

    for e in g_raw_friend_noPriv.get_edges():
        c = c + 1
        source = e[0]
        target = e[1]

        if (target, source) not in tuplelist:
            c_newE = c_newE + 1
            g_ap3.vp.approach3[target] = False          # This results in 187 nodes labeled as False and later on exploded for the Graph image
                                                        # Of the 311 identified invalide edges (c_newE) some regard the same "target". Some nodes are
                                                        # Thereby labeled False multiple times
        if c % 10000 == 0:
            print(c, "/", c_max)

    print(c_max, "/", c_max)

    print("Number of nodes identified as C: ", c_newE)

    no_v_before = len(g_ap3.get_vertices())
    no_e_before = len(g_ap3.get_edges())

    g_ap3 = gt.GraphView(g_ap3, vfilt=lambda v: g_ap3.vp.approach3[v] == True)

    print("Number of nodes (User & Issues)       before removing C: ", no_v_before)
    print("Number of edges (Friendship & Issues) before removing C: ", no_e_before)
    print("Number of nodes (User & Issues)       after removing C: ", len(g_ap3.get_vertices()))
    print("Number of edges (Friendship & Issues) after removing C: ", len(g_ap3.get_edges()))
    # edges have been removed. 311 (unjustified unidirectional friendship) + 311 (made bidirectional in approach A) + 187 (gives Issues relation, since 197 nodes where removed)
    # = 849

    g_ap3.save("Graph_Preprocessed_Approach3.graphml")

    g_ap3_friend = gt.GraphView(g_ap3, vfilt=lambda v: g_ap3.vp.userID[v] != "")
    g_ap3_issues = gt.GraphView(g_ap3, vfilt=lambda v: g_ap3.vp.issuesID[v] != "")


# Todo DELETE RESPECTIVE ISSUES NODES FROM USERS DELETED IN APPROACH B AND C

#--- Summary ---#

if approach1_bool == True:

    print("Summary")

    print(g_ap1)
    print(g_ap2)
    print(g_ap3)

    print("\n AP1 - Number of nodes (User): ", len(g_ap1_friend.get_vertices()))
    print("AP1 - Number of edges (Friends): ", len(g_ap1_friend.get_edges()))

    print("\n AP2 - Number of nodes (User): ", len(g_ap2_friend.get_vertices()))
    print("AP2 - Number of edges (Friends): ", len(g_ap2_friend.get_edges()))

    print("\n AP3 - Number of nodes (User): ", len(g_ap3_friend.get_vertices()))
    print("AP3 - Number of edges (Friends): ", len(g_ap3_friend.get_edges()))


    print("\n AP1 - Number of nodes (Issues): ", len(g_ap1_issues.get_vertices()))
    print("AP1 - Number of edges (gives_Issues): ", len(g_ap1.get_edges())-len(g_ap1_friend.get_edges()))

    print("\n AP2 - Number of nodes (Issues): ", len(g_ap2_issues.get_vertices()))
    print("AP2 - Number of edges (gives_Issues): ", len(g_ap2.get_edges())-len(g_ap2_friend.get_edges()))

    print("\n AP3 - Number of nodes (Issues): ", len(g_ap3_issues.get_vertices()))
    print("AP3 - Number of edges (gives_Issues): ", len(g_ap3.get_edges())-len(g_ap3_friend.get_edges()))