from neo4j import GraphDatabase
#from datetime import datetime
import json
#import sys

# This file is structured in the following manner.

# 1. Selection                          ### Selection of data included in database
# 2. Initialization                     ### Specifying Neo4j access, data input
# 3. Functions: Write Transactions      ### Defining MERGE-queries in write functions. These functions are called in "sessions - write" to populate the database
# 4. Functions: Read Transactions       ### Defining MATCH-queries in read  functions. These functions are called in "Sessions - read"  to read     the database
# 5. Sessions - write                   ### Parse and extract data from Json. Call write functions to populate database
# 6. Sessions - read                    ### Not necessary for Database creation and commented out. Formally used to double check population



#################
### Selection ###
#################
# Selection of data that is supposed to be included in the database. Everything is set True, except "sample_bool" for
# the final creation of the database

### Data ###
users_data_bool = True
debates_data_bool = True

### Nodes ###
user_bool = True
debate_bool = True
comment_bool = True
argument_bool = True
votemap_bool = True
opinion_bool = True
poll_bool = True
issues_bool = True
timeline_bool = True

### User Edges ###
friends_with_bool = True
debates_in_bool = True
gives_comment_bool = True
gives_argument_bool = True
gives_votemap_bool = True
gives_opinion_bool = True
gives_pollvote_bool = True
gives_issues_bool = True
user_timeline_bool = True

### Debate Edges ###
has_comment_bool = True
has_votemap_bool = True
has_argument_bool = True
debate_timeline_bool = True

### Comment Edges ###
comment_timeline_bool = True

### VoteMap Edges ###
refers_to_bool = True

### Sampling ###
sample_bool = False

### Indexing ###
index_bool = True

### Clear all ###
clearAll_bool = False

######################
### Initialization ###
######################
# Specifying Neo4j access, sample size and data input

print("Initialization")

driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "123"))

sample = 1

if users_data_bool == True:
    f = open('D:/Universitaet Mannheim/MMDS 6. Semester/Individual Project/users.json', "r")
    users_data = json.load(f)

if debates_data_bool == True:
    g = open('D:/Universitaet Mannheim/MMDS 6. Semester/Individual Project/debates.json', "r")
    debates_data = json.load(g)


#####################################
### Functions: Write Transactions ###
#####################################
# All Neo4j edges and nodes are created by accessing the database via these write functions

### Nodes ###

def add_user(tx, userName, userBirth, userDescr, userEduc, userElo, userEmail, userEthni, userSex, friend_privacy, userInterest, userInc,
                    userJoin, userOn, userUpd, userLook, userParty, userPercentile, userPoli, userPresi, userRels, userReli,
                    userURL, userWinR,
                    number_all_deb, number_lost_deb, number_tied_deb, number_won_deb, number_friends, number_opinion_arg, number_opinion_ques, number_poll_topics,
                    number_poll_votes, number_voted_deb):
    #print("add_user function is called with parameter", userName, userBirth)
    tx.run("MERGE (a:User {userID: $userName, birthday: $userBirth, description: $userDescr, education: $userEduc, elo_ranking: $userElo, " +
                    "email: $userEmail, ethnicity: $userEthni, gender: $userSex, friend_privacy: $friend_privacy, income: $userInc, interested: $userInterest, joined: $userJoin, last_online: $userOn, " +
                    "last_updated: $userUpd, looking: $userLook, party: $userParty, percentile: $userPercentile, political_ideology: $userPoli, president: $userPresi, relationship: $userRels, " +
                    "religious_ideology: $userReli, url: $userURL, win_ratio: $userWinR," +
                    "number_all_deb: $number_all_deb, number_lost_deb:$number_lost_deb, number_tied_deb: $number_tied_deb, number_won_deb: $number_won_deb, number_friends: $number_friends, " +
                    "number_opinion_arg: $number_opinion_arg, number_opinion_ques: $number_opinion_ques, number_poll_topics: $number_poll_topics, number_poll_votes: $number_poll_votes, " +
                    "number_voted_deb: $number_voted_deb})",
                    userName=userName, userBirth=userBirth, userDescr=userDescr, userEduc=userEduc, userElo=userElo, userEmail=userEmail,
                    userEthni=userEthni, userSex=userSex, friend_privacy=friend_privacy, userInc=userInc, userInterest=userInterest, userJoin=userJoin, userOn=userOn, userUpd=userUpd, userLook=userLook,
                    userParty=userParty, userPercentile=userPercentile, userPoli=userPoli, userPresi=userPresi, userRels=userRels, userReli=userReli, userURL=userURL,
                    userWinR=userWinR,
                    number_all_deb=number_all_deb, number_lost_deb=number_lost_deb, number_tied_deb=number_tied_deb, number_won_deb=number_won_deb, number_friends=number_friends,
                    number_opinion_arg=number_opinion_arg, number_opinion_ques=number_opinion_ques, number_poll_topics=number_poll_topics, number_poll_votes=number_poll_votes,
                    number_voted_deb=number_voted_deb)

                    # The following users.json entries are excluded from the User-node features, due to redundancy:
                    # 'all_debates'
                    # 'lost_debates'
                    # 'opinion_arguments'
                    # 'opinion_questions'
                    # 'poll_topics'
                    # 'poll_votes'
                    # 'voted_debates'
                    # 'won_debates'
                    # 'tied_debates'

                    # The following users.json entries are included to the User-node features, despite redundancy:
                    # 'number_of_all_debates'
                    # 'number_of_lost_debates'
                    # 'number_of_tied_debates'
                    # 'number_of_won_debates'
                    # 'number_of_friends'
                    # 'number_of_opinion_arguments'
                    # 'number_of_opinion_questions'
                    # 'number_of_poll_topics'
                    # 'number_of_poll_votes'
                    # 'number_of_voted_debates'
                    # might be excluded in future

def add_debate(tx, debateName, debateUrl, debateCategory, debateTitle, start_date, update_date, voting_style, debate_status, number_comments,
               number_views, number_rounds, number_votes):
    tx.run("MERGE (a:Debate {debateID: $debateName, url: $debateUrl, category: $debateCategory, title: $debateTitle, start: $start_date,"
           "update_date: $update_date, voting_style: $voting_style, debate_status: $debate_status, number_views: $number_views,"
           "number_comments: $number_comments, number_rounds: $number_rounds, number_votes: $number_votes})",
           debateName=debateName, debateUrl=debateUrl, debateCategory=debateCategory, debateTitle=debateTitle, start_date=start_date,
           update_date=update_date, voting_style=voting_style, debate_status=debate_status, number_comments=number_comments,
           number_views=number_views, number_rounds=number_rounds, number_votes=number_votes)

                    # The following users.json entries are excluded from the User-node features, due to redundancy:
                    # 'comments'
                    # 'votes'
                    # 'rounds'
                    # 'forfeit_label'
                    # 'forfeit_side'
                    # 'participant_1_link'
                    # 'participant_1_name'
                    # 'participant_1_points'
                    # 'participant_1_position'
                    # 'participant_1_status'
                    # 'participant_2_link'
                    # 'participant_2_name'
                    # 'participant_2_points'
                    # 'participant_2_position'
                    # 'participant_2_status'

                    # The following users.json entries are included to the User-node features, despite redundancy:
                    # 'number_of_comments'
                    # 'number_of_rounds'
                    # 'number_of_votes'

