import graph_tool.all as gt
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import sys


######################
### Initialization ###
######################

np.set_printoptions(threshold=sys.maxsize)

# DO NOT USE g_raw FOR ASSORTATIVITY ANALYSIS! It contains uni- and bilateral FRIENDS_WITH relations.
# This is intentional due to the optional privacy setting of friendships in debate.org. See report for details.
# g_raw contains nodes: User, Issues
# g_raw contains edges: FRIENDS_WITH, GIVES_ISSUES

g_all = gt.load_graph('Graph_Preprocessed_Approach1.graphml', fmt='graphml')        # dont forget to change file name in line 128 Degree Distribution, when switching to another approach
#g_all = gt.load_graph('Graph_Preprocessed_Approach2.graphml', fmt='graphml')
#g_all = gt.load_graph('Graph_Preprocessed_Approach3.graphml', fmt='graphml')


g_friend = gt.GraphView(g_all, vfilt=lambda v: g_all.vp.userID[v] != "")
# g_raw_friend contains nodes: Users; edges: FRIENDS_WITH

g_issues = gt.GraphView(g_all, vfilt=lambda v: g_all.vp.issuesID[v] != "")
# g_raw_issues contains nodes: Users, Issues; edges: GIVES_ISSUES

descBroad_bool = False
descDens_bool = False
descAvgD_bool = False
descDDist_bool = False
descCCG_bool = False
descDia_bool = False
descClose_bool = True
descClosePlot_bool = False
descBetw_bool = True
descBetwPlot_bool = False
descEV_bool = True
descEVPlot_bool = False

####################
### Descriptives ###
####################

### Deskriptives Friendship Network ###

#-- Identifying Largest Component --#


vprop_Lcomp, hist = gt.label_components(g_friend, attractors=False)
g_friend.vp.Lcomp = vprop_Lcomp

#print('comp id array: ', vprop_Lcomp.a[:45348])         # .a = .get_array()[:]
print("Max: ", max(vprop_Lcomp.a[:45348]), "\nMode: ", stats.mode(vprop_Lcomp.a[:45348]), "\nLength: ",  len(vprop_Lcomp.a[:45348]))

# Approach 1
# Max:  28737, Mode: 8 (16382 times), Length: 45348

LC_id = stats.mode(vprop_Lcomp.a[:45348])[0][0]

# gt.label_components() seems to create vPropertyMaps for all 90696 nodes of the original graph g_all. This is, even though
# the image of g_friend is used for the function as parameter. The function results in an propertyMap where all
# Issues nodes (that should not have been considered by the function in the first place) are labeled as component 0.
# This makes the component with ID 0 the biggest component (with size N/2 (Issues nodes) +1 (first User node).
# To address this problem, only the first half of the propertyMap array is considered. This is not elegant (for now)
# but functional

#print(hist)
print("Max: ", max(hist), "\nSum: ",sum(hist), "\nLength / Number of components in g_friend: ",  len(hist))

# Approach 1
# Max:  16382,  Sum:  45348.0, Length / Number of components in g_friend:  28738

# The hist array does not seem to be affected by this

g_friend_LC = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.Lcomp[v] == LC_id)


#-- Distribution - Component Size --#

x, y = np.unique(hist, return_counts=True)          #                            Approach 1  | Approach 2 | Approach 3
print(x)         # Size Category                    # 1    ,6,8,9,13,18,21,22,28,39,55,16382 |
print(y)         # Frequency                        # 28726,1,1,1, 1, 1, 2, 1, 1, 1, 1,    1 |

'''
fig, ax = plt.subplots()
plt.bar(x, y, color='grey')
ax.set_yscale('log')
ax.set_xscale('log')
plt.xlabel('Component size (log)')
plt.ylabel('Fequency (log)')
plt.savefig("component_size_hist_ap1.png")
plt.close()
'''




### Deskriptives Friendship Network ###

