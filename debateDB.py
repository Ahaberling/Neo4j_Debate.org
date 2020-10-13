from neo4j import GraphDatabase
import json
#import collections

######################
### Initialization ###
######################

f = open('D:/Universitaet Mannheim/MMDS 6. Semester/Individual Project/users.json', "r")
g = open('D:/Universitaet Mannheim/MMDS 6. Semester/Individual Project/debates.json', "r")

users_data = json.load(f)
debates_data = json.load(g)

driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "abc"))


user_bool = True
debate_bool = False
comment_bool = False
argument_bool = False
votemap_bool = True

friends_with_bool = False
debates_in_bool = False
gives_comment_bool = False
gives_argument_bool = False
gives_votemap_bool = False
user_timeline_bool = False

has_comment_bool = False
has_votemap_bool = False
has_round_bool = False
debate_timeline_bool = False

comment_timeline_bool = False

refers_to_bool = True

sample = 300

#####################################
### Functions: Write Transactions ###
#####################################

### Nodes ###

def add_user(tx, userName, userBirth, userDescr, userEduc, userElo, userEmail, userEthni, userSex, userInterest, userInc,
                    userJoin, userOn, userUpd, userLook, userParty, userPoli, userPresi, userRels, userReli,
                    userURL, userWinR):
    tx.run("MERGE (a:User {userID: $userName, birthday: $userBirth, description: $userDescr, education: $userEduc, elo_ranking: $userElo," +
                    "email: $userEmail, ethnicity: $userEthni, gender: $userSex, interested: $userInterest,income: $userInc, joined: $userJoin, last_online: $userOn," +
                    "last_updated: $userUpd, looking: $userLook, party: $userParty, political_ideology: $userPoli, president: $userPresi, relationship: $userRels," +
                    "religious_ideology: $userReli, url: $userURL, win_ratio: $userWinR})",
                    userName=userName, userBirth=userBirth, userDescr=userDescr, userEduc=userEduc, userElo=userElo, userEmail=userEmail,
                    userEthni=userEthni, userSex=userSex, userInterest=userInterest, userInc=userInc, userJoin=userJoin, userOn=userOn, userUpd=userUpd, userLook=userLook,
                    userParty=userParty, userPoli=userPoli, userPresi=userPresi, userRels=userRels, userReli=userReli, userURL=userURL,
                    userWinR=userWinR)

def add_debate(tx, debateName, debateUrl, debateCategory, debateTitle):
    tx.run("MERGE (a:Debate {debateID: $debateName, url: $debateUrl, category: $debateCategory, title: $debateTitle})",
           debateName=debateName, debateUrl=debateUrl, debateCategory=debateCategory, debateTitle=debateTitle)

def add_comment(tx, commentID, commentContent):
    tx.run("MERGE (a:Comment {commentID: $commentID, content: $commentContent})", commentID=commentID, commentContent=commentContent)

def add_argument(tx, argumentID, argumentContent):
    tx.run("MERGE (a:Argument {argumentID: $argumentID, content: $argumentContent})", argumentID=argumentID, argumentContent=argumentContent)

def add_voteMap_extended(tx, votemapID, beforeDebate, afterDebate, betterConduct, betterSpellingGrammar, convincingArguments,
                reliableSources, totalPoints):
    tx.run("MERGE (a:VoteMap {votemapID: $votemapID, beforeDebate: $beforeDebate, afterDebate: $afterDebate, " +
           "betterConduct: $betterConduct, betterSpellingGrammar: $betterSpellingGrammar, convincingArguments: $convincingArguments, " +
           "reliableSources: $reliableSources, totalPoints: $totalPoints})",
           votemapID=votemapID, beforeDebate=beforeDebate, afterDebate=afterDebate, betterConduct=betterConduct,
           betterSpellingGrammar=betterSpellingGrammar, convincingArguments=convincingArguments, reliableSources=reliableSources,
           totalPoints=totalPoints)

def add_voteMap_reduced(tx, votemapID, won):
    tx.run("MERGE (a:VoteMap {votemapID: $votemapID, won: $won})",
           votemapID=votemapID, won=won)

### User Edges ###

def add_friends_with(tx, userName, friendName):
    tx.run("MATCH (a:User {userID: $userName}) \n" +
           "MATCH (b:User {userID: $friendName}) \n" +
           "MERGE (a)-[:FRIENDS_WITH]->(b)", userName=userName, friendName=friendName)

