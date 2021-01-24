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

assortativePrePro_bool      = False
load_assortativePrePro_bool = True
uniqueVal_bool              = False
assortAllValues             = False
assortProConUnd             = False
assortProCon                = False
assortScore                 = False
assortPlot_abor             = True


##########################
### Assortative Mixing ###
##########################

# In the following User-nodes are enriched with information about their political stands. This is done via PropertyMaps.
# The information used to enrich is extracted from their respective Issues-node. Each User-node has exacly one corresponding Issues-node.
# Technically all nodes are enriched with these PropertyMaps, not only the user ones, but only the user-nodes matter and are
# considered for this analysis of assortative mixing

### Creating PropertyMaps ###

#-- Main Issues --#

if assortativePrePro_bool == True:
    vprop_abor = g_friend.new_vertex_property("string")  # abortion
    vprop_gay = g_friend.new_vertex_property("string")  # gay_marriage
    vprop_warm = g_friend.new_vertex_property("string")  # global_warming
    vprop_drug = g_friend.new_vertex_property("string")  # drug_legaliz
    vprop_health = g_friend.new_vertex_property("string")  # national_health_care

    vprop_abor_int = g_friend.new_vertex_property("int")  # abortion
    vprop_abor_int_mod = g_friend.new_vertex_property("int")
    vprop_gay_int = g_friend.new_vertex_property("int")  # gay_marriage
    vprop_warm_int = g_friend.new_vertex_property("int")  # global_warming
    vprop_drug_int = g_friend.new_vertex_property("int")  # drug_legaliz
    vprop_health_int = g_friend.new_vertex_property("int")  # national_health_care

    #-- Progressiveness Score using Main Issues --#

    vprop_prog = g_friend.new_vertex_property("int")  # float value indicating conservatism  (-5) - progressiveness (+5)
    vprop_prog_mod = g_friend.new_vertex_property("int")  # float value indicating conservatism  (0) - progressiveness (+10)
    # (sum of stances regarding abortion, ..., health care)
    # float because of the later used plotting function
    # vprop_prog = g_all.new_vertex_property("int16_t")

    #-- Issues used later (eventually) --#

    vprop_socia = g_all.new_vertex_property("string")  # socialism

    vprop_socia_int = g_all.new_vertex_property("int")  # socialism

    #-- Issues not created, because they are already innate to User-nodes --#

    # vprop_party = g_all.new_vertex_property("string")   # party
    # vprop_ideo = g_all.new_vertex_property("string")    # political_ideology


    ### Enriching g_all with empty PropertyMaps ###

    g_friend.vp.abor = vprop_abor
    g_friend.vp.abor = vprop_abor
    g_friend.vp.gay = vprop_gay
    g_friend.vp.warm = vprop_warm
    g_friend.vp.drug = vprop_drug
    g_friend.vp.health = vprop_health

    g_friend.vp.abor_int = vprop_abor_int
    g_friend.vp.abor_int_mod = vprop_abor_int_mod
    g_friend.vp.gay_int = vprop_gay_int
    g_friend.vp.warm_int = vprop_warm_int
    g_friend.vp.drug_int = vprop_drug_int
    g_friend.vp.health_int = vprop_health_int

    g_friend.vp.socia = vprop_socia

    g_friend.vp.socia_int = vprop_socia_int

    g_friend.vp.prog = vprop_prog
    g_friend.vp.prog_mod = vprop_prog_mod



    ### Filling PropertyMaps ###

    c = 0
    c_max = len(g_friend.get_vertices())

    for i in g_friend.get_vertices():  # this approach works because there is only one issues node for each respective user node
        neigh = g_all.get_all_neighbors(i)
        for j in neigh:
            if j not in g_friend.get_vertices():
                g_friend.vp.abor[i] = g_all.vp.abortion[j]
                g_friend.vp.gay[i] = g_all.vp.gay_marriage[j]
                g_friend.vp.warm[i] = g_all.vp.global_warming[j]
                g_friend.vp.drug[i] = g_all.vp.drug_legaliz[j]
                g_friend.vp.health[i] = g_all.vp.national_health_care[j]
                g_friend.vp.socia[i] = g_all.vp.socialism[j]

                if g_all.vp.abortion[j] == "Pro":
                    g_friend.vp.abor_int[i] = 1
                    g_friend.vp.abor_int_mod[i] = 2
                elif g_all.vp.abortion[j] == "Und":
                    g_friend.vp.abor_int[i] = 0
                elif g_all.vp.abortion[j] == "Con":
                    g_friend.vp.abor_int[i] = -1
                    g_friend.vp.abor_int_mod[i] = 1
                else:
                    g_friend.vp.abor_int[i] = -99

                if g_all.vp.gay_marriage[j] == "Pro":
                    g_friend.vp.gay_int[i] = 1
                elif g_all.vp.gay_marriage[j] == "Und":
                    g_friend.vp.gay_int[i] = 0
                elif g_all.vp.gay_marriage[j] == "Con":
                    g_friend.vp.gay_int[i] = -1
                else:
                    g_friend.vp.gay_int[i] = -99

                if g_all.vp.global_warming[j] == "Pro":
                    g_friend.vp.warm_int[i] = 1
                elif g_all.vp.global_warming[j] == "Und":
                    g_friend.vp.warm_int[i] = 0
                elif g_all.vp.global_warming[j] == "Con":
                    g_friend.vp.warm_int[i] = -1
                else:
                    g_friend.vp.warm_int[i] = -99

                if g_all.vp.drug_legaliz[j] == "Pro":
                    g_friend.vp.drug_int[i] = 1
                elif g_all.vp.drug_legaliz[j] == "Und":
                    g_friend.vp.drug_int[i] = 0
                elif g_all.vp.drug_legaliz[j] == "Con":
                    g_friend.vp.drug_int[i] = -1
                else:
                    g_friend.vp.drug_int[i] = -99

                if g_all.vp.national_health_care[j] == "Pro":
                    g_friend.vp.health_int[i] = 1
                elif g_all.vp.national_health_care[j] == "Und":
                    g_friend.vp.health_int[i] = 0
                elif g_all.vp.national_health_care[j] == "Con":
                    g_friend.vp.health_int[i] = -1
                else:
                    g_friend.vp.health_int[i] = -99

                if g_all.vp.socialism[j] == "Pro":
                    g_friend.vp.socia_int[i] = 1
                elif g_all.vp.socialism[j] == "Und":
                    g_friend.vp.socia_int[i] = 0
                elif g_all.vp.socialism[j] == "Con":
                    g_friend.vp.socia_int[i] = -1
                else:
                    g_friend.vp.socia_int[i] = -99


        if c % 1000 == 0:
            print("Filling PropertyMaps: ", c, "/", c_max)

        c = c + 1
    print("Filling PropertyMaps: ", c_max, "/", c_max)


    ### Filling prog_score PropertyMaps ###

    g_friend_prog_ProCon = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.abor[v] == "Pro" or g_friend.vp.abor[v] == "Con" or
                                                                 g_friend.vp.gay[v] == "Pro" or g_friend.vp.gay[v] == "Con" or
                                                                 g_friend.vp.warm[v] == "Pro" or g_friend.vp.warm[v] ==  "Con" or
                                                                 g_friend.vp.drug[v] == "Pro" or g_friend.vp.drug[v] == "Con" or
                                                                 g_friend.vp.health[v] == "Pro" or g_friend.vp.health[v] == "Con")
    # A User has to have at least one strong position on one of the key issues to get an progressiveness score

    c = 0
    c_max = len(g_friend_prog_ProCon.get_vertices())

    for i in g_friend_prog_ProCon.get_vertices():

        prog_score = 0
        if g_friend.vp.abor_int[i] != -99:
            prog_score = prog_score + g_friend.vp.abor_int[i]
        if g_friend.vp.gay_int[i] != -99:
            prog_score = prog_score + g_friend.vp.gay_int[i]
        if g_friend.vp.warm_int[i] != -99:
            prog_score = prog_score + g_friend.vp.warm_int[i]
        if g_friend.vp.drug_int[i] != -99:
            prog_score = prog_score + g_friend.vp.drug_int[i]
        if g_friend.vp.health_int[i] != -99:
            prog_score = prog_score + g_friend.vp.health_int[i]

        g_friend.vp.prog[i] = prog_score
        g_friend.vp.prog_mod[i] = prog_score + 5

        if c % 1000 == 0:
            print("Filling PropertyMaps - prog_score: ", c, "/", c_max)

        c = c + 1
    print("Filling PropertyMaps - prog_score: ", c_max, "/", c_max)

    g_friend.save("Graph_Preprocessed_Approach1+AssoPrePro.graphml")

