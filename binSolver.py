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


class Board:
    def __init__(self, size):
        self.board = []
        self.numLeft = 0
        self.columns = []
        self.rows = []
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
            for x in self.board[i]:
                if x == 2:
                    blue += 1
                elif x == 3:
                    red += 1
            self.rows.append([blue, red])
        for j in range(size):
            red = 0
            blue = 0
            for i in range(size):
                if self.board[i][j] == 2:
                    blue += 1
                elif self.board[i][j] == 3:
                    red += 1
            self.columns.append([blue, red])
    def markBlue(self, i, j):
        self.board[i][j] = 2
        moveToPosition(i, j)
        pyautogui.doubleClick()
        self.numLeft -= 1
        self.rows[i][0] += 1
        self.columns[j][0] += 1
    def markRed(self, i, j):
        self.board[i][j] = 3
        moveToPosition(i, j)
        pyautogui.click()
        self.numLeft -= 1
        self.rows[i][1] += 1
        self.columns[j][1] += 1
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
    def solve(self):
        # while numLeft != 0
        while self.numLeft > 0:
            self.checkForThrees()
            self.checkForDeterminedRowOrColumn()

print("\nStarting in 2 seconds...")
time.sleep(2)
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