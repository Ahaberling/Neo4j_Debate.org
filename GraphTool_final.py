import graph_tool.all as gt
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import sys


######################
### Initialization ###
######################

np.set_printoptions(threshold=sys.maxsize)

# DO NOT USE g_raw FOR ASSORTATIVITY ANALYSIS! It contains uni- and bilateral FRIENDS_WITH relations.
# This is intentional due to the optional privacy setting of friendships in debate.org. See report for details.
# g_raw contains nodes: User, Issues
# g_raw contains edges: FRIENDS_WITH, GIVES_ISSUES
g_raw = gt.load_graph('debate.org_with_issues_mod.graphml', fmt='graphml')


###########################
### Graph Preprocessing ###
###########################

#--- Approach 1: g_ ---#

# g_raw_friend contains User, FRIENDS_WITH
g_raw_friend = gt.GraphView(g_raw, vfilt=lambda v: g_raw.vp.userID[v] != "")
print("g_raw_friend nodes: ", len(g_raw_friend.get_vertices()))

#g_raw_friend_noPriv = gt.GraphView(g_raw_friend, vfilt=lambda v: g_raw.vp.friend_privacy[v] == False)  # 311 edges will be created (too much?)
g_raw_friend_noPriv = gt.GraphView(g_raw_friend, vfilt=lambda v: g_raw.vp.friend_privacy[v] == True)    # this should be 44804 edges
print("g_raw_friend_noPriv nodes: ", len(g_raw_friend_noPriv.get_vertices()))

#x = np.array([[],[]])

#for v in range(len(g_raw.get_vertices())):
    #source = g_raw_friend.get_edges()[v][0]
    #target = g_raw_friend.get_edges()[v][1]

    #print(g_raw_friend.get_edges()[v])
    #print(type(g_raw_friend.get_edges()[v]))

    #x = np.append(x, [source, target])

    #x2 = np.append(x, [source, source])
    #x3 = np.append(x, [45337, 45337])
    #x4 = np.append(x, [1000000000, 1000000001])

    #print(g_raw_friend.get_edges())

#print(len(g_raw_friend.get_edges()))
#print(type(g_raw_friend.get_edges()[0]))

#tuplelist = list(map(tuple, g_raw_friend.get_edges()))
tuplelist = list(map(tuple, g_raw_friend_noPriv.get_edges()))

#print(tuplelist)

print(len(g_raw.get_edges())) # 188965

c = 0
c_newE = 0
new_edges = []

'''for e in g_raw_friend_noPriv.get_edges():
    c = c + 1

    #print(e)
    source = e[0]
    target = e[1]

    if (target, source) not in tuplelist:
        c_newE = c_newE + 1
        g_raw.add_edge(target, source)
        new_edges.append((target, source))
        #e_inv = g_raw.add_edge(target, source)
        #print(e_inv)


    if c % 100 == 0:
        print(c)
'''

