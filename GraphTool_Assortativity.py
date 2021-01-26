import graph_tool.all as gt
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import sys


######################
### Initialization ###
######################

np.set_printoptions(threshold=sys.maxsize)

# DO NOT USE an unpreprocessed graphml FOR ASSORTATIVITY ANALYSIS! THEY contain uni- and bilateral FRIENDS_WITH relations.
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

assortativePrePro_bool      = False
save_assortativePrePro_bool = False
load_assortativePrePro_bool = True
uniqueVal_bool              = False
assortAllValues             = False
assortProConUnd             = False
assortProCon                = False
assortProgScore             = False
assort_Visual               = True
progScore_hist              = False
progScore_Visual            = False

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
    print("Creating PropertyMaps\n")

    # These are the propertyMaps with original ['Con' 'N/O' 'N/S' 'Pro' 'Und']-values
    # Only used for plain assortativity socres.
    vprop_abor = g_friend.new_vertex_property("string")  # abortion
    vprop_gay = g_friend.new_vertex_property("string")  # gay_marriage
    vprop_warm = g_friend.new_vertex_property("string")  # global_warming
    vprop_drug = g_friend.new_vertex_property("string")  # drug_legaliz
    vprop_health = g_friend.new_vertex_property("string")  # national_health_care

    # These are the propertyMaps with numeric values [-99 ('N/O', 'N/S'),  -1 ('Con'),   0 ('Und'),   1 ('Pro')]
    # Only used for creation of the progressiveness scores prog & prog_mod
    vprop_abor_int = g_friend.new_vertex_property("int")
    vprop_gay_int = g_friend.new_vertex_property("int")
    vprop_warm_int = g_friend.new_vertex_property("int")
    vprop_drug_int = g_friend.new_vertex_property("int")
    vprop_health_int = g_friend.new_vertex_property("int")

    # These are the propertyMaps with adjusted numeric values [1 ('Con'),   2 ('Pro')] (technically also 0 for everything else. Later excluded for analysis
    # GraphTools visualization of the assortativity can only handle positive skalars
    # [0 ('Con'),   1 ('Pro')] should work as well
    vprop_abor_int_mod = g_friend.new_vertex_property("int")
    vprop_gay_int_mod = g_friend.new_vertex_property("int")
    vprop_warm_int_mod = g_friend.new_vertex_property("int")
    vprop_drug_int_mod = g_friend.new_vertex_property("int")
    vprop_health_int_mod = g_friend.new_vertex_property("int")

    #-- Progressiveness Score using Main Issues --#

    # Sum of stances regarding the big 5 above (abortion, ..., health care)
    # vprop_prog_mod = vprop_prog + 5
    # (GraphTools visualization of the assortativity can only handle positive skalars)
    vprop_prog = g_friend.new_vertex_property("int")        # int value indicating conservatism  (-5) - progressiveness (+5)
    vprop_prog_mod = g_friend.new_vertex_property("int")    # int value indicating conservatism  (0) - progressiveness (+10)


    #-- Issues used later (eventually) --#

    # Not really used but kept vor now
    vprop_socia = g_all.new_vertex_property("string")  # socialism
    vprop_socia_int = g_all.new_vertex_property("int")  # socialism

    #-- Issues not created, because they are already innate to User-nodes --#

    # Not really used but kept vor now
    # vprop_party = g_all.new_vertex_property("string")   # party
    # vprop_ideo = g_all.new_vertex_property("string")    # political_ideology

    # All these different type of propertyMaps can be reduced to one or two in future to reduce redundancy

    ### Enriching g_all with empty PropertyMaps ###

    g_friend.vp.abor = vprop_abor
    g_friend.vp.gay = vprop_gay
    g_friend.vp.warm = vprop_warm
    g_friend.vp.drug = vprop_drug
    g_friend.vp.health = vprop_health

    g_friend.vp.abor_int = vprop_abor_int
    g_friend.vp.gay_int = vprop_gay_int
    g_friend.vp.warm_int = vprop_warm_int
    g_friend.vp.drug_int = vprop_drug_int
    g_friend.vp.health_int = vprop_health_int

    g_friend.vp.abor_int_mod = vprop_abor_int_mod
    g_friend.vp.gay_int_mod = vprop_gay_int_mod
    g_friend.vp.warm_int_mod = vprop_warm_int_mod
    g_friend.vp.drug_int_mod = vprop_drug_int_mod
    g_friend.vp.health_int_mod = vprop_health_int_mod

    g_friend.vp.socia = vprop_socia
    g_friend.vp.socia_int = vprop_socia_int

    g_friend.vp.prog = vprop_prog
    g_friend.vp.prog_mod = vprop_prog_mod

    print("Creating PropertyMaps - done\n")


    ### Filling PropertyMaps ###

    print("\nFilling PropertyMaps\n")

    # User node propertyMaps in g_friend are enriched with information saved in their respective Issues node in g_all
    # The following approach works because there is only one issues node for each respective user node
    # For all user nodes, find their neighbors that are not User nodes themself, and thereby Issue nodes. Copy the Issue
    # node value or fill it with coded values (_int, _int_mod)

    c = 0
    c_max = len(g_friend.get_vertices())

    for i in g_friend.get_vertices():
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
                    g_friend.vp.gay_int_mod[i] = 2
                elif g_all.vp.gay_marriage[j] == "Und":
                    g_friend.vp.gay_int[i] = 0
                elif g_all.vp.gay_marriage[j] == "Con":
                    g_friend.vp.gay_int[i] = -1
                    g_friend.vp.gay_int_mod[i] = 1
                else:
                    g_friend.vp.gay_int[i] = -99

                if g_all.vp.global_warming[j] == "Pro":
                    g_friend.vp.warm_int[i] = 1
                    g_friend.vp.warm_int_mod[i] = 2
                elif g_all.vp.global_warming[j] == "Und":
                    g_friend.vp.warm_int[i] = 0
                elif g_all.vp.global_warming[j] == "Con":
                    g_friend.vp.warm_int[i] = -1
                    g_friend.vp.warm_int_mod[i] = 1
                else:
                    g_friend.vp.warm_int[i] = -99

                if g_all.vp.drug_legaliz[j] == "Pro":
                    g_friend.vp.drug_int[i] = 1
                    g_friend.vp.drug_int_mod[i] = 2
                elif g_all.vp.drug_legaliz[j] == "Und":
                    g_friend.vp.drug_int[i] = 0
                elif g_all.vp.drug_legaliz[j] == "Con":
                    g_friend.vp.drug_int[i] = -1
                    g_friend.vp.drug_int_mod[i] = 1
                else:
                    g_friend.vp.drug_int[i] = -99

                if g_all.vp.national_health_care[j] == "Pro":
                    g_friend.vp.health_int[i] = 1
                    g_friend.vp.health_int_mod[i] = 2
                elif g_all.vp.national_health_care[j] == "Und":
                    g_friend.vp.health_int[i] = 0
                elif g_all.vp.national_health_care[j] == "Con":
                    g_friend.vp.health_int[i] = -1
                    g_friend.vp.health_int_mod[i] = 1
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

    # In order to ensure meaning full scores, a User has to have at least one strong position on one of
    # the 5 key issues to get an progressiveness score
    g_friend_prog_ProCon = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.abor[v] == "Pro" or g_friend.vp.abor[v] == "Con" or
                                                                 g_friend.vp.gay[v] == "Pro" or g_friend.vp.gay[v] == "Con" or
                                                                 g_friend.vp.warm[v] == "Pro" or g_friend.vp.warm[v] ==  "Con" or
                                                                 g_friend.vp.drug[v] == "Pro" or g_friend.vp.drug[v] == "Con" or
                                                                 g_friend.vp.health[v] == "Pro" or g_friend.vp.health[v] == "Con")

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
        g_friend.vp.prog_mod[i] = prog_score + 5                # GraphTool visualization only handles positie skalars

        if c % 1000 == 0:
            print("Filling PropertyMaps - prog_score: ", c, "/", c_max)

        c = c + 1
    print("Filling PropertyMaps - prog_score: ", c_max, "/", c_max)
    print("Filling PropertyMaps - done\n")


