import graph_tool.all as gt
import numpy as np
import matplotlib.pyplot as plt

#from pylab import *

'''
    with open("Output.txt", "w") as text_file:
    print("explo", file=text_file)
'''

'''
g = graph_tool.Graph()
v1 = g.add_vertex()
v2 = g.add_vertex()
e = g.add_edge(v1, v2)

graph_draw(g, vertex_text=g.vertex_index, output="two-nodes.pdf")

print(v1.out_degree())
print(e.source(), e.target(), "hahaha lalala")
print(e.source(), e.target())

vlist = g.add_vertex(10)
print(len(list(vlist)))

print(g)

v = g.add_vertex()
print(g.vertex_index[v])

print(int(v))
'''

'''
eprop = g.new_edge_property("string")
g.edge_properties["some name"] = eprop
g.list_properties()
'''



###########################################
### Descriptives of friendships network ###
###########################################

#g_friendship = gt.load_graph('debate.org_test_mod.graphml', fmt='graphml')
g_friendship = gt.load_graph('debate.org_friends_limit_mod.graphml', fmt='graphml')

#print(g_friendship)
#print(g.vertex_index[12])

#g_friendship.list_properties()

#print(g_friendship.vertex_properties.party[0])

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


#todo median degree

#-- Degree Distribution --#

degree_hist = gt.vertex_hist(g_friendship, "out") # 2d array with [frequency][degree]

print(degree_hist[1]) # HERE THE MAX IS 257 WHYYY?

y = degree_hist[0]
x = degree_hist[1][:-1]

print(len(y), len(x))



#ax.set_xscale('log')

fig, ax = plt.subplots()
plt.bar(x, y, color='grey')
ax.set_yscale('log')
ax.set_xscale('log')
plt.xlabel('Degree')
plt.ylabel('Fequency')


#plt.plot(x, y, 'o', color='black')
#plt.savefig("degree_hist.png")

"""
plt.savefig("degree_dist", dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None, metadata=None)
"""



#-- Closeness Distribution --#

#-- Betweenness Distribution --#

#-- Eigenvector Distribution --#

#-- Number of Components --#

#v = g_friendship.vertex(10)

#print(v)

vprop_comp = g_friendship.new_vertex_property("int")

g_friendship.vp.comp = vprop_comp

#g_friendship.vp.comp[v] = True

#print(g_friendship.vertex_properties.comp[8])

comp, hist = gt.label_components(g_friendship, vprop_comp, attractors=False)

#print(g_friendship.vertex_properties.comp[8])

print('comp array: ', comp.a) #  .a = .get_array()[:]

print(sum(comp.a), len(comp.a))



print('hist array: ', hist)
print(sum(hist), len(hist)) # why does it say that last value of 256 is occuring 622 times? its not occuring once. 622 is the size of the com array. weird shit
# larges component in lmited sample is labled 145 (300 times)

#-- Largest Components --#

#vprop_compL = g_friendship.new_vertex_property("bool")

#g_friendship.vp.compL = vprop_compL

u_frin = gt.extract_largest_component(g_friendship)
print('larges comp', u_frin)

#for i in len(comp):
 #g_friendship.vp.vprop_comp[i] = comp[i]

#print(comp, hist, )


sec_compL = np.sort(hist)

print(sec_compL)

sec_compL_pos = np.sort(hist)[-2:-1]

sec_compL_id = np.where(hist==sec_compL_pos)[0][0]


print(sec_compL_id)


sec_compL = gt.GraphView(g_friendship, vfilt= lambda v: g_friendship.vp.comp[v] == sec_compL_id)

print(sec_compL)


#-- (Pseudo-) Diameter --#

dist, ends = gt.pseudo_diameter(u_frin)

print('(Pseudo-) Diameter: ', dist)
print('(Pseudo-) Diameter start:', ends[0], 'end:', ends[1])



#-- paths ? --#

#-- Clustering Coefficiants global vs avg local --#


global_clus = gt.global_clustering(g_friendship)
print('global CC', global_clus)


#-- Size of Components --# ?

#-- Density of Components --# ?

#-- avg degree of Components --# ?


# Do people with shared political views flock together? see study in lecture

#-- Correlation analysis --#

#gt.combined_corr_hist


#graph_draw(g_friendship, vertex_text=g.vertex_index, output="g_friendship.pdf")

