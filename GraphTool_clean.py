import graph_tool.all as gt



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
vprop_ideo = g_all.new_vertex_property("string")    # political_ideology
#vprop_party = g_all.new_vertex_property("string")   # party # not created, because it is already innate to User-nodes


### Enriching g_all with empty PropertyMaps ###

g_all.vp.abor = vprop_abor
g_all.vp.gay = vprop_gay
g_all.vp.warm = vprop_warm
g_all.vp.drug = vprop_drug
g_all.vp.health = vprop_health

g_all.vp.socia = vprop_socia
g_all.vp.ideo = vprop_ideo
#g_all.vp.abor = vprop_party    # not created, because it is already innate to User-nodes


### Filling PropertyMaps ###

c = 0
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
            g_all.vp.ideo[i] = g_all.vp.political_ideology[j]

    if c % 1000 == 0:
        print(c)
    c = c+1

### Assortative Mixing Measure ###

g_friendship_mod = gt.GraphView(g_all, vfilt=lambda v: g_all.vp.userID[v] != "") # new subgraph of now enriched g_all

print("Assortative Mixing coefficient & variance - Abortion: ", gt.assortativity(g_friendship_mod, g_friendship_mod.vp.abor))

# todo how many unique values does abortion & co have?
# todo does the used assortativity measure work with multiple(?) categories? -> Is the measure correct?
# todo investigate the problem with plotting