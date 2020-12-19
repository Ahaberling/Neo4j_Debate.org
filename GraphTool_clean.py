import graph_tool.all as gt
import numpy as np
import matplotlib.pyplot as plt


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


##########################
### Assortative Mixing ###
##########################

# In the following User-nodes are enriched with information about their political stands. This is done via PropertyMaps.
# This information is extracted from their respective Issues-node. Each User-node has exacly one corresponding Issues-node.
# Technically all nodes are enriched with these PerpertyMaps, not only the user ones but only the user_nodes matter for
# this analysis of assortative mixing

### Creating PropertyMaps ###

vprop_abor = g_all.new_vertex_property("string")    # abortion
vprop_gay = g_all.new_vertex_property("string")     # gay_marriage
vprop_warm = g_all.new_vertex_property("string")    # global_warming
vprop_drug = g_all.new_vertex_property("string")    # drug_legaliz
vprop_health = g_all.new_vertex_property("string")  # national_health_care

vprop_socia = g_all.new_vertex_property("string")   # socialism

vprop_prog = g_all.new_vertex_property("int")    # int value indicating conservatism  (-5) - progressiveness (+5)
                                                    # (sum of stances regarding abortion, ..., health care

# not created, because it is already innate to User-nodes
#vprop_party = g_all.new_vertex_property("string")   # party
#vprop_ideo = g_all.new_vertex_property("string")    # political_ideology


### Enriching g_all with empty PropertyMaps ###

g_all.vp.abor = vprop_abor
g_all.vp.gay = vprop_gay
g_all.vp.warm = vprop_warm
g_all.vp.drug = vprop_drug
g_all.vp.health = vprop_health

g_all.vp.socia = vprop_socia

g_all.vp.prog = vprop_prog


### Filling PropertyMaps ###

c = 0
c_max = len(g_friendship.get_vertices())
for i in g_friendship.get_vertices():       # this approach works because there is only one issues node for each respective user node
    neigh = g_all.get_all_neighbors(i)
    for j in neigh:
        if j not in g_friendship.get_vertices():
            g_all.vp.abor[i] = g_all.vp.abortion[j]
            g_all.vp.gay[i] = g_all.vp.gay_marriage[j]
            g_all.vp.warm[i] = g_all.vp.global_warming[j]
            g_all.vp.drug[i] = g_all.vp.drug_legaliz[j]
            g_all.vp.health[i] = g_all.vp.national_health_care[j]
            g_all.vp.socia[i] = g_all.vp.socialism[j]

    if c % 1000 == 0:
        print("Filling PropertyMaps: ", c, "/", c_max)
    c = c+1
print("Filling PropertyMaps: ", c_max, "/", c_max)

### Unique Values of PropertyMaps ###

c = 0
c_max = len(g_all.get_vertices())
vals_abor = np.array([])
vals_gay = np.array([])
vals_warm = np.array([])
vals_drug = np.array([])
vals_health = np.array([])

vals_socia = np.array([])

vals_party = np.array([])
vals_ideo = np.array([])
'''
for v in g_all.vertices():
    vals_abor = np.append(vals_abor, g_all.vp.abor[v])
    vals_gay = np.append(vals_gay, g_all.vp.gay[v])
    vals_warm = np.append(vals_warm, g_all.vp.warm[v])
    vals_drug = np.append(vals_drug, g_all.vp.drug[v])
    vals_health = np.append(vals_health, g_all.vp.health[v])

    vals_socia = np.append(vals_socia, g_all.vp.socia[v])

    #vals_party = np.append(vals_party, g_all.vp.party[v]) # to many
    vals_ideo = np.append(vals_ideo, g_all.vp.political_ideology[v])

    if c % 1000 == 0:
        print("Identifying values range of PropertyMaps", c, "/", c_max)
    c = c + 1
print("Identifying values range of PropertyMaps", c_max, "/", c_max)
'''

### Assortative Mixing Measure with all values ###

g_friendship_prop = gt.GraphView(g_all, vfilt=lambda v: g_all.vp.userID[v] != "")  # new subgraph of now enriched g_all. g_all could have been used too,
                                                                                        # but this might be more efficient?

