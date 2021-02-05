import graph_tool.all as gt
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import sys


######################
### Initialization ###
######################

np.set_printoptions(threshold=sys.maxsize)

# DO NOT USE AN UNPREPROCESSED GRAPHML FOR ASSORTATIVITY ANALYSIS! They contain uni- and bilateral FRIENDS_WITH relations.
# This is intentional due to the optional privacy setting of friendships in debate.org. See report for details.
# g_raw contains nodes: User, Issues
# g_raw contains edges: FRIENDS_WITH, GIVES_ISSUES

g_all = gt.load_graph('Graph_Preprocessed_Approach1.graphml', fmt='graphml')
#g_all = gt.load_graph('Graph_Preprocessed_Approach2.graphml', fmt='graphml')
#g_all = gt.load_graph('Graph_Preprocessed_Approach3.graphml', fmt='graphml')


g_friend = gt.GraphView(g_all, vfilt=lambda v: g_all.vp.userID[v] != "")
# g_raw_friend contains nodes: Users; edges: FRIENDS_WITH

g_issues = gt.GraphView(g_all, vfilt=lambda v: g_all.vp.issuesID[v] != "")
# g_raw_issues contains nodes: Users, Issues; edges: GIVES_ISSUES


# All descriptives are focused on the Friendship Network and its Largest Component

descLC_bool = True              #-- Identifying Largest Component
descCompHist_bool = False        #-- Distribution (Component Size)
descBroad_bool = True           #-- Number of nodes, edges, node properties, edge properties
descDens_bool = True            #-- Density
descAvgD_bool = True            #-- Average Degree
descDDist_bool = True           #-- Degree Distribution
descCCG_bool = True             #-- Clustering Coefficiants (Global)
descDia_bool = True             #-- (Pseudo-) Diameter
descClose_bool = True           #-- Closeness Distribution
descClosePlot_bool = False
descBetw_bool = True            #-- Betweenness Distribution
                                # relies on intermediate result of descClose_bool
descBetwPlot_bool = False
descEV_bool = True              #-- Eigenvector Distribution
                                # relies on intermediate result of descClose_bool
descEVPlot_bool = False


####################
### Descriptives ###
####################

### Deskriptives Friendship Network ###

#-- Identifying Largest Component --#

if descLC_bool == True:
    print("\n\nIdentifying Largest Component\n")

    vprop_Lcomp, hist = gt.label_components(g_friend, attractors=False)
    g_friend.vp.Lcomp = vprop_Lcomp

                                                                                        # All results are based on preprocessing approach 1
    print("Number of unique components: ", max(vprop_Lcomp.a[:45348]))                  # 28737
    print("Id of largest component & size: ", stats.mode(vprop_Lcomp.a[:45348]))        # 8 & 16382
    print("Number of all nodes in friendship network: ",  len(vprop_Lcomp.a[:45348]))   # 45348

    LC_id = stats.mode(vprop_Lcomp.a[:45348])[0][0]

    # gt.label_components() seems to create vPropertyMaps for all 90696 nodes of the original graph g_all. This is, even though
    # the image of g_friend is used for the function as parameter. The function results in an propertyMap where all
    # Issues nodes (that should not have been considered by the function in the first place) are labeled as component 0.
    # This makes the component with ID 0 the biggest component (with size N/2 (Issues nodes) +1 (first User node).
    # To address this problem, only the first half of the propertyMap array is considered (only user nodes). This is not elegant (for now)
    # but functional
    # EDIT: This is a theme in GraphTool functions that carries on in this files

    g_friend_LC = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.Lcomp[v] == LC_id)

    print("\nIdentifying Largest Component - done\n")

#-- Distribution - Component Size --#

if descCompHist_bool == True:
    print("\n\nDistribution - Component Size\n")

    x, y = np.unique(hist, return_counts=True)
    print("Size categories of the components: ", x)     #     1,6,8,9,13,18,21,22,28,39,55,16382
    print("Frequency of the size categories: ", y)      # 28726,1,1,1, 1, 1, 2, 1, 1, 1, 1,    1


    fig, ax = plt.subplots()
    plt.bar(x, y, color='grey')
    ax.set_yscale('log')
    ax.set_xscale('log')
    #plt.title('Histogram of Component Size\nLast two Categories (Size: 55 & 16382) not visible (Count: 1)')
    plt.xlabel('Component Size (log)')
    plt.ylabel('Frequency (log)')
    plt.savefig("component_size_hist_ap1.png")          # unofrtunately the components of size 55 and 16382 are not displayed.
                                                        # This is due to the shrinking bar width with increase in x-axis
    plt.close()

    print("\nDistribution - Component Size -done\n")