#-- Number of nodes , edges, node properties, edge properties --#
if descBroad_bool == True:
    print("Desciptives: Broad - print(Graph Object) style")                 # Approach 1 | Approach 2 | Approach 3

    print("g_all, g_friend, g_issues")
    print(g_all)                                # Vertices                         90696 |  |
                                                # Edges                           234100 |  |
                                                # Internal vertex properties          84 |  |
                                                # Internal edge properties             2 |  |

    print(g_friend)                             # Vertices                         45348 |  |
                                                # Edges                           188752 |  |
                                                # Internal vertex properties          84 |  |
                                                # Internal edge properties             2 |  |

    print(g_issues)                             # Vertices                         45348 |  |
                                                # Edges                                0 |  |
                                                # Internal vertex properties          84 |  |
                                                # Internal edge properties             2 |  |

    print(g_friend_LC)                          # Vertices                         16382 |  |
                                                # Edges                           187478 |  |
                                                # Internal vertex properties          85 |  |
                                                # Internal edge properties             2 |  |

#-- Density of Friendship Network --#
if descDens_bool == True:

    print("Desciptives: Density - Friendship Network")                                      #             Approach 1 |             Approach 2 |             Approach 3

    v_friend = g_friend.get_vertices()
    e_friend = g_friend.get_edges()
    d_friend = len(e_friend) / ((len(v_friend) * (len(v_friend)-1))/2)

    v_friend_LC = g_friend_LC.get_vertices()
    e_friend_LC = g_friend_LC.get_edges()
    d_friend_LC = len(e_friend_LC) / ((len(v_friend_LC) * (len(v_friend_LC)-1))/2)

    print("Number of Nodes (g_friend): ", len(v_friend))                                #                  45348 | |
    print("Number of Edges (g_friend): ", len(e_friend))                                #                 188752 | |
    print("Density (g_friend): ",         d_friend)                                     # 0.00018357555878947262 | |

    print("\nDesciptives: Density - Friendship Network - Largest Component")

    print("Number of Nodes (g_friend): ", len(v_friend_LC))                             #                   | |
    print("Number of Edges (g_friend): ", len(e_friend_LC))                             #                  | |
    print("Density (g_friend): ",         d_friend_LC)                                  #  | |


#-- Avg Degree --#
if descAvgD_bool == True:

    print("Desciptives: Avg Degree - Friendship Network")                                           #             Approach 1 |             Approach 2 |             Approach 3

    degree_list = g_friend.get_in_degrees(g_friend.get_vertices())
    degree_list_LC = g_friend_LC.get_in_degrees(g_friend_LC.get_vertices())

    print("Sum of all Degrees / Number of Edges: ",    sum(degree_list))                            #               188752.0 | |
    print("Maximum of all Degrees: ",                  max(degree_list))                            #                 2025   | |
    print("Minimum of all Degrees: ",                  min(degree_list))                            #                    0   | |
    print("Length of Degree List / Number of Nodes: ", len(degree_list))                            #                45348   | |
    print("Avg Degree: ",                               sum(degree_list) / len(degree_list))        #      4.162300432213107 | |
    print("Median Degree: ",                            np.median(degree_list))                     #                    0.0 | |
    print("Mode Degree: ",                              stats.mode(degree_list)[0][0])              #                    0   | |

    print("\nDesciptives: Avg Degree - Friendship Network - Largest Component")

    print("Sum of all Degrees / Number of Edges: ",    sum(degree_list_LC))                         #                | |
    print("Maximum of all Degrees: ",                  max(degree_list_LC))                         #                    | |
    print("Minimum of all Degrees: ",                  min(degree_list_LC))                         #                       | |
    print("Length of Degree List / Number of Nodes: ", len(degree_list_LC))                         #                   | |
    print("Avg Degree: ",                               sum(degree_list_LC) / len(degree_list_LC))  #       | |
    print("Median Degree: ",                            np.median(degree_list_LC))                  #                     | |
    print("Mode Degree: ",                              stats.mode(degree_list_LC)[0][0])           #                       | |


