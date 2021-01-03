import graph_tool.all as gt
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

import sys
np.set_printoptions(threshold=sys.maxsize)


######################
### Initialization ###
######################

# g_all contains nodes: User, Issues
# g_all contains edges: FRIENDS_WITH, GIVES_ISSUES
g_all = gt.load_graph('debate.org_with_issues_mod.graphml', fmt='graphml')


### Subgraphs ###

# g_friendship contains User, FRIENDS_WITH
g_friendship = gt.GraphView(g_all, vfilt=lambda v: g_all.vp.userID[v] != "")

# g_issues contains Issues, GIVES_ISSUES
g_issues = gt.GraphView(g_all, vfilt=lambda v: g_all.vp.issuesID[v] != "")


####################
### Deskriptives ###
####################

print("PARTY UNIQUE VALUES?: ", g_all.vp.party.a)


### Number of nodes and edges #todo and other stuff? ###
print(g_all)
print(g_friendship)
print(g_issues)

#-- density --#

v_friendship = g_friendship.get_vertices()
e_friendship = g_friendship.get_edges()

#print(e_friendship)
print("Number of Nodes: ", len(v_friendship)) #  45348
print("Number of Edges: ", len(e_friendship)) # 143617

density = len(e_friendship) / ((len(v_friendship) *len(v_friendship)) / 2 )

print("Density: ", density)


## differenciation between connected and isolated ones? argument: the ones that choose not to participate in the network are not essential to the network measurements



#-- Avg Degree --#

degree_list = g_friendship.get_out_degrees(g_friendship.get_vertices())

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

helper = []
for i in np.unique(hist):
    helper[i] =

y = np.unique(comp.a)
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
closeness = gt.closeness(u_frin)
gt.graph_draw(u_frin, pos=None, vertex_fill_color=closeness,
              vertex_size=gt.prop_to_size(closeness, mi=5, ma=15),
              vcmap=matplotlib.cm.gist_heat,
              vorder=closeness, output="polblogs_closeness.pdf")
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