### Saving Assortativity-Preprocessed Graph ###

if save_assortativePrePro_bool == True:
    print("\nSaving Assortativity-Preprocessed Graph\n")
    g_friend.save("Graph_Preprocessed_Approach1+AssoPrePro.graphml")
    print("Saving Assortativity-Preprocessed Graph - done\n")


### Loading Assortativity-Preprocessed Graph ###

if load_assortativePrePro_bool == True:
    print("\nLoading Assortativity-Preprocessed Graph\n")
    g_friend = gt.load_graph('Graph_Preprocessed_Approach1+AssoPrePro.graphml', fmt='graphml')
    print("Loading Assortativity-Preprocessed Graph - done\n")

### Identifying Unique Values of PropertyMaps ###

if uniqueVal_bool == True:
    print("\nIdentifying Unique Values of PropertyMaps\n")

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

    vals_abor_int_mod = np.array([])
    vals_gay_int_mod = np.array([])
    vals_warm_int_mod = np.array([])
    vals_drug_int_mod = np.array([])
    vals_health_int_mod = np.array([])

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

        vals_abor_int_mod = np.append(vals_abor_int_mod, g_friend.vp.abor_int_mod[v])
        vals_gay_int_mod = np.append(vals_gay_int_mod, g_friend.vp.gay_int_mod[v])
        vals_warm_int_mod = np.append(vals_warm_int_mod, g_friend.vp.warm_int_mod[v])
        vals_drug_int_mod = np.append(vals_drug_int_mod, g_friend.vp.drug_int_mod[v])
        vals_health_int_mod = np.append(vals_health_int_mod, g_friend.vp.health_int_mod[v])

        vals_socia = np.append(vals_socia, g_friend.vp.socia[v])
        vals_socia_int = np.append(vals_socia_int, g_friend.vp.socia_int[v])

        vals_party = np.append(vals_party, g_all.vp.party[v])
        vals_ideo = np.append(vals_ideo, g_friend.vp.political_ideology[v])

        vals_progScore = np.append(vals_progScore, g_friend.vp.prog[v])
        vals_progScore_mod = np.append(vals_progScore_mod, g_friend.vp.prog_mod[v])

        if c % 1000 == 0:
            print("Identifying values range of PropertyMaps", c, "/", c_max)
        c = c + 1
    print("Identifying values range of PropertyMaps", c_max, "/", c_max)

    print("range of vals_abor: ", np.unique(vals_abor))                             # ['Con' 'N/O' 'N/S' 'Pro' 'Und']
    print("range of vals_gay: ", np.unique(vals_gay))                               #  same ...
    print("range of vals_warm: ", np.unique(vals_warm))
    print("range of vals_drug: ", np.unique(vals_drug))
    print("range of vals_health: ", np.unique(vals_health))
    print("range of vals_socia: ", np.unique(vals_socia))

    print("range of vals_abor_int: ", np.unique(vals_abor_int))                     # [-99.  -1.   0.   1.]
    print("range of vals_gay_int: ", np.unique(vals_gay_int))                       #  same ...
    print("range of vals_warm_int: ", np.unique(vals_warm_int))
    print("range of vals_drug_int: ", np.unique(vals_drug_int))
    print("range of vals_health_int: ", np.unique(vals_health_int))
    print("range of vals_socia_int: ", np.unique(vals_socia_int))

    print("range of vals_abor_int_mod: ", np.unique(vals_abor_int_mod))             # [0. 1. 2.]
    print("range of vals_gay_int_mod: ", np.unique(vals_gay_int_mod))               #  same ...
    print("range of vals_warm_int_mod: ", np.unique(vals_warm_int_mod))
    print("range of vals_drug_int_mod: ", np.unique(vals_drug_int_mod))
    print("range of vals_health_int_mod: ", np.unique(vals_health_int_mod))

    print("range of vals_party: ", np.unique(vals_party))                           # too many
    print("range of vals_ideo: ", np.unique(vals_ideo))                             # ['Anarchist' 'Apathetic' 'Communist' 'Conservative' 'Green' 'Labor'
                                                                                    # 'Liberal' 'Libertarian' 'Moderate' 'Not Saying' 'Other' 'Progressive'
                                                                                    # 'Socialist' 'Undecided']
    print("range of vals_progScore: ", np.unique(vals_progScore))                   # [-5. -4. -3. -2. -1.  0.  1.  2.  3.  4.  5.]
    print("range of vals_progScore_mod: ", np.unique(vals_progScore_mod))           #
    print("length of progScore: ", len(vals_progScore))                             # 45348

    print("\nIdentifying Unique Values of PropertyMaps - done\n")