#-- Degree Distribution --#
if descDDist_bool == True:

    print("Desciptives: Degree Distribution - Friendship Network")

    degree_hist = gt.vertex_hist(g_friend, "out") # 2d array with [frequency][degree]

    #print("Degree Distribution Frequency: \n", degree_hist[0])
    #print("Degree Distribution Values: \n", degree_hist[1])                 # todo ask Jonathan why my degree-value list is one value to large???

    print(len(degree_hist[0]), len(degree_hist[1]))


    y = degree_hist[0]
    x = degree_hist[1][:-1]                                                 # todo manually excluded for now. Find better why later

    fig, ax = plt.subplots()
    plt.bar(x, y, color='grey')
    ax.set_yscale('log')
    ax.set_xscale('log')
    plt.xlabel('Degree (log)')
    plt.ylabel('Fequency (log)')
    plt.savefig("degree_hist_g_friend_ap1.png")
    plt.close()

    degree_hist_LC = gt.vertex_hist(g_friend_LC, "out")  # 2d array with [frequency][degree]

    #print("Degree Distribution Frequency: \n", degree_hist_LC[0])
    #print("Degree Distribution Values: \n", degree_hist_LC[1])                 # todo ask Jonathan why my degree-value list is one value to large???

    print(len(degree_hist_LC[0]), len(degree_hist_LC[1]))


    y = degree_hist_LC[0]
    x = degree_hist_LC[1][:-1]                                                 # todo manually excluded for now. Find better why later

    fig, ax = plt.subplots()
    plt.bar(x, y, color='grey')
    ax.set_yscale('log')
    ax.set_xscale('log')
    plt.xlabel('Degree (log) - Largest Component')
    plt.ylabel('Fequency (log) - Largest Component')
    plt.savefig("degree_hist_g_friend_LC_ap1.png")
    plt.close()


#-- Clustering Coefficiants - Global --#
if descCCG_bool == True:

    print("Desciptives: Global Clustering Coefficiants - Friendship Network")                           #                              Approach 1 | Approach 2 | Approach 3
                                                                                                        #       coefficient,   standard deviation | |
                                                                                                        #     no. triangles, no. connected triples| |

    print('Global Clustering Coefficiants: ', gt.global_clustering(g_friend, ret_counts = True))        # 0.101803664507653, 0.013292495836611278 | |
                                                                                                        #           2583788,             76140324 | |
                                                                                                        # todo do these numbers of triples and triangles make sense?


### Deskriptives Friendship Network - Largest Component specific ###

#-- (Pseudo-) Diameter --#

if descDia_bool == True:
    dist, ends = gt.pseudo_diameter(g_friend_LC)

    print('(Pseudo-) Diameter: ', dist)
    print('(Pseudo-) Diameter start:', ends[0], 'end:', ends[1])


#-- Closeness Distribution --#

if descClose_bool == True:
    vprop_closeness = gt.closeness(g_friend_LC)
    g_friend_LC.vp.closeness = vprop_closeness

    close_array = np.array(vprop_closeness.a)
    #close_array_wo_0 = close_array[close_array != 0]

    close_array_index_LC = np.where(close_array != 0)
    close_array_LC = close_array[close_array_index_LC]

    print("Avg Closeness Centrality: ", sum(close_array_LC)/len(close_array_LC))


    #plt.hist(close_array_LC, bins=np.linspace(0, 0.6, 21), color='grey', log=True,)
    plt.hist(close_array_LC, bins=np.linspace(0, 0.6, 13), color='grey', log=True,)
    plt.xticks(np.linspace(0, 0.6, 13), rotation=45, fontsize=6)
    plt.xlabel('Closeness - Largest Component')
    plt.ylabel('Fequency (log) - Largest Component')
    plt.savefig("closeness_hist_g_friend_LC_ap1.png")
    plt.close()