def add_comment(tx, commentID, commentTime, commentContent):
    tx.run(
        "MERGE (a:Comment {commentID: $commentID, commentTime: $commentTime, content: $commentContent})",
        commentID=commentID, commentTime=commentTime, commentContent=commentContent)

def add_argument(tx, argumentID, argumentContent):
    tx.run("MERGE (a:Argument {argumentID: $argumentID, argumentContent: $argumentContent})", argumentID=argumentID, argumentContent=argumentContent)

def add_voteMap_extended(tx, votemapID, beforeDebate, afterDebate, betterConduct, betterSpellingGrammar, convincingArguments, reliableSources, totalPoints):
    tx.run("MERGE (a:VoteMap {votemapID: $votemapID, beforeDebate: $beforeDebate, afterDebate: $afterDebate, " +
           "betterConduct: $betterConduct, betterSpellingGrammar: $betterSpellingGrammar, convincingArguments: $convincingArguments, " +
           "reliableSources: $reliableSources, totalPoints: $totalPoints})",
           votemapID=votemapID, beforeDebate=beforeDebate, afterDebate=afterDebate, betterConduct=betterConduct,
           betterSpellingGrammar=betterSpellingGrammar, convincingArguments=convincingArguments, reliableSources=reliableSources,
           totalPoints=totalPoints)

def add_voteMap_reduced(tx, votemapID, won):
    tx.run("MERGE (a:VoteMap {votemapID: $votemapID, won: $won})",
           votemapID=votemapID, won=won)

def add_opinion(tx, opinionID, opinionLink):
    tx.run("MERGE (a:Opinion {opinionID: $opinionID, opinionLink: $opinionLink})",
           opinionID=opinionID, opinionLink=opinionLink)

def add_poll(tx, pollID, pollLink):
    tx.run("MERGE (a:Poll {pollID: $pollID, pollLink: $pollLink})",
           pollID=pollID, pollLink=pollLink)

def add_issues(tx, issuesID, abortion, affirmative_a, animal_rights, obama, border, capitalism, civil_unions, death_penalty, drug_legaliz, electoral_college, enviro_prot,
               estate_tax, eu, euthanasia, federal_reserve, flat_tax, free_trade, gay_marriage, global_warming, globalization, gold_standard, gun_rights, homeschooling,
               internet_censor, iran_iraq_war, labor_union, legal_prostit, medicaid_care, medical_marijuana, military_interv, minimum_wage, national_health_care,
               nat_ret_sales_tax, occupy_movement, progressive_tax, racial_profiling, redistribution, smoking_ban, social_programs, social_security, socialism, stimulus_spending,
               term_limits, torture, united_nations, war_afghanistan, war_terror, welfare):
    tx.run("MERGE (a:Issues {issuesID: $issuesID, abortion: $abortion, affirmative_a: $affirmative_a, animal_rights: $animal_rights, obama: $obama, border: $border, capitalism: $capitalism, " +
           "civil_unions: $civil_unions, death_penalty: $death_penalty, drug_legaliz: $drug_legaliz, electoral_college: $electoral_college, enviro_prot: $enviro_prot, estate_tax: $estate_tax, " +
           "eu: $eu, euthanasia: $euthanasia, federal_reserve: $federal_reserve, flat_tax: $flat_tax, free_trade: $free_trade, gay_marriage: $gay_marriage, global_warming: $global_warming, " +
           "globalization: $globalization, gold_standard: $gold_standard, gun_rights: $gun_rights, homeschooling: $homeschooling, internet_censor: $internet_censor, iran_iraq_war: $iran_iraq_war, " +
           "labor_union: $labor_union, legal_prostit: $legal_prostit, medicaid_care: $medicaid_care, medical_marijuana: $medical_marijuana, military_interv: $military_interv, " +
           "minimum_wage: $minimum_wage, national_health_care: $national_health_care, nat_ret_sales_tax: $nat_ret_sales_tax, occupy_movement: $occupy_movement, progressive_tax: $progressive_tax, " +
           "racial_profiling: $racial_profiling, redistribution: $redistribution, smoking_ban: $smoking_ban, social_programs: $social_programs, social_security: $social_security, " +
           "socialism: $socialism, stimulus_spending: $stimulus_spending, term_limits: $term_limits, torture: $torture, united_nations: $united_nations, war_afghanistan: $war_afghanistan, " +
           "war_terror: $war_terror, welfare: $welfare})",
           issuesID=issuesID, abortion=abortion, affirmative_a=affirmative_a, animal_rights=animal_rights, obama=obama, border=border, capitalism=capitalism, civil_unions=civil_unions,
           death_penalty=death_penalty, drug_legaliz=drug_legaliz, electoral_college=electoral_college, enviro_prot=enviro_prot, estate_tax=estate_tax, eu=eu, euthanasia=euthanasia,
           federal_reserve=federal_reserve, flat_tax=flat_tax, free_trade=free_trade, gay_marriage=gay_marriage, global_warming=global_warming, globalization=globalization,
           gold_standard=gold_standard, gun_rights=gun_rights, homeschooling=homeschooling, internet_censor=internet_censor, iran_iraq_war=iran_iraq_war,
           labor_union=labor_union, legal_prostit=legal_prostit, medicaid_care=medicaid_care, medical_marijuana=medical_marijuana, military_interv=military_interv,
           minimum_wage=minimum_wage, national_health_care=national_health_care, nat_ret_sales_tax=nat_ret_sales_tax, occupy_movement=occupy_movement, progressive_tax=progressive_tax,
           racial_profiling=racial_profiling, redistribution=redistribution, smoking_ban=smoking_ban, social_programs=social_programs, social_security=social_security,
           socialism=socialism, stimulus_spending=stimulus_spending, term_limits=term_limits, torture=torture, united_nations=united_nations, war_afghanistan=war_afghanistan,
           war_terror=war_terror, welfare=welfare)

def add_timeline(tx, year):
    tx.run("MERGE (a:Timeline {year: $year})",
           year=year)

### User Edges ###

def add_friends_with(tx, userName, friendName):
    tx.run("MATCH (a:User {userID: $userName}) \n" +
           "MATCH (b:User {userID: $friendName}) \n" +
           "MERGE (a)-[:FRIENDS_WITH]->(b)", userName=userName, friendName=friendName)

def add_debates_in(tx, userName, debateName, debateForfeit, debatePoints, debatePosition, debateWinning):
    tx.run(
           "MATCH (a:User {userID: $userName}) \n" +
           "MATCH (b:Debate {debateID: $debateName}) \n" +
           "MERGE (a)-[:DEBATES_IN {forfeit: $debateForfeit, debatePoints: $debatePoints, position: $debatePosition, winning: $debateWinning }]->(b)",
           userName=userName, debateName=debateName, debateForfeit=debateForfeit, debatePoints=debatePoints, debatePosition=debatePosition, debateWinning=debateWinning)