print("Abortion value range:  ", np.unique(vals_abor))
print("Assortative Mixing coefficient & variance - Abortion: ", gt.assortativity(g_friendship_prop, g_friendship_prop.vp.abor))
print("\n")
print("Gay Marriage value range:  ", np.unique(vals_gay))
print("Assortative Mixing coefficient & variance - Gay Marriage: ", gt.assortativity(g_friendship_prop, g_friendship_prop.vp.gay))
print("\n")
print("Global Warming value range:  ", np.unique(vals_warm))
print("Assortative Mixing coefficient & variance - Global Warming Exists: ", gt.assortativity(g_friendship_prop, g_friendship_prop.vp.warm))
print("\n")
print("Drug Legalization value range:  ", np.unique(vals_drug))
print("Assortative Mixing coefficient & variance - Drug Legalization: ", gt.assortativity(g_friendship_prop, g_friendship_prop.vp.drug))
print("\n")
print("National Health Care value range:  ", np.unique(vals_health))
print("Assortative Mixing coefficient & variance - National Health Care: ", gt.assortativity(g_friendship_prop, g_friendship_prop.vp.health))
print("\n")
#print("\n")
print("Socialism value range:  ", np.unique(vals_socia))
print("Assortative Mixing coefficient & variance - Socialism: ", gt.assortativity(g_friendship_prop, g_friendship_prop.vp.socia))
print("\n")
#print("\n")
#print("Political Party value range:  ", np.unique(vals_party)) # to many
#print("Assortative Mixing coefficient & variance - Political Party: ", gt.assortativity(g_friendship_prop, g_friendship_prop.vp.party))
#print("\n")
print("Political Ideology value range:  ", np.unique(vals_ideo))
print("Assortative Mixing coefficient & variance - Political Ideology: ", gt.assortativity(g_friendship_prop, g_friendship_prop.vp.political_ideology))


### Assortative Mixing Measure with Pro-, Con- Undecided-values ###

#g_friendship_prop_filter1 = gt.GraphView(g_all, vfilt=lambda v: g_all.vp.userID[v] != "")

g_friendship_abor_ProConUnd = gt.GraphView(g_all, vfilt=lambda v: g_all.vp.abor[v] == "Pro" or g_all.vp.abor[v] == "Con" or g_all.vp.abor[v] == "Und")
g_friendship_abor_ProConUnd = gt.GraphView(g_friendship_prop, vfilt=lambda v: g_friendship_prop.vp.abor[v] == "Pro" or g_friendship_prop.vp.abor[v] == "Con" or g_friendship_prop.vp.abor[v] == "Und")
g_friendship_gay_ProConUnd = gt.GraphView(g_friendship_prop, vfilt=lambda v: g_friendship_prop.vp.gay[v] == "Pro" or g_friendship_prop.vp.gay[v] == "Con" or g_friendship_prop.vp.gay[v] == "Und")
g_friendship_warm_ProConUnd = gt.GraphView(g_friendship_prop, vfilt=lambda v: g_friendship_prop.vp.warm[v] == "Pro" or g_friendship_prop.vp.warm[v] == "Con" or g_friendship_prop.vp.warm[v] == "Und")
g_friendship_drug_ProConUnd = gt.GraphView(g_friendship_prop, vfilt=lambda v: g_friendship_prop.vp.drug[v] == "Pro" or g_friendship_prop.vp.drug[v] == "Con" or g_friendship_prop.vp.drug[v] == "Und")
g_friendship_health_ProConUnd = gt.GraphView(g_friendship_prop, vfilt=lambda v: g_friendship_prop.vp.health[v] == "Pro" or g_friendship_prop.vp.health[v] == "Con" or g_friendship_prop.vp.health[v] == "Und")

g_friendship_socia_ProConUnd = gt.GraphView(g_friendship_prop, vfilt=lambda v: g_friendship_prop.vp.socia[v] == "Pro" or g_friendship_prop.vp.socia[v] == "Con" or g_friendship_prop.vp.socia[v] == "Und")