### Load Assortativity-Preprocessed Graph ###

if load_assortativePrePro_bool == True:
    g_friend = gt.load_graph('Graph_Preprocessed_Approach1+AssoPrePro.graphml', fmt='graphml')


### Unique Values of PropertyMaps ###

if uniqueVal_bool == True:

    vals_abor = np.array([])
    vals_gay = np.array([])
    vals_warm = np.array([])
    vals_drug = np.array([])
    vals_health = np.array([])

    vals_abor_int = np.array([])
    vals_gay_int = np.array([])
    vals_warm_int = np.array([])
    vals_drug_int = np.array([])
    vals_health_int = np.array([])

    vals_socia = np.array([])

    vals_socia_int = np.array([])

    vals_party = np.array([])
    vals_ideo = np.array([])

    vals_progScore = np.array([])
    vals_progScore_mod = np.array([])


    c = 0
    c_max = len(g_friend.get_vertices())

    for v in g_friend.vertices():
        vals_abor = np.append(vals_abor, g_friend.vp.abor[v])
        vals_gay = np.append(vals_gay, g_friend.vp.gay[v])
        vals_warm = np.append(vals_warm, g_friend.vp.warm[v])
        vals_drug = np.append(vals_drug, g_friend.vp.drug[v])
        vals_health = np.append(vals_health, g_friend.vp.health[v])

        vals_abor_int = np.append(vals_abor_int, g_friend.vp.abor_int[v])
        vals_gay_int = np.append(vals_gay_int, g_friend.vp.gay_int[v])
        vals_warm_int = np.append(vals_warm_int, g_friend.vp.warm_int[v])
        vals_drug_int = np.append(vals_drug_int, g_friend.vp.drug_int[v])
        vals_health_int = np.append(vals_health_int, g_friend.vp.health_int[v])

        vals_socia = np.append(vals_socia, g_friend.vp.socia[v])

        vals_socia_int = np.append(vals_socia_int, g_friend.vp.socia_int[v])

        vals_party = np.append(vals_party, g_all.vp.party[v]) # to many
        vals_ideo = np.append(vals_ideo, g_friend.vp.political_ideology[v])

        vals_progScore = np.append(vals_progScore, g_friend.vp.prog[v])
        vals_progScore_mod = np.append(vals_progScore_mod, g_friend.vp.prog_mod[v])

        if c % 1000 == 0:
            print("Identifying values range of PropertyMaps", c, "/", c_max)
        c = c + 1
    print("Identifying values range of PropertyMaps", c_max, "/", c_max)

    print("range of vals_abor: ", np.unique(vals_abor))                     # ['Con' 'N/O' 'N/S' 'Pro' 'Und']
    print("range of vals_gay: ", np.unique(vals_gay))                       #  same ...
    print("range of vals_warm: ", np.unique(vals_warm))
    print("range of vals_drug: ", np.unique(vals_drug))
    print("range of vals_health: ", np.unique(vals_health))
    print("range of vals_socia: ", np.unique(vals_socia))

    print("range of vals_abor_int: ", np.unique(vals_abor_int))             # [-99.  -1.   0.   1.]
    print("range of vals_gay_int: ", np.unique(vals_gay_int))               #  same ...
    print("range of vals_warm_int: ", np.unique(vals_warm_int))
    print("range of vals_drug_int: ", np.unique(vals_drug_int))
    print("range of vals_health_int: ", np.unique(vals_health_int))
    print("range of vals_socia_int: ", np.unique(vals_socia_int))

    print("range of vals_party: ", np.unique(vals_party))                   # too many
    print("range of vals_ideo: ", np.unique(vals_ideo))                     # ['Anarchist' 'Apathetic' 'Communist' 'Conservative' 'Green' 'Labor'
                                                                            # 'Liberal' 'Libertarian' 'Moderate' 'Not Saying' 'Other' 'Progressive'
                                                                            # 'Socialist' 'Undecided']
    print("range of vals_progScore: ", np.unique(vals_progScore))           # [-5. -4. -3. -2. -1.  0.  1.  2.  3.  4.  5.]
    print("range of vals_progScore_mod: ", np.unique(vals_progScore_mod))   #
    print("length of progScore: ", len(vals_progScore))                     # 45348