def add_gives_comment(tx, userName, commentID):
    tx.run("MATCH (a:User {userID: $userName}) \n" +
           "MATCH (b:Comment {commentID: $commentID}) \n" +
           "MERGE (a)-[:GIVES_COMMENT]->(b)", userName=userName, commentID=commentID)

def add_gives_argument(tx, userID, argumentID):
    tx.run("MATCH (a:User {userID: $userID}) \n" +
           "MATCH (b:Argument {argumentID: $argumentID}) \n" +
           "MERGE (a)-[:GIVES_ARGUMENT]->(b)", userID=userID, argumentID=argumentID)

def add_gives_voteMap(tx, userID, votemapID):

    tx.run("MATCH (a:User {userID: $userID}) \n" +
           "MATCH (b:VoteMap {votemapID: $votemapID}) \n" +
           "MERGE (a)-[:GIVES_VOTEMAP]->(b)", userID=userID, votemapID=votemapID)

def add_gives_opinion(tx, userID, opinionID, opinionText):
    tx.run("MATCH (a:User {userID: $userID}) \n" +
           "MATCH (b:Opinion {opinionID: $opinionID}) \n" +
           "MERGE (a)-[rel:GIVES_OPINION {opinionText: $opinionText}]->(b)", userID=userID, opinionID=opinionID, opinionText=opinionText)

def add_gives_pollvote(tx, userID, pollID, pollText, pollExplanation):
    tx.run("MATCH (a:User {userID: $userID}) \n" +
           "MATCH (b:Poll {pollID: $pollID}) \n" +
           "MERGE (a)-[rel:GIVES_POLLVOTE {pollText: $pollText, pollExplanation: $pollExplanation}]->(b)", userID=userID, pollID=pollID, pollText=pollText, pollExplanation=pollExplanation)

def add_gives_issues(tx,userID, issuesID):
    tx.run("MATCH (a:User {userID: $userID}) \n" +
           "MATCH (b:Issues {issuesID: $issuesID}) \n" +
           "MERGE (a)-[rel:GIVES_ISSUES]->(b)", userID=userID, issuesID=issuesID)

# Alternative timeline appoach - not used in final
'''
def add_user_timeline(tx, prevUserID, debateID):
    tx.run("MATCH (a:User {userID: $debateID}) \n" +
           "MATCH (b:User {userID: $prevUserID}) \n" +
           "MERGE (b)-[:BEFORE]->(a)", debateID=debateID, prevUserID=prevUserID)
'''

def add_user_timeline(tx, userID, year):
    tx.run("MATCH (a:User {userID: $userID}) \n" +
           "MATCH (b:Timeline {year: $year}) \n" +
           "MERGE (a)-[:IN_TIMELINE]->(b)", userID=userID, year=year)


### Debate Edges ###

def add_has_comment(tx, debateName, commentID):
    tx.run("MATCH (a:Debate {debateID: $debateName}) \n" +
           "MATCH (b:Comment {commentID: $commentID}) \n" +
           "MERGE (a)-[:HAS_COMMENT]->(b)", debateName=debateName, commentID=commentID)

def add_has_voteMap(tx, debateID, votemapID):
    tx.run("MATCH (a:Debate {debateID: $debateID}) \n" +
           "MATCH (b:VoteMap {votemapID: $votemapID}) \n" +
           "MERGE (a)-[:HAS_VOTEMAP]->(b)",
           debateID=debateID, votemapID=votemapID)

def add_has_argument(tx, debateID, argumentID):
    tx.run("MATCH (a:Debate {debateID: $debateID}) \n" +
           "MATCH (b:Argument {argumentID: $argumentID}) \n" +
           "MERGE (a)-[:HAS_ARGUMENT]->(b)", debateID=debateID, argumentID=argumentID)

# Alternative timeline appoach - not used in final
'''
def add_debate_timeline(tx, debateID, prevDebateID):
    #print('add_debate_timeline is called with \n')
    #print(debateID, prevDebateID)
    tx.run("MATCH (a:Debate {debateID: $debateID}) \n" +
           "MATCH (b:Debate {debateID: $prevDebateID}) \n" +
           "MERGE (b)-[:BEFORE]->(a)", debateID=debateID, prevDebateID=prevDebateID)
'''

def add_debate_timeline(tx, debateID, year):
    tx.run("MATCH (a:Debate {debateID: $debateID}) \n" +
           "MATCH (b:Timeline {year: $year}) \n" +
           "MERGE (a)-[:IN_TIMELINE]->(b)", debateID=debateID, year=year)


### Comment Edges ###

# Alternative timeline appoach - not used in final
'''
def add_comment_timeline(tx, prevCommentID, commentID):
    tx.run("MATCH (a:Comment {commentID: $commentID}) \n" +
           "MATCH (b:Comment {commentID: $prevCommentID}) \n" +
           "MERGE (b)-[:BEFORE]->(a)", commentID=commentID, prevCommentID=prevCommentID)
'''

def add_comment_timeline(tx, commentID, year):
    tx.run("MATCH (a:Comment {commentID: $commentID}) \n" +
           "MATCH (b:Timeline {year: $year}) \n" +
           "MERGE (a)-[:IN_TIMELINE]->(b)", commentID=commentID, year=year)


### VoteMap Edges ###

def add_refers_to(tx, votemapID, userID):
    tx.run("MATCH (a:VoteMap {votemapID: $votemapID}) \n" +
            "MATCH (b:User {userID: $userID}) \n" +
            "MERGE (a)-[:REFERS_TO]->(b)",
            votemapID=votemapID, userID=userID)


### Indexing ###

def add_user_index(tx):
    tx.run("CREATE INDEX user_index FOR (n:User) ON (n.userID) ")

def add_debate_index(tx):
    tx.run("CREATE INDEX debate_index FOR (n:Debate) ON (n.debateID) ")

def add_comment_index(tx):
    tx.run("CREATE INDEX comment_index FOR (n:Comment) ON (n.commentID) ")

def add_argument_index(tx):
    tx.run("CREATE INDEX argument_index FOR (n:Argument) ON (n.argumentID) ")

def add_votemap_index(tx):
    tx.run("CREATE INDEX votemap_index FOR (n:Votemap) ON (n.votemapID) ")

def add_opinion_index(tx):
    tx.run("CREATE INDEX opinion_index FOR (n:Opinion) ON (n.opinionID) ")

def add_poll_index(tx):
    tx.run("CREATE INDEX poll_index FOR (n:Poll) ON (n.pollID) ")

def add_issues_index(tx):
    tx.run("CREATE INDEX issues_index FOR (n:Issues) ON (n.issuesID) ")


### Miscellaneous ###

def delete_all(tx):
    tx.run("MATCH (n) DETACH DELETE n")


