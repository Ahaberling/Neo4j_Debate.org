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

descBroad_bool = True
descDens_bool = True
descAvgD_bool = True
descDDist_bool = True
descCCG_bool = True


####################
### Descriptives ###
####################

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

    print(g_issues)                             # Vertices                          45348 |  |
                                                # Edges                                 0 |  |
                                                # Internal vertex properties           84 |  |
                                                # Internal edge properties              2 |  |

#-- Density of Friendship Network --#
if descDens_bool == True:

    print("Desciptives: Density - Friendship Network")                                      #             Approach 1 |             Approach 2 |             Approach 3

    v_friendship = g_friend.get_vertices()
    e_friendship = g_friend.get_edges()
    d_friendship = len(e_friendship) / ((len(v_friendship) * (len(v_friendship)-1))/2)

    print("Number of Nodes (g_friend): ", len(v_friendship))                                #                  45348 | |
    print("Number of Edges (g_friend): ", len(e_friendship))                                #                 188752 | |
    print("Density (g_friend): ",         d_friendship)                                     # 0.00018357555878947262 | |


#-- Avg Degree --#
if descAvgD_bool == True:

    print("Desciptives: Avg Degree - Friendship Network")                                   #             Approach 1 |             Approach 2 |             Approach 3

    degree_list = g_friend.get_in_degrees(g_friend.get_vertices())

    print("Sum of all Degrees / Number of Edges: ",    sum(degree_list))                    #               188752.0 | |
    print("Maximum of all Degrees: ",                  max(degree_list))                    #                 2025   | |
    print("Minimum of all Degrees: ",                  min(degree_list))                    #                    0   | |
    print("Length of Degree List / Number of Nodes: ", len(degree_list))                    #                45348   | |

    print("Avg Degree: ",                               sum(degree_list) / len(degree_list))#      4.162300432213107 | |
    print("Median Degree: ",                            np.median(degree_list))             #                    0.0 | |
    print("Mode Degree: ",                              stats.mode(degree_list)[0][0])      #                    0   | |

    degree_list = g_friend.get_out_degrees(g_friend.get_vertices())

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

    print("Desciptives: Degree Distribution - Friendship Network")

    degree_hist = gt.vertex_hist(g_friend, "out") # 2d array with [frequency][degree]

    print("Degree Distribution Frequency: \n", degree_hist[0])
    print("Degree Distribution Values: \n", degree_hist[1])                 # todo ask Jonathan why my degree-value list is one value to large???

    print(len(degree_hist[0]), len(degree_hist[1]))


    y = degree_hist[0]
    x = degree_hist[1][:-1]                                                 # todo manually excluded for now. Find better why later

    fig, ax = plt.subplots()
    plt.bar(x, y, color='grey')
    ax.set_yscale('log')
    ax.set_xscale('log')
    plt.xlabel('Degree')
    plt.ylabel('Fequency')
    plt.savefig("degree_hist_g_friend_ap1.png")


#-- Clustering Coefficiants - Global --#
if descCCG_bool == True:

    print("Desciptives: Global Clustering Coefficiants - Friendship Network")                           #                              Approach 1 | Approach 2 | Approach 3
                                                                                                        #       coefficient,   standard deviation | |
                                                                                                        #     no. triangles, no. connected triples| |

    print('Global Clustering Coefficiants: ', gt.global_clustering(g_friend, ret_counts = True))        # 0.101803664507653, 0.013292495836611278 | |
                                                                                                        #           2583788,             76140324 | |
                                                                                                        # todo do these numbers of triples and triangles make sense?

    
    vprop_compID = g_friend.new_vertex_property("int")
    #g_friend.vp.compID = vprop_compID

    comp, hist = gt.label_components(g_friend, vprop_compID, directed=None, attractors=False)


    print('comp array: ', comp.a) #  .a = .get_array()[:]

    print(max(comp.a), stats.mode(comp.a), len(comp.a))

    print(g_friend.vp.comp[15])


    """
    vprop_comp = g_friendship.new_vertex_property("int")
    
    g_friendship.vp.comp = vprop_comp
    
    #g_friendship.vp.comp[v] = True
    
    #print(g_friendship.vertex_properties.comp[8])
    
    comp, hist = gt.label_components(g_friendship, vprop_comp, attractors=False)
    
    #print(g_friendship.vertex_properties.comp[8])
    
    print('comp id array: ', comp.a) #  .a = .get_array()[:]
    
    
    print(sum(comp.a), len(comp.a))
    """

    '''

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

