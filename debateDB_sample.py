from neo4j import GraphDatabase
import json
import collections

######################
### Initialization ###
######################

f = open('D:/Universitaet Mannheim/MMDS 6. Semester/Individual Project/users.json', "r")
g = open('D:/Universitaet Mannheim/MMDS 6. Semester/Individual Project/debates.json', "r")

users_data = json.load(f)
debates_data = json.load(g)

driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "abc"))


############################################
### Functions: Write Transactions - Node ###
############################################

### User ###

def add_user(tx, userName):
    tx.run("MERGE (a:User {name: $userName})", userName=userName)

def add_user_extend(tx, userName, userBirth, userDescr, userEduc, userElo, userEmail, userEthni, userSex, userInterest, userInc,
                    userJoin, userOn, userUpd, userLook, userParty, userPoli, userPresi, userRels, userReli,
                    userURL, userWinR):
    tx.run("MERGE (a:User {name: $userName, birthday: $userBirth, description: $userDescr, education: $userEduc, elo_ranking: $userElo," +
                    "email: $userEmail, ethnicity: $userEthni, gender: $userSex, interested: $userInterest,income: $userInc, joined: $userJoin, last_online: $userOn," +
                    "last_updated: $userUpd, looking: $userLook, party: $userParty, political_ideology: $userPoli, president: $userPresi, relationship: $userRels," +
                    "religious_ideology: $userReli, url: $userURL, win_ratio: $userWinR})",
                    userName=userName, userBirth=userBirth, userDescr=userDescr, userEduc=userEduc, userElo=userElo, userEmail=userEmail,
                    userEthni=userEthni, userSex=userSex, userInterest=userInterest, userInc=userInc, userJoin=userJoin, userOn=userOn, userUpd=userUpd, userLook=userLook,
                    userParty=userParty, userPoli=userPoli, userPresi=userPresi, userRels=userRels, userReli=userReli, userURL=userURL,
                    userWinR=userWinR)


### Debate ###

def add_debate(tx, debateName, debateUrl, debateCategory, debateTitle):
    tx.run("MERGE (a:Debate {name: $debateName, url: $debateUrl, category: $debateCategory, title: $debateTitle})",
           debateName=debateName, debateUrl=debateUrl, debateCategory=debateCategory, debateTitle=debateTitle)


### COMMENT ###

def add_comment(tx, commentID, commentContent):
    tx.run("MERGE (a:Comment {name: $commentID, content: $commentContent})", commentID=commentID, commentContent=commentContent)


### CATEGORY ###

def add_category(tx, categoryName):
    tx.run("MERGE (a:Category {name: $categoryName})", categoryName=categoryName)


### VOTEMAP ###

def add_voteMap(tx, votemapID):
    tx.run("MERGE (a:VoteMap {name: $votemapID})", votemapID=votemapID)


### ARGUMENT ###

def add_argument(tx, argumentID, argumentContent):
    tx.run("MERGE (a:Argument {id: $argumentID, content: $argumentContent})", argumentID=argumentID, argumentContent=argumentContent)


############################################
### Functions: Write Transactions - Edge ###
############################################

#---------------
#---- USER -----
#---------------

### User-User ###

def add_friends_with(tx, userName, friendName):
    tx.run("MATCH (a:User {name: $userName}) \n" +
           "MATCH (b:User {name: $friendName}) \n" +
           "MERGE (a)-[:FRIENDS_WITH]->(b)", userName=userName, friendName=friendName)

### User-Debate ###

def add_debates_in(tx, userName, debateName, debateForfeit, debateWinning, debatePosition):
    tx.run("MATCH (a:User {name: $userName}) \n" +
           "MATCH (b:Debate {name: $debateName}) \n" +
           "MERGE (a)-[:DEBATES_IN {forfeit: $debateForfeit, winning: $debateWinning, position: $debatePosition }]->(b)",
           userName=userName, debateName=debateName, debateForfeit=debateForfeit, debateWinning=debateWinning, debatePosition=debatePosition)
    #print(userName, debateName, debateForfeit)