### Assortative Mixing Measure with all values ###

if assortAllValues == True:
    print("\nAssortative Mixing Measure with all values \n ")

    print("Assortative Mixing coefficient & variance - Abortion (All): ", gt.assortativity(g_friend, g_friend.vp.abor))                         # (0.061846867674553066, 0.001464899208148559)
    print("Assortative Mixing coefficient & variance - Gay Marriage (All): ", gt.assortativity(g_friend, g_friend.vp.gay))                      # (0.06246704352686685,  0.0015132098680730064)
    print("Assortative Mixing coefficient & variance - Global Warming Exists (All): ", gt.assortativity(g_friend, g_friend.vp.warm))            # (0.048342380606636745, 0.0014676785291116404)
    print("Assortative Mixing coefficient & variance - Drug Legalization (All): ", gt.assortativity(g_friend, g_friend.vp.drug))                # (0.03809495337105788,  0.0014262205176255286)
    print("Assortative Mixing coefficient & variance - National Health Care (All): ", gt.assortativity(g_friend, g_friend.vp.health))           # (0.047837000682192106, 0.00143117395965968)
    print("Assortative Mixing coefficient & variance - Socialism (All): ", gt.assortativity(g_friend, g_friend.vp.socia))                       # (0.07804511040744438,  0.0014569231664940563)
    # print("Assortative Mixing coefficient & variance - Political Party (All): ", gt.assortativity(g_friend, g_friend.vp.party))               # too many values
    print("Assortative Mixing coefficient & variance - Political Ideology (All): ", gt.assortativity(g_friend, g_friend.vp.political_ideology)) # (0.03452145283371659,  0.0009357000699059733)

    print("Assortative Mixing Measure with all values -done\n ")


### Assortative Mixing Measure with Pro-, Con- Undecided-values ###

if assortProConUnd == True:
    print("\nAssortative Mixing Measure with Pro-, Con- Undecided-values \n ")

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


    print("Assortative Mixing coefficient & variance - Abortion (Pro/Con/Und): ",
          gt.assortativity(g_friendship_abor_ProConUnd, g_friendship_abor_ProConUnd.vp.abor))                       # (0.09625261506808915, 0.0027700516901654018)
    print("Assortative Mixing coefficient & variance - Gay Marriage (Pro/Con/Und): ",
          gt.assortativity(g_friendship_gay_ProConUnd, g_friendship_gay_ProConUnd.vp.gay))                          # (0.1122712125196475,  0.0031318690069598956)
    print("Assortative Mixing coefficient & variance - Global Warming Exists (Pro/Con/Und): ",
          gt.assortativity(g_friendship_warm_ProConUnd, g_friendship_warm_ProConUnd.vp.warm))                       # (0.0685673224407381,  0.002971210396617389)
    print("Assortative Mixing coefficient & variance - Drug Legalization (Pro/Con/Und): ",
          gt.assortativity(g_friendship_drug_ProConUnd, g_friendship_drug_ProConUnd.vp.drug))                       # (0.04011152144315785, 0.002678409360280249)
    print("Assortative Mixing coefficient & variance - National Health Care (Pro/Con/Und): ",
          gt.assortativity(g_friendship_health_ProConUnd, g_friendship_health_ProConUnd.vp.health))                 # (0.07609283739357957, 0.003188937109138192)
    print("Assortative Mixing coefficient & variance - Socialism (Pro/Con/Und): ",
          gt.assortativity(g_friendship_socia_ProConUnd, g_friendship_socia_ProConUnd.vp.socia))                    # (0.0698114035393093,  0.003652874749801286)
    #print("Assortative Mixing coefficient & variance - Political Party (): ",
    #     gt.assortativity(g_friendship_ideo_ProConUnd, g_friendship_ideo_ProConUnd.vp.party))
    print("Assortative Mixing coefficient & variance - Political Ideology (Conservative/Progressive/Liberal): ",
          gt.assortativity(g_friendship_ideo_ProConUnd, g_friendship_ideo_ProConUnd.vp.political_ideology))         # (0.11264537783898422, 0.006033204640854704)

    print("\nAssortative Mixing Measure with Pro-, Con- Undecided-values - done\n ")

### Assortative Mixing Measure with Pro-, Con-values ###

if assortProCon == True:
    print("\nAssortative Mixing Measure with Pro-, Con-values\n ")

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


    print("Assortative Mixing coefficient & variance - Abortion (Pro/Con): ",
          gt.assortativity(g_friendship_abor_ProCon, g_friendship_abor_ProCon.vp.abor))                     # (0.12011913045326039, 0.003422742356890999)
    print("Assortative Mixing coefficient & variance - Gay Marriage (Pro/Con): ",
          gt.assortativity(g_friendship_gay_ProCon, g_friendship_gay_ProCon.vp.gay))                        # (0.13033958488615244, 0.0036290093108955774)
    print("Assortative Mixing coefficient & variance - Global Warming Exists (Pro/Con): ",
          gt.assortativity(g_friendship_warm_ProCon, g_friendship_warm_ProCon.vp.warm))                     # (0.09081850115390559, 0.004121836202129812)
    print("Assortative Mixing coefficient & variance - Drug Legalization (Pro/Con): ",
          gt.assortativity(g_friendship_drug_ProCon, g_friendship_drug_ProCon.vp.drug))                     # (0.05697916407569793, 0.0036383643016529754)
    print("Assortative Mixing coefficient & variance - National Health Care (Pro/Con): ",
          gt.assortativity(g_friendship_health_ProCon, g_friendship_health_ProCon.vp.health))               # (0.10011300389123652, 0.00410472672307498)
    print("Assortative Mixing coefficient & variance - Socialism (Pro/Con): ",
          gt.assortativity(g_friendship_socia_ProCon, g_friendship_socia_ProCon.vp.socia))                  # (0.10237919081490211, 0.005327132988348007)
    # print("Assortative Mixing coefficient & variance - Political Party (): ",
    #     gt.assortativity(g_friendship_ideo_ProCon, g_friendship_ideo_ProCon.vp.party))
    print("Assortative Mixing coefficient & variance - Political Ideology (Conservative/Progressive): ",
          gt.assortativity(g_friendship_ideo_ProCon, g_friendship_ideo_ProCon.vp.political_ideology))       # (0.14303240713892656, 0.012044364508357112)

    print("\nAssortative Mixing Measure with Pro-, Con-values - done\n ")

