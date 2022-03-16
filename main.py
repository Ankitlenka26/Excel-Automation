from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from readExcel import inputMainFunc
from writeExcel import outputMainFunc
result = inputMainFunc()
gameIds = result[0]
noOfGamesPerBoot = result[1]
bootPrice = result[2]
bootDurations = result[3]
# to find next empty slots


def findNextEmptySlot(currentGameArray, j, gameSum):
    for i in range(j, gameSum):
        if(currentGameArray[i] == -1):
            return i
    return -1

# to find the position of gameIds


def findGameArray(tempArray, gameSum):
    currentGameArray = [-1 for i in range(gameSum)]
    for i in range(len(tempArray)):
        currentIntegerPart = 0
        currentFractionalPart = 0.0
        prevFractionalPart = 0.0
        j = 0
        while(j < gameSum):
            currentIntegerPart = int(tempArray[i][2] + prevFractionalPart)
            currentFractionalPart = float("{:.5f}".format(
                (tempArray[i][2] + prevFractionalPart) - int(tempArray[i][2] + prevFractionalPart)))
            if(currentGameArray[j] == -1):
                if(tempArray[i][0] > 0):
                    currentGameArray[j] = tempArray[i][1]
                    tempArray[i][0] -= 1
                else:
                    break
                j += currentIntegerPart
            else:
                ne = findNextEmptySlot(currentGameArray, j, gameSum)
                if(tempArray[i][0] > 0):
                    currentGameArray[ne] = tempArray[i][1]
                    tempArray[i][0] -= 1
                else:
                    break
                if(ne == -1):
                    break
                else:
                    j = ne+currentIntegerPart
            prevFractionalPart = currentFractionalPart

        # print(currentGameArray)

    for i in range(len(tempArray)):
        if(tempArray[i][0] <= 0):
            continue
        for j in range(gameSum):
            if(currentGameArray[j] == -1 and tempArray[i][0] != 0):
                currentGameArray[j] = tempArray[i][1]
                tempArray[i][0] -= 1

    return currentGameArray

# to find all gameIds


def makeGameIdArray(gameArray, noOfGameIds, bootNo, noOfGamesSum):
    tempArray = []  # to store no of games for a particular boot , game_id , totalgames/noofgames of that boot
    for i in range(noOfGameIds):
        tempArray.append([gameArray[i][bootNo], i, float(
            "{:.5f}".format(noOfGamesSum/gameArray[i][bootNo]))])
    tempArray.sort(reverse=True)
    print(tempArray)
    return findGameArray(tempArray, noOfGamesSum)


noOfGameIds = len(gameIds)
noOfBoots = len(bootDurations)

noOfGames = [0 for i in range(noOfBoots)]
firstWaitingTimeGames = [0 for i in range(noOfBoots)]
secondWaitingTimeGames = [0 for i in range(noOfBoots)]
waitingTime = [0 for i in range(noOfBoots)]
noOfMinutes = 1440
firstToSecond = [0 for i in range(noOfBoots)]
for i in range(len(noOfGamesPerBoot)):
    for j in range(len(noOfGamesPerBoot[i])):
        noOfGames[j] += noOfGamesPerBoot[i][j]
# print(noOfGames)
waitTimeArray = [[0, 0] for i in range(noOfBoots)]
for i in range(noOfBoots):
    waitTimeArray[i][0] = (1440//noOfGames[i])  # average minutes
    waitTimeArray[i][1] = int(
        (1440.0/noOfGames[i] - waitTimeArray[i][0])*60)  # average seconds

print(waitTimeArray)
sumOfGamesEachBoot = [0 for i in range(noOfBoots)]
for i in range(noOfBoots):
    for j in range(noOfGameIds):
        sumOfGamesEachBoot[i] += noOfGamesPerBoot[j][i]

print(sumOfGamesEachBoot)

finalGameArray = []
for i in range(noOfBoots):  # to change
    finalGameArray.append(makeGameIdArray(
        noOfGamesPerBoot, noOfGameIds, i, sumOfGamesEachBoot[i]))

for i in range(len(finalGameArray)):
    print(finalGameArray[i])

# datetime object containing current date and time
dt = date.today()
time_zero = datetime.combine(
    dt, datetime.min.time()) + relativedelta(minutes=0)
print(time_zero)
finalData = [[] for i in range(noOfBoots)]
for i in range(noOfBoots):
    currentBootTimeStart = datetime.combine(
        dt, datetime.min.time())
    timeReqdInMinutes = bootDurations[i]
    prevMatchStartTime = datetime.combine(
        dt, datetime.min.time()) + relativedelta(minutes=0)
    for j in range(noOfGames[i]):
        currentData = []
        currentData.append(bootPrice[i])
        if(j == 0):
            waitTime = relativedelta(minutes=0, seconds=0)
        else:
            waitTime = relativedelta(
                minutes=waitTimeArray[i][0], seconds=waitTimeArray[i][1])
        matchStartTime = (currentBootTimeStart-time_zero +
                          prevMatchStartTime) + waitTime
        matchEndTime = matchStartTime+relativedelta(minutes=timeReqdInMinutes)
        mst = matchStartTime.strftime("%Y-%m-%d %I:%M:%S %p")
        met = matchEndTime.strftime("%Y-%m-%d %I:%M:%S %p")
        currentData.append(mst)
        currentData.append(met)
        currentData.append(gameIds[finalGameArray[i][j]])
        prevMatchStartTime = matchStartTime
        # print(currentData)
        finalData[i].append(currentData)

outputMainFunc(finalData, noOfBoots, noOfGames)
