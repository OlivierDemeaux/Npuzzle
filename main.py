import re
import sys
import os.path
from os import path

"""
define class Node that wwill contain all our information about a specific node
"""
class Node:
    def __init__(self, board, hValue, state, parent, posOfZero):
        self.board = board
        self.hValue = hValue
        if (parent):
            self.gValue = parent.gValue + 1
        else:
            self.gValue = 0
        self.fValue = self.gValue + self.hValue
        self.state = state
        self.parent = parent
        self.posOfZero = posOfZero
        self.boardString = list(map(str, board))

def error(err):
    print(err)
    sys.exit()

def cleanContent(data):
    """
    Function to clean the input file of comments, empty lines and spaces
    """
    valid = []
    data = data.split('\n')
    for elem in data:
        elem = elem.split("#")[0].strip()
        if (len(elem) > 0):
            valid.append(elem.split(" "))
    return valid

def isInt(x):
    try:
        int(x)
        return True
    except:
        return False

def checkTotalNumber(data):
    """
    Check if there is the right total number of numbers
    """
    total = 0
    arrayNumbers = []
    nestedArray = []
    print(data)
    if (isInt(data[0][0]) == False):
        error('Please use numbers')
    boardSize = int(data[0][0])
    for line in data[1:]:
        currentLine = []
        for number in line:
            if (isInt(number)):
                currentLine.append(int(number))
                arrayNumbers.append(int(number))
        if (len(currentLine) != boardSize):
            error('Incorrect number of numbers or invalid characteres')
        nestedArray.append(currentLine)
    if (len(arrayNumbers) != boardSize**2):
        error('Invalid, incorrect number of numbers')
    if (max(arrayNumbers) != (boardSize**2 - 1)):
        error('Invalid, numbers are incorrect')
    for number in arrayNumbers:
        if (arrayNumbers.count(number) != 1):
            error("Invalid, twice same number")
    if (min(arrayNumbers) != 0):
        error('Invalid, lowest number isn\'t 0')
    return(nestedArray, boardSize)

def board2D(data):
    """
    Put the input in a 2d board
    """
    board = []
    for line in data:
        lineBoard = []
        for number in line:
            lineBoard.append(int(number))
        board.append(lineBoard)
    return (board)

def checkDifferences(board):
    """
    Check the number of differences to see if board valid.
    For each number, check if every number greater than it is behind it.
    If not, differences += 1
    """
    total = 0
    for m in range(len(board)):
        for n in range(len(board[0])):
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if (board[m][n] != 0):
                        if (board[m][n] < board[i][j]):
                            if (m*len(board) + n > i*len(board) + j):
                                total += 1
    return (total)
    if (total % 2 == 0 or total == 0):
        return ('Valid')
    return ('Invalid')

