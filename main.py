from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from readExcel import gameIds, noOfGamesPerBoot, bootDurations

# to find next empty slot


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
        # print(noOfGamesPerBoot[i][j])
        noOfGames[j] += noOfGamesPerBoot[i][j]
# print(noOfGames)

for i in range(len(noOfGames)):
    waitingTime[i] = 1440.0/noOfGames[i]
# print(waitingTime)

for i in range(len(noOfGames)):
    fraction = waitingTime[i] - int(waitingTime[i])
    fraction = float("{:.5f}".format(fraction))
    ratio = (1-fraction)/fraction
    firstWaitingTimeGames[i] = (int)(noOfGames[i]*(ratio)/(ratio+1))
    secondWaitingTimeGames[i] = noOfGames[i] - firstWaitingTimeGames[i]
    firstToSecond[i] = firstWaitingTimeGames[i]/secondWaitingTimeGames[i]
# print(firstWaitingTimeGames)
# print(secondWaitingTimeGames)
# print(firstToSecond)

waitTimeArray = [[], [], [], [], [], []]
for i in range(len(noOfGamesPerBoot[0])):
    j = 0
    fracSum = 0.0
    while j < noOfGames[i]:
        if(firstToSecond[i] >= 1):
            for k in range(int(firstToSecond[i])):
                j += 1
                waitTimeArray[i].append(int(waitingTime[i]))
            fracSum += firstToSecond[i] - int(firstToSecond[i])
            if(fracSum > 1):
                j += 1
                if(j > noOfGames[i]):
                    break
                waitTimeArray[i].append(int(waitingTime[i]))
                fracSum -= 1
            j += 1
            if(j > noOfGames[i]):
                break
            waitTimeArray[i].append(int(waitingTime[i])+1)
    print(waitTimeArray[i])
    print(len(waitTimeArray[i]))
sum = []
for i in range(noOfBoots):
    temp = 0
    for j in range(len(waitTimeArray[i])):
        temp += waitTimeArray[i][j]
    sum.append(temp)
print(sum)
# # now we have to distribute all gameIds evenly throughout the day
# # for every boot we will distribute the gameIds evenly
# gameIdArray = [[] , [] , [] , [] , [] , []]
# for i in range(len(gameIdArray)):
#     integerGames = []
#     fractionalGames = []
#     for j in range(len(gameNBoots)):
#         if(j==0) :
#             integerGames.append(1)
#             fractionalGames.append(0.0)
#         else :
#             integerGames.append(int(gameNBoots[j][i]/gameNBoots[0][i]))
#             fractionalGames.append(float(gameNBoots[j][i]/gameNBoots[0][i]) - int(gameNBoots[j][i]/gameNBoots[0][i]))
#     idx = 0
#     tempFractional = [0.0 , 0.0 , 0.0];
#     # print(integerGames)
#     # print(fractionalGames)
#     for count in range(gameNBoots[0][i]):
#         for k in range(len(integerGames)):
#             currentCount = integerGames[k]
#             tempFractional[k] += fractionalGames[k]
#             while(currentCount):
#                 gameIdArray[i].append(k)
#                 currentCount -= 1
#         for k in range(len(fractionalGames)):
#             if(tempFractional[k] >= 1):
#                 gameIdArray[i].append(k)
#                 tempFractional[k] -= 1
#     print(gameIdArray[i])


# function to evenly distribute the games

# def fillingIndices(bootNo, gameNBoots):
#     gameArray = []
#     sumOfGames = 0
#     for i in range(len(gameNBoots)):
#         sumOfGames += gameNBoots[i][bootNo]

#     for i in range(len(gameNBoots)):

#     return gameArray


# def puttingWaitTimeAndGameTogether(waitTimeArray , gameIdArray) :
#     return {}

# gamesArray = []
# for i in range(len(waitTimeArray)):
#     gamesArray.append(fillingIndices(i ,gameNBoots))

# finalData = puttingWaitTimeAndGameTogether(waitTimeArray , gamesArray)
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
        currentData.append(i)
        if(j == 0):
            waitTime = relativedelta(minutes=0)
        else:
            waitTime = relativedelta(minutes=waitTimeArray[i][j])
            # print(waitTime)
        matchStartTime = (currentBootTimeStart-time_zero +
                          prevMatchStartTime) + waitTime
        matchEndTime = matchStartTime+relativedelta(minutes=timeReqdInMinutes)
        mst = matchStartTime.strftime("%Y-%m-%d, %H:%M:%S")
        met = matchEndTime.strftime("%Y-%m-%d, %H:%M:%S")
        currentData.append(mst)
        currentData.append(met)
        currentData.append(finalGameArray[i][j])
        prevMatchStartTime = matchStartTime
        print(currentData)
        finalData[i].append(currentData)

# print(finalData)
for i in range(noOfBoots):
    print(len(finalData[i]))
