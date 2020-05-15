# Author: Corey Cunningham
# Date: 05-15-2020
# Class: CS 162
# Assignment: Portfolio Project
# Description: Implementation of an abstract board game called Gess


class Board:

    def __init__(self):
        self._spaces = [[None for x in range(0, 18)] for x in range(0, 18)]
        self.initialize_player("player1")
        self.initialize_player("player2")

    def initialize_player(self, player):
        # generate initialize spots for each piece
        # x_coord is really the y_coord in the representation on the board but in the array
        # it's reversed which is confusing
        row1 = row3 = [x for x in range(0, 18) if x not in [0, 2, 4, 13, 15, 17]]
        row2 = [x for x in range(0, 18) if x not in [3, 5, 10, 12, 14]]
        row4 = [3, 5, 10, 12, 14]
        initial_rows = [row1, row2, row3, row4]
        # loop through rows and initialize empty spots to either player1 or player 2
        for index, row in enumerate(initial_rows):
            if player == "player1":
                x_coord = index
            else:
                x_coord = 17 - index
            for space in row:
                y_coord = space
                # special case for last row
                if index == 3:
                    if player == "player2":
                        self._spaces[x_coord - 2][y_coord] = Piece(player)
                    else:
                        self._spaces[x_coord + 2][y_coord] = Piece(player)
                else:
                    self._spaces[x_coord][y_coord] = Piece(player)

    def print(self):
            count = 0
            for row in self._spaces:
                print(str(count) + " " if count < 10 else count, row)
                count += 1
            letters = " "
            for letter in range(97, 115):
                letters += "     " + chr(letter)
            print(letters)


class Piece:

    def __init__(self, player):
        self._player = player

    def get_player(self):
        return self._player

    def __str__(self):
        return " X " if self._player == "player1" else "  O "

    def __repr__(self):
        return "  X " if self._player == "player1" else "  O "

class GessGame:
    def __init__(self):
        # make 18 x 18 board
        self._board = [[None for x in range(0, 18)] for x in range(0, 18)]

    def get_game_state(self):
        pass

    def resign_game(self, player):
        pass

    def make_move(self, old_loc, new_loc):
        pass


board = Board()
board.print()