### Assortative Mixing Measure with Progressiveness Score ###


if assortProgScore == True:
    print("\nAssortative Mixing Measure with Progressiveness Score \n ")

    # GraphTool can't handle negative skalars
    #print("Assortative Mixing coefficient & variance (skalar) - Progessiveness Score  (-5/5): ",
          #gt.scalar_assortativity(g_friend, g_friend.vp.prog))
    #print("Assortative Mixing coefficient & variance (categorial) - Progessiveness Score  (-5/5): ",
          #gt.assortativity(g_friend, g_friend.vp.prog))

    print("Assortative Mixing coefficient & variance (skalar) - Progessiveness Score modified  (0/10): ",
          gt.scalar_assortativity(g_friend, g_friend.vp.prog_mod))                                                  # (0.08902024125553645, 0.0023132698355785675)
    #print("Assortative Mixing coefficient & variance (categorial) - Progessiveness Score modified  (0/10): ",
          #gt.assortativity(g_friend, g_friend.vp.prog_mod))

    print("\nAssortative Mixing Measure with Progressiveness Score - done\n ")


### Assortative Mixing Visualization ###

if assort_Visual == True:
    print("\nAssortative Mixing Visualization\n")

    # The nature of debate.org friendship edges is bidrectional. Iff A is befriended with B, then B is also befriended with A. When visualizing
    # Assortativive Mixing these relations can be represented unidirectionally or bidirectionally. In the following visualization the unidirectional
    # approach is choosen. This is due to the used GraphTool convention of displaying a bidrectional edge as 2 reziproc unidirectional edges.
    # A blueprint for a bidirectional approach is represented as well (commented out with ""). Notice, the interpretation of the visualization then changes.


    #-- Assortativity Abortion --#
    print("Abortion Visualization\n")

    g_friendship_abor = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.abor_int_mod[v] == 2 or g_friend.vp.abor_int_mod[v] == 1)
    g_friendship_aborPro = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.abor_int_mod[v] == 2)
    g_friendship_aborCon = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.abor_int_mod[v] == 1)

    #print("Number of Users nodes and Friendship edges: ", g_friendship_abor)    # 13675 vertices, 84130 edges
    #print("Number of pro user", g_friendship_aborPro)                           #  6877 vertices, 23464 edges
    #print("Number of con user", g_friendship_aborCon)                           #  6798 vertices, 23654 edges

    h = gt.corr_hist(g_friendship_abor, g_friendship_abor.vp.abor_int_mod, g_friendship_abor.vp.abor_int_mod)
    h_abor = h[0][1:3, 1:3]
    h_abor_rel = h_abor / sum(sum(h_abor))

    #print("h_abor: ", h_abor)                           # [[23654. 18506.]
                                                         #  [18506. 23464.]]
    #print("sum of h_abor: ", sum(sum(h_abor)))          #   84130.0
    #print("h_abor_rel (in percent): ", h_abor_rel)      # [[0.28116011 0.2199691 ]
                                                         #  [0.2199691  0.2789017 ]]
    #print(aborH_unidirec_rel = aborH_unidirec_rel.T)    # True

    # 18506*2 unidrectional friendship relations are between nodes of different abortion values
    # 23654   unidrectional are between nodes of abortion value "Con"
    # 23464   unidrectional are between nodes of abortion value "Pro"

    print("Normailization by #Edges/#Nodes:")
    print("Normalization of Edges Con - Con: ", h_abor[0][0]), "/" , len(g_friendship_aborCon.get_vertices())
    print("Normalization of Edges Con - Con: ", h_abor[0][0]    /    len(g_friendship_aborCon.get_vertices()))
    print("Normalization of Edges Pro - Pro: ", h_abor[1][1]), "/" , len(g_friendship_aborPro.get_vertices())
    print("Normalization of Edges Pro - Pro: ", h_abor[1][1]    /    len(g_friendship_aborPro.get_vertices()))

    plt.clf()
    plt.title("Unidirectional Edges between Users \n Absolute and Relative (84130 total)")
    plt.xlabel("Source Abortion Value")
    plt.ylabel("Target Abortion Value")
    plt.xticks(ticks=[0,1], labels=('Con', 'Pro'))
    plt.yticks(ticks=[0,1], labels=('Con', 'Pro'))
    plt.text(-0.30, 0, "0.281% (23654)")
    plt.text(-0.30, 1, "0.22% (18506)")
    plt.text(0.70, 0, "0.22% (18506)")
    plt.text(0.70, 1, "0.279% (23464)")
    plt.imshow(h_abor_rel, interpolation="nearest", origin="lower", vmin=0, vmax=1)
    plt.colorbar()
    plt.savefig("corr_abor.svg")


    #-- Assortativity Abortion (bidirectional) --#

    """
    print("\n\n#-- Assortativity Abortion (bidirectional) --#\n")
    
    aborH_bidirec = h_abor
    aborH_bidirec[0][0] = aborH_bidirec[0][0]/2
    aborH_bidirec[1][1] = aborH_bidirec[1][1]/2
    aborH_bidirec_rel = aborH_bidirec / (aborH_bidirec[0][0] + aborH_bidirec[0][1] + aborH_bidirec[1][1])
    print("abor_hist_unidirec: ", aborH_bidirec)                        # [[11827. 18506.]
                                                                        #  [18506. 11732.]]
    print("sum of bidirectional relations (half of the unidrec above): ",
          (aborH_bidirec[0][0] + aborH_bidirec[0][1] + aborH_bidirec[1][1]))
                                                                        #   42065.0
    print("aborH_bidirec_rel (in percent): ", aborH_bidirec_rel)        # [[0.28116011 0.43993819]
                                                                        #  [0.43993819 0.2789017 ]]

    # 18506   bidrectional friendship relations are between nodes of different abortion values
    # 23654/2 bidrectional are between nodes of abortion value "Con"
    # 23464/2 bidrectional are between nodes of abortion value "Pro"

    plt.clf()
    plt.xlabel("Source Abortion Value")
    plt.ylabel("Target Abortion Value")
    plt.xticks(ticks=[0,1], labels=('Con', 'Pro'))
    plt.yticks(ticks=[0,1], labels=('Con', 'Pro'))
    plt.text(-0.30, 0, "0.281% (11827)")
    plt.text(-0.30, 1, "0.44% (18506)")
    plt.text(0.70, 0, "0.44% (18506)")
    plt.text(0.70, 1, "0.279% (11732)")
    plt.imshow(aborH_bidirec_rel, interpolation="nearest", origin="lower", vmin=0, vmax=1)
    plt.colorbar()
    plt.savefig("corr_abor_bidirec.svg")
    """

    # -- Assortativity Gay Marriage --#
    print("Gay Marriage Visualization\n")

    g_friendship_gay = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.gay_int_mod[v] == 2 or g_friend.vp.gay_int_mod[v] == 1)
    g_friendship_gayPro = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.gay_int_mod[v] == 2)
    g_friendship_gayCon = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.gay_int_mod[v] == 1)

    #print("Number of Users nodes and Friendship edges: ", g_friendship_gay)   # 12374 vertices and 81542 edges
    #print("Number of pro user", g_friendship_gayPro)                          #  8756 vertices and 43298 edges
    #print("Number of con user", g_friendship_gayCon)                          #  3618 vertices and  9044 edges

    h = gt.corr_hist(g_friendship_gay, g_friendship_gay.vp.gay_int_mod, g_friendship_gay.vp.gay_int_mod)
    h_gay = h[0][1:3, 1:3]
    h_gay_rel = h_gay / sum(sum(h_gay))

    #print("gayH_unidirec: ", h_gay)                             # [[ 9044. 14600.]
                                                                 #  [14600. 43298.]]
    #print("sum of gayH_unidirec: ", sum(sum(h_gay)))            #   81542.0
    #print("gayH_unidirec_rel (in percent): ", h_gay_rel)        # [[0.11091217 0.17904883]
                                                                 #  [0.17904883 0.53099016]]

    # 14600*2 unidrectional friendship relations are between nodes of different gay marriage values
    #  9044   unidrectional are between nodes of gay marriage value "Con"
    # 43298   unidrectional are between nodes of gay marriage value "Pro"

    print("Normailization by #Edges/#Nodes:")
    print("Normalization of Edges Con - Con: ", h_gay[0][0], "/" , len(g_friendship_gayCon.get_vertices()))
    print("Normalization of Edges Con - Con: ", h_gay[0][0] / len(g_friendship_gayCon.get_vertices()))
    print("Normalization of Edges Pro - Pro: ", h_gay[1][1], "/" , len(g_friendship_gayPro.get_vertices()))
    print("Normalization of Edges Pro - Pro: ", h_gay[1][1] / len(g_friendship_gayPro.get_vertices()))


    plt.clf()
    plt.title("Unidirectional Edges between Users \n Absolute and Relative (81542 total)")
    plt.xlabel("Source Gay Marriage Value")
    plt.ylabel("Target Gay Marriage Value")
    plt.xticks(ticks=[0,1], labels=('Con', 'Pro'))
    plt.yticks(ticks=[0,1], labels=('Con', 'Pro'))
    plt.text(-0.30, 0, "0.111% (9044)")
    plt.text(-0.30, 1, "0.179% (14600)")
    plt.text(0.70, 0, "0.179% (14600)")
    plt.text(0.70, 1, "0.531% (43298)")
    plt.imshow(h_gay_rel, interpolation="nearest", origin="lower", vmin=0, vmax=1)
    plt.colorbar()
    plt.savefig("corr_gay.svg")



    # -- Assortativity Global Warming (is real) --#

    print("Global Warming (is real) Visualization\n")

    g_friendship_warm = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.warm_int_mod[v] == 2 or g_friend.vp.warm_int_mod[v] == 1)
    g_friendship_warmPro = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.warm_int_mod[v] == 2)
    g_friendship_warmCon = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.warm_int_mod[v] == 1)

    #print("Number of Users nodes and Friendship edges: ", g_friendship_warm)   # 10729 vertices and 65486 edges
    #print("Number of pro user", g_friendship_warmPro)                          #  7925 vertices and 39210 edges
    #print("Number of con user", g_friendship_warmCon)                          #  2804 vertices and 4750 edges

    h = gt.corr_hist(g_friendship_warm, g_friendship_warm.vp.warm_int_mod, g_friendship_warm.vp.warm_int_mod)
    h_warm = h[0][1:3, 1:3]
    h_warm_rel = h_warm / sum(sum(h_warm))

    #print("h_warm: ", h_warm)                              # [[ 4750. 10763.]
                                                            #  [10763. 39210.]]
    #print("sum of h_warm: ", sum(sum(h_warm)))             #   65486.0
    #print("warmH_unidirec_rel (in percent): ", h_warm_rel) # [[0.07253459 0.16435574]
                                                            #  [0.16435574 0.59875393]]

    # 10763*2 unidrectional friendship relations are between nodes of different abortion values
    # 4750   unidrectional are between nodes of abortion value "Con"
    # 39210   unidrectional are between nodes of abortion value "Pro"

    print("Normailization by #Edges/#Nodes:")
    print("Normalization of Edges Con - Con: ", h_warm[0][0], "/", len(g_friendship_warmCon.get_vertices()))
    print("Normalization of Edges Con - Con: ", h_warm[0][0] / len(g_friendship_warmCon.get_vertices()))
    print("Normalization of Edges Pro - Pro: ", h_warm[1][1], "/", len(g_friendship_warmPro.get_vertices()))
    print("Normalization of Edges Pro - Pro: ", h_warm[1][1] / len(g_friendship_warmPro.get_vertices()))


    plt.clf()
    plt.title("Unidirectional Edges between Users \n Absolute and Relative (65486 total)")
    plt.xlabel("Source Global Warming (is real) Value")
    plt.ylabel("Target Global Warming (is real) Value")
    plt.xticks(ticks=[0,1], labels=('Con', 'Pro'))
    plt.yticks(ticks=[0,1], labels=('Con', 'Pro'))
    plt.text(-0.30, 0, "0.073% (4750)")
    plt.text(-0.30, 1, "0.164% (10763)")
    plt.text(0.70, 0, "0.164% (10763)")
    plt.text(0.70, 1, "0.588% (39210)")
    plt.imshow(h_warm_rel, interpolation="nearest", origin="lower", vmin=0, vmax=1)
    plt.colorbar()
    plt.savefig("corr_warm.svg")


    # -- Assortativity Drug Legalization --#

    print("Drug Legalization Visualization\n")

    g_friendship_drug = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.drug_int_mod[v] == 2 or g_friend.vp.drug_int_mod[v] == 1)
    g_friendship_drugPro = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.drug_int_mod[v] == 2)
    g_friendship_drugCon = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.drug_int_mod[v] == 1)

    #print("Number of Users nodes and Friendship edges: ", g_friendship_drug)   # 12009 vertices and 76244 edges
    #print("Number of pro user", g_friendship_drugPro)                          #  6207 vertices and 30226 edges
    #print("Number of con user", g_friendship_drugCon)                          #  5802 vertices and 12100 edges

    h = gt.corr_hist(g_friendship_drug, g_friendship_drug.vp.drug_int_mod, g_friendship_drug.vp.drug_int_mod)
    h_drug = h[0][1:3, 1:3]
    h_drug_rel = h_drug / sum(sum(h_drug))

    #print("h_drug: ", h_drug)                           # [[12100. 16959.]
                                                         #  [16959. 30226.]]
    #print("sum of h_drug: ", sum(sum(h_drug)))          #   76244.0
    #print("h_drug_rel (in percent): ", h_drug_rel)      # [[0.15870101 0.22243062]
                                                         #  [0.22243062 0.39643775]]

    # 16959*2 unidrectional friendship relations are between nodes of different abortion values
    # 12100   unidrectional are between nodes of abortion value "Con"
    # 30226   unidrectional are between nodes of abortion value "Pro"

    print("Normailization by #Edges/#Nodes:")
    print("Normalization of Edges Con - Con: ", h_drug[0][0], "/", len(g_friendship_drugCon.get_vertices()))
    print("Normalization of Edges Con - Con: ", h_drug[0][0] / len(g_friendship_drugCon.get_vertices()))
    print("Normalization of Edges Pro - Pro: ", h_drug[1][1], "/", len(g_friendship_drugPro.get_vertices()))
    print("Normalization of Edges Pro - Pro: ", h_drug[1][1] / len(g_friendship_drugPro.get_vertices()))


    plt.clf()
    plt.title("Unidirectional Edges between Users \n Absolute and Relative (76244 total)")
    plt.xlabel("Source Drug Legalization Value")
    plt.ylabel("Target Drug Legalization Value")
    plt.xticks(ticks=[0,1], labels=('Con', 'Pro'))
    plt.yticks(ticks=[0,1], labels=('Con', 'Pro'))
    plt.text(-0.30, 0, "0.159% (12100)")
    plt.text(-0.30, 1, "0.222% (16959)")
    plt.text(0.70, 0, "0.222% (16959)")
    plt.text(0.70, 1, "0.396% (30226)")
    plt.imshow(h_drug_rel, interpolation="nearest", origin="lower", vmin=0, vmax=1)
    plt.colorbar()
    plt.savefig("corr_drug.svg")


    # -- Assortativity National Health Care --#

    print("National Health Care Visualization\n")

    g_friendship_health = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.health_int_mod[v] == 2 or g_friend.vp.health_int_mod[v] == 1)
    g_friendship_healthPro = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.health_int_mod[v] == 2)
    g_friendship_healthCon = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.health_int_mod[v] == 1)

    #print("Number of Users nodes and Friendship edges: ", g_friendship_health)    # 9079 vertices and 59208 edges
    #print("Number of pro user", g_friendship_healthPro)                          #  5873 vertices and 20926 edges
    #print("Number of con user", g_friendship_healthCon)                          #  3206 vertices and 12218 edges

    h = gt.corr_hist(g_friendship_health, g_friendship_health.vp.health_int_mod, g_friendship_health.vp.health_int_mod)
    h_health = h[0][1:3, 1:3]
    h_health_rel = h_health / sum(sum(h_health))

    #print("h_health: ", h_health)                           # [[12218. 13032.]
                                                             #  [13032. 20926.]]
    #print("sum of h_health: ", sum(sum(h_health)))          #   59208.0
    #print("h_health_rel (in percent): ", h_health_rel)      # [[0.20635725 0.22010539]
                                                             #  [0.22010539 0.35343197]]

    # 18506*2 unidrectional friendship relations are between nodes of different abortion values
    # 23654   unidrectional are between nodes of abortion value "Con"
    # 23464   unidrectional are between nodes of abortion value "Pro"

    print("Normailization by #Edges/#Nodes:")
    print("Normalization of Edges Con - Con: ", h_health[0][0], "/", len(g_friendship_healthCon.get_vertices()))
    print("Normalization of Edges Con - Con: ", h_health[0][0] / len(g_friendship_healthCon.get_vertices()))
    print("Normalization of Edges Pro - Pro: ", h_health[1][1], "/", len(g_friendship_healthPro.get_vertices()))
    print("Normalization of Edges Pro - Pro: ", h_health[1][1] / len(g_friendship_healthPro.get_vertices()))


    plt.clf()
    plt.title("Unidirectional Edges between Users \n Absolute and Relative (59208 total)")
    plt.xlabel("Source National Health Care Value")
    plt.ylabel("Target National Health Care Value")
    plt.xticks(ticks=[0,1], labels=('Con', 'Pro'))
    plt.yticks(ticks=[0,1], labels=('Con', 'Pro'))
    plt.text(-0.30, 0, "0.206% (12218)")
    plt.text(-0.30, 1, "0.22% (13032)")
    plt.text(0.70, 0, "0.22% (13032)")
    plt.text(0.70, 1, "0.353% (20926)")
    plt.imshow(h_health_rel, interpolation="nearest", origin="lower", vmin=0, vmax=1)
    plt.colorbar()
    plt.savefig("corr_health.svg")

    print("Assortative Mixing Visualization - done\n")



