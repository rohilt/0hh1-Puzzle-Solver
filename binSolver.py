from matplotlib import pyplot as plt
import numpy as np
import pyautogui
from skimage import io
import time

startLoc = (550, 1350)

print("Welcome to the 0hh1 puzzle solver! \n")
size = int(input("What is the board size? "))
scaleFactor = int(1200/size)

def moveToPosition(i, j):
    pyautogui.moveTo(startLoc[1] + j*scaleFactor, startLoc[0] + i*scaleFactor)

def similarRowOrColumn(x, y):
    for i in range(size):
        if x.data[i] + y.data[i] == 5:
            return False
    return True

class RoC:
    def __init__(self, id):
        self.data = []
        self.id = id
        self.undetermined = size
    def append(self, x):
        self.data.append(x)

class Board:
    def __init__(self, size):
        self.board = []
        self.numLeft = 0
        self.columns = []
        self.rows = []
        self.compareColumns = []
        self.compareRows = []
    def similarRow(self, i1, i2):
        for j in range(size):
            if self.board[i1][j] + self.board[i2][j] == 5:
                return False
        return True
    def similarColumn(self, j1, j2):
        for i in range(size):
            if self.board[i][j1] + self.board[i][j2] == 5:
                return False
        return True
    def input(self, img):
        for i in range(size):
            temp = []
            for j in range(size):
                if (img[startLoc[0] + i*scaleFactor][startLoc[1] + j*scaleFactor] == [42, 42, 42]).all():
                    temp.append(1)
                    self.numLeft += 1
                elif (img[startLoc[0] + i*scaleFactor][startLoc[1] + j*scaleFactor] == [0, 0, 255]).all():
                    temp.append(2)
                elif (img[startLoc[0] + i*scaleFactor][startLoc[1] + j*scaleFactor] == [255, 0, 0]).all():
                    temp.append(3)
            self.board.append(temp)
        for i in range(size):
            red = 0
            blue = 0
            temp = RoC(i)
            countBlanks = 0
            for x in self.board[i]:
                temp.append(x)
                if x == 1:
                    countBlanks += 1
                if x == 2:
                    blue += 1
                elif x == 3:
                    red += 1
            self.rows.append([blue, red])
            temp.undetermined = countBlanks
            addedToExisting = False
            for x in self.compareRows:
                similar = True
                for y in x:
                    if not similarRowOrColumn(y, temp):
                        similar = False
                if similar:
                    x.append(temp)
                    addedToExisting = True
            if not addedToExisting:
                self.compareRows.append([temp])
        for j in range(size):
            red = 0
            blue = 0
            temp = RoC(j)
            countBlanks = 0
            for i in range(size):
                temp.append(self.board[i][j])
                if self.board[i][j] == 1:
                    countBlanks += 1
                if self.board[i][j] == 2:
                    blue += 1
                elif self.board[i][j] == 3:
                    red += 1
            self.columns.append([blue, red])
            temp.undetermined = countBlanks
            addedToExisting = False
            for x in self.compareColumns:
                similar = True
                for y in x:
                    if not similarRowOrColumn(y, temp):
                        similar = False
                if similar:
                    x.append(temp)
                    addedToExisting = True
            if not addedToExisting:
                self.compareColumns.append([temp])
    def markBlue(self, i, j):
        self.board[i][j] = 2
        moveToPosition(i, j)
        pyautogui.doubleClick()
        self.numLeft -= 1
        self.rows[i][0] += 1
        self.columns[j][0] += 1
        rowData = []
        rowUndetermined = 0
        columnData = []
        columnUndetermined = 0
        for x in self.compareRows:
            for y in x:
                if y.id == i:
                    y.data[j] = 2
                    rowData = y.data
                    rowUndetermined = y.undetermined - 1
            x = [y for y in x if not y.id == i]
        temp = RoC(i)
        temp.undetermined = rowUndetermined
        temp.data = rowData
        addedToExisting = False
        for x in self.compareRows:
            similar = True
            for y in x:
                if not similarRowOrColumn(y, temp):
                    similar = False
            if similar:
                x.append(temp)
                addedToExisting = True
        if not addedToExisting:
            self.compareRows.append([temp])

        for x in self.compareColumns:
            for y in x:
                if y.id == j:
                    y.data[i] = 2
                    columnData = y.data
                    columnUndetermined = y.undetermined - 1
            x = [y for y in x if not y.id == j]
        temp2 = RoC(j)
        temp2.undetermined = columnUndetermined
        temp2.data = columnData
        addedToExisting = False
        for x in self.compareColumns:
            similar = True
            for y in x:
                if not similarRowOrColumn(y, temp2):
                    similar = False
            if similar:
                x.append(temp2)
                addedToExisting = True
        if not addedToExisting:
            self.compareRows.append([temp2])

    def markRed(self, i, j):
        self.board[i][j] = 3
        moveToPosition(i, j)
        pyautogui.click()
        self.numLeft -= 1
        self.rows[i][1] += 1
        self.columns[j][1] += 1
        rowData = []
        rowUndetermined = 0
        columnData = []
        columnUndetermined = 0
        for x in self.compareRows:
            for y in x:
                if y.id == i:
                    y.data[j] = 3
                    rowData = y.data
                    rowUndetermined = y.undetermined - 1
            x = [y for y in x if not y.id == i]
        temp = RoC(i)
        temp.undetermined = rowUndetermined
        temp.data = rowData
        addedToExisting = False
        for x in self.compareRows:
            similar = True
            for y in x:
                if not similarRowOrColumn(y, temp):
                    similar = False
            if similar:
                x.append(temp)
                addedToExisting = True
        if not addedToExisting:
            self.compareRows.append([temp])

        for x in self.compareColumns:
            for y in x:
                if y.id == j:
                    y.data[i] = 3
                    columnData = y.data
                    columnUndetermined = y.undetermined - 1
            x = [y for y in x if not y.id == j]
        temp2 = RoC(j)
        temp2.undetermined = columnUndetermined
        temp2.data = columnData
        addedToExisting = False
        for x in self.compareColumns:
            similar = True
            for y in x:
                if not similarRowOrColumn(y, temp2):
                    similar = False
            if similar:
                x.append(temp2)
                addedToExisting = True
        if not addedToExisting:
            self.compareRows.append([temp2])
    def checkForThrees(self):
        swapsMade = True
        while swapsMade:
            swapsMade = False
            for i in range(size):
                for j in range(size):
                    if self.board[i][j] == 2:
                        if j+2 < size and j+2 >= 0:
                            if self.board[i][j+1] == 2 and self.board[i][j+2] == 1:
                                self.markRed(i, j+2)
                                swapsMade = True
                            elif self.board[i][j+1] == 1 and self.board[i][j+2] == 2:
                                self.markRed(i, j+1)
                                swapsMade = True
                        if j-2 < size and j-2 >= 0:
                            if self.board[i][j-1] == 2 and self.board[i][j-2] == 1:
                                self.markRed(i, j-2)
                                swapsMade = True
                            elif self.board[i][j-1] == 1 and self.board[i][j-2] == 2:
                                self.markRed(i, j-1)
                                swapsMade = True
                        if i+2 < size and i+2 >= 0:
                            if self.board[i+1][j] == 2 and self.board[i+2][j] == 1:
                                self.markRed(i+2, j)
                                swapsMade = True
                            elif self.board[i+1][j] == 1 and self.board[i+2][j] == 2:
                                self.markRed(i+1, j)
                                swapsMade = True
                        if i-2 < size and i-2 >= 0:
                            if self.board[i-1][j] == 2 and self.board[i-2][j] == 1:
                                self.markRed(i-2, j)
                                swapsMade = True
                            elif self.board[i-1][j] == 1 and self.board[i-2][j] == 2:
                                self.markRed(i-1, j)
                                swapsMade = True
                    elif self.board[i][j] == 3:
                        if j+2 < size and j+2 >= 0:
                            if self.board[i][j+1] == 3 and self.board[i][j+2] == 1:
                                self.markBlue(i, j+2)
                                swapsMade = True
                            elif self.board[i][j+1] == 1 and self.board[i][j+2] == 3:
                                self.markBlue(i, j+1)
                                swapsMade = True
                        if j-2 < size and j-2 >= 0:
                            if self.board[i][j-1] == 3 and self.board[i][j-2] == 1:
                                self.markBlue(i, j-2)
                                swapsMade = True
                            elif self.board[i][j-1] == 1 and self.board[i][j-2] == 3:
                                self.markBlue(i, j-1)
                                swapsMade = True
                        if i+2 < size and i+2 >= 0:
                            if self.board[i+1][j] == 3 and self.board[i+2][j] == 1:
                                self.markBlue(i+2, j)
                                swapsMade = True
                            elif self.board[i+1][j] == 1 and self.board[i+2][j] == 3:
                                self.markBlue(i+1, j)
                                swapsMade = True
                        if i-2 < size and i-2 >= 0:
                            if self.board[i-1][j] == 3 and self.board[i-2][j] == 1:
                                self.markBlue(i-2, j)
                                swapsMade = True
                            elif self.board[i-1][j] == 1 and self.board[i-2][j] == 3:
                                self.markBlue(i-1, j)
                                swapsMade = True
    def checkForDeterminedRowOrColumn(self):
        for x in range(len(self.rows)):
            if self.rows[x][0] == size/2:
                for j in range(size):
                    if self.board[x][j] == 1:
                        self.markRed(x, j)
            elif self.rows[x][1] == size/2:
                for j in range(size):
                    if self.board[x][j] == 1:
                        self.markBlue(x, j)
        for x in range(len(self.columns)):
            if self.columns[x][0] == size/2:
                for i in range(size):
                    if self.board[i][x] == 1:
                        self.markRed(i, x)
            elif self.columns[x][1] == size/2:
                for i in range(size):
                    if self.board[i][x] == 1:
                        self.markBlue(i, x)
    def checkForSimilarRowsOrColumns(self):
        almostCompleteRows = []
        completeRows = []
        for x in range(len(self.rows)):
            if self.rows[x][0] == size/2 and self.rows[x][1] == size/2:
                completeRows.append(x)
            elif self.rows[x][0] == (size/2 - 1) and self.rows[x][1] == (size/2 - 1):
                almostCompleteRows.append(x)
        for x in completeRows:
            for y in almostCompleteRows:
                if self.similarRow(x, y):
                    for j in range(size):
                        if self.board[y][j] == 1 and self.board[x][j] == 2:
                            self.markRed(y, j)
                        elif self.board[y][j] == 1 and self.board[x][j] == 3:
                            self.markBlue(y, j)
        almostCompleteColumns = []
        completeColumns = []
        for x in range(len(self.columns)):
            if self.columns[x][0] == size/2 and self.columns[x][1] == size/2:
                completeColumns.append(x)
            elif self.columns[x][0] == (size/2 - 1) and self.columns[x][1] == (size/2 - 1):
                almostCompleteColumns.append(x)
        for x in completeColumns:
            for y in almostCompleteColumns:
                if self.similarColumn(x, y):
                    for i in range(size):
                        if self.board[i][y] == 1 and self.board[i][x] == 2:
                            self.markRed(i, y)
                        elif self.board[i][y] == 1 and self.board[i][x] == 3:
                            self.markBlue(i, y)

    def solve(self):
        while board.numLeft > 0:
            initBoard = board.board
            self.checkForThrees()
            self.checkForDeterminedRowOrColumn()
            if initBoard == board.board:
                self.checkForSimilarRowsOrColumns()
            #self.checkForSimilarRowsOrColumns()
            # try checking for swaps by comparing board state, then if no swaps brute force check for similar rows/columns

print("\nStarting in 3 seconds...")
time.sleep(3)
pyautogui.screenshot('myScreenshot.png')
img = io.imread('myScreenshot.png')
#print(pyautogui.position())
red = img[:, :, 0] > 150
blue = img[:, :, 2] > 150
#dark = img[:, :, 2] > 100
img[red] = [255, 0, 0]
img[blue] = [0, 0, 255]

board = Board(size)
board.input(img)
board.solve()
#plt.imshow(img, interpolation = 'nearest')
#plt.show()