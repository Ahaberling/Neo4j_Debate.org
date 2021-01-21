import graph_tool.all as gt
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
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

descBroad_bool = True
descDens_bool = True
descAvgD_bool = True
descDDist_bool = True
descCCG_bool = True

###########################
### Graph Preprocessing ###
###########################

# There are 3 kind of User nodes that are handled differently by each of the following approaches. Kind of User nodes in focus:
#A: User nodes with friendship visibility setting on PRIVATE AND     being nominated as friend by any other User node (jusitfied unidirectional edge)
#B: User nodes with friendship visibility setting on PRIVATE AND NOT being nominated as friend by any other User node (isolated)
#C: User nodes with friendship visibility setting on PUBLIC  AND     being nominated as friend by any other User node
#   AND and empty friends list (UNjusitfied unidirectional edge - faulty. These 331 nodes must not exist. I assume this is caused by faulty data crawling/scraping)

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

    print("Number of nodes (User & Issues)       before removing B: ", no_v_before)
    print("Number of edges (Friendship & Issues) before removing B: ", no_e_before)
    print("Number of nodes (User & Issues)       after removing B: ", len(g_ap2.get_vertices()))
    print("Number of edges (Friendship & Issues) after removing B: ", len(g_ap2.get_edges()))

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
            g_ap3.vp.approach3[target] = False

        if c % 10000 == 0:
            print(c, "/", c_max)

    print(c_max, "/", c_max)

    print("Number of nodes identified as C: ", c_newE)

    no_v_before = len(g_ap3.get_vertices())
    no_v_before = len(g_ap3.get_edges())

    g_ap3 = gt.GraphView(g_ap3, vfilt=lambda v: g_ap3.vp.approach3[v] == True)

    print("Number of nodes (User & Issues)       before removing C: ", no_v_before)
    print("Number of edges (Friendship & Issues) before removing C: ", no_v_before)
    print("Number of nodes (User & Issues)       after removing C: ", len(g_ap3.get_vertices()))
    print("Number of edges (Friendship & Issues) after removing C: ", len(g_ap3.get_edges()))

    g_ap3_friend = gt.GraphView(g_ap3, vfilt=lambda v: g_ap3.vp.userID[v] != "")
    g_ap3_issues = gt.GraphView(g_ap3, vfilt=lambda v: g_ap3.vp.issuesID[v] != "")


####################
### Descriptives ###
####################

### Deskriptives Friendship Network ###

#-- Number of nodes , edges, node properties, edge properties --#
if descBroad_bool == True:
    print("Desciptives: Broad - print(Graph Object) style")

    print("g_raw, g_raw_friend, g_raw_issues")
    print(g_raw)                        #  vertices and  edges,  internal vertex properties, 2 internal edge properties
    print(g_raw_friend)                 #  vertices and  edges,  internal vertex properties, 2 internal edge properties
    print(g_raw_issues)                 #  vertices and  edges,  internal vertex properties, 2 internal edge properties

    if approach1_bool == True:
        print("g_ap1, g_ap1_friend, g_ap1_issues")
        print(g_ap1)                    #  vertices and  edges,  internal vertex properties, 2 internal edge properties
        print(g_ap1_friend)             #  vertices and  edges,  internal vertex properties, 2 internal edge properties
        print(g_ap1_issues)             #  vertices and  edges,  internal vertex properties, 2 internal edge properties

    if approach2_bool == True:
        print("g_ap2, g_ap2_friend, g_ap2_issues")
        print(g_ap2)                    #  vertices and  edges,  internal vertex properties, 2 internal edge properties
        print(g_ap2_friend)             #  vertices and  edges,  internal vertex properties, 2 internal edge properties
        print(g_ap2_issues)             #  vertices and  edges,  internal vertex properties, 2 internal edge properties

    if approach3_bool == True:
        print("g_ap3, g_ap3_friend, g_ap3_issues")
        print(g_ap3)                    #  vertices and  edges,  internal vertex properties, 2 internal edge properties
        print(g_ap3_friend)             #  vertices and  edges,  internal vertex properties, 2 internal edge properties
        print(g_ap3_issues)             #  vertices and  edges,  internal vertex properties, 2 internal edge properties


#-- Density of Friendship Network --#
if descDens_bool == True:

    print("Desciptives: Density - only for friendship network of approach1 - g_ap1_friend")

    v_friendship = g_ap1_friend.get_vertices()
    e_friendship = g_ap1_friend.get_edges()
    d_friendship = len(e_friendship) / ((len(v_friendship) * (len(v_friendship)-1))/2)

    print("Number of Nodes (g_ap1_friend): ", len(v_friendship))   #
    print("Number of Edges (g_ap1_friend): ", len(e_friendship))   #
    print("Density (g_ap1_friend): ", d_friendship)                #