### User-Comment ###

def add_gives_comment(tx, userName, commentID):
    tx.run("MATCH (a:User {name: $userName}) \n" +
           "MATCH (b:Comment {name: $commentID}) \n" +
           "MERGE (a)-[:GIVES_COMMENT]->(b)", userName=userName, commentID=commentID)


'''### User-Category ###

def add_has_stance(tx, userName, categoryName):
    tx.run("MATCH (a:User {name: $userName}) \n" +
           "MATCH (b:Category {name: $categoryName}) \n" +
           "MERGE (a)-[:HAS_STANCE]->(b)", userName=userName, categoryName=categoryName) # pro/con
'''

### User-Argument ###

def add_gives_argument(tx, userName, argumentID):
    tx.run("MATCH (a:User {name: $userName}) \n" +
           "MATCH (b:Argument {name: $argumentID}) \n" +
           "MERGE (a)-[:GIVES_ARGUMENT]->(b)", userName=userName, argumentID=argumentID)


### User-VoteMap ###

def add_gives_voteMap(tx, userName, votemapID):
    tx.run("MATCH (a:User {name: $userName}) \n" +
           "MATCH (b:VoteMap {name: $votemapID}) \n" +
           "MERGE (a)-[:GIVES_VOTEMAP]->(b)", userName=userName, votemapID=votemapID)

#----------------
#---- DEBATE ----
#----------------

### Debate-Comment ###

def add_has_comment(tx, debateName, commentID):
    tx.run("MATCH (a:Debate {name: $debateName}) \n" +
           "MATCH (b:Comment {name: $commentID}) \n" +
           "MERGE (a)-[:HAS_COMMENT]->(b)", debateName=debateName, commentID=commentID)


### Debate-Category ###

def add_has_category(tx, debateName, categoryName):
    tx.run("MATCH (a:Debate {name: $debateName}) \n" +
           "MATCH (b:Category {name: $categoryName}) \n" +
           "MERGE (a)-[:HAS_CATEGORY]->(b)", debateName=debateName, categoryName=categoryName)


### Debate-VoteMap ###

def add_has_voteMap(tx, debateName, votemapID):
    tx.run("MATCH (a:Debate {name: $debateName}) \n" +
           "MATCH (b:VoteMap {name: $votemapID}) \n" +
           "MERGE (a)-[:HAS_VOTEMAP]->(b)", debateName=debateName, votemapID=votemapID)


### Debate-Argument ###

def add_round(tx, debateName, argumentID):
    tx.run("MATCH (a:Debate {name: $debateName}) \n" +
           "MATCH (b:Argument {name: $argumentID}) \n" +
           "MERGE (a)-[:ROUND]->(b)", debateName=debateName, argumentID=argumentID)


#-----------------
#---- VOTEMAP ----
#-----------------

### VoteMap-User ###

def add_receives_voteMap(tx, votemapID, userName):
    tx.run("MATCH (a:VoteMap {name: $votemapID}) \n" +
           "MATCH (b:User {name: $userName}) \n" +
           "MERGE (a)-[:RECEIVES_VOTEMAP]->(b)", votemapID=votemapID, userName=userName)


#----------------
#--- TIMELINE ---
#----------------

#- before
#- after

#def user_after(tx, )

#todo how to handle last online?  x years ago - right now. Extra entity "year" with before links & links to users/debates/comments?
#todo how to handle 2 debates being on the same day?


#-----------------------
#---- MISCELLANEOUS ----
#-----------------------

def delete_all(tx):
    tx.run("MATCH (n) DETACH DELETE n")


####################################
### Functions: Read Transactions ###
####################################
category_distri = []
interested_distri=[]

def return_all(tx):
    tx.run("MATCH (n) RETURN n")