#g_friendship_party_ProConUnd = gt.GraphView(g_friendship_prop, vfilt=lambda v: g_friendship_prop.vp.party[v] == "Pro" or g_friendship_prop.vp.party[v] == "Con" or g_friendship_prop.vp.party[v] == "Und")
g_friendship_ideo_ProConUnd = gt.GraphView(g_friendship_prop, vfilt=lambda v: g_friendship_prop.vp.political_ideology[v] == "Conservative" or g_friendship_prop.vp.political_ideology[v] == "Progressive" or g_friendship_prop.vp.political_ideology[v] == "Liberal")

print("Assortative Mixing coefficient & variance - Abortion (Pro/Con/Und): ", gt.assortativity(g_friendship_abor_ProConUnd, g_friendship_abor_ProConUnd.vp.abor))
print("Assortative Mixing coefficient & variance - Gay Marriage (Pro/Con/Und): ", gt.assortativity(g_friendship_gay_ProConUnd, g_friendship_gay_ProConUnd.vp.gay))
print("Assortative Mixing coefficient & variance - Global Warming Exists (Pro/Con/Und): ", gt.assortativity(g_friendship_warm_ProConUnd, g_friendship_warm_ProConUnd.vp.warm))
print("Assortative Mixing coefficient & variance - Drug Legalization (Pro/Con/Und): ", gt.assortativity(g_friendship_drug_ProConUnd, g_friendship_drug_ProConUnd.vp.drug))
print("Assortative Mixing coefficient & variance - National Health Care (Pro/Con/Und): ", gt.assortativity(g_friendship_health_ProConUnd, g_friendship_health_ProConUnd.vp.health))
print("\n")
print("Assortative Mixing coefficient & variance - Socialism (Pro/Con/Und): ", gt.assortativity(g_friendship_socia_ProConUnd, g_friendship_socia_ProConUnd.vp.socia))
print("\n")
#print("Assortative Mixing coefficient & variance - Political Party (): ", gt.assortativity(g_friendship_ideo_ProConUnd, g_friendship_ideo_ProConUnd.vp.party))
print("Assortative Mixing coefficient & variance - Political Ideology (Conservative/Progressive/Liberal): ", gt.assortativity(g_friendship_ideo_ProConUnd, g_friendship_ideo_ProConUnd.vp.political_ideology))


### Assortative Mixing Measure with Pro-, Con- Undecided-values ###

g_friendship_abor_ProCon = gt.GraphView(g_friendship_prop, vfilt=lambda v: g_friendship_prop.vp.abor[v] == "Pro" or g_friendship_prop.vp.abor[v] == "Con")
g_friendship_gay_ProCon = gt.GraphView(g_friendship_prop, vfilt=lambda v: g_friendship_prop.vp.gay[v] == "Pro" or g_friendship_prop.vp.gay[v] == "Con")
g_friendship_warm_ProCon = gt.GraphView(g_friendship_prop, vfilt=lambda v: g_friendship_prop.vp.warm[v] == "Pro" or g_friendship_prop.vp.warm[v] == "Con")
g_friendship_drug_ProCon = gt.GraphView(g_friendship_prop, vfilt=lambda v: g_friendship_prop.vp.drug[v] == "Pro" or g_friendship_prop.vp.drug[v] == "Con")
g_friendship_health_ProCon = gt.GraphView(g_friendship_prop, vfilt=lambda v: g_friendship_prop.vp.health[v] == "Pro" or g_friendship_prop.vp.health[v] == "Con")

g_friendship_socia_ProCon = gt.GraphView(g_friendship_prop, vfilt=lambda v: g_friendship_prop.vp.socia[v] == "Pro" or g_friendship_prop.vp.socia[v] == "Con")

#g_friendship_party_ProCon = gt.GraphView(g_friendship_prop, vfilt=lambda v: g_friendship_prop.vp.party[v] == "Pro" or g_friendship_prop.vp.party[v] == "Con")
g_friendship_ideo_ProCon = gt.GraphView(g_friendship_prop, vfilt=lambda v: g_friendship_prop.vp.political_ideology[v] == "Conservative" or g_friendship_prop.vp.political_ideology[v] == "Progressive")