def add_debates_in(tx, userName, debateName, debateForfeit, debateWinning, debatePosition):
    tx.run("MATCH (a:User {userID: $userName}) \n" +
           "MATCH (b:Debate {debateID: $debateName}) \n" +
           "MERGE (a)-[:DEBATES_IN {forfeit: $debateForfeit, winning: $debateWinning, position: $debatePosition }]->(b)",
           userName=userName, debateName=debateName, debateForfeit=debateForfeit, debateWinning=debateWinning, debatePosition=debatePosition)

def add_gives_comment(tx, userName, commentID):
    tx.run("MATCH (a:User {userID: $userName}) \n" +
           "MATCH (b:Comment {commentID: $commentID}) \n" +
           "MERGE (a)-[:GIVES_COMMENT]->(b)", userName=userName, commentID=commentID)

def add_gives_argument(tx, userName, argumentID):
    tx.run("MATCH (a:User {userID: $userName}) \n" +
           "MATCH (b:Argument {argumentID: $argumentID}) \n" +
           "MERGE (a)-[:GIVES_ARGUMENT]->(b)", userName=userName, argumentID=argumentID)

def add_gives_voteMap(tx, userName, votemapID):
    tx.run("MATCH (a:User {userID: $userName}) \n" +
           "MATCH (b:VoteMap {votemapID: $votemapID}) \n" +
           "MERGE (a)-[:GIVES_VOTEMAP]->(b)", userName=userName, votemapID=votemapID)

def add_user_timeline(tx):
    tx.run(''' insert ''')


### Debate Edges ###

def add_has_comment(tx, debateName, commentID):
    tx.run("MATCH (a:Debate {debateID: $debateName}) \n" +
           "MATCH (b:Comment {commentID: $commentID}) \n" +
           "MERGE (a)-[:HAS_COMMENT]->(b)", debateName=debateName, commentID=commentID)

def add_has_voteMap(tx, debateName, votemapID):
    tx.run("MATCH (a:Debate {debateID: $debateName}) \n" +
           "MATCH (b:VoteMap {votemapID: $votemapID}) \n" +
           "MERGE (a)-[:HAS_VOTEMAP]->(b)", debateName=debateName, votemapID=votemapID)

def add_has_round(tx, debateName, argumentID):
    tx.run("MATCH (a:Debate {debateID: $debateName}) \n" +
           "MATCH (b:Argument {argumentID: $argumentID}) \n" +
           "MERGE (a)-[:HAS_ROUND]->(b)", debateName=debateName, argumentID=argumentID)

def add_debate_timeline(tx):
    tx.run( ''' insert ''')


### Comment Edges ###

def add_comment_timeline(tx):
    tx.run( ''' insert ''')


### VoteMap Edges ###

def add_refers_to(tx, votemapID, userID):
    tx.run("MATCH (a:VoteMap {votemapID: $votemapID}) \n" +
           "MATCH (b:User {userID: $userID}) \n" +
           "MERGE (a)-[:REFERS_TO]->(b)", votemapID=votemapID, userID=userID)


### Miscellaneous ###

def delete_all(tx):
    tx.run("MATCH (n) DETACH DELETE n")


####################################
### Functions: Read Transactions ###
####################################

### Nodes ###

def read_user(tx):
    result = tx.run("MATCH (n:User) \n" +
           "RETURN n.userID, n.birthday, n.last_online, n.interested,n.income")
    for record in result:
        print(record["n.userID"])

def read_debate(tx):
    result = tx.run("MATCH (n:Debate) \n" +
           "RETURN n.debateID, n.url, n.category, n.title")
    for record in result:
        print(record["n.debateID"])

def read_argument(tx):
    result = tx.run("MATCH (n:Argument) \n" +
           "RETURN n.argumentID, n.content")
    for record in result:
        print(record["n.argumentID"], record['n.content'])

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



### User Edges ###

def read_friends_with(tx):
    result = tx.run("MATCH (a:User)-[:FRIENDS_WITH]->(b:User) RETURN a.userID, b.userID")
    for record in result:
        print("{} nominated {}".format(record["a.userID"], record["b.userID"]))