#-- Number of nodes, edges, node properties, edge properties --#

if descBroad_bool == True:

    print("\n\nDesciptives: Broad - print(Graph Object) style\n")

    print("g_all")
    print(g_all, "\n")                          # Vertices                         90696
                                                # Edges                           234100
                                                # Internal vertex properties          84
                                                # Internal edge properties             2
    print("g_friend")
    print(g_friend, "\n")                       # Vertices                         45348
                                                # Edges                           188752
                                                # Internal vertex properties          84
                                                # Internal edge properties             2
    print("g_issues")
    print(g_issues, "\n")                       # Vertices                         45348
                                                # Edges                                0
                                                # Internal vertex properties          84
                                                # Internal edge properties             2
    print("g_friend_LC")
    print(g_friend_LC, "\n")                    # Vertices                         16382
                                                # Edges                           187478
                                                # Internal vertex properties          85
                                                # Internal edge properties             2

    print("\nDesciptives: Broad - print(Graph Object) style - done\n")

#-- Density of Friendship Network --#
if descDens_bool == True:

    print("\nDesciptives: Density - Friendship Network\n")

    v_friend = g_friend.get_vertices()
    e_friend = g_friend.get_edges()
    d_friend = len(e_friend) / ((len(v_friend) * (len(v_friend)-1))/2)

    v_friend_LC = g_friend_LC.get_vertices()
    e_friend_LC = g_friend_LC.get_edges()
    d_friend_LC = len(e_friend_LC) / ((len(v_friend_LC) * (len(v_friend_LC)-1))/2)

    print("Number of Nodes (g_friend): ", len(v_friend))                                #                  45348
    print("Number of Edges (g_friend): ", len(e_friend))                                #                 188752
    print("Density (g_friend): ",         d_friend)                                     # 0.00018357555878947262

    print("\nDesciptives: Density - Friendship Network - Largest Component\n")

    print("Number of Nodes (g_friend): ", len(v_friend_LC))                             #                 16382
    print("Number of Edges (g_friend): ", len(e_friend_LC))                             #                187478
    print("Density (g_friend): ",         d_friend_LC)                                  # 0.0013972463236576174

    print("\nDesciptives: Density - Friendship Network - done\n")

#-- Average Degree of Friendship Network --#
if descAvgD_bool == True:

    print("\n\nDescriptives: Average Degree - Friendship Network\n")

    degree_list = g_friend.get_in_degrees(g_friend.get_vertices())
    degree_list_LC = g_friend_LC.get_in_degrees(g_friend_LC.get_vertices())

    print("Sum of all Degrees / Number of Edges: ",    sum(degree_list))                            # 188752.0
    print("Maximum of all Degrees: ",                  max(degree_list))                            #   2025
    print("Minimum of all Degrees: ",                  min(degree_list))                            #      0
    print("Length of Degree List / Number of Nodes: ", len(degree_list))                            #  45348
    print("Avg Degree: ",                               sum(degree_list) / len(degree_list))        #      4.162300432213107
    print("Median Degree: ",                            np.median(degree_list))                     #      0.0
    print("Mode Degree: ",                              stats.mode(degree_list)[0][0])              #      0

    print("\nDesciptives: Avg Degree - Friendship Network - Largest Component\n")

    print("Sum of all Degrees / Number of Edges: ",    sum(degree_list_LC))                         # 187478.0
    print("Maximum of all Degrees: ",                  max(degree_list_LC))                         #   2025
    print("Minimum of all Degrees: ",                  min(degree_list_LC))                         #      1
    print("Length of Degree List / Number of Nodes: ", len(degree_list_LC))                         #  16382
    print("Avg Degree: ",                               sum(degree_list_LC) / len(degree_list_LC))  #     11.444146013917715
    print("Median Degree: ",                            np.median(degree_list_LC))                  #      2.0
    print("Mode Degree: ",                              stats.mode(degree_list_LC)[0][0])           #      1

    print("\n\nDescriptives: Average Degree - done\n")


