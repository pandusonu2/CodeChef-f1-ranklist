from django.shortcuts import render
from makeDB.views import getCompletedContests
from makeDB.models import User, Score
import json, requests, operator

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
        for j in points:
            try:
                user = Score.objects.get(points=j, contest=contestList[i]).user_set.all()[0].userName
            except Exception:
                continue
            if user not in users:
                users[user] = ResPer(user)
            users[user].addScore(contestList[i], j)
        if "COOK" in contestList[i]:
            cooks.append(contestList[i])
        elif "LTIME" in contestList[i]:
            ltimes.append(contestList[i])
        else:
            longs.append(contestList[i])
    allUsers = []
    for x in users.keys():
        for y in longs:
            if y not in users[x].scoreMap:
                users[x].orderList.append(0)
            else:
                users[x].orderList.append(users[x].scoreMap[y])
        for y in cooks:
            if y not in users[x].scoreMap:
                users[x].orderList.append(0)
            else:
                users[x].orderList.append(users[x].scoreMap[y])
        for y in ltimes:
            if y not in users[x].scoreMap:
                users[x].orderList.append(0)
            else:
                users[x].orderList.append(users[x].scoreMap[y])
        allUsers.append(users[x])
    allUsers.sort(key=operator.attrgetter("score"), reverse=True)
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

    def addScore(self, cID, s):
        self.score = self.score + s
        self.scoreMap[cID] = s
    
