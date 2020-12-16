import graph_tool.all as gt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy import stats

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



#################################################
### Descriptives of whole friendships network ###
#################################################

#g_friendship = gt.load_graph('debate.org_test_mod.graphml', fmt='graphml')
#g_friendship = gt.load_graph('debate.org_friends_limit_mod.graphml', fmt='graphml')
g_all = gt.load_graph('debate.org_with_issues_mod.graphml', fmt='graphml')

# create propertymap
# get all nodes with userID != ""
# for those nodes look for their neighboors wit h issuesID != ""
# fill property map with the certain value of interest



#g_all.list_properties()

#print("value: ", g_all.vertex_properties.party[70000])

g_friendship = gt.GraphView(g_all, vfilt=lambda v: g_all.vp.userID[v] != "")
g_issues = gt.GraphView(g_all, vfilt=lambda v: g_all.vp.issuesID[v] != "")

#g_issues.list_properties()

#print("PARTY UNIQUE VALUES?: ", g_all.vp.party.a)
print("PARTY UNIQUE VALUES?: ")
'''
vals = np.array([])
for v in g_friendship.vertices():
    vals = np.append(vals, g_friendship.vp.party[v])

print(vals)
print(np.unique(vals))
'''
print("party value of node 30.000: ", g_all.vp.party[30000])

print("get_vertices() below: ")
print(g_friendship.get_vertices())
print(g_issues.get_vertices())
print("get_vertices() above: ")

vprop_abor = g_all.new_vertex_property("string")
g_all.vp.abor = vprop_abor

#print("abortion value: ", g_all.vp.abortion[60000])
print("abortion value: ", g_all.vp.abor[30000])





c = 0
for i in g_friendship.get_vertices():       # this approach works because there is only one issues node for each respective user node
    abor = g_all.get_all_neighbors(i)
    for j in abor:
        if j not in g_friendship.get_vertices():
            g_all.vp.abor[i] = g_all.vp.abortion[j]
    if c % 1000 == 0:
        print(c)
    c = c+1



print("abortion value: ", g_all.vp.abor[30000])

c = 0
vals = np.array([])
for v in g_all.vertices():
    vals = np.append(vals, g_all.vp.abor[v])
    if c % 1000 == 0:
        print(c)
    c = c + 1

print(vals)
print(np.unique(vals))

g_friendship = gt.GraphView(g_all, vfilt=lambda v: g_all.vp.userID[v] != "")

print("abortion value: ", g_friendship.vp.abor[30000])

#g_friendship_abor_ProCon = gt.GraphView(g_friendship, vfilt=lambda v: g_friendship.vp.abor[v] == ("Pro" | "Con"))
g_friendship_abor_ProCon = gt.GraphView(g_friendship, vfilt=lambda v: g_friendship.vp.abor[v] == "Pro" or g_friendship.vp.abor[v] == "Con")
#g_friendship_abor_ProConUnd = gt.GraphView(g_friendship, vfilt=lambda v: g_friendship.vp.abor[v] == ("Pro" | "Con" | "Und"))
g_friendship_abor_ProConUnd = gt.GraphView(g_friendship, vfilt=lambda v: g_friendship.vp.abor[v] == "Pro" or g_friendship.vp.abor[v] == "Con" or g_friendship.vp.abor[v] == "Und")

c = 0
vals = np.array([])
for v in g_friendship_abor_ProCon.vertices():
    vals = np.append(vals, g_friendship_abor_ProCon.vp.abor[v])
    if c % 1000 == 0:
        print(c)
    c = c + 1

print('g_friendship_abor_ProCon: ', np.unique(vals))

c = 0
vals = np.array([])
for v in g_friendship_abor_ProConUnd.vertices():
    vals = np.append(vals, g_friendship_abor_ProConUnd.vp.abor[v])
    if c % 1000 == 0:
        print(c)
    c = c + 1

print('g_friendship_abor_ProConUnd', np.unique(vals))


#print(gt.assortativity(g_friendship, "abor"))
print(gt.assortativity(g_friendship, g_friendship.vp.abor))
#print(gt.assortativity(g_friendship, vprop_abor))


h = gt.corr_hist(g_friendship, g_friendship.vp.abor, g_friendship.vp.abor)
plt.clf()
plt.xlabel("Source abortion")
plt.ylabel("Target abortion")
plt.imshow(h[0].T, interpolation="nearest", origin="lower")
plt.colorbar()
plt.savefig("corr.svg")


#g_friendship = gt.GraphView(g_all, vfilt= lambda v: g_friendship.vp.comp[v] == sec_compL_id)

#print(g_friendship)
#print(g.vertex_index[12])

#g_friendship.list_properties()

#print(g_friendship.vertex_properties.party[0])
'''
gt.graph_draw(g_friendship, pos=None, vertex_fill_color=None, # todo Why is this directed?
              vertex_size=None,
              vcmap=matplotlib.cm.gist_heat,
              vorder=None, output="g_friendship.pdf")
'''
print(g_all)
print(g_friendship)

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