# [(29115, 44), (15112, 198), (40623, 289), (2580, 289), (36931, 419), (10876, 1417), (18613, 1737), (20942, 1750), (23128, 1750), (7454, 1750), (8625, 1750), (39496, 2138), (376, 2259), (19877, 3291), (15574, 3513), (31329, 3513), (4374, 3513), (38637, 3513), (8398, 3513), (25104, 3513), (29384, 3592), (4466, 3652), (13023, 3674), (8398, 3674), (26497, 3763), (35266, 3786), (29984, 4071), (1962, 4288), (38187, 4310), (20416, 4310), (2580, 4650), (29700, 4650), (21192, 5139), (18749, 5139), (15112, 5223), (44546, 5454), (18749, 5558), (42723, 5587), (4984, 5595), (25101, 5708), (2580, 5708), (38443, 5708), (10839, 5772), (39110, 5772), (43926, 5772), (10839, 5864), (29384, 5915), (37917, 6071), (4984, 6292), (39496, 6292), (36921, 6292), (17634, 6425), (41276, 6615), (6671, 6720), (30196, 7104), (36312, 7311), (7091, 7672), (42008, 7893), (10972, 8100), (33376, 8126), (23758, 8126), (9299, 8126), (36747, 8538), (29115, 8538), (32005, 8538), (6367, 8546), (7454, 8769), (11060, 8933), (22223, 9328), (27668, 9733), (37268, 9733), (36586, 10026), (1231, 10142), (38514, 10508), (25101, 10508), (35888, 10737), (18873, 10765), (42008, 11035), (4065, 11523), (29255, 11523), (36312, 11523), (12732, 11523), (15365, 11523), (17708, 11523), (7077, 11523), (7756, 11523), (37816, 11523), (20115, 11523), (30580, 11523), (31164, 11523), (39527, 11523), (28617, 11523), (13269, 11523), (18873, 12189), (7091, 12620), (41195, 13152), (25346, 13528), (42104, 14436), (31693, 14481), (6367, 14710), (9170, 14710), (14364, 14710), (30624, 14710), (15808, 14710), (15454, 14710), (45251, 14710), (40623, 14710), (42318, 14710), (17391, 14710), (30843, 14710), (21192, 14860), (20942, 14860), (38025, 14860), (32218, 14868), (17092, 14897), (37917, 15500), (38443, 15500), (10459, 15500), (17092, 15554), (17092, 15885), (38025, 15885), (40825, 16210), (36586, 16241), (26646, 16430), (36921, 16753), (376, 16753), (6227, 17674), (11911, 17674), (20942, 17674), (13003, 17693), (38569, 17731), (34008, 17731), (10407, 17731), (7619, 17731), (17253, 17731), (35266, 17731), (779, 17731), (30085, 17731), (16528, 17731), (31395, 17731), (6367, 17775), (8678, 18407), (26617, 18407), (17321, 18407), (8554, 18407), (4918, 18769), (38443, 18914), (27668, 19111), (1240, 19225), (38514, 19279), (21433, 19709), (11135, 19709), (7502, 19709), (23629, 19709), (35245, 19709), (28392, 19709), (21192, 19709), (8678, 19709), (19073, 19709), (17092, 19709), (35266, 19709), (17253, 19709), (12609, 19709), (38569, 19709), (27299, 19709), (30196, 19709), (36971, 19709), (29255, 20108), (21152, 20198), (42799, 20302), (18613, 20302), (1270, 20707), (29255, 20889), (17307, 21391), (17307, 21432), (26617, 21466), (31385, 21466), (17253, 21466), (17321, 22188), (35245, 22236), (37917, 22546), (26617, 22824), (42104, 22824), (32218, 22824), (4466, 22824), (18749, 22976), (17281, 22976), (20942, 22976), (13023, 23439), (38025, 23439), (3154, 23506), (38514, 23506), (486, 23538), (17634, 23538), (28484, 23798), (1270, 23906), (25856, 24107), (7619, 24256), (36058, 24495), (26553, 24495), (36701, 24676), (45251, 24991), (10214, 25009), (11581, 25300), (33896, 25547), (41596, 25559), (41596, 25732), (39154, 26184), (30837, 26184), (8625, 26206), (8625, 26210), (31164, 26294), (8029, 26581), (17442, 26938), (28484, 26951), (40300, 26970), (4466, 27581), (40658, 27840), (43773, 28055), (21433, 28458), (40300, 28458), (30085, 28985), (7956, 29291), (39496, 29862), (11922, 29869), (3154, 30160), (7502, 30533), (29255, 30628), (21152, 30964), (35245, 31079), (21192, 31079), (42654, 31153), (38871, 31453), (13799, 31543), (13027, 31543), (20115, 31993), (1231, 32923), (7956, 32991), (36921, 33015), (6563, 33125), (42799, 33140), (40300, 33312), (8554, 33470), (38871, 33512), (31329, 33566), (14694, 33600), (21371, 33600), (5995, 33600), (44285, 33600), (38871, 33600), (27531, 33600), (3615, 33600), (11071, 33600), (6671, 33600), (37441, 33600), (15437, 33600), (15112, 33908), (12776, 34192), (37268, 34286), (27668, 34514), (26617, 34514), (1270, 34514), (14184, 34514), (31385, 34514), (39527, 34784), (38053, 34792), (17687, 35534), (36747, 35912), (37542, 35912), (43574, 36537), (18873, 36537), (25927, 36604), (31870, 36783), (33896, 37148), (13463, 37157), (41276, 37400), (1498, 37426), (31329, 37688), (26646, 38107), (31419, 38342), (6227, 38353), (16528, 38353), (7956, 38678), (35245, 38747), (8398, 38783), (7502, 38916), (2580, 39201), (30085, 39201), (8625, 39718), (15112, 39718), (37542, 39736), (26497, 39774), (2034, 39774), (43641, 40450), (26617, 40786), (40300, 40786), (10407, 40786), (42799, 40786), (10972, 40786), (10839, 40933), (34008, 41137), (7617, 41323), (19877, 41670), (7091, 41944), (43773, 41973), (31419, 42159), (33616, 42161), (15144, 42231), (38053, 42231), (6563, 42456), (11581, 42904), (1231, 42904), (36747, 42904), (42104, 43158), (10407, 43158), (8678, 43158), (31395, 43158), (15112, 43182), (7502, 43187), (32005, 43324), (19552, 43432), (12776, 43432), (40300, 43975), (16528, 43975), (7619, 43975), (16119, 43975), (5007, 43975), (5480, 44074), (44595, 44082), (22223, 44329), (20115, 45014)]

