from django.shortcuts import render
from makeDB.views import getCompletedContests
from makeDB.models import User, Score
import json, requests, operator

def helperFunc1(listL, user):
    for contest in listL:
        if contest not in user.scoreMap:
            user.orderList.append(0)
        else:
            user.orderList.append(user.scoreMap[contest])

def index(request, period):
    contestList = getCompletedContests()
    year, sem = period[:2], period[2:]
    start = (int(year) - 14) * 12
    if sem == "O":
        start = start + 6
    users = {}
    points = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
    longs, cooks, ltimes = [], [], []
    for i in range(max(0,start * 3), min(len(contestList), (start * 3) + 15)):
        contestType = -1
        if "COOK" in contestList[i]:
            contestType = 1
            cooks.append(contestList[i])
        elif "LTIME" in contestList[i]:
            contestType = 2
            ltimes.append(contestList[i])
        else:
            contestType = 0
            longs.append(contestList[i])
        for j in points:
            try:
                user = Score.objects.get(points=j, contest=contestList[i]).user_set.all()[0].userName
            except Exception:
                continue
            if user not in users:
                users[user] = ResPer(user)
            users[user].addScore(contestList[i], j, contestType)
    allUsers = []
    for x in users.keys():
        for listX in [longs, cooks, ltimes]:
            helperFunc1(listX, users[x])
        allUsers.append(users[x])
    allUsers.sort(key=operator.attrgetter("score"), reverse=True)
    counter, rank, prev = 1, 1, 0
    for x in allUsers:
        if x.score == prev:
            x.rank = rank
        else:
            x.rank = counter
            rank = counter
        prev = x.score
        counter = counter + 1
    context = {
        'long': longs,
        'cook': cooks,
        'ltime': ltimes,
        'sorted_ranks': allUsers,
    }
    return render(request, 'showTables/index.html', context)

class ResPer:
    def __init__(self, uID):
        self.userName = uID
        self.score = 0
        self.scoreMap = {}
        self.orderList = []
        self.rank = -1
        self.diffRanks = [0, 0, 0]

    def addScore(self, cID, s, t):
        self.score = self.score + s
        self.diffRanks[t] = self.diffRanks[t] + s
        self.scoreMap[cID] = s

