import operator
from collections import defaultdict
from app.models import *

w = Week.query.order_by(Week.date.asc()).first()
submissions = Submission.query.filter(Submission.week_id == w.id).all()

positions = len(submissions[0].rankings)
points = list(range(positions, 0, -1))
print(points)

teams = defaultdict(lambda: 0)

for submission in submissions:
    for ranking in submission.rankings:
        print("%s position %s, gets %s points" % (ranking.team.name,
                                               ranking.position,
                                               points[ranking.position-1]))
        teams[ranking.team.name] += points[ranking.position-1]


print(teams)

top_teams = sorted(teams.items(), key=operator.itemgetter(1), reverse=True)
print(top_teams)

for top_team in top_teams:
    print("%s: %s" % (top_team[0], top_team[1]))


rank = 1
rankings = {}
while rank < 11:
    ranked_teams = []
    pos = rank-1
    s = "rank: %s" % (str(rank))
    s += " %s" % top_teams[pos][0]
    ranked_teams.append(top_teams[pos][0])
    print("rank %s and %s" % (str(rank), top_teams[pos][0]))

    curr = 0
    while top_teams[pos][1] == top_teams[pos+1][1]:
        s += "\n\t %s" % top_teams[pos+1][0]
        ranked_teams.append(top_teams[pos+1][0])
        print ("rank %s include %s " % (str(rank), top_teams[pos+1][0]))
        pos += 1
        curr += 1

    rankings[rank] = ranked_teams
    if pos >= rank:
        # rank = ((pos + 1) - rank) + rank + 1
        rank = pos + 2
    else:
        rank += 1

    print(s)


from pprint import pprint
pprint(rankings)

#counter=0
#flag=False
#rank=1
##import pdb; pdb.set_trace()
#for i,item in enumerate(top_teams):
#    s = "position %s" % (rank)
#    s += " %s" % item[0]
#
#    while True:
#        counter = i
#        if counter < len(top_teams)-1:
#            if item[i] == top_teams[counter+1][1]:
#                s = s + " %s" % top_teams[i+1][1]
#                counter += 1
#                continue
#            else:
#                rank += 1
#                counter += 1
#                break
#
#    if flag:
#        flag = False
#        continue
#
#    print(s)
#
#    if counter > 9:
#        break