def read_debates_in(tx):
    result = tx.run("MATCH (a:User)-[rel:DEBATES_IN]->(b:Debate) RETURN a.userID, b.debateID, rel.forfeit ,rel.winning, rel.position")
    for record in result:
        print("{} debated in {} and has ff-value {}".format(record["a.userID"], record["b.debateID"], record["rel.forfeit"]))

def read_gives_comment(tx):
    result = tx.run("MATCH (a:User)-[rel:GIVES_COMMENT]->(b:Comment) RETURN a.userID, b.commentID, b.content")
    for record in result:
        print("{} gives comment {} with content {}".format(record["a.userID"], record["b.commentID"], record["b.content"]))
        #print(record)

def read_gives_argument(tx):
    result = tx.run("MATCH (a:User)-[:GIVES_ARGUMENT]->(b:Argument) RETURN a.userID, b.argumentID, b.content")
    for record in result:
        print("{} has argued in {} with content {}".format(record["a.userID"], record["b.argumentID"], record["b.content"]))

def read_gives_voteMap(tx):
    result = tx.run(''' inster ''')

def read_user_timeline(tx):
    result = tx.run(''' inster ''')


### Debate Edges ###

def read_has_comment(tx):
    result = tx.run("MATCH (a:Debate)-[rel:HAS_COMMENT]->(b:Comment) RETURN a.debateID, b.commentID, b.content")
    for record in result:
        print("{} has comment {} with content {}".format(record["a.debateID"], record["b.commentID"], record["b.content"]))

def read_has_voteMap(tx):
    result = tx.run(''' insert ''')

def read_has_round(tx):
    result = tx.run("MATCH (a:Debate)-[:ROUND]->(b:Argument) RETURN a.debateID, b.argumentID, b.content")
    for record in result:
        print("{} has argument {} with content {}".format(record["a.debateID"], record["b.argumentID"], record["b.content"]))

def read_debate_timeline(tx):
    result = tx.run(''' insert ''')


### Comment Edges ###

def read_comment_timeline(tx):
    result = tx.run(''' inster ''')


### VoteMap Edges ###

def read_refers_to(tx):
    result = tx.run("MATCH (a:VoteMap)-[:REFERS_TO]->(b:User) RETURN a.votemapID, b.userID")
    for record in result:
        print("{} with {} points refers to {}".format(record["a.votemapID"], record["b.userID"]))


### Miscellaneous ###

def read_all(tx):
    tx.run("MATCH (n) RETURN n")


########################
### Sessions - write ###
########################