### Assortative Mixing Measure with all values ###

if assortAllValues == True:

    print("\n\nAssortative Mixing Measure with all values \n ")
    print("Assortative Mixing coefficient & variance - Abortion (All): ", gt.assortativity(g_friend, g_friend.vp.abor))
    print("Assortative Mixing coefficient & variance - Gay Marriage (All): ", gt.assortativity(g_friend, g_friend.vp.gay))
    print("Assortative Mixing coefficient & variance - Global Warming Exists (All): ", gt.assortativity(g_friend, g_friend.vp.warm))
    print("Assortative Mixing coefficient & variance - Drug Legalization (All): ", gt.assortativity(g_friend, g_friend.vp.drug))
    print("Assortative Mixing coefficient & variance - National Health Care (All): ", gt.assortativity(g_friend, g_friend.vp.health))
    print("Assortative Mixing coefficient & variance - Socialism (All): ", gt.assortativity(g_friend, g_friend.vp.socia))
    # print("Assortative Mixing coefficient & variance - Political Party (All): ", gt.assortativity(g_friend, g_friend.vp.party))           # too many values
    print("Assortative Mixing coefficient & variance - Political Ideology (All): ", gt.assortativity(g_friend, g_friend.vp.political_ideology))



### Assortative Mixing Measure with Pro-, Con- Undecided-values ###