def read_user(tx):
    result = tx.run("MATCH (n:User) \n" +
           "RETURN n.name, n.birthday, n.last_online, n.interested,n.income")
    for record in result:
        #print(record["n.interested"]) #, record['n.last_online'])
        #last_online_distri.append(record['n.last_online'])
        interested_distri.append(record['n.interested'])
        #income_distri.append(record['n.income'])
        print(record)


def read_debate(tx):
    result = tx.run("MATCH (n:Debate) \n" +
           "RETURN n.name, n.url, n.category, n.title")
    for record in result:
        print(record["n.category"])
        category_distri.append(record['n.category'])
        #print(record)


def read_debates_in(tx):
    result = tx.run("MATCH (a:User)-[rel:DEBATES_IN]->(b:Debate) RETURN a.name, b.name, rel.forfeit ,rel.winning, rel.position")
    for record in result:
        #print("{} debated in {} and has ff-value {}".format(record["a.name"], record["b.name"], record["rel.forfeit"], record["rel.winning"], record["rel.position"]))
        print("{} {} {}".format(record["rel.forfeit"], record["rel.winning"], record["rel.position"]))


def read_friendship(tx):
    result = tx.run("MATCH (a:User)-[:FRIENDS_WITH]->(b:User) RETURN a.name, b.name")
    for record in result:
        print("{} nominated {}".format(record["a.name"], record["b.name"]))
        #print('Here should be the friendships: ', record)

def read_gives_comment(tx):
    result = tx.run("MATCH (a:User)-[rel:GIVES_COMMENT]->(b:Comment) RETURN a.name, b.commentID, b.commentContent")
    for record in result:
        #print("{} gives comment {} with content {}".format(record["a.name"], record["b.commentID"], record["b.commentContent"]))
        print(record)

def read_has_comment(tx):
    result = tx.run("MATCH (a:Debate)-[rel:HAS_COMMENT]->(b:Comment) RETURN a.title, b.commentID, b.commentContent")
    for record in result:
        print("{} has comment {} with content {}".format(record["a.title"], record["b.commentID"], record["b.commentContent"]))
        #print(record)

def read_argument(tx):
    result = tx.run("MATCH (n:Argument) \n" +
           "RETURN n.id, n.content")
    for record in result:
        print(record["n.id"], record['n.content'])
        category_distri.append(record['n.category'])
        #print(record)

########################
### Sessions - write ###
########################

sample = 1


