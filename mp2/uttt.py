import random
import time
from inspect import CORO_CLOSED
from time import sleep
from math import inf
from random import randint


class ultimateTicTacToe:
    def __init__(self):
        """
        Initialization of the game.
        """
        self.board = [['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_']]
        self.maxPlayer = 'X'
        self.minPlayer = 'O'
        self.maxDepth = 3
        # The start indexes of each local board
        self.globalIdx = [(0, 0), (0, 3), (0, 6), (3, 0), (3, 3), (3, 6), (6, 0), (6, 3), (6, 6)]

        # Start local board index for reflex agent playing
        self.startBoardIdx = 4
        # self.startBoardIdx=randint(0,8)
        self.centerMaxUtility = 50
        # utility value for reflex offensive and reflex defensive agents
        self.winnerMaxUtility = 10000
        self.twoInARowMaxUtility = 500
        self.preventThreeInARowMaxUtility = 100
        self.cornerMaxUtility = 30

        self.winnerMinUtility = -10000
        self.twoInARowMinUtility = -100
        self.preventThreeInARowMinUtility = -500
        self.cornerMinUtility = -30

        self.expandedNodes = 0
        self.currPlayer = True

    def printGameBoard(self):
        """
        This function prints the current game board.
        """
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[:3]]) + '\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[3:6]]) + '\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[6:9]]) + '\n')

    def globalLoc2BoardIdx(self, i, j):
        return (i % 3) * 3 + j % 3

    def evaluatePredifined(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for predifined agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        # YOUR CODE HERE
        score = 0
        if isMax:
            for coord in self.globalIdx:
                if self.checkWinner(coord) == 1:
                    return self.winnerMaxUtility
                for i in range(3):
                    if (self.board[coord[0] + i][coord[1]] == 'X' and \
                        self.board[coord[0] + i][coord[1] + 1] == 'X' and \
                        self.board[coord[0] + i][coord[1] + 2] == '_') or \
                            (self.board[coord[0] + i][coord[1]] == 'X' and \
                             self.board[coord[0] + i][coord[1] + 1] == '_' and \
                             self.board[coord[0] + i][coord[1] + 2] == 'X') or \
                            (self.board[coord[0] + i][coord[1]] == '_' and \
                             self.board[coord[0] + i][coord[1] + 1] == 'X' and \
                             self.board[coord[0] + i][coord[1] + 2] == 'X'):
                        score += self.twoInARowMaxUtility
                    elif (self.board[coord[0] + i][coord[1]] == 'O' and \
                          self.board[coord[0] + i][coord[1] + 1] == 'O' and \
                          self.board[coord[0] + i][coord[1] + 2] == 'X') or \
                            (self.board[coord[0] + i][coord[1]] == 'O' and \
                             self.board[coord[0] + i][coord[1] + 1] == 'X' and \
                             self.board[coord[0] + i][coord[1] + 2] == 'O') or \
                            (self.board[coord[0] + i][coord[1]] == 'X' and \
                             self.board[coord[0] + i][coord[1] + 1] == 'O' and \
                             self.board[coord[0] + i][coord[1] + 2] == 'O'):
                        score += self.preventThreeInARowMaxUtility
                    if (self.board[coord[0]][coord[1] + i] == 'X' and \
                        self.board[coord[0] + 1][coord[1] + i] == 'X' and \
                        self.board[coord[0] + 2][coord[1] + i] == '_') or \
                            (self.board[coord[0]][coord[1] + i] == 'X' and \
                             self.board[coord[0] + 1][coord[1] + i] == '_' and \
                             self.board[coord[0] + 2][coord[1] + i] == 'X') or \
                            (self.board[coord[0]][coord[1] + i] == '_' and \
                             self.board[coord[0] + 1][coord[1] + i] == 'X' and \
                             self.board[coord[0] + 2][coord[1] + i] == 'X'):
                        score += self.twoInARowMaxUtility
                    elif (self.board[coord[0]][coord[1] + i] == 'O' and \
                          self.board[coord[0] + 1][coord[1] + i] == 'O' and \
                          self.board[coord[0] + 2][coord[1] + i] == 'X') or \
                            (self.board[coord[0]][coord[1] + i] == 'O' and \
                             self.board[coord[0] + 1][coord[1] + i] == 'X' and \
                             self.board[coord[0] + 2][coord[1] + i] == 'O') or \
                            (self.board[coord[0]][coord[1] + i] == 'X' and \
                             self.board[coord[0] + 1][coord[1] + i] == 'O' and \
                             self.board[coord[0] + 2][coord[1] + i] == 'O'):
                        score += self.preventThreeInARowMaxUtility
                if (self.board[coord[0]][coord[1]] == '_' and \
                    self.board[coord[0] + 1][coord[1] + 1] == 'X' and \
                    self.board[coord[0] + 2][coord[1] + 2] == 'X') or \
                        (self.board[coord[0]][coord[1]] == 'X' and \
                         self.board[coord[0] + 1][coord[1] + 1] == '_' and \
                         self.board[coord[0] + 2][coord[1] + 2] == 'X') or \
                        (self.board[coord[0]][coord[1]] == 'X' and \
                         self.board[coord[0] + 1][coord[1] + 1] == 'X' and \
                         self.board[coord[0] + 2][coord[1] + 2] == '_'):
                    score += self.twoInARowMaxUtility
                elif (self.board[coord[0]][coord[1]] == 'X' and \
                      self.board[coord[0] + 1][coord[1] + 1] == 'O' and \
                      self.board[coord[0] + 2][coord[1] + 2] == 'O') or \
                        (self.board[coord[0]][coord[1]] == 'O' and \
                         self.board[coord[0] + 1][coord[1] + 1] == 'X' and \
                         self.board[coord[0] + 2][coord[1] + 2] == 'O') or \
                        (self.board[coord[0]][coord[1]] == 'O' and \
                         self.board[coord[0] + 1][coord[1] + 1] == 'O' and \
                         self.board[coord[0] + 2][coord[1] + 2] == 'X'):
                    score += self.preventThreeInARowMaxUtility
                if (self.board[coord[0] + 2][coord[1]] == '_' and \
                    self.board[coord[0] + 1][coord[1] + 1] == 'X' and \
                    self.board[coord[0]][coord[1] + 2] == 'X') or \
                        (self.board[coord[0] + 2][coord[1]] == 'X' and \
                         self.board[coord[0] + 1][coord[1] + 1] == '_' and \
                         self.board[coord[0]][coord[1] + 2] == 'X') or \
                        (self.board[coord[0] + 2][coord[1]] == 'X' and \
                         self.board[coord[0] + 1][coord[1] + 1] == 'X' and \
                         self.board[coord[0]][coord[1] + 2] == '_'):
                    score += self.twoInARowMaxUtility
                elif (self.board[coord[0] + 2][coord[1]] == 'X' and \
                      self.board[coord[0] + 1][coord[1] + 1] == 'O' and \
                      self.board[coord[0]][coord[1] + 2] == 'O') or \
                        (self.board[coord[0] + 2][coord[1]] == 'O' and \
                         self.board[coord[0] + 1][coord[1] + 1] == 'X' and \
                         self.board[coord[0]][coord[1] + 2] == 'O') or \
                        (self.board[coord[0] + 2][coord[1]] == 'O' and \
                         self.board[coord[0] + 1][coord[1] + 1] == 'O' and \
                         self.board[coord[0]][coord[1] + 2] == 'X'):
                    score += self.preventThreeInARowMaxUtility

                if score != 0:
                    return score
                else:
                    if self.board[coord[0]][coord[1]] == 'X':
                        score += self.cornerMaxUtility
                    if self.board[coord[0] + 2][coord[1]] == 'X':
                        score += self.cornerMaxUtility
                    if self.board[coord[0]][coord[1] + 2] == 'X':
                        score += self.cornerMaxUtility
                    if self.board[coord[0] + 2][coord[1] + 2] == 'X':
                        score += self.cornerMaxUtility

        else:
            for coord in self.globalIdx:
                if self.checkWinner(coord) == -1:
                    return self.winnerMinUtility
                for i in range(3):
                    if (self.board[coord[0] + i][coord[1]] == 'O' and \
                        self.board[coord[0] + i][coord[1] + 1] == 'O' and \
                        self.board[coord[0] + i][coord[1] + 2] == '_') or \
                            (self.board[coord[0] + i][coord[1]] == 'O' and \
                             self.board[coord[0] + i][coord[1] + 1] == '_' and \
                             self.board[coord[0] + i][coord[1] + 2] == 'O') or \
                            (self.board[coord[0] + i][coord[1]] == '_' and \
                             self.board[coord[0] + i][coord[1] + 1] == 'O' and \
                             self.board[coord[0] + i][coord[1] + 2] == 'O'):
                        score += self.twoInARowMinUtility
                    elif (self.board[coord[0] + i][coord[1]] == 'X' and \
                          self.board[coord[0] + i][coord[1] + 1] == 'X' and \
                          self.board[coord[0] + i][coord[1] + 2] == 'O') or \
                            (self.board[coord[0] + i][coord[1]] == 'X' and \
                             self.board[coord[0] + i][coord[1] + 1] == 'O' and \
                             self.board[coord[0] + i][coord[1] + 2] == 'X') or \
                            (self.board[coord[0] + i][coord[1]] == 'O' and \
                             self.board[coord[0] + i][coord[1] + 1] == 'X' and \
                             self.board[coord[0] + i][coord[1] + 2] == 'X'):
                        score += self.preventThreeInARowMinUtility
                    if (self.board[coord[0]][coord[1] + i] == 'O' and \
                        self.board[coord[0] + 1][coord[1] + i] == 'O' and \
                        self.board[coord[0] + 2][coord[1] + i] == '_') or \
                            (self.board[coord[0]][coord[1] + i] == 'O' and \
                             self.board[coord[0] + 1][coord[1] + i] == '_' and \
                             self.board[coord[0] + 2][coord[1] + i] == 'O') or \
                            (self.board[coord[0]][coord[1] + i] == '_' and \
                             self.board[coord[0] + 1][coord[1] + i] == 'O' and \
                             self.board[coord[0] + 2][coord[1] + i] == 'O'):
                        score += self.twoInARowMinUtility
                    elif (self.board[coord[0]][coord[1] + i] == 'X' and \
                          self.board[coord[0] + 1][coord[1] + i] == 'X' and \
                          self.board[coord[0] + 2][coord[1] + i] == 'O') or \
                            (self.board[coord[0]][coord[1] + i] == 'X' and \
                             self.board[coord[0] + 1][coord[1] + i] == 'O' and \
                             self.board[coord[0] + 2][coord[1] + i] == 'X') or \
                            (self.board[coord[0]][coord[1] + i] == 'O' and \
                             self.board[coord[0] + 1][coord[1] + i] == 'X' and \
                             self.board[coord[0] + 2][coord[1] + i] == 'X'):
                        score += self.preventThreeInARowMinUtility
                if (self.board[coord[0]][coord[1]] == '_' and \
                    self.board[coord[0] + 1][coord[1] + 1] == 'O' and \
                    self.board[coord[0] + 2][coord[1] + 2] == 'O') or \
                        (self.board[coord[0]][coord[1]] == 'O' and \
                         self.board[coord[0] + 1][coord[1] + 1] == '_' and \
                         self.board[coord[0] + 2][coord[1] + 2] == 'O') or \
                        (self.board[coord[0]][coord[1]] == 'O' and \
                         self.board[coord[0] + 1][coord[1] + 1] == 'O' and \
                         self.board[coord[0] + 2][coord[1] + 2] == '_'):
                    score += self.twoInARowMinUtility
                elif (self.board[coord[0]][coord[1]] == 'O' and \
                      self.board[coord[0] + 1][coord[1] + 1] == 'X' and \
                      self.board[coord[0] + 2][coord[1] + 2] == 'X') or \
                        (self.board[coord[0]][coord[1]] == 'X' and \
                         self.board[coord[0] + 1][coord[1] + 1] == 'O' and \
                         self.board[coord[0] + 2][coord[1] + 2] == 'X') or \
                        (self.board[coord[0]][coord[1]] == 'X' and \
                         self.board[coord[0] + 1][coord[1] + 1] == 'X' and \
                         self.board[coord[0] + 2][coord[1] + 2] == 'O'):
                    score += self.preventThreeInARowMinUtility
                if (self.board[coord[0] + 2][coord[1]] == '_' and \
                    self.board[coord[0] + 1][coord[1] + 1] == 'O' and \
                    self.board[coord[0]][coord[1] + 2] == 'O') or \
                        (self.board[coord[0] + 2][coord[1]] == 'O' and \
                         self.board[coord[0] + 1][coord[1] + 1] == '_' and \
                         self.board[coord[0]][coord[1] + 2] == 'O') or \
                        (self.board[coord[0] + 2][coord[1]] == 'O' and \
                         self.board[coord[0] + 1][coord[1] + 1] == 'O' and \
                         self.board[coord[0]][coord[1] + 2] == '_'):
                    score += self.twoInARowMinUtility
                elif (self.board[coord[0] + 2][coord[1]] == 'O' and \
                      self.board[coord[0] + 1][coord[1] + 1] == 'X' and \
                      self.board[coord[0]][coord[1] + 2] == 'X') or \
                        (self.board[coord[0] + 2][coord[1]] == 'X' and \
                         self.board[coord[0] + 1][coord[1] + 1] == 'O' and \
                         self.board[coord[0]][coord[1] + 2] == 'X') or \
                        (self.board[coord[0] + 2][coord[1]] == 'X' and \
                         self.board[coord[0] + 1][coord[1] + 1] == 'X' and \
                         self.board[coord[0]][coord[1] + 2] == 'O'):
                    score += self.preventThreeInARowMinUtility

            if score != 0:
                return score
            else:
                if self.board[coord[0]][coord[1]] == 'O':
                    score += self.cornerMaxUtility
            if self.board[coord[0] + 2][coord[1]] == 'O':
                score += self.cornerMaxUtility
            if self.board[coord[0]][coord[1] + 2] == 'O':
                score += self.cornerMaxUtility
            if self.board[coord[0] + 2][coord[1] + 2] == 'O':
                score += self.cornerMaxUtility

        return score

    def evaluateDesigned(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for your own agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        # YOUR CODE HERE
        score = 0
        if isMax:
            for coord in self.globalIdx:
                if self.checkWinner(coord) == 1:
                    return self.winnerMaxUtility
                for i in range(3):
                    if (self.board[coord[0] + i][coord[1]] == 'X' and \
                        self.board[coord[0] + i][coord[1] + 1] == 'X' and \
                        self.board[coord[0] + i][coord[1] + 2] == '_') or \
                            (self.board[coord[0] + i][coord[1]] == 'X' and \
                             self.board[coord[0] + i][coord[1] + 1] == '_' and \
                             self.board[coord[0] + i][coord[1] + 2] == 'X') or \
                            (self.board[coord[0] + i][coord[1]] == '_' and \
                             self.board[coord[0] + i][coord[1] + 1] == 'X' and \
                             self.board[coord[0] + i][coord[1] + 2] == 'X'):
                        score += self.twoInARowMaxUtility
                    elif (self.board[coord[0] + i][coord[1]] == 'O' and \
                          self.board[coord[0] + i][coord[1] + 1] == 'O' and \
                          self.board[coord[0] + i][coord[1] + 2] == 'X') or \
                            (self.board[coord[0] + i][coord[1]] == 'O' and \
                             self.board[coord[0] + i][coord[1] + 1] == 'X' and \
                             self.board[coord[0] + i][coord[1] + 2] == 'O') or \
                            (self.board[coord[0] + i][coord[1]] == 'X' and \
                             self.board[coord[0] + i][coord[1] + 1] == 'O' and \
                             self.board[coord[0] + i][coord[1] + 2] == 'O'):
                        score += self.preventThreeInARowMaxUtility
                    if (self.board[coord[0]][coord[1] + i] == 'X' and \
                        self.board[coord[0] + 1][coord[1] + i] == 'X' and \
                        self.board[coord[0] + 2][coord[1] + i] == '_') or \
                            (self.board[coord[0]][coord[1] + i] == 'X' and \
                             self.board[coord[0] + 1][coord[1] + i] == '_' and \
                             self.board[coord[0] + 2][coord[1] + i] == 'X') or \
                            (self.board[coord[0]][coord[1] + i] == '_' and \
                             self.board[coord[0] + 1][coord[1] + i] == 'X' and \
                             self.board[coord[0] + 2][coord[1] + i] == 'X'):
                        score += self.twoInARowMaxUtility
                    elif (self.board[coord[0]][coord[1] + i] == 'O' and \
                          self.board[coord[0] + 1][coord[1] + i] == 'O' and \
                          self.board[coord[0] + 2][coord[1] + i] == 'X') or \
                            (self.board[coord[0]][coord[1] + i] == 'O' and \
                             self.board[coord[0] + 1][coord[1] + i] == 'X' and \
                             self.board[coord[0] + 2][coord[1] + i] == 'O') or \
                            (self.board[coord[0]][coord[1] + i] == 'X' and \
                             self.board[coord[0] + 1][coord[1] + i] == 'O' and \
                             self.board[coord[0] + 2][coord[1] + i] == 'O'):
                        score += self.preventThreeInARowMaxUtility
                if (self.board[coord[0]][coord[1]] == '_' and \
                    self.board[coord[0] + 1][coord[1] + 1] == 'X' and \
                    self.board[coord[0] + 2][coord[1] + 2] == 'X') or \
                        (self.board[coord[0]][coord[1]] == 'X' and \
                         self.board[coord[0] + 1][coord[1] + 1] == '_' and \
                         self.board[coord[0] + 2][coord[1] + 2] == 'X') or \
                        (self.board[coord[0]][coord[1]] == 'X' and \
                         self.board[coord[0] + 1][coord[1] + 1] == 'X' and \
                         self.board[coord[0] + 2][coord[1] + 2] == '_'):
                    score += self.twoInARowMaxUtility
                elif (self.board[coord[0]][coord[1]] == 'X' and \
                      self.board[coord[0] + 1][coord[1] + 1] == 'O' and \
                      self.board[coord[0] + 2][coord[1] + 2] == 'O') or \
                        (self.board[coord[0]][coord[1]] == 'O' and \
                         self.board[coord[0] + 1][coord[1] + 1] == 'X' and \
                         self.board[coord[0] + 2][coord[1] + 2] == 'O') or \
                        (self.board[coord[0]][coord[1]] == 'O' and \
                         self.board[coord[0] + 1][coord[1] + 1] == 'O' and \
                         self.board[coord[0] + 2][coord[1] + 2] == 'X'):
                    score += self.preventThreeInARowMaxUtility
                if (self.board[coord[0] + 2][coord[1]] == '_' and \
                    self.board[coord[0] + 1][coord[1] + 1] == 'X' and \
                    self.board[coord[0]][coord[1] + 2] == 'X') or \
                        (self.board[coord[0] + 2][coord[1]] == 'X' and \
                         self.board[coord[0] + 1][coord[1] + 1] == '_' and \
                         self.board[coord[0]][coord[1] + 2] == 'X') or \
                        (self.board[coord[0] + 2][coord[1]] == 'X' and \
                         self.board[coord[0] + 1][coord[1] + 1] == 'X' and \
                         self.board[coord[0]][coord[1] + 2] == '_'):
                    score += self.twoInARowMaxUtility
                elif (self.board[coord[0] + 2][coord[1]] == 'X' and \
                      self.board[coord[0] + 1][coord[1] + 1] == 'O' and \
                      self.board[coord[0]][coord[1] + 2] == 'O') or \
                        (self.board[coord[0] + 2][coord[1]] == 'O' and \
                         self.board[coord[0] + 1][coord[1] + 1] == 'X' and \
                         self.board[coord[0]][coord[1] + 2] == 'O') or \
                        (self.board[coord[0] + 2][coord[1]] == 'O' and \
                         self.board[coord[0] + 1][coord[1] + 1] == 'O' and \
                         self.board[coord[0]][coord[1] + 2] == 'X'):
                    score += self.preventThreeInARowMaxUtility

                if score != 0:
                    return score
                else:
                    if self.board[coord[0] + 1][coord[1] + 1] == 'O':
                        score += self.centerMaxUtility
                    if self.board[coord[0]][coord[1]] == 'X':
                        score += self.cornerMaxUtility
                    if self.board[coord[0] + 2][coord[1]] == 'X':
                        score += self.cornerMaxUtility
                    if self.board[coord[0]][coord[1] + 2] == 'X':
                        score += self.cornerMaxUtility
                    if self.board[coord[0] + 2][coord[1] + 2] == 'X':
                        score += self.cornerMaxUtility

        else:
            for coord in self.globalIdx:
                if self.checkWinner(coord) == -1:
                    return self.winnerMinUtility
                for i in range(3):
                    if (self.board[coord[0] + i][coord[1]] == 'O' and \
                        self.board[coord[0] + i][coord[1] + 1] == 'O' and \
                        self.board[coord[0] + i][coord[1] + 2] == '_') or \
                            (self.board[coord[0] + i][coord[1]] == 'O' and \
                             self.board[coord[0] + i][coord[1] + 1] == '_' and \
                             self.board[coord[0] + i][coord[1] + 2] == 'O') or \
                            (self.board[coord[0] + i][coord[1]] == '_' and \
                             self.board[coord[0] + i][coord[1] + 1] == 'O' and \
                             self.board[coord[0] + i][coord[1] + 2] == 'O'):
                        score += self.twoInARowMinUtility
                    elif (self.board[coord[0] + i][coord[1]] == 'X' and \
                          self.board[coord[0] + i][coord[1] + 1] == 'X' and \
                          self.board[coord[0] + i][coord[1] + 2] == 'O') or \
                            (self.board[coord[0] + i][coord[1]] == 'X' and \
                             self.board[coord[0] + i][coord[1] + 1] == 'O' and \
                             self.board[coord[0] + i][coord[1] + 2] == 'X') or \
                            (self.board[coord[0] + i][coord[1]] == 'O' and \
                             self.board[coord[0] + i][coord[1] + 1] == 'X' and \
                             self.board[coord[0] + i][coord[1] + 2] == 'X'):
                        score += self.preventThreeInARowMinUtility
                    if (self.board[coord[0]][coord[1] + i] == 'O' and \
                        self.board[coord[0] + 1][coord[1] + i] == 'O' and \
                        self.board[coord[0] + 2][coord[1] + i] == '_') or \
                            (self.board[coord[0]][coord[1] + i] == 'O' and \
                             self.board[coord[0] + 1][coord[1] + i] == '_' and \
                             self.board[coord[0] + 2][coord[1] + i] == 'O') or \
                            (self.board[coord[0]][coord[1] + i] == '_' and \
                             self.board[coord[0] + 1][coord[1] + i] == 'O' and \
                             self.board[coord[0] + 2][coord[1] + i] == 'O'):
                        score += self.twoInARowMinUtility
                    elif (self.board[coord[0]][coord[1] + i] == 'X' and \
                          self.board[coord[0] + 1][coord[1] + i] == 'X' and \
                          self.board[coord[0] + 2][coord[1] + i] == 'O') or \
                            (self.board[coord[0]][coord[1] + i] == 'X' and \
                             self.board[coord[0] + 1][coord[1] + i] == 'O' and \
                             self.board[coord[0] + 2][coord[1] + i] == 'X') or \
                            (self.board[coord[0]][coord[1] + i] == 'O' and \
                             self.board[coord[0] + 1][coord[1] + i] == 'X' and \
                             self.board[coord[0] + 2][coord[1] + i] == 'X'):
                        score += self.preventThreeInARowMinUtility
                if (self.board[coord[0]][coord[1]] == '_' and \
                    self.board[coord[0] + 1][coord[1] + 1] == 'O' and \
                    self.board[coord[0] + 2][coord[1] + 2] == 'O') or \
                        (self.board[coord[0]][coord[1]] == 'O' and \
                         self.board[coord[0] + 1][coord[1] + 1] == '_' and \
                         self.board[coord[0] + 2][coord[1] + 2] == 'O') or \
                        (self.board[coord[0]][coord[1]] == 'O' and \
                         self.board[coord[0] + 1][coord[1] + 1] == 'O' and \
                         self.board[coord[0] + 2][coord[1] + 2] == '_'):
                    score += self.twoInARowMinUtility
                elif (self.board[coord[0]][coord[1]] == 'O' and \
                      self.board[coord[0] + 1][coord[1] + 1] == 'X' and \
                      self.board[coord[0] + 2][coord[1] + 2] == 'X') or \
                        (self.board[coord[0]][coord[1]] == 'X' and \
                         self.board[coord[0] + 1][coord[1] + 1] == 'O' and \
                         self.board[coord[0] + 2][coord[1] + 2] == 'X') or \
                        (self.board[coord[0]][coord[1]] == 'X' and \
                         self.board[coord[0] + 1][coord[1] + 1] == 'X' and \
                         self.board[coord[0] + 2][coord[1] + 2] == 'O'):
                    score += self.preventThreeInARowMinUtility
                if (self.board[coord[0] + 2][coord[1]] == '_' and \
                    self.board[coord[0] + 1][coord[1] + 1] == 'O' and \
                    self.board[coord[0]][coord[1] + 2] == 'O') or \
                        (self.board[coord[0] + 2][coord[1]] == 'O' and \
                         self.board[coord[0] + 1][coord[1] + 1] == '_' and \
                         self.board[coord[0]][coord[1] + 2] == 'O') or \
                        (self.board[coord[0] + 2][coord[1]] == 'O' and \
                         self.board[coord[0] + 1][coord[1] + 1] == 'O' and \
                         self.board[coord[0]][coord[1] + 2] == '_'):
                    score += self.twoInARowMinUtility
                elif (self.board[coord[0] + 2][coord[1]] == 'O' and \
                      self.board[coord[0] + 1][coord[1] + 1] == 'X' and \
                      self.board[coord[0]][coord[1] + 2] == 'X') or \
                        (self.board[coord[0] + 2][coord[1]] == 'X' and \
                         self.board[coord[0] + 1][coord[1] + 1] == 'O' and \
                         self.board[coord[0]][coord[1] + 2] == 'X') or \
                        (self.board[coord[0] + 2][coord[1]] == 'X' and \
                         self.board[coord[0] + 1][coord[1] + 1] == 'X' and \
                         self.board[coord[0]][coord[1] + 2] == 'O'):
                    score += self.preventThreeInARowMinUtility

            if score != 0:
                return score
            else:
                if self.board[coord[0] + 1][coord[1] + 1] == 'O':
                    score += self.centerMaxUtility
                if self.board[coord[0]][coord[1]] == 'O':
                    score += self.cornerMaxUtility
                if self.board[coord[0] + 2][coord[1]] == 'O':
                    score += self.cornerMaxUtility
                if self.board[coord[0]][coord[1] + 2] == 'O':
                    score += self.cornerMaxUtility
                if self.board[coord[0] + 2][coord[1] + 2] == 'O':
                    score += self.cornerMaxUtility
        return score

    def checkMovesLeft(self, coord):
        """
        This function checks whether any legal move remains on the board.
        output:
        movesLeft(bool): boolean variable indicates whether any legal move remains
                        on the board.
        """
        # YOUR CODE HERE
        movesLeft = False
        for i in range(3):
            for j in range(3):
                if '_' in self.board[coord[0] + i][coord[1] + j]:
                    movesLeft = True
                    break
            if movesLeft:
                return True
        return False

    def checkWinner(self, check_move_idx):
        # Return termimnal node status for maximizer player 1-win,0-tie,-1-lose
        """
        This function checks whether there is a winner on the board.
        output:
        winner(int): Return 0 if there is no winner.
                     Return 1 if maxPlayer is the winner.
                     Return -1 if miniPlayer is the winner.
                     Return 2 if game continues
        """
        # YOUR CODE HERE
        winner = 0
        # check rows & columns
        for coord in self.globalIdx:
            for i in range(3):
                if (self.board[coord[0] + i][coord[1]] == 'X' and \
                    self.board[coord[0] + i][coord[1] + 1] == 'X' and \
                    self.board[coord[0] + i][coord[1] + 2] == 'X') or \
                        (self.board[coord[0]][coord[1] + i] == 'X' and \
                         self.board[coord[0] + 1][coord[1] + i] == 'X' and \
                         self.board[coord[0] + 2][coord[1] + i] == 'X'):
                    winner = 1

                elif (self.board[coord[0] + i][coord[1]] == 'O' and \
                      self.board[coord[0] + i][coord[1] + 1] == 'O' and \
                      self.board[coord[0] + i][coord[1] + 2] == 'O') or \
                        (self.board[coord[0]][coord[1] + i] == 'O' and \
                         self.board[coord[0] + 1][coord[1] + i] == 'O' and \
                         self.board[coord[0] + 2][coord[1] + i] == 'O'):

                    winner = -1

            # Check diagonal
            if (self.board[coord[0]][coord[1]] == 'X' and \
                self.board[coord[0] + 1][coord[1] + 1] == 'X' and \
                self.board[coord[0] + 2][coord[1] + 2] == 'X') or \
                    (self.board[coord[0] + 2][coord[1]] == 'X' and \
                     self.board[coord[0] + 1][coord[1] + 1] == 'X' and \
                     self.board[coord[0]][coord[1] + 2] == 'X'):
                winner = 1
            elif (self.board[coord[0]][coord[1]] == 'O' and \
                  self.board[coord[0] + 1][coord[1] + 1] == 'O' and \
                  self.board[coord[0] + 2][coord[1] + 2] == 'O') or \
                    (self.board[coord[0] + 2][coord[1]] == 'O' and \
                     self.board[coord[0] + 1][coord[1] + 1] == 'O' and \
                     self.board[coord[0]][coord[1] + 2] == 'O'):
                winner = -1

        # check if tie
        if winner == 0 and self.checkMovesLeft(check_move_idx):
            return 2
        return winner

    def alphabeta(self, depth, currBoard, alpha, beta, isMax):
        """
         This function implements alpha-beta algorithm for ultimate tic-tac-toe game.
         input args:
         depth(int): current depth level
         currBoardIdx(int): current local board index
         alpha(float): alpha value
         beta(float): beta value
         isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                      True for maxPlayer, False for minPlayer
         output:
         bestValue(float):the bestValue that current player may have
         """
        # YOUR CODE HERE
        if self.checkWinner == 1:
            return self.winnerMaxUtility
        elif self.checkWinner == -1:
            return self.winnerMinUtility
        elif self.checkWinner == 0:
            return 0

        if depth == 4:
            return self.evaluatePredifined(not isMax)

        if isMax:
            bestValue = -inf
            for i in range(3):
                for j in range(3):
                    x = i + currBoard[0]
                    y = j + currBoard[1]

                    if self.board[x][y] == '_':
                        self.board[x][y] = 'X'
                        nextBoard = self.globalIdx[self.globalLoc2BoardIdx(x, y)]
                        bestValue = max(bestValue,
                                        self.alphabeta(depth + 1, nextBoard, alpha, beta, not isMax))
                        alpha = max(alpha, bestValue)
                        self.board[x][y] = '_'
                    if beta <= alpha:
                        return bestValue
                if beta <= alpha:
                    return bestValue
            return bestValue

        else:
            bestValue = inf
            for i in range(3):
                for j in range(3):
                    x = i + currBoard[0]
                    y = j + currBoard[1]
                    if self.board[x][y] == '_':
                        self.board[x][y] = 'O'
                        nextBoard = self.globalIdx[self.globalLoc2BoardIdx(x, y)]
                        bestValue = min(bestValue,
                                        self.alphabeta(depth + 1, nextBoard, alpha, beta, not isMax))
                        beta = min(beta, bestValue)
                        self.board[x][y] = '_'
                    if beta <= alpha:
                        return bestValue
                if beta <= alpha:
                    return bestValue
            return bestValue

    def alphabeta_new(self, depth, currBoard, alpha, beta, isMax):
        """
         This function implements alpha-beta algorithm for ultimate tic-tac-toe game.
         input args:
         depth(int): current depth level
         currBoardIdx(int): current local board index
         alpha(float): alpha value
         beta(float): beta value
         isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                      True for maxPlayer, False for minPlayer
         output:
         bestValue(float):the bestValue that current player may have
         """
        # YOUR CODE HERE
        if self.checkWinner == 1:
            return self.winnerMaxUtility
        elif self.checkWinner == -1:
            return self.winnerMinUtility
        elif self.checkWinner == 0:
            return 0

        if depth == 4:
            return self.evaluateDesigned(not isMax)

        if isMax:
            bestValue = -inf
            for i in range(3):
                for j in range(3):
                    x = i + currBoard[0]
                    y = j + currBoard[1]

                    if self.board[x][y] == '_':
                        self.board[x][y] = 'X'
                        nextBoard = self.globalIdx[self.globalLoc2BoardIdx(x, y)]
                        bestValue = max(bestValue,
                                        self.alphabeta_new(depth + 1, nextBoard, alpha, beta, not isMax))
                        alpha = max(alpha, bestValue)
                        self.board[x][y] = '_'
                    if beta <= alpha:
                        return bestValue
                if beta <= alpha:
                    return bestValue
            return bestValue

        else:
            bestValue = inf
            for i in range(3):
                for j in range(3):
                    x = i + currBoard[0]
                    y = j + currBoard[1]
                    if self.board[x][y] == '_':
                        self.board[x][y] = 'O'
                        nextBoard = self.globalIdx[self.globalLoc2BoardIdx(x, y)]
                        bestValue = min(bestValue,
                                        self.alphabeta_new(depth + 1, nextBoard, alpha, beta, not isMax))
                        beta = min(beta, bestValue)
                        self.board[x][y] = '_'
                    if beta <= alpha:
                        return bestValue
                if beta <= alpha:
                    return bestValue
            return bestValue


    def minimax(self, depth, currBoard, isMax):
        """
        This function implements minimax algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        # YOUR CODE HERE
        if self.checkWinner == 1:
            return self.winnerMaxUtility
        elif self.checkWinner == -1:
            return self.winnerMinUtility
        elif self.checkWinner == 0:
            return 0

        if depth == 4:
            return self.evaluatePredifined(not isMax)

        if isMax:
            bestValue = -100000
            for i in range(3):
                for j in range(3):
                    x = currBoard[0] + i
                    y = currBoard[1] + j
                    if self.board[x][y] == '_':
                        self.board[x][y] = 'X'
                        nextBoard = self.globalIdx[self.globalLoc2BoardIdx(x, y)]
                        bestValue = max(bestValue, self.minimax(depth + 1, currBoard, not isMax))
                        self.board[x][y] = '_'
            return bestValue

        else:
            bestValue = 100000
            for i in range(3):
                for j in range(3):
                    x = currBoard[0] + i
                    y = currBoard[1] + j
                    if self.board[x][y] == '_':
                        self.board[x][y] = 'O'
                        nextBoard = self.globalIdx[self.globalLoc2BoardIdx(x, y)]
                        bestValue = min(bestValue, self.minimax(depth + 1, currBoard, not isMax))
                        self.board[x][y] = '_'
            return bestValue


    def playGamePredifinedAgent(self, maxFirst, isMinimaxOffensive, isMinimaxDefensive):
        """
        This function implements the processes of the game of predifined offensive agent vs defensive agent.
        input args:
        maxFirst(bool): boolean variable indicates whether maxPlayer or minPlayer plays first.
                        True for maxPlayer plays first, and False for minPlayer plays first.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for offensive agent.
                        True is minimax and False is alpha-beta.
        isMinimaxDefensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for defensive agent.
                        True is minimax and False is alpha-beta.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        bestValue(list of float): list of bestValue at each move
        expandedNodes(list of int): list of expanded nodes at each move
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        # YOUR CODE HERE
        currBoardIdx = self.startBoardIdx
        self.currPlayer = maxFirst
        bestMove = []
        bestValue = []
        gameBoards = []
        self.expandedNodes = 0
        alpha = -inf
        beta = inf
        expandedNodes = []
        best_coord = (4, 4)
        # winner=0
        while self.checkMovesLeft(self.globalIdx[currBoardIdx]) and self.checkWinner(self.globalIdx[currBoardIdx]) == 2:

            currBoardIdx = self.globalLoc2BoardIdx(best_coord[0], best_coord[1])
            best_coord = (-1, -1)
            x = self.globalIdx[currBoardIdx][1]
            y = self.globalIdx[currBoardIdx][0]
            if self.currPlayer:
                best_value = -inf
                print("----------Max Move------------")
                for j in range(3):
                    for i in range(3):
                        if self.board[y + j][x + i] == '_':
                            tempBoardIdx = self.globalLoc2BoardIdx(y + j, x + i)
                            self.board[y + j][x + i] = self.maxPlayer
                            if isMinimaxOffensive:
                                now_value = self.minimax(1, self.globalIdx[tempBoardIdx], not self.currPlayer)
                            else:
                                now_value = self.alphabeta(1, self.globalIdx[tempBoardIdx], alpha, beta, not self.currPlayer)
                            self.board[y + j][x + i] = '_'
                            if now_value > best_value:
                                best_value = now_value
                                best_coord = (y + j, x + i)
                self.board[best_coord[0]][best_coord[1]] = self.maxPlayer
            else:
                best_value = inf
                for j in range(3):
                    for i in range(3):
                        if self.board[y + j][x + i] == '_':
                            tempBoardIdx = self.globalLoc2BoardIdx(y + j, x + i)
                            self.board[y + j][x + i] = self.minPlayer
                            if isMinimaxDefensive:
                                now_value = self.minimax(1, self.globalIdx[tempBoardIdx], not self.currPlayer)
                            else:
                                now_value = self.alphabeta(1, self.globalIdx[tempBoardIdx], alpha, beta, not self.currPlayer)
                            self.board[y + j][x + i] = '_'
                            if now_value < best_value:
                                best_value = now_value
                                best_coord = (y + j, x + i)
                self.board[best_coord[0]][best_coord[1]] = self.minPlayer
            bestValue.append(best_value)
            bestMove.append(best_coord)
            gameBoards.append(self.board)
            expandedNodes.append(self.expandedNodes)
            self.currPlayer = not self.currPlayer
            self.printGameBoard()

        winner = self.checkWinner(self.globalIdx[currBoardIdx])
        return gameBoards, bestMove, expandedNodes, bestValue, winner


    def playGameYourAgent(self):
        """
        This function implements the processes of the game of your own agent vs predifined offensive agent.
        input args:
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        # YOUR CODE HERE
        currBoardIdx = self.startBoardIdx
        self.currPlayer = True
        bestMove = []
        bestValue = []
        gameBoards = []
        self.expandedNodes = 0
        alpha = -inf
        beta = inf
        expandedNodes = []
        best_coord = (4, 4)
        # winner=0
        while self.checkMovesLeft(self.globalIdx[currBoardIdx]) and self.checkWinner(self.globalIdx[currBoardIdx]) == 2:

            currBoardIdx = self.globalLoc2BoardIdx(best_coord[0], best_coord[1])
            best_coord = (-1, -1)
            x = self.globalIdx[currBoardIdx][1]
            y = self.globalIdx[currBoardIdx][0]
            if self.currPlayer:
                best_value = -inf
                print("----------Max Move------------")
                for j in range(3):
                    for i in range(3):
                        if self.board[y + j][x + i] == '_':
                            tempBoardIdx = self.globalLoc2BoardIdx(y + j, x + i)
                            self.board[y + j][x + i] = self.maxPlayer
                            now_value = self.alphabeta(1, self.globalIdx[tempBoardIdx], alpha, beta,
                                                       not self.currPlayer)
                            self.board[y + j][x + i] = '_'
                            if now_value > best_value:
                                best_value = now_value
                                best_coord = (y + j, x + i)
                            if now_value == best_value:
                                val = random.randint(0, 1)
                                if val:
                                    best_value = now_value
                                    best_coord = (y + j, x + i)

                self.board[best_coord[0]][best_coord[1]] = self.maxPlayer
            else:
                best_value = inf
                for j in range(3):
                    for i in range(3):
                        if self.board[y + j][x + i] == '_':
                            tempBoardIdx = self.globalLoc2BoardIdx(y + j, x + i)
                            self.board[y + j][x + i] = self.minPlayer
                            now_value = self.alphabeta_new(1, self.globalIdx[tempBoardIdx], alpha, beta,
                                                           not self.currPlayer)
                            self.board[y + j][x + i] = '_'
                            if now_value < best_value:
                                best_value = now_value
                                best_coord = (y + j, x + i)
                self.board[best_coord[0]][best_coord[1]] = self.minPlayer
            bestValue.append(best_value)
            bestMove.append(best_coord)
            gameBoards.append(self.board)
            expandedNodes.append(self.expandedNodes)
            self.currPlayer = not self.currPlayer
            self.printGameBoard()

        winner = self.checkWinner(self.globalIdx[currBoardIdx])
        return gameBoards, bestMove, expandedNodes, bestValue, winner

        return gameBoards, bestMove, winner


    def playGameHuman(self):
        """
        This function implements the processes of the game of your own agent vs a human.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        # YOUR CODE HERE
        bestMove = []
        gameBoards = []
        winner = 0
        currBoardIdx = self.startBoardIdx
        best_coord = (4,4)

        while self.checkMovesLeft(self.globalIdx[currBoardIdx]) and self.checkWinner(self.globalIdx[currBoardIdx]) == 2:
            currBoardIdx = self.globalLoc2BoardIdx(best_coord[0], best_coord[1])
            x = self.globalIdx[currBoardIdx][1]
            y = self.globalIdx[currBoardIdx][0]
            if (self.currPlayer):
                isValidInput = False
                best_coord = (-1, -1)
                while not isValidInput:
                    print("Current chess board:")
                    self.printGameBoard()
                    print("Current game pad:" + str(self.globalIdx[currBoardIdx]))
                    raw_input = input("Please input the current chess board's location 'x:(0-2), y:(0,2)': ")
                    try:
                        splited_input_str = raw_input.split(',')
                        print(splited_input_str)
                        user_coord = (int(splited_input_str[0]), int(splited_input_str[1]))
                        best_coord = (user_coord[0] + y, user_coord[1] + x)
                        if user_coord[0] in range(3) and user_coord[1] in range(3) and self.board[best_coord[0]][best_coord[1]]=="_":
                            isValidInput = True
                        else:
                            isValidInput = False
                        best_coord = (user_coord[0]+y, user_coord[1]+x)
                    except:
                        print("Invalid Input, Please Try again.")
                self.board[best_coord[0]][best_coord[1]] = self.maxPlayer
            else:
                best_value = inf
                for j in range(3):
                    for i in range(3):
                        if self.board[y + j][x + i] == '_':
                            tempBoardIdx = self.globalLoc2BoardIdx(y + j, x + i)
                            self.board[y + j][x + i] = self.minPlayer
                            now_value = self.alphabeta_new(1, self.globalIdx[tempBoardIdx], -inf, inf,
                                                       not self.currPlayer)
                            self.board[y + j][x + i] = '_'
                            if now_value < best_value:
                                best_value = now_value
                                best_coord = (y + j, x + i)
                self.board[best_coord[0]][best_coord[1]] = self.minPlayer
                print("Offensive move:")
                print("Coord:"+str(best_coord))
                self.printGameBoard()
            bestMove.append(best_coord)
            gameBoards.append(self.board)
            self.currPlayer = not self.currPlayer

        winner = self.checkWinner(currBoardIdx)
        return gameBoards, bestMove, winner


if __name__ == "__main__":
    uttt = ultimateTicTacToe()
    random.seed(time.time())
    # feel free to write your own test code
    # gameBoards, bestMove, expandedNodes, bestValue, winner = uttt.playGamePredifinedAgent(True, True, True)
    # gameBoards, bestMove, expandedNodes, bestValue, winner = uttt.playGameYourAgent()
    #
    bestMove, gameBoards, winner = uttt.playGameHuman()
    if winner == 1:
        print("The winner is maxPlayer!!!")
    elif winner == -1:
        print("The winner is minPlayer!!!")
    else:
        print("Tie. No winner:(")