print("Assortative Mixing coefficient & variance - Abortion (Pro/Con): ", gt.assortativity(g_friendship_abor_ProCon, g_friendship_abor_ProCon.vp.abor))
print("Assortative Mixing coefficient & variance - Gay Marriage (Pro/Con): ", gt.assortativity(g_friendship_gay_ProCon, g_friendship_gay_ProCon.vp.gay))
print("Assortative Mixing coefficient & variance - Global Warming Exists (Pro/Con): ", gt.assortativity(g_friendship_warm_ProCon, g_friendship_warm_ProCon.vp.warm))
print("Assortative Mixing coefficient & variance - Drug Legalization (Pro/Con): ", gt.assortativity(g_friendship_drug_ProCon, g_friendship_drug_ProCon.vp.drug))
print("Assortative Mixing coefficient & variance - National Health Care (Pro/Con): ", gt.assortativity(g_friendship_health_ProCon, g_friendship_health_ProCon.vp.health))
print("\n")
print("Assortative Mixing coefficient & variance - Socialism (Pro/Con): ", gt.assortativity(g_friendship_socia_ProCon, g_friendship_socia_ProCon.vp.socia))
print("\n")
#print("Assortative Mixing coefficient & variance - Political Party (): ", gt.assortativity(g_friendship_ideo_ProCon, g_friendship_ideo_ProCon.vp.party))
print("Assortative Mixing coefficient & variance - Political Ideology (Conservative/Progressive): ", gt.assortativity(g_friendship_ideo_ProCon, g_friendship_ideo_ProCon.vp.political_ideology))


### Assortative Mixing Measure with skalar score ###

c = 0
c_max = len(g_all.get_vertices())
val1, val2, val3, val4, val5 = 0, 0, 0, 0, 0

for i in g_all.vertices():
    if g_all.vp.abor == "Pro":
        val1 = 1
    elif g_all.vp.abor == "Con":
        val1 = -1
    else:
        val1 = 0

    if g_all.vp.gay == "Pro":
        val2 = 1
    elif g_all.vp.gay == "Con":
        val2 = -1
    else:
        val2 = 0

    if g_all.vp.warm == "Pro":
        val3 = 1
    elif g_all.vp.warm == "Con":
        val3 = -1
    else:
        val3 = 0

    if g_all.vp.drug == "Pro":
        val4 = 1
    elif g_all.vp.drug == "Con":
        val4 = -1
    else:
        val4 = 0

    if g_all.vp.health == "Pro":
        val5 = 1
    elif g_all.vp.health == "Con":
        val5 = -1
    else:
        val5 = 0

    prog_score = val1+val2+val3+val4+val5
    g_all.vp.prog[i] = prog_score

    if c % 1000 == 0:
        print("Creating Progressiveness Score", c, "/", c_max)
    c = c + 1
print("Creating Progressiveness Score", c_max, "/", c_max)


c = 0
c_max = len(g_all.get_vertices())
vals_prog = np.array([])

for v in g_all.vertices():
    vals_prog = np.append(vals_prog, g_all.vp.prog[v])

    if c % 1000 == 0:
        print("Identifying values range of Progresiveness Score", c, "/", c_max)
    c = c + 1
print("Identifying values range of Progresiveness Score", c_max, "/", c_max)

print("Progresiveness Score value range: ",np.unique(vals_prog))

print("Assortative Mixing coefficient & variance (skalar) - Progessiveness Score  (-5/5): ", gt.scalar_assortativity(g_all, g_all.vp.prog))
print("Assortative Mixing coefficient & variance (categorial) - Progessiveness Score  (-5/5): ", gt.assortativity(g_all, g_all.vp.prog))


### Assortative Mixing plots ###

h = gt.corr_hist(g_all, g_all.vp.abor, g_all.vp.abor)

plt.clf()

#plt.xlabel("Source out-degree")
#plt.ylabel("Target out-degree")

plt.imshow(h[0].T, interpolation="nearest", origin="lower")

#plt.colorbar()

plt.savefig("corr_abor.svg")

# todo how many unique values does abortion & co have?
# todo does the used assortativity measure work with multiple(?) categories? -> Is the measure correct?
# todo investigate the problem with plotting