####################################
### Functions: Read Transactions ###
####################################
# All Neo4j edges and nodes are read by accessing the database via these write functions

### Nodes ###

def read_user(tx):
    result = tx.run("MATCH (n:User) \n" +
           "RETURN n.userID, n.birthday, n.last_online, n.income, n.interested, n.friend_privacy")
    for record in result:
        print(record["n.userID"], record["n.birthday"], record["n.income"], record["n.interested"], record["n.friend_privacy"])

def read_debate(tx):
    result = tx.run("MATCH (n:Debate) \n" +
           "RETURN n.debateID, n.url, n.category, n.title")
    for record in result:
        print(record["n.debateID"])

def read_argument(tx):
    result = tx.run("MATCH (n:Argument) \n" +
           "RETURN n.argumentID, n.argumentContent")
    for record in result:
        print(record["n.argumentID"], record['n.argumentContent'])

def read_comment(tx):
    result = tx.run("MATCH (n:Comment) \n" +
                    "RETURN n.commentID, n.content")
    for record in result:
        print("{} has content {}".format(record["n.commentID"], record["n.content"]))

def read_voteMap(tx):
    result = tx.run("MATCH (n:VoteMap) \n" +
                    "RETURN n.votemapID, n.beforeDebate, n.afterDebate, n.betterConduct, n.betterSpellingGrammar, n.convincingArguments, \n" +
                    "n.reliableSources, n.totalPoints, n.won")
    for record in result:
        print("{} has agreed before debate: {}, and overall: {} - {}".format(record["n.votemapID"], record["n.beforeDebate"], record["n.totalPoints"], record["n.won"]))

def read_opinion(tx):
    result = tx.run("MATCH (n:Opinion) \n" +
                    "RETURN n.opinionID, n.opinionLink, n.opinionText")
    for record in result:
        print("{} has link {} with text {}".format(record["n.opinionID"], record["n.opinionLink"], record["n.opinionText"]))

def read_poll(tx):
    result = tx.run("MATCH (n:Poll) \n" +
                    "RETURN n.pollID, n.pollLink, n.pollText, n.pollExplanation")
    for record in result:
        print("{} has link {} with text {} and explanation: {}".format(record["n.pollID"], record["n.pollLink"], record["n.pollText"], record["n.pollExplanation"]))

def read_issues(tx):
    result = tx.run("MATCH (n:Issues) \n" +
                    "RETURN n.issuesID, n.abortion, n.affirmative_a, n.animal_rights")
    for record in result:
        print("issuesID: {}, abortion: {}, affirmative_a: {},animal_rights: {}".format(record["n.issuesID"], record["n.abortion"], record["n.affirmative_a"], record["n.animal_rights"]))


def read_timeline(tx):
    result = tx.run("MATCH (n:Timeline) \n" +
                        "RETURN n.year")
    for record in result:
        print("year node: {}".format(record["n.year"]))


### User Edges ###

def read_friends_with(tx):
    result = tx.run("MATCH (a:User)-[:FRIENDS_WITH]->(b:User) RETURN a.userID, b.userID")
    for record in result:
        print("{} nominated {}".format(record["a.userID"], record["b.userID"]))

def read_debates_in(tx):
    result = tx.run("MATCH (a:User)-[rel:DEBATES_IN]->(b:Debate) RETURN a.userID, b.debateID, rel.forfeit, rel.debatePoints, rel.position ,rel.winning")
    for record in result:
        print("{} debated in {} and has ff-value {} and points {}".format(record["a.userID"], record["b.debateID"], record["rel.forfeit"], record["rel.debatePoints"]))

def read_gives_comment(tx):
    result = tx.run("MATCH (a:User)-[rel:GIVES_COMMENT]->(b:Comment) RETURN a.userID, b.commentID, b.content")
    for record in result:
        print("{} gives comment {} with content {}".format(record["a.userID"], record["b.commentID"], record["b.content"]))

def read_gives_argument(tx):
    result = tx.run("MATCH (a:User)-[:GIVES_ARGUMENT]->(b:Argument) RETURN a.userID, b.argumentID, b.argumentContent")
    for record in result:
        print("{} has argued in {} with content {}".format(record["a.userID"], record["b.argumentID"], record["b.argumentContent"]))

def read_gives_voteMap(tx):
    result = tx.run("MATCH (a:User)-[:GIVES_VOTEMAP]->(b:VoteMap) RETURN a.userID, b.votemapID")
    for record in result:
        print("{} gives votemap {}".format(record["a.userID"], record["b.votemapID"]))

def read_gives_opinion(tx):
    result = tx.run("MATCH (a:User)-[rel:GIVES_OPINION]->(b:Opinion) RETURN a.userID, b.opinionID, rel.opinionText")
    for record in result:
        print("{} gives opinion {} with value {}".format(record["a.userID"], record["b.opinionID"], record["rel.opinionText"]))

def read_gives_pollvote(tx):
    result = tx.run("MATCH (a:User)-[rel:GIVES_POLLVOTE]->(b:Poll) RETURN a.userID, b.pollID, rel.pollText, rel.pollExplanation")
    for record in result:
        print("{} gives pollvote {} with value {} and explanation {} ".format(record["a.userID"], record["b.pollID"], record["rel.pollText"], record["rel.pollExplanation"]))

def read_gives_issues(tx):
    result = tx.run("MATCH (a:User)-[rel:GIVES_ISSUES]->(b:Issues) RETURN a.userID, b.issuesID, b.abortion")
    for record in result:
        print("{} gives Issues {} with abortion value {} ".format(record["a.userID"], record["b.issuesID"], record["b.abortion"]))

# Alternative timeline approach - not used in final
'''
def read_user_timeline(tx):
    result = tx.run("MATCH (a:User)-[:BEFORE]->(b:User) RETURN a.userID, a.joined , b.userID, b.joined")
    for record in result:
        print("User {} joined on {} before User {} joined on {}".format(record["a.userID"], record["a.joined"], record["b.userID"], record["b.joined"]))
'''

def read_user_timeline(tx):
    result = tx.run("MATCH (a:User)-[:IN_TIMELINE]->(b:Timeline) RETURN a.userID, a.joined, b.year")
    for record in result:
        print("User {} joined on {} and is in timeline {}".format(record["a.userID"], record["a.joined"], record["b.year"]))


### Debate Edges ###

def read_has_comment(tx):
    result = tx.run("MATCH (a:Debate)-[rel:HAS_COMMENT]->(b:Comment) RETURN a.debateID, b.commentID, b.content")
    for record in result:
        print("{} has comment {} with content {}".format(record["a.debateID"], record["b.commentID"], record["b.content"]))

def read_has_voteMap(tx):
    result = tx.run("MATCH (a:Debate)-[rel:HAS_VOTEMAP]->(b:VoteMap) RETURN a.debateID, b.votemapID, b.totalPoints")
    for record in result:
        print("{} has votemap: {} with points: {}".format(record["a.debateID"], record["b.votemapID"], record["b.totalPoints"]))