### Progressiveness Score - Histogram ###

if progScore_hist == True:

    print("\nProgressiveness Score - Histogram\n")

    g_friend_prog_ProCon = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.abor[v] == "Pro" or g_friend.vp.abor[v] == "Con" or
                                                                 g_friend.vp.gay[v] == "Pro" or g_friend.vp.gay[v] == "Con" or
                                                                 g_friend.vp.warm[v] == "Pro" or g_friend.vp.warm[v] ==  "Con" or
                                                                 g_friend.vp.drug[v] == "Pro" or g_friend.vp.drug[v] == "Con" or
                                                                 g_friend.vp.health[v] == "Pro" or g_friend.vp.health[v] == "Con")

    #print(g_friend_prog_ProCon)                                            # 16992 vertices and 118534 edges

    valid_progScore_id = []
    for v in g_friend.get_vertices():
        if g_friend.vp.abor[v] == "Pro" or g_friend.vp.abor[v] == "Con" or g_friend.vp.gay[v] == "Pro" or g_friend.vp.gay[v] == "Con" or g_friend.vp.warm[v] == "Pro" or g_friend.vp.warm[v] ==  "Con" or g_friend.vp.drug[v] == "Pro" or g_friend.vp.drug[v] == "Con" or g_friend.vp.health[v] == "Pro" or g_friend.vp.health[v] == "Con":
            valid_progScore_id.append(v)

    #print("valid_progScore_id: ", len(valid_progScore_id))                 # 16992

    valid_progScore_val = g_friend_prog_ProCon.vp.prog_mod.a[valid_progScore_id]

    #print("len(valid_progScore_val): ", len(valid_progScore_val))          # 16992

    print("Progressiveness Score maximum of nodes with valid value: ", max(valid_progScore_val))                                # 10
    print("Progressiveness Score minimum of nodes with valid value: ", min(valid_progScore_val))                                #  0
    print("Progressiveness Score average of nodes with valid value: ", sum(valid_progScore_val) / len(valid_progScore_val))     #

    #hist = np.histogram(valid_progScore_val)           # does some weird shit (adding the frequencies of the two highest values together and thereby
                                                        # returning one frequency bucket too few

    #Alternative:
    x = np.unique(valid_progScore_val)
    y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in valid_progScore_val:
        y[i] = y[i] +1

    fig, ax = plt.subplots()
    plt.bar(x, y, color='grey')
    plt.title('Histogram progressiveness Scores')
    plt.xlabel('Progressiveness Scores')
    plt.xticks(np.linspace(0, 10, 11))
    plt.ylabel('Frequency (16992 total)')
    plt.savefig("progScore_hist_ap1.png")
    plt.close()

    print("\nProgressiveness Score - Histogram - done\n")