if assortProConUnd == True:

    g_friendship_abor_ProConUnd = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.abor[v] == "Pro" or
                                                                                  g_friend.vp.abor[v] == "Con" or
                                                                                  g_friend.vp.abor[v] == "Und")
    g_friendship_gay_ProConUnd = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.gay[v] == "Pro" or
                                                                                 g_friend.vp.gay[v] == "Con" or
                                                                                 g_friend.vp.gay[v] == "Und")
    g_friendship_warm_ProConUnd = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.warm[v] == "Pro" or
                                                                                  g_friend.vp.warm[v] == "Con" or
                                                                                  g_friend.vp.warm[v] == "Und")
    g_friendship_drug_ProConUnd = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.drug[v] == "Pro" or
                                                                                  g_friend.vp.drug[v] == "Con" or
                                                                                  g_friend.vp.drug[v] == "Und")
    g_friendship_health_ProConUnd = gt.GraphView(g_friend,  vfilt=lambda v: g_friend.vp.health[v] == "Pro" or
                                                                                    g_friend.vp.health[v] == "Con" or
                                                                                    g_friend.vp.health[v] == "Und")

    g_friendship_socia_ProConUnd = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.socia[v] == "Pro" or
                                                                                   g_friend.vp.socia[v] == "Con" or
                                                                                   g_friend.vp.socia[v] == "Und")

    # g_friendship_party_ProConUnd = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.party[v] == "" or g_friend.vp.party[v] == "" or g_friend.vp.party[v] == "")
    g_friendship_ideo_ProConUnd = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.political_ideology[v] == "Conservative" or
                                                                         g_friend.vp.political_ideology[v] == "Progressive" or
                                                                         g_friend.vp.political_ideology[v] == "Liberal")

    print("\n\nAssortative Mixing Measure with Pro-, Con- Undecided-values \n ")

    print("Assortative Mixing coefficient & variance - Abortion (Pro/Con/Und): ",
          gt.assortativity(g_friendship_abor_ProConUnd, g_friendship_abor_ProConUnd.vp.abor))
    print("Assortative Mixing coefficient & variance - Gay Marriage (Pro/Con/Und): ",
          gt.assortativity(g_friendship_gay_ProConUnd, g_friendship_gay_ProConUnd.vp.gay))
    print("Assortative Mixing coefficient & variance - Global Warming Exists (Pro/Con/Und): ",
          gt.assortativity(g_friendship_warm_ProConUnd, g_friendship_warm_ProConUnd.vp.warm))
    print("Assortative Mixing coefficient & variance - Drug Legalization (Pro/Con/Und): ",
          gt.assortativity(g_friendship_drug_ProConUnd, g_friendship_drug_ProConUnd.vp.drug))
    print("Assortative Mixing coefficient & variance - National Health Care (Pro/Con/Und): ",
          gt.assortativity(g_friendship_health_ProConUnd, g_friendship_health_ProConUnd.vp.health))
    print("Assortative Mixing coefficient & variance - Socialism (Pro/Con/Und): ",
          gt.assortativity(g_friendship_socia_ProConUnd, g_friendship_socia_ProConUnd.vp.socia))
    #print("Assortative Mixing coefficient & variance - Political Party (): ",
    #     gt.assortativity(g_friendship_ideo_ProConUnd, g_friendship_ideo_ProConUnd.vp.party))
    print("Assortative Mixing coefficient & variance - Political Ideology (Conservative/Progressive/Liberal): ",
          gt.assortativity(g_friendship_ideo_ProConUnd, g_friendship_ideo_ProConUnd.vp.political_ideology))

