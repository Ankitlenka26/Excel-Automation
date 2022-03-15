import openpyxl

wb = openpyxl.load_workbook("testExcel.xlsx")

sheetObj = wb['Sheet1']
row = sheetObj.max_row
column = sheetObj.max_column
# print(row)
# print(column)
# 1st row -> contain all the info about which column contains what
# 2nd row -> n-1 row => no of games per gameId values
# nth row -> the duration of game in each boot
# 1st column except first row is gameIds
# indexing in excel starts from 1 and it starts from 0 in python
gameIds = [0 for i in range(row-2)]  # present in 1st column
noOfGamesPerBoot = [[0 for i in range(column-1)] for j in range(row-2)]
bootDurations = [0 for i in range(column-1)]
# populating the noOfGamesPerBoot matrix
for i in range(row-2):
    for j in range(column-1):
        noOfGamesPerBoot[i][j] = (sheetObj.cell(i+2, j+2).value)
# print(noOfGamesPerBoot)

# for adding gameIds
for i in range(row-2):
    gameIds[i] = sheetObj.cell(i+2, 1).value
# print(gameIds)

# for adding bootDurations
for i in range(column-1):
    bootDurations[i] = sheetObj.cell(row, i+2).value