### Assortative Mixing Visualization - Progressiveness Score ###

if progScore_Visual == True:


    g_friend_prog_ProCon = gt.GraphView(g_friend, vfilt=lambda v: g_friend.vp.abor[v] == "Pro" or g_friend.vp.abor[v] == "Con" or
                                                                  g_friend.vp.gay[v] == "Pro" or g_friend.vp.gay[v] == "Con" or
                                                                  g_friend.vp.warm[v] == "Pro" or g_friend.vp.warm[v] == "Con" or
                                                                  g_friend.vp.drug[v] == "Pro" or g_friend.vp.drug[v] == "Con" or
                                                                  g_friend.vp.health[v] == "Pro" or g_friend.vp.health[v] == "Con")


    g_friendship_prog_mod_0 = gt.GraphView(g_friend_prog_ProCon, vfilt=lambda v: g_friend.vp.prog_mod[v] == 0)
    g_friendship_prog_mod_1 = gt.GraphView(g_friend_prog_ProCon, vfilt=lambda v: g_friend.vp.prog_mod[v] == 1)
    g_friendship_prog_mod_2 = gt.GraphView(g_friend_prog_ProCon, vfilt=lambda v: g_friend.vp.prog_mod[v] == 2)
    g_friendship_prog_mod_3 = gt.GraphView(g_friend_prog_ProCon, vfilt=lambda v: g_friend.vp.prog_mod[v] == 3)
    g_friendship_prog_mod_4 = gt.GraphView(g_friend_prog_ProCon, vfilt=lambda v: g_friend.vp.prog_mod[v] == 4)
    g_friendship_prog_mod_5 = gt.GraphView(g_friend_prog_ProCon, vfilt=lambda v: g_friend.vp.prog_mod[v] == 5)
    g_friendship_prog_mod_6 = gt.GraphView(g_friend_prog_ProCon, vfilt=lambda v: g_friend.vp.prog_mod[v] == 6)
    g_friendship_prog_mod_7 = gt.GraphView(g_friend_prog_ProCon, vfilt=lambda v: g_friend.vp.prog_mod[v] == 7)
    g_friendship_prog_mod_8 = gt.GraphView(g_friend_prog_ProCon, vfilt=lambda v: g_friend.vp.prog_mod[v] == 8)
    g_friendship_prog_mod_9 = gt.GraphView(g_friend_prog_ProCon, vfilt=lambda v: g_friend.vp.prog_mod[v] == 9)
    g_friendship_prog_mod_10 = gt.GraphView(g_friend_prog_ProCon, vfilt=lambda v: g_friend.vp.prog_mod[v] == 10)

    '''
    print("g_friend_prog_ProCon - all: ", g_friend_prog_ProCon)         # 16992 vertices and 118534 edges
    print("g_friendship_prog_mod - 0: ", g_friendship_prog_mod_0)       #   544 vertices and    262 edges
    print("g_friendship_prog_mod - 1: ", g_friendship_prog_mod_1)       #   496 vertices and    278 edges
    print("g_friendship_prog_mod - 2: ", g_friendship_prog_mod_2)       #  1017 vertices and    874 edges
    print("g_friendship_prog_mod - 3: ", g_friendship_prog_mod_3)       #  1443 vertices and    708 edges
    print("g_friendship_prog_mod - 4: ", g_friendship_prog_mod_4)       #  2335 vertices and   1966 edges h
    print("g_friendship_prog_mod - 5: ", g_friendship_prog_mod_5)       #  1546 vertices and    450 edges
    print("g_friendship_prog_mod - 6: ", g_friendship_prog_mod_6)       #  2679 vertices and   2064 edges h
    print("g_friendship_prog_mod - 7: ", g_friendship_prog_mod_7)       #  1852 vertices and   1136 edges
    print("g_friendship_prog_mod - 8: ", g_friendship_prog_mod_8)       #  2035 vertices and   2282 edges h
    print("g_friendship_prog_mod - 9: ", g_friendship_prog_mod_9)       #  1327 vertices and   1112 edges
    print("g_friendship_prog_mod - 10: ", g_friendship_prog_mod_10)     #  1718 vertices and   3248 edges h
    '''

    h = gt.corr_hist(g_friend_prog_ProCon, g_friend.vp.prog_mod, g_friend.vp.prog_mod)

    #print("h[0]: ", h[0])  #[[ 262.,  245.,  445.,  375.,  537.,  255.,  438.,  302.,  401.,  272.,  445.],
                            # [ 245.,  278.,  465.,  408.,  612.,  287.,  484.,  332.,  438.,  301.,  474.],
                            # [ 445.,  465.,  874.,  771., 1309.,  579., 1119.,  747., 1054.,  641., 1093.],
                            # [ 375.,  408.,  771.,  708., 1232.,  545.,  992.,  707.,  995.,  619.,  935.],
                            # [ 537.,  612., 1309., 1232., 1966., 1026., 1911., 1322., 1844., 1189., 1948.],
                            # [ 255.,  287.,  579.,  545., 1026.,  450.,  951.,  737.,  946.,  617., 1032.],
                            # [ 438.,  484., 1119.,  992., 1911.,  951., 2064., 1474., 2028., 1384., 2325.],
                            # [ 302.,  332.,  747.,  707., 1322.,  737., 1474., 1136., 1560., 1089., 1703.],
                            # [ 401.,  438., 1054.,  995., 1844.,  946., 2028., 1560., 2282., 1531., 2688.],
                            # [ 272.,  301.,  641.,  619., 1189.,  617., 1384., 1089., 1531., 1112., 1918.],
                            # [ 445.,  474., 1093.,  935., 1948., 1032., 2325., 1703., 2688., 1918., 3248.]]

    #print(h[0] == h[0].T)  # True



    print("sum(sum(h[0])):", sum(sum(h[0])))

    #print(h[0])

    h_rel = h[0] / sum(sum(h[0]))

    plt.clf()
    plt.xlabel("Source Progressiveness Score (118534 edges total)")
    plt.ylabel("Target Progressiveness Score")
    plt.xticks(ticks=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    plt.yticks(ticks=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    plt.imshow(h_rel, interpolation="nearest", origin="lower", vmin=0, vmax=0.03)
    plt.colorbar()
    plt.savefig("corr_prog_unidirec.svg")


    x = np.unique(valid_progScore_val)

    y = [h[0][0][0] / len(g_friendship_prog_mod_0.get_vertices()),
         h[0][1][1] / len(g_friendship_prog_mod_1.get_vertices()),
         h[0][2][2] / len(g_friendship_prog_mod_2.get_vertices()),
         h[0][3][3] / len(g_friendship_prog_mod_3.get_vertices()),
         h[0][4][4] / len(g_friendship_prog_mod_4.get_vertices()),
         h[0][5][5] / len(g_friendship_prog_mod_5.get_vertices()),
         h[0][6][6] / len(g_friendship_prog_mod_6.get_vertices()),
         h[0][7][7] / len(g_friendship_prog_mod_7.get_vertices()),
         h[0][8][8] / len(g_friendship_prog_mod_8.get_vertices()),
         h[0][9][9] / len(g_friendship_prog_mod_9.get_vertices()),
         h[0][10][10] / len(g_friendship_prog_mod_10.get_vertices())]

    print("Normailization by #Edges/#Nodes:")
    print("Normalization of Edges 0 - 0: ", y[0])
    print("Normalization of Edges 1 - 1: ", y[1])
    print("Normalization of Edges 2 - 2: ", y[2])
    print("Normalization of Edges 3 - 3: ", y[3])
    print("Normalization of Edges 4 - 4: ", y[4])
    print("Normalization of Edges 5 - 5: ", y[5])
    print("Normalization of Edges 6 - 6: ", y[6])
    print("Normalization of Edges 7 - 7: ", y[7])
    print("Normalization of Edges 8 - 8: ", y[8])
    print("Normalization of Edges 9 - 9: ", y[9])
    print("Normalization of Edges 10 - 10: ", y[10])


    fig, ax = plt.subplots()
    plt.bar(x, y, color='grey')
    plt.xlabel('Progressiveness Scores')
    plt.xticks(np.linspace(0, 10, 11))
    plt.ylabel('Number of Edges between nodes of the same progressiveness score, normalized by respective number of nodes ')
    plt.savefig("progScore_edgeNom_hist_ap1.png")
    plt.close()