### Assortative Mixing Measure with Pro-, Con-values ###

if assortProCon == True:

    g_friendship_abor_ProCon = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.abor[v] == "Pro" or
                                                                               g_friend.vp.abor[v] == "Con")
    g_friendship_gay_ProCon = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.gay[v] == "Pro" or
                                                                               g_friend.vp.gay[v] == "Con")
    g_friendship_warm_ProCon = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.warm[v] == "Pro" or
                                                                               g_friend.vp.warm[v] == "Con")
    g_friendship_drug_ProCon = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.drug[v] == "Pro" or
                                                                               g_friend.vp.drug[v] == "Con")
    g_friendship_health_ProCon = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.health[v] == "Pro" or
                                                                                 g_friend.vp.health[v] == "Con")

    g_friendship_socia_ProCon = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.socia[v] == "Pro" or
                                                                                g_friend.vp.socia[v] == "Con")

    # g_friendship_party_ProCon = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.party[v] == "" or g_friend.vp.party[v] == "")
    g_friendship_ideo_ProCon = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.political_ideology[v] == "Conservative"
                                                                      or g_friend.vp.political_ideology[v] == "Progressive")

    print("\n\nAssortative Mixing Measure with Pro-, Con-values \n ")

    print("Assortative Mixing coefficient & variance - Abortion (Pro/Con): ",
          gt.assortativity(g_friendship_abor_ProCon, g_friendship_abor_ProCon.vp.abor))
    print("Assortative Mixing coefficient & variance - Gay Marriage (Pro/Con): ",
          gt.assortativity(g_friendship_gay_ProCon, g_friendship_gay_ProCon.vp.gay))
    print("Assortative Mixing coefficient & variance - Global Warming Exists (Pro/Con): ",
          gt.assortativity(g_friendship_warm_ProCon, g_friendship_warm_ProCon.vp.warm))
    print("Assortative Mixing coefficient & variance - Drug Legalization (Pro/Con): ",
          gt.assortativity(g_friendship_drug_ProCon, g_friendship_drug_ProCon.vp.drug))
    print("Assortative Mixing coefficient & variance - National Health Care (Pro/Con): ",
          gt.assortativity(g_friendship_health_ProCon, g_friendship_health_ProCon.vp.health))
    print("Assortative Mixing coefficient & variance - Socialism (Pro/Con): ",
          gt.assortativity(g_friendship_socia_ProCon, g_friendship_socia_ProCon.vp.socia))
    # print("Assortative Mixing coefficient & variance - Political Party (): ",
    #     gt.assortativity(g_friendship_ideo_ProCon, g_friendship_ideo_ProCon.vp.party))
    print("Assortative Mixing coefficient & variance - Political Ideology (Conservative/Progressive): ",
          gt.assortativity(g_friendship_ideo_ProCon, g_friendship_ideo_ProCon.vp.political_ideology))


### Assortative Mixing Measure with score ###


if assortScore == True:


    print("Assortative Mixing coefficient & variance (skalar) - Progessiveness Score  (-5/5): ",
          gt.scalar_assortativity(g_friend, g_friend.vp.prog))
    print("Assortative Mixing coefficient & variance (categorial) - Progessiveness Score  (-5/5): ",
          gt.assortativity(g_friend, g_friend.vp.prog))

    print("Assortative Mixing coefficient & variance (skalar) - Progessiveness Score modified  (0/10): ",
          gt.scalar_assortativity(g_friend, g_friend.vp.prog_mod))
    print("Assortative Mixing coefficient & variance (categorial) - Progessiveness Score modified  (0/10): ",
          gt.assortativity(g_friend, g_friend.vp.prog_mod))



### Assortative Mixing plots ###

