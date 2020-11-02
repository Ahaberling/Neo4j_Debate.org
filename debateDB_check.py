from neo4j import GraphDatabase

driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "abc"))


####################################
### Functions: Read Transactions ###
####################################
# All Neo4j edges and nodes are read by accessing the database via these write functions

### Nodes ###

def read_user(tx):
    result = tx.run("MATCH (n:User) \n" +
           #"RETURN n.userID, n.birthday, n.last_online, n.income, n.interested, n.friend_privacy")
           #"RETURN keys(n)")
           "RETURN n")
    for record in result:
        print(record)
        '''print("userID: {} // birthday: {} // description: {} // education: {} // elo_ranking: {} // email: {} // ethnicity: {} // gender: {} // friend_privacy: {} // " +
              "income : {} // interested: {} // joined: {} // last_online: {} // last_updated: {} // looking: {} // party: {} // percentile: {} // political_ideology: {} // " +
              "president: {} // relationship: {} // religious_ideology: {} // url: {} // win_ratio: {} // number_all_deb: {} // number_lost_deb: {} // number_tied_deb: {} // " +
              "number_won_deb: {} // number_friends: {} // number_opinion_arg: {} // number_opinion_ques: {} // number_poll_topics: {} // number_poll_votes: {} // " +
              "number_voted_deb: {} ".format(record["n.userID"], record["n.birthday"], record["n.income"], record["n.interested"], record["n.friend_privacy"]
                                             , record["n.friend_privacy"], record["n.friend_privacy"], record["n.friend_privacy"], record["n.friend_privacy"]
                                             , record["n.friend_privacy"], record["n.friend_privacy"], record["n.friend_privacy"], record["n.friend_privacy"]
                                             , record["n.friend_privacy"], record["n.friend_privacy"], record["n.friend_privacy"], record["n.friend_privacy"]
                                             , record["n.friend_privacy"], record["n.friend_privacy"], record["n.friend_privacy"], record["n.friend_privacy"]
                                             , record["n.friend_privacy"], record["n.friend_privacy"], record["n.friend_privacy"], record["n.friend_privacy"]))'''



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
    #result = tx.run("MATCH (a:User)-[rel:DEBATES_IN]->(b:Debate) RETURN a.userID, b.debateID, rel.forfeit, rel.debatePoints, rel.position ,rel.winning")
    result = tx.run("MATCH (a:User)-[rel:DEBATES_IN]->(b:Debate) RETURN rel")
    for record in result:
        #print("{} debated in {} and has ff-value {} and points {}".format(record["a.userID"], record["b.debateID"], record["rel.forfeit"], record["rel.debatePoints"]))
        print(record)

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

# Alternative timeline approach
'''def read_user_timeline(tx):
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

# Alternative timeline approach
'''def read_debate_timeline(tx):
    result = tx.run("MATCH (a:Debate)-[:BEFORE]->(b:Debate) RETURN a.debateID, a.start , b.debateID, b.start")
    #print('read_debate_timeline is called')
    for record in result:
        print("{} with {} took place before {} with {}".format(record["a.debateID"], record["a.start"], record["b.debateID"], record["b.start"]))
'''

def read_debate_timeline(tx):
    result = tx.run("MATCH (a:Debate)-[:IN_TIMELINE]->(b:Timeline) RETURN a.debateID, a.start , b.year")
    for record in result:
        print("{} with {} is in Timeline {}".format(record["a.debateID"], record["a.start"], record["b.year"]))


### Comment Edges ###

# Alternative timeline approach
'''def read_comment_timeline(tx):
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



with driver.session() as session:


    #######################
    ### Sessions - read ###
    #######################

    # session.read_transaction(read_all)

    # session.read_transaction(read_user)                        # ok
    # session.read_transaction(read_debate)                      # ok
    # session.read_transaction(read_comment)                     # ok
    # session.read_transaction(read_argument)                    # ok
    # session.read_transaction(read_voteMap)                     # ok
    # session.read_transaction(read_opinion)                     # ok
    # session.read_transaction(read_poll)                        # ok
    # session.read_transaction(read_issues)                      # ok
    # session.read_transaction(read_timeline)                    # ok

    # session.read_transaction(read_friends_with)                # ok
     session.read_transaction(read_debates_in)                  # ok
    # session.read_transaction(read_gives_comment)               # ok
    # session.read_transaction(read_gives_argument)              # ok
    # session.read_transaction(read_gives_voteMap)               # ok
    # session.read_transaction(read_gives_opinion)               # ok
    # session.read_transaction(read_gives_pollvote)              # ok
    # session.read_transaction(read_gives_issues)                # ok
    # session.read_transaction(read_user_timeline)               # ok

    # session.read_transaction(read_has_comment)                 # ok
    # session.read_transaction(read_has_voteMap)                 # ok
    # session.read_transaction(read_has_argument)                # ok
    # session.read_transaction(read_debate_timeline)             # ok

    # session.read_transaction(read_comment_timeline)            # ok

    # session.read_transaction(read_refers_to)                   # ok

print("-- read done --")