def read_has_argument(tx):
    result = tx.run("MATCH (a:Debate)-[:HAS_ARGUMENT]->(b:Argument) RETURN a.debateID, b.argumentID, b.argumentContent")
    for record in result:
        print("{} has argument {} with content {}".format(record["a.debateID"], record["b.argumentID"], record["b.argumentContent"]))

# Alternative timeline approach - not used in final
'''
def read_debate_timeline(tx):
    result = tx.run("MATCH (a:Debate)-[:BEFORE]->(b:Debate) RETURN a.debateID, a.start , b.debateID, b.start")
    for record in result:
        print("{} with {} took place before {} with {}".format(record["a.debateID"], record["a.start"], record["b.debateID"], record["b.start"]))
'''

def read_debate_timeline(tx):
    result = tx.run("MATCH (a:Debate)-[:IN_TIMELINE]->(b:Timeline) RETURN a.debateID, a.start , b.year")
    for record in result:
        print("{} with {} is in Timeline {}".format(record["a.debateID"], record["a.start"], record["b.year"]))


### Comment Edges ###

# Alternative timeline approach - not used in final
'''
def read_comment_timeline(tx):
    result = tx.run("MATCH (a:Comment)-[:BEFORE]->(b:Comment) RETURN a.commentID, a.commentTime , b.commentID, b.commentTime")
    for record in result:
        print("Comment {} with date {} was created before comment {} with date {}".format(record["a.commentID"], record["a.commentTime"], record["b.commentID"], record["b.commentTime"]))
'''

def read_comment_timeline(tx):
    result = tx.run("MATCH (a:Comment)-[:IN_TIMELINE]->(b:Timeline) RETURN a.commentID, a.commentTime , b.year")
    for record in result:
        print("Comment {} with date {} is in Timeline {}".format(record["a.commentID"], record["a.commentTime"], record["b.year"]))


### VoteMap Edges ###

def read_refers_to(tx):
    result = tx.run("MATCH (a:VoteMap)-[:REFERS_TO]->(b:User) RETURN a.votemapID, b.userID")
    for record in result:
        print("{} refers to {}".format(record["a.votemapID"], record["b.userID"]))


### Miscellaneous ###

def read_all(tx):
    tx.run("MATCH (n) RETURN n")


########################
### Sessions - write ###
########################
# All neo4j node and edges are created in one session. At first "users_data" and "debates_data" are accessed and looped
# over to extract all relevant information for node creation. At the same time the extracted information is feed via the
# previously defined write-functions to the data base in order to create the respective node. Time line nodes
# representing the year span of the dataset are generated as well.
# In a second step "users_data" and "debates_data" are traversed again to extract and feed edge relevant data. This way
# neo4j edges are created as well (accessing the respective, previously defined write-functions)

# tl;dr
# 1. loop node creation
# 2. loop edge creation