with driver.session() as session:

    ###---------------###
    ### Miscellaneous ###
    ###---------------###

    ### Cleaning ###

    session.write_transaction(delete_all)


    ###-------###
    ### Nodes ###
    ###-------###

    ### User Node ###
    if user_bool == True:

        userList = []
        c = 0
        for i in users_data:
            c = c + 1
            userList.append(i)
            session.write_transaction(add_user, i, users_data[i]['birthday'], users_data[i]['description'], users_data[i]['education'],
                                      users_data[i]['elo_ranking'], users_data[i]['email'], users_data[i]['ethnicity'], users_data[i]['gender'],
                                      users_data[i]['interested'], users_data[i]['income'], users_data[i]['joined'], users_data[i]['last_online'], users_data[i]['last_updated'],
                                      users_data[i]['looking'], users_data[i]['party'], users_data[i]['political_ideology'], users_data[i]['president'],
                                      users_data[i]['relationship'], users_data[i]['religious_ideology'], users_data[i]['url'], users_data[i]['win_ratio'])
            if c % 100 == 0:
                print(c)
            if c >= sample:
                break
        print("-- user nodes done --")


    ### Debate Node ###
    if debate_bool == True:

        c = 0
        for i in debates_data:
            c = c + 1
            session.write_transaction(add_debate, i, debates_data[i]['url'], debates_data[i]['category'], debates_data[i]['title'])
            if c % 100 == 0:
                print(c)
            if c >= sample:
                break
        print("-- debate nodes done --")

    ### Comment Nodes ###
    if comment_bool == True:

        c = 0
        for i in debates_data:
            c = c + 1
            c2 = 0
            for k in debates_data[i]['comments']:
                c2 = c2 + 1
                commentID = str(str(i) + '_Comment_' + str(c2))
                session.write_transaction(add_comment, commentID, k['comment_text'])
            if c % 100 == 0:
                print(c)
            if c >= sample:
                break
        print("-- comment nodes done --")


    ### Argument Nodes ###
    if argument_bool == True:

        c = 0
        for i in debates_data:
            c = c + 1
            c2 = 0
            for k in debates_data[i]['rounds']:
                c2 = c2 + 1
                for p in k:
                    argumentID = str(str(i) + "_round_" + str(c2) + "_"+ str(p['side']))
                    session.write_transaction(add_argument, argumentID, p['text'])
            if c % 100 == 0:
                print(c)
            if c >= sample:
                break
        print("-- argument nodes done --")


    ### VoteMap Nodes ###
    if votemap_bool == True:

        c = 0
        for i in debates_data:
            c = c + 1
            c2 = 0
            for k in debates_data[i]['votes']:
                c2 = c2 + 1
                c3 = 0
                for p in k['votes_map']:
                    if c3 == 2:                               # VoteMaps consist of 3 parts. Bools of votes given to participant1, to participant2 and a redundant part 3 called tied with the same variables that are simply the first two variables connected with an logic AND
                        break
                    votemapID = str(str(i) + '_' + str(k['user_name']) + '_' + str(p))
                    if 'Agreed with before the debate' in k['votes_map'][p]:
                        session.write_transaction(add_voteMap_extended, votemapID, k['votes_map'][p]['Agreed with before the debate'], k['votes_map'][p]['Agreed with after the debate'],
                                              k['votes_map'][p]['Who had better conduct'],k['votes_map'][p]['Had better spelling and grammar'],k['votes_map'][p]['Made more convincing arguments'],
                                              k['votes_map'][p]['Used the most reliable sources'],k['votes_map'][p]['Total points awarded']) # "Total points awarded" kinda redundant
                    else:
                        session.write_transaction(add_voteMap_reduced, votemapID, k['votes_map'][p]['Who won the debate'])
                    c3 = c3 + 1
            if c % 100 == 0:
                print(c)
            if c >= sample:
                break
        print("-- voteMap nodes done --")

    print("-- Nodes done --")


    ###------------###
    ### User Edges ###
    ###------------###

    ### User Edge - friends_with ###
    if friends_with_bool == True:

        c = 0
        for i in users_data:
            c = c + 1
            if (users_data[i]['friends'] != []):
                if (users_data[i]['friends'] != "private"):                         #todo represent them in the database as node feature friendship: private
                    for k in users_data[i]['friends']:
                        if k in userList:
                            session.write_transaction(add_friends_with, i, k)
            if c % 100 == 0:
                print(c)
            if c >= sample:
                break
        print("-- user edges - friends_with done --")


    ### User Edges - debates_in ###
    if debates_in_bool == True:

        c = 0
        for i in debates_data:
            c = c + 1
            forfeit_bool1 = False
            winning_bool1 = False
            forfeit_bool2 = False
            winning_bool2 = False

            if debates_data[i]['participant_1_name'] in userList:
                if debates_data[i]['forfeit_side'] == debates_data[i]['participant_1_name']:
                    forfeit_bool1 = True
                if debates_data[i]['participant_1_status'] == "Winning":
                    winning_bool1 = True
                session.write_transaction(add_debates_in, debates_data[i]['participant_1_name'], i, forfeit_bool1, winning_bool1, debates_data[i]['participant_1_position'])     #todo check if there is inconsistency in participants and user.json

            if debates_data[i]['participant_2_name'] in userList:
                if debates_data[i]['forfeit_side'] == debates_data[i]['participant_2_name']:
                    forfeit_bool2 = True
                if debates_data[i]['participant_2_status'] == "Winning":
                    winning_bool2 = True
                session.write_transaction(add_debates_in, debates_data[i]['participant_2_name'], i, forfeit_bool2, winning_bool2, debates_data[i]['participant_2_position'])     #todo check if there is inconsistency in participants and user.json

            if c % 100 == 0:
                print(c)
            if c >= sample:
                break
        print("-- user edges - debates_in done --")


    ### User Edge - gives_comment ###
    if gives_comment_bool == True:

        c = 0
        for i in debates_data:
            c = c + 1
            c2 = 0
            for k in debates_data[i]['comments']:
                c2 = c2 + 1
                commentID = str(str(i) + '_Comment_' + str(c2))
                session.write_transaction(add_gives_comment, k['user_name'], commentID)
            if c % 100 == 0:
                print(c)
            if c >= sample:
                break
        print("-- user edge - gives_comment done --")


    ### User Edge - gives_argument ###
    if gives_argument_bool == True:

        c = 0
        for i in debates_data:
            c = c + 1
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
            if c % 100 == 0:
                print(c)
            if c >= sample:
                break
        print("-- user edge - gives_argument done --")


    ### User Edge - gives_voteMap ###
    #if gives_votemap_bool == True:

        ''' insert '''


    ### User Edge - user_timeline ###
    #if user_timeline_bool == True:

        ''' insert '''


    ###--------------###
    ### Debate Edges ###
    ###--------------###

    ### Debate Edge - has_comment ###
    if has_comment_bool == True:

        c = 0
        for i in debates_data:
            c = c + 1
            c2 = 0
            for k in debates_data[i]['comments']:
                c2 = c2 + 1
                commentID = str(str(i) + '_Comment_' + str(c2))
                session.write_transaction(add_has_comment, i, commentID)
            if c % 100 == 0:
                print(c)
            if c >= sample:
                break
        print("-- debate edge - has_comment done --")


    ### Debate Edge - has_round ###
    #if has_votemap_bool == True:
        ''' insert '''


    ### Debate Edge - has_round ###
    if has_round_bool == True:

        c = 0
        for i in debates_data:
            c = c + 1
            c2 = 0
            for k in debates_data[i]['rounds']:
                c2 = c2 + 1
                for p in k:
                    UserID = ""
                    argumentID = str(str(i) + "_round_" + str(c2) + "_" + str(p['side']))
                    session.write_transaction(add_has_round, i, argumentID)
            if c % 100 == 0:
                print(c)
            if c >= sample:
                break
        print("-- debate edge - has_round done --")


    ### Debate Edge - debate_timeline ###
    #if debate_timeline_bool == True:

        ''' insert '''


    ###---------------###
    ### Comment Edges ###
    ###---------------###

    ### Comment Edge - comment_timeline ###
    #if comment_timeline_bool == True:

        ''' insert '''


    ###---------------###
    ### VoteMap Edges ###
    ###---------------###

    ### VoteMap Edge - refers_to ###
    if refers_to_bool == True:

        c = 0
        for i in debates_data:
            c = c + 1
            c2 = 0
            for k in debates_data[i]['votes']:
                c2 = c2 + 1
                c3 = 0
                for p in k['votes_map']:
                    if c3 == 2:                               # VoteMaps consist of 3 parts. Bools of votes given to participant1, to participant2 and a redundant part 3 called tied with the same variables that are simply the first two variables connected with an logic AND
                        break
                    votemapID = str(str(i) + '_' + str(k['user_name']) + '_' + str(p))
                    #print(votemapID, p)
                    session.write_transaction(add_refers_to, votemapID, p)
                    c3 = c3 + 1
            if c % 100 == 0:
                print(c)
            if c >= sample:
                break
        print("-- votemap edge - refers_to done --")



    print("-- write done --")

#######################
### Sessions - read ###
#######################

    #session.read_transaction(read_all)

    #session.read_transaction(read_user)                         # ok
    #session.read_transaction(read_debate)                       # ok
    #session.read_transaction(read_comment)                     # ok
    #session.read_transaction(read_argument)                    # ok
    session.read_transaction(read_voteMap)                     # todo

    #session.read_transaction(read_friends_with)                # ok
    #session.read_transaction(read_debates_in)                  # ok
    #session.read_transaction(read_gives_comment)               # ok i think
    #session.read_transaction(read_gives_argument)              # ok
    #session.read_transaction(read_gives_voteMap)               # todo
    #session.read_transaction(read_user_timeline)               # todo

    #session.read_transaction(read_has_comment)                 # ok
    #session.read_transaction(read_has_voteMap)                 # todo
    #session.read_transaction(read_has_round)                   # todo
    #session.read_transaction(read_debate_timeline)             # todo

    #session.read_transaction(read_comment_timeline)            # todo
    #session.read_transaction(read_refers_to)                   # todo

    print("-- read done --")