with driver.session() as session:

    ### cleaning ###

    session.write_transaction(delete_all)

    ### user nodes ###

    userList = []
    c = 0
    for i in users_data:
        c = c + 1
        userList.append(i)
        session.write_transaction(add_user_extend, i, users_data[i]['birthday'], users_data[i]['description'], users_data[i]['education'],
                                  users_data[i]['elo_ranking'], users_data[i]['email'], users_data[i]['ethnicity'], users_data[i]['gender'],
                                  users_data[i]['interested'], users_data[i]['income'], users_data[i]['joined'], users_data[i]['last_online'], users_data[i]['last_updated'],
                                  users_data[i]['looking'], users_data[i]['party'], users_data[i]['political_ideology'], users_data[i]['president'],
                                  users_data[i]['relationship'], users_data[i]['religious_ideology'], users_data[i]['url'], users_data[i]['win_ratio'])

        if c % 100 == 0:
            print(c)
        if c >= sample:
            break

    print("-- user nodes done --")

    ### user edges - friendship ###

    '''c = 0
    for i in users_data:
        c = c + 1

        if (users_data[i]['friends'] != []):
            if (users_data[i]['friends'] != "private"):                         #todo represent them in the database as node feature friendship: private
                for k in users_data[i]['friends']:
                    #print(i, "nominates", k)
                    #session.write_transaction(add_friends_with, i, k)

                    if k in userList:
                        session.write_transaction(add_friends_with, i, k)
                        #print(i, "nominates", k)

        if c % 100 == 0:
            print(c)
        if c >= sample:
            break

    print("-- user edges - friendship done --")'''

    ### debate nodes ###

    c = 0
    for i in debates_data:
        c = c + 1
        session.write_transaction(add_debate, i, debates_data[i]['url'], debates_data[i]['category'], debates_data[i]['title'])
        #print('debate: ', i)
        #print(debates_data[i])

        if c % 100 == 0:
            print(c)
        if c >= sample:
            break
    print("-- debate nodes done --")

    ### user edges - debates ###

    '''c = 0
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
            #print('PARTICIPANT 1 CHECK: ', debates_data[i]['participant_1_name'], i, forfeit_bool)

        if debates_data[i]['participant_2_name'] in userList:
            if debates_data[i]['forfeit_side'] == debates_data[i]['participant_2_name']:
                forfeit_bool2 = True

            if debates_data[i]['participant_2_status'] == "Winning":
                winning_bool2 = True

            session.write_transaction(add_debates_in, debates_data[i]['participant_2_name'], i, forfeit_bool2, winning_bool2, debates_data[i]['participant_2_position'])     #todo check if there is inconsistency in participants and user.json
            #print("PARTICIPANT 2 CHECK: ", debates_data[i]['participant_2_name'], i, forfeit_bool)

        if c % 100 == 0:
            print(c)
        if c >= sample:
            break

    print("-- user edges - debates_in done --")'''

    ### comment nodes ###

    c = 0
    for i in debates_data:
        c = c + 1
        c2 = 0
        for k in debates_data[i]['comments']:
            c2 = c2 + 1
            commentID = str(str(i) + '_Comment_' + str(c2))
            session.write_transaction(add_comment, commentID, k['comment_text'])
            #print(k)
            #print(k['comment_text'])


        if c % 100 == 0:
            print(c)
        if c >= sample:
            break
    print("-- comment nodes done --")

     ### user edge - gives_comment ###

    c = 0
    for i in debates_data:
        c = c + 1
        c2 = 0
        for k in debates_data[i]['comments']:
            c2 = c2 + 1
            commentID = str(str(i) + '_Comment_' + str(c2))
            session.write_transaction(add_gives_comment, k['user_name'], commentID)
            #print(k)
            #print(k['comment_text'])
        if c % 100 == 0:
            print(c)
        if c >= sample:
            break

    print("-- user edge - gives_comment done --")


    ### debate edge - has_comment ###

    c = 0
    for i in debates_data:
        c = c + 1
        c2 = 0
        for k in debates_data[i]['comments']:
            c2 = c2 + 1
            commentID = str(str(i) + '_Comment_' + str(c2))
            session.write_transaction(add_has_comment, i, commentID)
            #print(k)
            #print(k['comment_text'])
        if c % 100 == 0:
            print(c)
        if c >= sample:
            break

    print("-- debate edge - has_comment done --")


    ### argument nodes ###

    c = 0
    for i in debates_data:
        c = c + 1
        c2 = 0
        for k in debates_data[i]['rounds']:
            c2 = c2 + 1
            for p in k:
                argumentID = str(str(i) + "_round_" + str(c2) + "_"+ str(p['side']))
                #print(i, p['text'])
                #commentID = str(str(i) + '_Comment_' + str(c2))
                session.write_transaction(add_argument, argumentID, p['text'])
                #print(argumentID, p['text'])
                #print(k['comment_text'])


        if c % 100 == 0:
            print(c)
        if c >= 10:
            break
    print("-- comment nodes done --")

    print("-- write done --")


#######################
### Sessions - read ###
#######################

    #session.read_transaction(read_user)
    #session.read_transaction(read_friendship)
    #session.read_transaction(read_debate)
    #session.read_transaction(read_debates_in)
    #session.read_transaction(read_gives_comment)
    #session.read_transaction(read_has_comment)
    session.read_transaction(read_has_comment)

    print("-- read done --")


###############
### Closing ###
###############


driver.close()
f.close()

#print(interested_distri)
#counter = collections.Counter(category_distri)
#print(counter)

print("-- all done --")
#print(people)






#todo do we take url? Its just the universal + username