with driver.session() as session:

    ###---------------###
    ### Miscellaneous ###
    ###---------------###

    ### Cleaning ###

    if clearAll_bool == True:
        session.write_transaction(delete_all)

        print("Cleaning - done")


    ###--------------------###
    ### Nodes - users_data ###
    ###--------------------###

    userList = []
    c = 0

    for i in users_data:
        c = c + 1


        ### User Node ###
        if user_bool == True:

            userList.append(i)                          # created for "DEBATES_IN" and "FRIENDS_WITH"-relations later
            if users_data[i]['friends'] == 'private':
                friend_privacy = True
            else:
                friend_privacy = False

            session.write_transaction(add_user, i, users_data[i]['birthday'], users_data[i]['description'], users_data[i]['education'],
                                      users_data[i]['elo_ranking'], users_data[i]['email'], users_data[i]['ethnicity'], users_data[i]['gender'], friend_privacy,
                                      users_data[i]['income'], users_data[i]['interested'], users_data[i]['joined'], users_data[i]['last_online'], users_data[i]['last_updated'],
                                      users_data[i]['looking'], users_data[i]['party'], users_data[i]['percentile'], users_data[i]['political_ideology'], users_data[i]['president'],
                                      users_data[i]['relationship'], users_data[i]['religious_ideology'], users_data[i]['url'], users_data[i]['win_ratio'],
                                      users_data[i]['number_of_all_debates'], users_data[i]['number_of_lost_debates'], users_data[i]['number_of_tied_debates'],
                                      users_data[i]['number_of_won_debates'], users_data[i]['number_of_friends'], users_data[i]['number_of_opinion_arguments'],
                                      users_data[i]['number_of_opinion_questions'], users_data[i]['number_of_poll_topics'], users_data[i]['number_of_poll_votes'],
                                      users_data[i]['number_of_voted_debates'])
            #print("user information is extracted with value ", i, users_data[i]['birthday'])


        ### Opinion Nodes ###
        if opinion_bool == True:

            for k in users_data[i]['opinion_arguments']:
                session.write_transaction(add_opinion, k['opinion title'], k['opinion link'])


        ### Poll Nodes ###
        if poll_bool == True:

            for k in users_data[i]['poll_votes']:
                session.write_transaction(add_poll, k['vote title'], k['vote link'])


        ### Issues Nodes ###
        if issues_bool == True:

            issuesID = i + '_issues'
            k = users_data[i]['big_issues_dict']
            session.write_transaction(add_issues, issuesID, k['Abortion'], k['Affirmative Action'],
                                      k['Animal Rights'], k['Barack Obama'], k['Border Fence'], k['Capitalism'],
                                      k['Civil Unions'],
                                      k['Death Penalty'], k['Drug Legalization'], k['Electoral College'],
                                      k['Environmental Protection'], k['Estate Tax'], k['European Union'],
                                      k['Euthanasia'],
                                      k['Federal Reserve'], k['Flat Tax'], k['Free Trade'], k['Gay Marriage'],
                                      k['Global Warming Exists'], k['Globalization'], k['Gold Standard'],
                                      k['Gun Rights'],
                                      k['Homeschooling'], k['Internet Censorship'], k['Iran-Iraq War'],
                                      k['Labor Union'], k['Legalized Prostitution'], k['Medicaid & Medicare'],
                                      k['Medical Marijuana'],
                                      k['Military Intervention'], k['Minimum Wage'], k['National Health Care'],
                                      k['National Retail Sales Tax'], k['Occupy Movement'],
                                      k['Progressive Tax'],
                                      k['Racial Profiling'], k['Redistribution'], k['Smoking Ban'],
                                      k['Social Programs'], k['Social Security'], k['Socialism'],
                                      k['Stimulus Spending'], k['Term Limits'],
                                      k['Torture'], k['United Nations'], k['War in Afghanistan'],
                                      k['War on Terror'], k['Welfare'])


        if c % 100 == 0:
            print('Nodes - users_data: ', c)
        if sample_bool == True and c >= sample:
            print("-- Nodes - users_data done --")
            break


    ###----------------------###
    ### Nodes - debates_data ###
    ###----------------------###

    c = 0

    for i in debates_data:
        c = c + 1

        ### Debate Node ###
        if debate_bool == True:

            session.write_transaction(add_debate, i, debates_data[i]['url'], debates_data[i]['category'],
                                      debates_data[i]['title'], debates_data[i]['start_date'],
                                      debates_data[i]['update_date'], debates_data[i]['voting_style'],
                                      debates_data[i]['debate_status'], debates_data[i]['number_of_comments'],
                                      debates_data[i]['number_of_views'], debates_data[i]['number_of_rounds'],
                                      debates_data[i]['number_of_votes'])


        ### Comment Nodes ###
        if comment_bool == True:

            c2 = 0
            for k in debates_data[i]['comments']:
                c2 = c2 + 1
                commentID = str(str(i) + '_Comment_' + str(c2))
                session.write_transaction(add_comment, commentID, k['time'], k['comment_text'])


        ### Argument Nodes ###
        if argument_bool == True:

            c2 = 0
            for k in debates_data[i]['rounds']:
                c2 = c2 + 1
                for p in k:
                    argumentID = str(str(i) + "_round_" + str(c2) + "_" + str(p['side']))
                    session.write_transaction(add_argument, argumentID, p['text'])


        ### VoteMap Nodes ###
        if votemap_bool == True:

                c2 = 0
                for k in debates_data[i]['votes']:
                    c2 = c2 + 1
                    c3 = 0
                    for p in k['votes_map']:
                        if c3 == 2:
                            break    # VoteMaps consist of 3 parts: bools of votes given to participant1, to
                                     # participant2 and a redundant part 3 called "tied". It contains the same variables.
                                     # Part 3 is simply the first two variables connected with an logic AND. See report,
                                     # for details
                        votemapID = str(str(i) + '_' + str(k['user_name']) + '_' + str(p))
                        if 'Agreed with before the debate' in k['votes_map'][p]:
                            session.write_transaction(add_voteMap_extended, votemapID,
                                                      k['votes_map'][p]['Agreed with before the debate'],
                                                      k['votes_map'][p]['Agreed with after the debate'],
                                                      k['votes_map'][p]['Who had better conduct'],
                                                      k['votes_map'][p]['Had better spelling and grammar'],
                                                      k['votes_map'][p]['Made more convincing arguments'],
                                                      k['votes_map'][p]['Used the most reliable sources'],
                                                      k['votes_map'][p][
                                                          'Total points awarded'])  # "Total points awarded" might be redundant
                        else:
                            session.write_transaction(add_voteMap_reduced, votemapID,
                                                      k['votes_map'][p]['Who won the debate'])
                        c3 = c3 + 1


        if c % 100 == 0:
            print('Nodes - debates_data: ', c)
        if sample_bool == True and c >= sample:
            print("-- Nodes - debates_data done --")
            break


    ###------------------###
    ### Nodes - Timeline ###
    ###------------------###

    if timeline_bool == True:
        for i in range(2007, 2019):                     # Conflicting Information. "http://www.cs.cornell.edu/~esindurmus/ddo.html"
                                                        # states a data collection up to November 2017. Yet, the Json contains users
                                                        # created in 2019. See Report for Details
            session.write_transaction(add_timeline, i)  # Neo4j cares about the data type that is submitted (here int)
        print("-- Nodes - Timeline done --")


    ###----------###
    ### Indexing ###
    ###----------###

    if index_bool == True:

        session.write_transaction(add_user_index)
        session.write_transaction(add_debate_index)
        session.write_transaction(add_comment_index)
        session.write_transaction(add_argument_index)
        session.write_transaction(add_votemap_index)
        session.write_transaction(add_opinion_index)
        session.write_transaction(add_poll_index)
        session.write_transaction(add_issues_index)


    ###--------------------###
    ### Edges - users_data ###
    ###--------------------###

    c = 0
    for i in users_data:
        c = c + 1

        ### User Edge - friends_with ###
        if friends_with_bool == True:

            if (users_data[i]['friends'] != []):
                if (users_data[i]['friends'] != "private"):
                    for k in users_data[i]['friends']:
                        if k in userList:
                            session.write_transaction(add_friends_with, i, k)


        ### User Edge - gives_opinion ###
        if gives_opinion_bool == True:

            for k in users_data[i]['opinion_arguments']:
                session.write_transaction(add_gives_opinion, i, k['opinion title'], k['opinion text'])


        ### User Edge - gives_pollvote ###
        if gives_pollvote_bool == True:

            for k in users_data[i]['poll_votes']:
                session.write_transaction(add_gives_pollvote, i, k['vote title'], k['vote text'], k['vote explanation'])


        ### User Edge - gives_issues ###
        if gives_issues_bool == True:

            issuesID = i + '_issues'
            session.write_transaction(add_gives_issues, i, issuesID)


        ### User Edge - user_timeline ###
        ### Extraction on November 2017 "http://www.cs.cornell.edu/~esindurmus/ddo.html" ###
        # Conflicting with data in Json (User created in 2019), see report.
        # This timeline creation might need to be revisited

        if user_timeline_bool == True:

            if 'Years' in users_data[i]['joined'] or 'Year' in users_data[i]['joined']:
                if users_data[i]['joined'][1] != ' ':
                    joined_year = 2017 - int(users_data[i]['joined'][0:2])
                else:
                    joined_year = 2017 - int(users_data[i]['joined'][0])
            else:
                joined_year = 2017#
            session.write_transaction(add_user_timeline, i, joined_year)  # -[IN_TIMELINE]->


        if c % 100 == 0:
            print('Edges - users_data: ', c)
        if sample_bool == True and c >= sample:
            print("-- Edges - users_data done --")
            break



    ###----------------------###
    ### Edges - debates_data ###
    ###----------------------###

    c = 0
    for i in debates_data:
        c = c + 1

        ### User Edges - debates_in ###
        if debates_in_bool == True:

            forfeit_bool1 = False
            winning_bool1 = False
            forfeit_bool2 = False
            winning_bool2 = False

            if debates_data[i]['participant_1_name'] in userList:
                if debates_data[i]['forfeit_side'] == debates_data[i]['participant_1_name']:
                    forfeit_bool1 = True
                if debates_data[i]['participant_1_status'] == "Winning":
                    winning_bool1 = True
                session.write_transaction(add_debates_in, debates_data[i]['participant_1_name'], i, forfeit_bool1,
                                          debates_data[i]['participant_1_points'],
                                          debates_data[i]['participant_1_position'],
                                          winning_bool1)

            if debates_data[i]['participant_2_name'] in userList:
                if debates_data[i]['forfeit_side'] == debates_data[i]['participant_2_name']:
                    forfeit_bool2 = True
                if debates_data[i]['participant_2_status'] == "Winning":
                    winning_bool2 = True
                session.write_transaction(add_debates_in, debates_data[i]['participant_2_name'], i, forfeit_bool2,
                                          debates_data[i]['participant_2_points'],
                                          debates_data[i]['participant_2_position'],
                                          winning_bool2)


        ### User Edge - gives_comment ###
        if gives_comment_bool == True:

            c2 = 0
            for k in debates_data[i]['comments']:
                c2 = c2 + 1
                commentID = str(str(i) + '_Comment_' + str(c2))
                session.write_transaction(add_gives_comment, k['user_name'], commentID)


        ### User Edge - gives_argument ###
        if gives_argument_bool == True:

            c2 = 0
            for k in debates_data[i]['rounds']:
                c2 = c2 + 1
                for p in k:
                    argumentID = str(str(i) + "_round_" + str(c2) + "_" + str(p['side']))
                    if p['side'] == "Pro":
                        UserID = debates_data[i]['participant_1_name']  # participant_1_position is always "Pro"
                    else:
                        UserID = debates_data[i]['participant_2_name']
                    session.write_transaction(add_gives_argument, UserID, argumentID)


        ### User Edge - gives_voteMap ###
        if gives_votemap_bool == True:

            c2 = 0
            for k in debates_data[i]['votes']:
                c2 = c2 + 1
                c3 = 0
                for p in k['votes_map']:
                    if c3 == 2:
                        break
                    votemapID = str(str(i) + '_' + str(k['user_name']) + '_' + str(p))
                    session.write_transaction(add_gives_voteMap, k['user_name'], votemapID)
                    c3 = c3 + 1


        ### Debate Edge - has_comment ###
        if has_comment_bool == True:

            c2 = 0
            for k in debates_data[i]['comments']:
                c2 = c2 + 1
                commentID = str(str(i) + '_Comment_' + str(c2))
                session.write_transaction(add_has_comment, i, commentID)


        ### Debate Edge - has_votemap ###
        if has_votemap_bool == True:

            c2 = 0
            for k in debates_data[i]['votes']:
                c2 = c2 + 1
                c3 = 0
                for p in k['votes_map']:
                    if c3 == 2:
                        break
                    votemapID = str(str(i) + '_' + str(k['user_name']) + '_' + str(p))
                    session.write_transaction(add_has_voteMap, i, votemapID)
                    c3 = c3 + 1


        ### Debate Edge - has_argument ###
        if has_argument_bool == True:

            c2 = 0
            for k in debates_data[i]['rounds']:
                c2 = c2 + 1
                for p in k:
                    UserID = ""
                    argumentID = str(str(i) + "_round_" + str(c2) + "_" + str(p['side']))
                    session.write_transaction(add_has_argument, i, argumentID)


        ### VoteMap Edge - refers_to ###
        if refers_to_bool == True:

            c2 = 0
            for k in debates_data[i]['votes']:
                c2 = c2 + 1
                c3 = 0
                for p in k['votes_map']:
                    if c3 == 2:
                        break
                    votemapID = str(str(i) + '_' + str(k['user_name']) + '_' + str(p))
                    session.write_transaction(add_refers_to, votemapID, p)
                    c3 = c3 + 1


        ### Debate Edge - debate_timeline ###
        if debate_timeline_bool == True:
            session.write_transaction(add_debate_timeline, i,
                                      int(debates_data[i]['start_date'][-4:]))  # -[IN_TIMELINE]->


        ### Debate Edge - comment_timeline ###
        if comment_timeline_bool == True:

            c2 = 0
            for k in debates_data[i]['comments']:
                c2 = c2 + 1
                commentID = str(str(i) + '_Comment_' + str(c2))

                if 'years' in k['time'] or 'year' in k['time']:
                    if k['time'][1] != ' ':
                        created_year = 2017 - int(k['time'][0:2])
                    else:
                        created_year = 2017 - int(k['time'][0])
                else:
                    created_year = 2017

                session.write_transaction(add_comment_timeline, commentID, created_year)  # -[IN_TIMELINE]->


        if c % 100 == 0:
            print('Edges - debates_data: ', c)
        if sample_bool == True and c >= sample:
            print("-- Edges - debates_data done --")
            break


    # Alternative timeline appoach - not used in final
    '''
    ###-----------------------###
    ### Timeline - users_data ###
    ###-----------------------###



    c = 0
    for i in users_data:
        c = c + 1

        ### Extraction on November 2017 ###
        ### User Edge - user_timeline ###
        if user_timeline_bool == True:

            if 'Years' in users_data[i]['joined'] or 'Year' in users_data[i]['joined']:
                if users_data[i]['joined'][1] != ' ':
                    joined_year = 2017 - int(users_data[i]['joined'][0:2])
                else:
                    joined_year = 2017 - int(users_data[i]['joined'][0])
            else:
                joined_year = 2017

            #print(i, joined_year)
            session.write_transaction(add_user_timeline, i, joined_year)  # -[IN_TIMELINE]->

        if c % 100 == 0:
            print('Edges - user_timeline: ', c)
        if sample_bool == True and c >= sample:
            print("-- Edges - user_timeline done --")
            break'''

    '''
    joined_array = np.array([])
    userID_array = np.array([])
    c = 0
    for i in users_data:
        c = c + 1

        ### User Edge - user_timeline - extraction (Part1 in Loop) ###
        if user_timeline_bool == True:

            if 'Years' in users_data[i]['joined'] or 'Year' in users_data[i]['joined']:
                if users_data[i]['joined'][1] != ' ':
                    joined_days = int(users_data[i]['joined'][0:2]) * 365
                else:
                    joined_days = int(users_data[i]['joined'][0]) * 365
            elif 'Months' in users_data[i]['joined'] or 'Month' in users_data[i]['joined']:
                if users_data[i]['joined'][1] != ' ':
                    joined_days = int(users_data[i]['joined'][0:2]) * 30
                else:
                    joined_days = int(users_data[i]['joined'][0]) * 30

            elif 'Weeks' in users_data[i]['joined'] or 'Week' in users_data[i]['joined']:
                if users_data[i]['joined'][1] != ' ':
                    joined_days = int(users_data[i]['joined'][0:2]) * 7
                else:
                    joined_days = int(users_data[i]['joined'][0]) * 7

            elif 'Days' in users_data[i]['joined'] or 'Day' in users_data[i]['joined']:
                if users_data[i]['joined'][1] != ' ':
                    joined_days = int(users_data[i]['joined'][0:2])
                else:
                    joined_days = int(users_data[i]['joined'][0])

            else:
                joined_days = 'unidentified joined period'

            userID_array = np.append(userID_array, i)
            joined_array = np.append(joined_array, joined_days)

        if c % 100 == 0:
            print('Timeline - users_data Part1: ', c)
        if sample_bool == True and c >= sample:
            print("-- Timeline - users_data Part1 done --")
            break

    ### User Edge - user_timeline - manipulation (Part2 outside Loop) ###
    if user_timeline_bool == True:

        sort_joined_array_index = np.argsort(joined_array)

        sort_joined_array = joined_array[sort_joined_array_index]
        sort_userID_array = userID_array[sort_joined_array_index]

        sort_joined_array_unique = np.unique(sort_joined_array)

        for i in range(len(sort_joined_array_unique) - 1):

            focal_date = sort_joined_array_unique[i]
            next_date = sort_joined_array_unique[i + 1]

            focal_date_index = np.where(sort_joined_array == sort_joined_array_unique[i])
            next_date_index = np.where(sort_joined_array == sort_joined_array_unique[i + 1])

            for userID in sort_userID_array[focal_date_index]:
                for prevuserID in sort_userID_array[next_date_index]:
                    session.write_transaction(add_user_timeline, prevuserID, userID)  # -[Before]->

    print("-- Timeline - users_data Part2 done --")
    '''

    '''
    ###-------------------------###
    ### Timeline - debates_data ###
    ###-------------------------###


    c = 0
    for i in debates_data:
        c = c + 1

        ### Debate Edge - debate_timeline ###
        if debate_timeline_bool == True:

            session.write_transaction(add_debate_timeline, i, int(debates_data[i]['start_date'][-4:]))  # -[IN_TIMELINE]->
            

        ### Debate Edge - comment_timeline ###
        if comment_timeline_bool == True:

            c2 = 0
            for k in debates_data[i]['comments']:
                c2 = c2 + 1
                commentID = str(str(i) + '_Comment_' + str(c2))

                if 'years' in k['time'] or 'year' in k['time']:
                    if k['time'][1] != ' ':
                        created_year = 2017 - int(k['time'][0:2])
                    else:
                        created_year = 2017 - int(k['time'][0])
                else:
                    created_year = 2017

                session.write_transaction(add_comment_timeline, commentID, created_year)  # -[IN_TIMELINE]->

        if c % 100 == 0:
            print('Timeline - debates_data: ', c)
        if sample_bool == True and c >= sample:
            print("-- Timeline - debates_data done --")
            break'''



    '''
    debate_day_array = np.array([], dtype='datetime64')
    debate_title_array = np.array([])

    created_array = np.array([])
    commentID_array = np.array([])

    c = 0
    for i in debates_data:
        c = c + 1

        ### Debate Edge - debate_timeline - extraction (part1 in Loop) ###
        if debate_timeline_bool == True:

            debate_day = datetime.strptime((debates_data[i]['start_date']), '%m/%d/%Y').date()
            debate_day_array = np.append(debate_day_array, debate_day)
            debate_title_array = np.append(debate_title_array, [i])
            sort_order_array = np.argsort(debate_day_array)

        ### Debate Edge - comment_timeline - extraction (part1 in Loop) ###
        if comment_timeline_bool == True:

            c2 = 0
            for k in debates_data[i]['comments']:
                c2 = c2 + 1
                commentID = str(str(i) + '_Comment_' + str(c2))

                if 'years' in k['time'] or 'year' in k['time']:
                    if k['time'][1] != ' ':
                        created_days = int(k['time'][0:2]) * 365
                    else:
                        created_days = int(k['time'][0]) * 365

                elif 'months' in k['time'] or 'month' in k['time']:
                    if k['time'][1] != ' ':
                        created_days = int(k['time'][0:2]) * 30
                    else:
                        created_days = int(k['time'][0]) * 30

                elif 'weeks' in k['time'] or 'week' in k['time']:
                    if k['time'][1] != ' ':
                        created_days = int(k['time'][0:2]) * 7
                    else:
                        created_days = int(k['time'][0]) * 7

                elif 'days' in k['time'] or 'day' in k['time']:
                    if k['time'][1] != ' ':
                        created_days = int(k['time'][0:2])
                    else:
                        created_days = int(k['time'][0])

                else:
                    created_days = 'unidentified created period'

                commentID_array = np.append(commentID_array, commentID)
                created_array = np.append(created_array, created_days)

        if c % 100 == 0:
            print('Timeline - debates_data Part1: ', c)
        if sample_bool == True and c >= sample:
            print("-- Timeline - debates_data Part1 done --")
            break



    ### Debate Edge - debate_timeline - manipulation (Part2 outside Loop) ###
    if debate_timeline_bool == True:

        sort_order_array = np.argsort(debate_day_array)

        sorted_title_array = debate_title_array[sort_order_array]
        sorted_day_array = debate_day_array[sort_order_array]
        sorted_day_array_unique = np.unique(debate_day_array[sort_order_array])

        for i in range(len(sorted_day_array_unique) - 1):

            focal_date = sorted_day_array_unique[i]
            next_date = sorted_day_array_unique[i + 1]

            focal_date_index = np.where(sorted_day_array == sorted_day_array_unique[i])
            next_date_index = np.where(sorted_day_array == sorted_day_array_unique[i + 1])

            for debateID in sorted_title_array[focal_date_index]:
                for prevdebateID in sorted_title_array[next_date_index]:
                    session.write_transaction(add_debate_timeline, prevdebateID, debateID)  # -[Before]->

    ### Debate Edge - comment_timeline - manipulation (Part2 outside Loop) ###
    if debate_timeline_bool == True:

        sort_created_array_index = np.argsort(created_array)

        sort_created_array = created_array[sort_created_array_index]
        sort_comment_array = commentID_array[sort_created_array_index]

        sort_created_array_unique = np.unique(sort_created_array)

        for i in range(len(sort_created_array_unique) - 1):

            focal_date = sort_created_array_unique[i]
            next_date = sort_created_array_unique[i + 1]

            focal_date_index = np.where(sort_created_array == sort_created_array_unique[i])
            next_date_index = np.where(sort_created_array == sort_created_array_unique[i + 1])

            for commentID in sort_comment_array[focal_date_index]:
                for prevcommentID in sort_comment_array[next_date_index]:
                    session.write_transaction(add_comment_timeline, prevcommentID, commentID)  # -[Before]->

    print("-- Timeline - debates_data Part2 done --")
    '''

    print("-- write done --")


    #######################
    ### Sessions - read ###
    #######################

    # session.read_transaction(read_all)

    # session.read_transaction(read_user)
    # session.read_transaction(read_debate)
    # session.read_transaction(read_comment)
    # session.read_transaction(read_argument)
    # session.read_transaction(read_voteMap)
    # session.read_transaction(read_opinion)
    # session.read_transaction(read_poll)
    # session.read_transaction(read_issues)
    # session.read_transaction(read_timeline)

    # session.read_transaction(read_friends_with)
    # session.read_transaction(read_debates_in)
    # session.read_transaction(read_gives_comment)
    # session.read_transaction(read_gives_argument)
    # session.read_transaction(read_gives_voteMap)
    # session.read_transaction(read_gives_opinion)
    # session.read_transaction(read_gives_pollvote)
    # session.read_transaction(read_gives_issues)                
    # session.read_transaction(read_user_timeline)

    # session.read_transaction(read_has_comment)
    # session.read_transaction(read_has_voteMap)
    # session.read_transaction(read_has_argument)
    # session.read_transaction(read_debate_timeline)

    # session.read_transaction(read_comment_timeline)

    # session.read_transaction(read_refers_to)

    print("-- read done --")