"""
piece of code to generate the perfectState, according to the board size
"""
def spiral(n):
    def spiral_part(x, y, n):
        if x == -1 and y == 0:
            return -1
        if y == (x+1) and x < (n // 2):
            return spiral_part(x-1, y-1, n-1) + 4*(n-y)
        if x < (n-y) and y <= x:
            return spiral_part(y-1, y, n) + (x-y) + 1
        if x >= (n-y) and y <= x:
            return spiral_part(x, y-1, n) + 1
        if x >= (n-y) and y > x:
            return spiral_part(x+1, y, n) + 1
        if x < (n-y) and y > x:
            return spiral_part(x, y-1, n) - 1

    array = [[0] * n for j in range(n)]
    for x in range(n):
        for y in range(n):
            array[x][y] = spiral_part(y, x, n)
            array[x][y] += 1
            if (array[x][y] == n**2):
                array[x][y] = 0
    return array

# def storePerfecState(perfectState);

def checkHammingHeuristicValue(board, boardSize, perfectState):
    """
    Check heuristic value for the board compared
    to the Perfect State. Difference = 1.
    Hamming heuristic function
    """
    heuristicValue = 0
    for line in range(len(board)):
        for number in range(len(board[0])):
            if (board[line][number] == 0):
                row, col = line, number
            if (board[line][number] != perfectState[line][number]):
                if (board[line][number] != 0):
                    heuristicValue += 1
    return (heuristicValue, row, col)

def checkLinearConflic(board, boardSize, perfectState):
    """
    """
    linearValue = 0
    manhattanValue, row, col = checkManhattanHeuristicValue(board, boardSize, perfectState)
    if (manhattanValue == 0):
        return (manhattanValue, row, col)
    for line in range(len(board)):
        for number in range(len(board[0])):
            for perfectLine in range(len(perfectState)):
                for perfectNum in range(len(perfectState[0])):
                    if (board[line][number] == perfectState[perfectLine][perfectNum]):
                        if (line == perfectLine or number == perfectNum):
                            for line2 in range(len(board)):
                                for number2 in range(len(board[0])):
                                    if (board[line2][number2] == perfectState[perfectLine][perfectNum]):
                                        if (line2 == perfectLine or number2 == perfectNum):
                                            linearValue += 1
    linearValue = linearValue + manhattanValue
    return (linearValue, row, col)


def checkManhattanHeuristicValue(board, boardSize, perfectState):
    """
    manhattan-distance heuristic value
    """
    manhattanValue = 0
    for line in range(len(board)):
        for number in range(len(board[0])):
            if(board[line][number] == 0):
                row, col = line, number
            for perfectLine in range(len(perfectState)):
                for perfectNum in range(len(perfectState[0])):
                    if (board[line][number] == perfectState[perfectLine][perfectNum]):
                        x = 0
                        y = 0
                        if (line > perfectLine):
                            x = line - perfectLine
                        else:
                            x = perfectLine - line
                        if (number > perfectNum):
                            y = number - perfectNum
                        else:
                            y = perfectNum - number
                        manhattanValue = manhattanValue + (x + y)
    return (manhattanValue, row, col)

def saveNode(board, hValue, parent, posOfZero):
    """
    save the board, h value, f value and g value in a node class
    for historic
    """
    gValue = 0
    if (parent):
        gValue = parent.gValue + 1
    fValue = gValue + hValue
    state ='open'
    node = Node(board, hValue, state, parent, posOfZero)
    nodeHistoric.append(node)
    return (node)

def swap(currentX, currentY, nextX, nextY, board, boardSize, perfectState, parent, choosenHeuristic):
    """
    function to swap a piece in contact with the '0', check the heuristicValue of the new
    puzzle, then save thatt node and return it
    """
    savedBoard = []
    for key in board:
        savedBoard.append(key[:])
    tmp = savedBoard[nextX][nextY]
    savedBoard[nextX][nextY] = 0
    savedBoard[currentX][currentY] = tmp
    if (choosenHeuristic == 'manhattan'):
        result = checkManhattanHeuristicValue(savedBoard, boardSize, perfectState)
    elif (choosenHeuristic == 'hamming' or choosenHeuristic == 'default'):
        result = checkHammingHeuristicValue(savedBoard, boardSize, perfectState)
    else:
        result = checkLinearConflic(board, boardSize, perfectState)
    newNode = saveNode(savedBoard, result[0], parent, [nextX, nextY])
    return (newNode)

def makeMove(node, perfectState, choosenHeuristic):
    """
    move pieces in the open slot from every directions available
    """
    currentMoves = []
    bestNextNode = node

    if (node.posOfZero[0] > 0):
        boardUp = swap(node.posOfZero[0], node.posOfZero[1], node.posOfZero[0] - 1, node.posOfZero[1], node.board, range(len(node.board)), perfectState, node, choosenHeuristic)
        currentMoves.append(boardUp)
    if (node.posOfZero[0] < boardSize - 1):
        boardDown = swap(node.posOfZero[0], node.posOfZero[1], node.posOfZero[0] + 1, node.posOfZero[1], node.board, range(len(node.board)), perfectState, node, choosenHeuristic)
        currentMoves.append(boardDown)
    if (node.posOfZero[1] < boardSize - 1):
        boardRight = swap(node.posOfZero[0], node.posOfZero[1], node.posOfZero[0], node.posOfZero[1] + 1, node.board, range(len(node.board)), perfectState, node, choosenHeuristic)
        currentMoves.append(boardRight)
    if (node.posOfZero[1] > 0):
        boardLeft = swap(node.posOfZero[0], node.posOfZero[1], node.posOfZero[0], node.posOfZero[1] - 1, node.board, range(len(node.board)), perfectState, node, choosenHeuristic)
        currentMoves.append(boardLeft)

    return (currentMoves)

def solveNpuzzle(board, boardSize, perfectState, choosenHeuristic):
    """
    main function to solve the puzzle
    """
    if (choosenHeuristic == 'manhattan'):
        heuristicValue, row, col = checkManhattanHeuristicValue(board, boardSize, perfectState)
    elif (choosenHeuristic == 'hamming' or choosenHeuristic == 'default'):
        heuristicValue, row, col = checkHammingHeuristicValue(board, boardSize, perfectState)
    elif (choosenHeuristic == 'linearConflict'):
        heuristicValue, row, col = checkLinearConflic(board, boardSize, perfectState)
    posOfZero = row, col
    open = []
    closed = []
    openCounter = 0
    lenClosed = 0
    primordialNode = saveNode(board, heuristicValue, None, posOfZero)
    open.append(primordialNode)
    if (heuristicValue == 0):
        print ("Puzzle solved!")
        sys.exit()
    else:
        while 1:
            min = None
            for node in open:
                if (min == None or min.fValue > node.fValue):
                    min = node
            if (min.hValue == 0):
                return (min, len(open), len(closed))
            children = makeMove(min, perfectState, choosenHeuristic)
            closed.append(min)
            open.remove(min)
            for child in children:
                for node in open:
                    '''
                    '''
                    if (child.boardString == node.boardString and child.fValue < node.fValue):
                        open.remove(node)
                open.append(child)
                openCounter += 1

def checkSolvability(board, perfectState):
    """
    """
    start = checkDifferences(board)
    end = checkDifferences(perfectState)
    if (len(board) % 2 == 0):
        start += int(getZeroIndex(board) / len(board))
        end += int(getZeroIndex(perfectState) / len(board))
    if ((start % 2 == end % 2) is False):
        error('Unsolvable')

def checkValid(data, boardSize, choosenHeuristic):
    """
    Do all the checks for the puzzle
    """
    perfectState = []
    for row in spiral(boardSize):
        perfectState.append(row)
    checkSolvability(data, perfectState)
    lenOpen = 0
    lenClosed = 0
    finalNode, lenOpen, lenClosed = solveNpuzzle(board, boardSize, perfectState, choosenHeuristic)
    print('Total number of states in the \'opened\' set: {}'.format(lenOpen))
    print('Maximun number of states ever represented in memory at the same time: {}'.format(lenClosed))
    return (finalNode)

def printTraceback(finalNode):
    """
    """
    traceback = []
    while finalNode:
        traceback.append(finalNode.board)
        finalNode = finalNode.parent
    print('Number of moves:', len(traceback) - 1)
    print('this is traceback')
    for i in reversed(traceback):
        print(i)

def getZeroIndex(board):
    i = 0
    while (i < len(board)):
        j = 0
        while (j < len(board[i])):
            if (board[i][j] == 0):
                return ((i * len(board)) + j)
            j += 1
        i += 1
    error('Unexpected error')



choosenHeuristic = 'default'

"""
Check that the path is valid, then that thhe heuristic value is correct
"""
file = None
data = None
if (len(sys.argv) > 1):
    if (path.exists(sys.argv[1])):
        file = open(sys.argv[1])
        data = file.read()
    else:
        error('Please choose an existing path')
    if (sys.argv[2] == '-h'):
        if (len(sys.argv) > 3):
            if (sys.argv[3] == '1'):
                choosenHeuristic = 'manhattan'
            elif (sys.argv[3] == '2'):
                choosenHeuristic = 'hamming'
            elif (sys.argv[3] == '3'):
                choosenHeuristic = 'linearConflict'
            else:
                error('Please choose a heuristic value (ex: \'1\', \'2\')')
        else:
            error('Please choose a heuristic value (ex: \'1\', \'2\')')
    else:
        error('please only use the -h flag')
else:
    error('You need to choose some arguments (ex: file path, heuristic value)')


nodeHistoric = []
finalNode = None
lenOpen = 0
lenClosed = 0
data = cleanContent(data)
preBoard, boardSize = checkTotalNumber(data)
board = board2D(preBoard)
isValid = checkValid(board, boardSize, choosenHeuristic)
printTraceback(isValid)
