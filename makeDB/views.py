from django.db import models
from django.shortcuts import redirect
from .models import User, Score
import json, requests, re

def getCode(htmlLine):
    htmlLine = htmlLine.strip()
    htmlLine = htmlLine.replace("<td>", "")
    htmlLine = htmlLine.replace("</td>", "")
    return htmlLine

def check(cc):
    if re.match('COOK[0-9]{2}', cc):
        return True
    if re.match('LTIME[0-9]{2}', cc):
        return True
    monthList = ['JAN', 'FEB', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUG', 'SEPT', 'OCT', 'NOV', 'DEC']
    for i in monthList:
        if re.match(i + '[0-9]{2}', cc):
            return True
    return False

def getCompletedContests():
    li = requests.get(url="https://www.codechef.com/contests")
    li = li.text.split('\n')
    iterator = 0
    while("Past Contests" not in li[iterator]):
        iterator = iterator + 1
    while("<tbody>" not in li[iterator]):
        iterator = iterator + 1
    contestList = []
    print("Reached....")
    while("JAN14" not in li[iterator]):
        if "<tr>" in li[iterator]:
            cc = getCode(li[iterator + 1])
            if check(cc):
                contestList.append(cc)
        iterator = iterator + 1
    return contestList[::-1]

def getRanks(cc):
    college = "National Institute of Technology, Durgapur"
    jsons = requests.get(url="https://www.codechef.com/api/rankings/" + cc + "?sortBy=rank&order=asc&page=1&itemsPerPage=25&filterBy=Institution%3D" + college)
    jsons = jsons.json()
    ret = []
    for i in range(min(10, len(jsons["list"]))):
        ret.append(jsons["list"][i]["user_handle"])
    return ret

def createDB(request):
    completeContest = getCompletedContests()
    for i in completeContest:
        print("Processing " + i)
        if Score.objects.filter(contest=i).count() == 10:
            continue
        ranks = getRanks(i)
        score = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
        for j in range(min(10, len(ranks))):
            sc, created = Score.objects.get_or_create(
                contest = i,
                points = score[j],
            )
            if created == False:
                continue
            sc.save()
            obj, created = User.objects.get_or_create(
                userName = ranks[j],
            )
            obj.score.add(sc)
            obj.save()
    return redirect('/showTables/14E')