#-- Degree Distribution of Friendship Network --#
if descDDist_bool == True:
    print("\n\nDesciptives: Degree Distribution - Friendship Network")

    degree_hist = gt.vertex_hist(g_friend, "out")

    #print("Degree Distribution Frequency: \n", degree_hist[0])
    #print("Degree Distribution Values: \n", degree_hist[1])
    #print(len(degree_hist[0]), len(degree_hist[1]))

    y = degree_hist[0]
    x = degree_hist[1][:-1]                                                 # gt.vertex_hist results in a 2d histogram array [[frequency][degree]]
                                                                            # degree_hist that has 1 entry too much in the second
                                                                            # For whatever reason, the second dimension [degree] hast one entry too much
                                                                            # The last value of [degree]is excluded manually for both diemnsions being
                                                                            # of same size. There is no theoretical explanation for why the last value
                                                                            # should be part of the array. Confusing, but not relevant for the following analysis

    fig, ax = plt.subplots()
    plt.bar(x, y, color='grey')
    ax.set_yscale('log')
    ax.set_xscale('log')
    #plt.title('Histogram of Degree Distribution')
    plt.xlabel('Degree (log)')
    plt.ylabel('Frequency (log)')
    plt.savefig("degree_hist_g_friend_ap1.png")
    plt.close()

    print("Desciptives: Degree Distribution - Friendship Network - Largest Component\n")

    degree_hist_LC = gt.vertex_hist(g_friend_LC, "out")

    #print("Degree Distribution Frequency: \n", degree_hist_LC[0])
    #print("Degree Distribution Values: \n", degree_hist_LC[1])
    #print(len(degree_hist_LC[0]), len(degree_hist_LC[1]))

    y = degree_hist_LC[0]
    x = degree_hist_LC[1][:-1]

    fig, ax = plt.subplots()
    plt.bar(x, y, color='grey')
    ax.set_yscale('log')
    ax.set_xscale('log')
    #plt.title('Histogram of Degree Distribution\nLargest Component')
    plt.xlabel('Degree (log)')
    plt.ylabel('Frequency (log)')
    plt.savefig("degree_hist_g_friend_LC_ap1.png")
    plt.close()

    print("\n\nDesciptives: Degree Distribution - done \n")

#-- Clustering Coefficiants (Global) - of Friendship Network--#
if descCCG_bool == True:

    print("\nDesciptives: Global Clustering Coefficiants \n")
                                                                                                        #       coefficient,   standard deviation

    print('Global Clustering Coefficiants - Friendship Network: ', gt.global_clustering(g_friend))      # 0.101803664507653, 0.013292495836611278
    print('Global Clustering Coefficiants - Largest Component: ', gt.global_clustering(g_friend_LC))    # 0.10158343197387348, 0.013265280343602718

    print("\nDesciptives: Global Clustering Coefficiants - done\n")


### Deskriptives Friendship Network - Largest Component specific ###

#-- (Pseudo-) Diameter of Largest Component --#

if descDia_bool == True:

    print("\n\nDeskriptives Friendship Network - Largest Component specific - (Pseudo-) Diameter\n")

    dist, ends = gt.pseudo_diameter(g_friend_LC)

    print('(Pseudo-) Diameter: ', dist)                                         # 14.0
    #print('(Pseudo-) Diameter start:', ends[0], 'end:', ends[1])                # start: 1275 end: 37966

    print("\n\nDeskriptives Friendship Network - Largest Component specific - (Pseudo-) Diameter -done\n")

#-- Closeness Distribution of Largest Component --#

if descClose_bool == True:

    print("\n\n#-- Closeness Distribution --#\n")

    vprop_closeness = gt.closeness(g_friend_LC)
    g_friend_LC.vp.closeness = vprop_closeness

    close_array = np.array(vprop_closeness.a)

    close_array_index_LC = np.where(close_array != 0)
    close_array_LC = close_array[close_array_index_LC]

    print("Avg Closeness Centrality: ", sum(close_array_LC)/len(close_array_LC))        # 0.2769106346214449
    print("Median Closeness Centrality: ", np.median(close_array_LC) )                  # 0.27148728827604496
    print("Mode Closeness Centrality: ", stats.mode(close_array_LC))                 # 0.2712535187945024


    plt.hist(close_array_LC, bins=np.linspace(0, 0.6, 13), color='grey', log=True,)
    plt.xticks(np.linspace(0, 0.6, 13), rotation=45, fontsize=6)
    #plt.title('Histogram of Closeness Centrality\nLargest Component')
    plt.xlabel('Closeness Centrality')
    plt.ylabel('Frequency (log)')
    plt.savefig("closeness_hist_g_friend_LC_ap1.png")
    plt.close()