if descClosePlot_bool == True:
    gt.graph_draw(g_friend_LC, pos=None, vertex_fill_color=vprop_closeness,
                  vertex_size=gt.prop_to_size(vprop_closeness, mi=5, ma=15),
                  vcmap=plt.cm.gist_heat,
                  vorder=vprop_closeness, output="closeness_g_friend_LC_ap1.pdf")

'''
    gt.graph_draw(g, pos=g.vp["pos"], vertex_fill_color=c, vertex_size = gt.prop_to_size(c, mi=5, ma=15),
                  vcmap = matplotlib.cm.gist_heat, vorder = c, output = "polblogs_closeness.pdf")
'''

#-- Betweenness Distribution --#

if descBetw_bool == True:
    vprop_betweenness, eprop_betweenness = gt.betweenness(g_friend_LC)
    g_friend_LC.vp.v_betweenness = vprop_betweenness
    g_friend_LC.ep.e_betweenness = eprop_betweenness

    v_between_array = np.array(vprop_betweenness.a)
    v_between_array_LC = v_between_array[close_array_index_LC]


    plt.hist(v_between_array_LC, bins=np.linspace(0, 0.14, 15), color='grey', log=True,)
    #plt.hist(v_between_array_wo_0, color='grey', log=True,)
    plt.xticks(np.linspace(0, 0.14, 15), rotation=45, fontsize=6)
    plt.xlabel('Betweeness - Largest Component')
    plt.ylabel('Fequency (log) - Largest Component')
    plt.savefig("v_betweenness_hist_g_friend_LC_ap1.png")
    plt.close()

if descBetwPlot_bool == True:

    gt.graph_draw(g_friend_LC, pos=None, vertex_fill_color=vprop_betweenness,
                  vertex_size = gt.prop_to_size(vprop_betweenness, mi=5, ma=15),
                  edge_pen_width = gt.prop_to_size(eprop_betweenness, mi=0.5, ma=5), vcmap = plt.cm.gist_heat,
                  vorder = vprop_betweenness, output = "betweenness_g_friend_LC_ap1.pdf")

'''    
    gt.graph_draw(g_friend_LC, pos=None, vertex_fill_color=vp, vertex_size = gt.prop_to_size(vp, mi=5, ma=15),
                  edge_pen_width = gt.prop_to_size(ep, mi=0.5, ma=5), vcmap = plt.cm.gist_heat,
                  vorder = vp, output = "polblogs_betweenness.pdf")
'''

#-- Eigenvector Distribution --#

if descEV_bool == True:
    w = g_friend_LC.new_edge_property("double")
    w.a = np.random.random(len(w.a)) * 42
    ee, x = gt.eigenvector(g_friend_LC, w)

    eigenVec_array = np.array(x.a)
    eigenVec_array_LC = eigenVec_array[close_array_index_LC]

    print(ee)

    print(len(eigenVec_array_LC))

    print("Avg Eigenvector Centrality: ", sum(eigenVec_array_LC)/len(eigenVec_array_LC), "Max: ", max(eigenVec_array_LC), "Min: ", min(eigenVec_array_LC), "length: ", len(eigenVec_array_LC))


    #plt.hist(eigenVec_array_LC, bins=np.linspace(0, 0.14, 21), color='grey', log=True,)
    plt.hist(eigenVec_array_LC, bins=np.linspace(0, 0.18, 19), color='grey', log=True,)
    #plt.hist(v_between_array_wo_0, color='grey', log=True,)
    plt.xticks(np.linspace(0, 0.18, 19), rotation=45, fontsize=6)
    plt.xlabel('Eigenvector Values - Largest Component')
    plt.ylabel('Fequency (log) - Largest Component')
    plt.savefig("eigenVector_hist_g_friend_LC_ap1.png")
    plt.close()


if descEVPlot_bool == True:

    gt.graph_draw(g_friend_LC, pos=None, vertex_fill_color=x,
                  vertex_size=gt.prop_to_size(x, mi=5, ma=15), vcmap=plt.cm.gist_heat,
                  vorder=x, output="eigenvetcor_g_friend_LC_ap1.pdf")