if assortPlot_abor == True:

    #g_friendship_abor = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.abor_int[v] == 1 or g_friend.vp.abor_int[v] == -1)
    g_friendship_abor = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.abor_int_mod[v] == 2 or g_friend.vp.abor_int_mod[v] == 1)
    g_friendship_aborPro = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.abor_int_mod[v] == 2)
    g_friendship_aborCon = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.abor_int_mod[v] == 1)

    print("Number of pro user", g_friendship_aborPro)
    print("Number of con user", g_friendship_aborCon)

    h = gt.corr_hist(g_friendship_abor, g_friendship_abor.vp.abor_int_mod, g_friendship_abor.vp.abor_int_mod)
    abor_hist = h[0][1:3, 1:3]

    '''    
    plt.clf()
    plt.xlabel("Source Abortion Value")
    plt.ylabel("Target Abortion Value")
    #plt.xticks(ticks=[1,2], label=["Con", "Pro"], rotation=45, fontsize=6)
    #plt.xlim([1, 2])
    plt.imshow(h[0].T, interpolation="nearest", origin="lower")
    plt.colorbar()
    plt.savefig("corr_abor.svg")
    '''

    print("h: \n", h)
    print("h[0].T: \n", h[0].T)
    print("h[0][1:3]: \n", h[0][1:3])
    print("h[0][1:3, 1:3]: \n", h[0][1:3, 1:3])
    print("abor_hist: \n", abor_hist)
    print("abor_hist[0]: \n", abor_hist[0])
    print("sum(abor_hist[0]): \n", sum(abor_hist[0]))
    print("abor_hist/sum(abor_hist[0]): \n", abor_hist/sum(abor_hist[0]))

    tuplelist = list(map(tuple, g_friendship_abor.get_edges()))

    c = 0
    c_newE = 0
    c_max = len(g_friendship_abor.get_edges())

    for e in g_friendship_abor.get_edges():
        c = c + 1
        source = e[0]
        target = e[1]

        if (target, source) not in tuplelist: # target and source switched to create the missing edge in the opposite direction
            c_newE = c_newE + 1
            print("target, source")

        if c % 10000 == 0:
            print(c, "/", c_max)

    print(c_max, "/", c_max)

    print(c_newE)

    ''' g_friendship_abor_ProConUnd_int = gt.GraphView(g_friendship_prop,
                                                    vfilt=lambda v: g_friendship_prop.vp.abor[v] == 1 or
                                                                    g_friendship_prop.vp.abor[v] == 0 or
                                                                    g_friendship_prop.vp.abor[v] == 2)
    '''
    '''
    h = gt.corr_hist(g_friendship_abor_ProConUnd_int, g_friendship_abor_ProConUnd_int.vp.abor_int,
                     g_friendship_abor_ProConUnd_int.vp.abor_int)
    plt.clf()
    plt.xlabel("Source Progressiveness Score")
    plt.ylabel("Target Progressiveness Score")
    plt.imshow(h[0].T, interpolation="nearest", origin="lower")
    plt.colorbar()
    plt.savefig("corr_abor_und.svg")
    
    
    
    #h = gt.corr_hist(g_all, g_all.vp.abor, g_all.vp.abor)
    h = gt.corr_hist(g_all, "out", "out")
    plt.clf()
    plt.xlabel("Source out-degree")
    plt.ylabel("Target out-degree")
    plt.imshow(h[0].T, interpolation="nearest", origin="lower")
    plt.colorbar()
    plt.savefig("corr_out.svg")
    #print(h)

    
    h = gt.corr_hist(g_friendship_skalar, g_friendship_skalar.vp.prog, g_friendship_skalar.vp.prog)
    plt.clf()
    plt.xlabel("Source Progressiveness Score")
    plt.ylabel("Target Progressiveness Score")
    plt.imshow(h[0].T, interpolation="nearest", origin="lower")
    plt.colorbar()
    plt.savefig("corr_prog.svg")
    
    h = gt.corr_hist(g_friendship_skalar_mod, g_friendship_skalar_mod.vp.prog, g_friendship_skalar_mod.vp.prog)
    plt.clf()
    plt.xlabel("Source Progressiveness Score")
    plt.ylabel("Target Progressiveness Score")
    plt.imshow(h[0].T, interpolation="nearest", origin="lower")
    plt.colorbar()
    plt.savefig("corr_prog_mod.svg")
    
    
    '''