if descClosePlot_bool == True:

    # Screenshot added to Github (less loading time)
    gt.graph_draw(g_friend_LC, pos=None, vertex_fill_color=vprop_closeness,
                  vertex_size=gt.prop_to_size(vprop_closeness, mi=5, ma=15),
                  vcmap=plt.cm.gist_heat,
                  vorder=vprop_closeness, output="closeness_g_friend_LC_ap1.pdf")


#-- Betweenness Distribution of Largest Component --#

if descBetw_bool == True:

    print("\n\n#-- Betweenness Distribution --#\n")

    vprop_betweenness, eprop_betweenness = gt.betweenness(g_friend_LC)
    g_friend_LC.vp.v_betweenness = vprop_betweenness
    g_friend_LC.ep.e_betweenness = eprop_betweenness

    v_between_array = np.array(vprop_betweenness.a)
    v_between_array_LC = v_between_array[close_array_index_LC]

    print("Avg Vertex Betweenness Centrality: ", sum(v_between_array_LC) / len(v_between_array_LC))     # 0.000163803122932315
    print("Median Betweenness Centrality: ", np.median(v_between_array_LC))                             # 0.0
    print("Mode Betweenness Centrality: ", stats.mode(v_between_array_LC))                           # 0.0

    plt.hist(v_between_array_LC, bins=np.linspace(0, 0.14, 15), color='grey', log=True,)
    plt.xticks(np.linspace(0, 0.14, 15), rotation=45, fontsize=6)
    #plt.title('Histogram of Betweeness Centrality\nLargest Component')
    plt.xlabel('Vertex Betweeness Centrality')
    plt.ylabel('Frequency (log)')
    plt.savefig("v_betweenness_hist_g_friend_LC_ap1.png")
    plt.close()

if descBetwPlot_bool == True:

    # Screenshot added to Github (less loading time)
    gt.graph_draw(g_friend_LC, pos=None, vertex_fill_color=vprop_betweenness,
                  vertex_size = gt.prop_to_size(vprop_betweenness, mi=5, ma=15),
                  edge_pen_width = gt.prop_to_size(eprop_betweenness, mi=0.5, ma=5), vcmap = plt.cm.gist_heat,
                  vorder = vprop_betweenness, output = "betweenness_g_friend_LC_ap1.pdf")


#-- Eigenvector Distribution of Largest Component --#

if descEV_bool == True:

    print("\n\n#-- Eigenvector Distribution --#\n")

    w = g_friend_LC.new_edge_property("double")
    w.a = np.random.random(len(w.a)) * 42
    ee, x = gt.eigenvector(g_friend_LC, w)

    eigenVec_array = np.array(x.a)
    eigenVec_array_LC = eigenVec_array[close_array_index_LC]

    print("Eigenvalue of Largest Component: ", ee)                                          # 3028.056712035545


    print("Avg Eigenvector Centrality: ", sum(eigenVec_array_LC)/len(eigenVec_array_LC))    #    0.0023861077211674566
    print("Median Eigenvector Centrality: ", np.median(eigenVec_array_LC))                  #    0.0002809208037315768
    print("Mode Eigenvector Centrality: ", stats.mode(eigenVec_array_LC))                   #    5.780324396860505e-18


    plt.hist(eigenVec_array_LC, bins=np.linspace(0, 0.18, 19), color='grey', log=True,)
    plt.xticks(np.linspace(0, 0.18, 19), rotation=45, fontsize=6)
    #plt.title('Histogram of Eigenvector Centrality\nLargest Component')
    plt.xlabel('Eigenvector Centrality')
    plt.ylabel('Frequency (log)')
    plt.savefig("eigenVector_hist_g_friend_LC_ap1.png")
    plt.close()


if descEVPlot_bool == True:

    # Screenshot added to Github (less loading time)
    gt.graph_draw(g_friend_LC, pos=None, vertex_fill_color=x,
                  vertex_size=gt.prop_to_size(x, mi=5, ma=15), vcmap=plt.cm.gist_heat,
                  vorder=x, output="eigenvetcor_g_friend_LC_ap1.pdf")