#-- Avg Degree --#
if descAvgD_bool == True:

    print("Desciptives: Avg Degree - only for friendship network of approach1 - g_ap1_friend")

    degree_list = g_ap1_friend.get_in_degrees(g_ap1_friend.get_vertices())

    print("Sum of all Degrees / Number of Edges: ",    sum(degree_list)) #
    print("Maximum of all Degrees: ",                  max(degree_list)) #
    print("Minimum of all Degrees: ",                  min(degree_list)) #
    print("Length of Degree List / Number of Nodes: ", len(degree_list)) #

    print("Avg Degree: ", sum(degree_list) / len(degree_list))
    print("Median Degree: ", np.median(degree_list))
    print("Mode Degree: ", stats.mode(degree_list)[0][0])

    degree_list = g_ap1_friend.get_out_degrees(g_ap1_friend.get_vertices())

    print("TEST WITH OUTDEGREE. MUST BE SAME VALUES")
    print("Sum of all Degrees / Number of Edges: ",    sum(degree_list)) #
    print("Maximum of all Degrees: ",                  max(degree_list)) #
    print("Minimum of all Degrees: ",                  min(degree_list)) #
    print("Length of Degree List / Number of Nodes: ", len(degree_list)) #

    print("Avg Degree: ", sum(degree_list) / len(degree_list))
    print("Median Degree: ", np.median(degree_list))
    print("Mode Degree: ", stats.mode(degree_list)[0][0])



#-- Degree Distribution --#
if descDDist_bool == True:

    print("Desciptives: Degree Distribution - only for friendship network of approach1 - g_ap1_friend")

    degree_hist = gt.vertex_hist(g_ap1_friend, "out") # 2d array with [frequency][degree]

    print("Degree Distribution Frequency: ", degree_hist[0])
    print("Degree Distribution Values: ", degree_hist[1]) # HERE THE MAX IS 257 WHYYY?

    print(len(degree_hist[0]), len(degree_hist[1]))

    y = degree_hist[0]
    x = degree_hist[1][:-1] # very weird, manually excluded for now

    #ax.set_xscale('log')

    fig, ax = plt.subplots()
    plt.bar(x, y, color='grey')
    ax.set_yscale('log')
    ax.set_xscale('log')
    plt.xlabel('Degree')
    plt.ylabel('Fequency')


    plt.plot(x, y, 'o', color='black')
    plt.savefig("degree_hist_g_ap1_friend.png")

    """
    plt.savefig("degree_dist", dpi=None, facecolor='w', edgecolor='w',
            orientation='portrait', papertype=None, format=None,
            transparent=False, bbox_inches=None, pad_inches=0.1,
            frameon=None, metadata=None)
    """


#-- Clustering Coefficiants - Global --#
if descCCG_bool == True:

    print("Desciptives: Global Clustering Coefficiants - only for friendship network of approach1 - g_ap1_friend")

    print('Global Clustering Coefficiants of g_ap1_friend: ', gt.global_clustering(g_ap1_friend))

'''
    vprop_comp = g_friendship.new_vertex_property("int")

    g_friendship.vp.comp = vprop_comp

    #g_friendship.vp.comp[v] = True

    #print(g_friendship.vertex_properties.comp[8])

    comp, hist = gt.label_components(g_friendship, vprop_comp, attractors=False)

    #print(g_friendship.vertex_properties.comp[8])

    print('comp id array: ', comp.a) #  .a = .get_array()[:]


    print(sum(comp.a), len(comp.a))



    print('comp hist/frequency array: ', hist)
    print(sum(hist), len(hist)) # why does it say that last value of 256 is occuring 622 times? its not occuring once. 622 is the size of the com array. weird shit
    # larges component in lmited sample is labled 145 (300 times)

    print("Number of copmonents in whole Graph: ", len(hist))



#-- number of components histogram --#



x, y = np.unique(hist, return_counts=True)

'''
'''
helper = []
for i in np.unique(hist):
    helper[i] =

y = np.unique(comp.a)
'''
'''
print('this is x: ', x)
print('this is y: ', y)


fig, ax = plt.subplots()
plt.bar(x, y, color='grey')
ax.set_yscale('log')
ax.set_xscale('log')
plt.xlabel('Component size')
plt.ylabel('Fequency')


#plt.plot(x, y, 'o', color='black')
plt.savefig("component_number_hist.png")


u_frin = gt.extract_largest_component(g_friendship)
print('larges comp', u_frin)

#diameter is obviously 0 because of the disconnectivity

#################################################
### Descriptives of larges component ###
#################################################


#-- density of LC--#

density_compL = len(u_frin) / ((len(u_frin) * len(u_frin)) / 2 )

print("Density of LC: ", density_compL)

#-- (Pseudo-) Diameter --#
dist, ends = gt.pseudo_diameter(u_frin)

print('(Pseudo-) Diameter: ', dist)
print('(Pseudo-) Diameter start:', ends[0], 'end:', ends[1])



#-- Closeness Distribution --#
'''
'''
closeness = gt.closeness(u_frin)
gt.graph_draw(u_frin, pos=None, vertex_fill_color=closeness,
              vertex_size=gt.prop_to_size(closeness, mi=5, ma=15),
              vcmap=matplotlib.cm.gist_heat,
              vorder=closeness, output="polblogs_closeness.pdf")
'''
'''
#-- Betweenness Distribution --#

#-- Eigenvector Distribution --#


#vprop_compL = g_friendship.new_vertex_property("bool")

#g_friendship.vp.compL = vprop_compL



#for i in len(comp):
 #g_friendship.vp.vprop_comp[i] = comp[i]

#print(comp, hist, )


#################################################
### Descriptives of second larges component ?###
#################################################

sec_compL = np.sort(hist)

print(sec_compL)

sec_compL_pos = np.sort(hist)[-2:-1]

sec_compL_id = np.where(hist==sec_compL_pos)[0][0]


print(sec_compL_id)


sec_compL = gt.GraphView(g_friendship, vfilt= lambda v: g_friendship.vp.comp[v] == sec_compL_id)

print(sec_compL)
'''