print(g_raw.vp.userID[44])
print(g_raw.vp.userID[29115])
print(g_raw_friend.vp.userID[44])
print(g_raw_friend.vp.userID[29115])
print(g_raw_friend_noPriv.vp.userID[44])
print(g_raw_friend_noPriv.vp.userID[29115])
print(new_edges)

print(c_newE)

print(len(g_raw.get_edges()))
'''
    #mask = np.isin(g_raw_friend.get_edges(), e)
    #mask2 = np.nonzero(mask)
    #print(mask2)

    #if np.array([source,source]) in g_raw_friend.get_edges():
    if (source, source) in tuplelist:
        #print("FOUND", type(np.array([source,source])))
        print("FOUND", (source, source))
    else:
        #print("NOT FOUND", np.array([source,source]))
        print("NOT FOUND", (source, source))

    #index = np.where(g_raw_friend.get_edges() == e)
    #print(index)

    break
'''
'''    if x3 in g_raw_friend.get_edges():
        print("FOUND")
    else:
        print("NOT FOUND")

    #if [source, source] in g_raw_friend.get_edges():
        #print("test is in g_raw_friend")


    break
'''

# e = g.add_edge(v1, v2)



'''

#########################
### Subgraph Creation ###
#########################


# g_friendship contains User, FRIENDS_WITH
g_friendship = gt.GraphView(g_all, vfilt=lambda v: g_all.vp.userID[v] != "")

# g_issues contains Issues, GIVES_ISSUES
g_issues = gt.GraphView(g_all, vfilt=lambda v: g_all.vp.issuesID[v] != "")




####################
### Deskriptives ###
####################

### Deskriptives Friendship Network ###

#-- Number of nodes , edges, node properties, edge properties --#

print(g_all)                # 90696 vertices and 188965 edges, 84 internal vertex properties, 2 internal edge properties
print(g_friendship)         # 45348 vertices and 143617 edges, 84 internal vertex properties, 2 internal edge properties
print(g_issues)             # 45348 vertices and 0      edges, 84 internal vertex properties, 2 internal edge properties


#-- Density of Friendship Network --#

v_friendship = g_friendship.get_vertices()
e_friendship = g_friendship.get_edges()

print("Number of Nodes: ", len(v_friendship))   #  45348
print("Number of Edges: ", len(e_friendship))   # 143617

d_friendship = len(e_friendship) / ((len(v_friendship) * (len(v_friendship)-1))/2)
print("Density: ", d_friendship)                # 0.00013967836646323054


#-- Avg Degree --#

degree_list = g_friendship.get_in_degrees(g_friendship.get_vertices())
print(degree_list)

#in:    sum:  143617.0 max:  2025 min:  0 len:  45348   Avg Degree:  3.1669974420040576
#out:   sum:  143617.0 max:   888 min:  0 len:  45348   Avg Degree:  3.1669974420040576
# Avg Degree:  3.1669974420040576
# Median Degree:  0.0
# Mode Degree:  0

print("sum: ", sum(degree_list), "max: ", max(degree_list), "min: ", min(degree_list), "len: ", len(degree_list))
# sum = number of edges, len = number of verticies

#print("degree_list: ", degree_list)# HERE THE MAX IS 256

avg_degree =  sum(degree_list) / len(degree_list)

print("Avg Degree: ", avg_degree)


print("Median Degree: ", np.median(degree_list))

print("Mode Degree: ", stats.mode(degree_list)[0][0])
#print("Mode Degree: ", stats.mode(degree_list, axis = None))



#-- Degree Distribution --#

degree_hist = gt.vertex_hist(g_friendship, "out") # 2d array with [frequency][degree]

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
#plt.savefig("degree_hist.png")

"""
plt.savefig("degree_dist", dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None, metadata=None)
"""

#-- Clustering Coefficiants global vs avg local --#


global_clus = gt.global_clustering(g_friendship)
print('global CC', global_clus)




#v = g_friendship.vertex(10)

#print(v)

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









#-- paths ? --#



#-- Size of Components --# ?

#-- Density of Components --# ?

#-- avg degree of Components --# ?


# Do people with shared political views flock together? see study in lecture

#-- Correlation analysis --#

#gt.combined_corr_hist


#graph_draw(g_friendship, vertex_text=g.vertex_index, output="g_friendship.pdf")


'''