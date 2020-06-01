# Author: Corey Cunningham
# Date: 05-15-2020
# Class: CS 162
# Assignment: Portfolio Project
# Description: Implementation of an abstract board game called Gess,
#              Running this file allows one to play the game in the command line


class Board:
    """
    Represents the game board a 18x18 2 dimensional array with board[x][y] where
    x represents a row and y represents a column
    """
    def __init__(self):
        """
        initializes the game board to have two types of pieces, player1 and player2
        the pieces are laid out according to the rules of Gess.
        """
        self._spaces = [[None for _ in range(0, 18)] for _ in range(0, 18)]
        self._player1 = Piece("player1")
        self._player2 = Piece("player2")
        self.initialize_player(self._player1)
        self.initialize_player(self._player2)

    def initialize_player(self, player):
        """
        places Piece objects on the board at the appropriate places
        :param player: "player1" or "player2" (String)
        """
        # generate initialize spots for each piece
        # x_coord is really the y_coord in the representation on the board but in the array
        # it's reversed which is confusing
        row1 = row3 = [x for x in range(0, 18) if x not in [0, 2, 4, 13, 15, 17]]
        row2 = [x for x in range(0, 18) if x not in [3, 5, 10, 12, 14]]
        row4 = [1, 4, 7, 10, 13, 16]
        initial_rows = [row1, row2, row3, row4]
        # loop through rows and initialize empty spots to either player1 or player 2
        for index, row in enumerate(initial_rows):
            if player.get_player() == "player1":
                x_coord = index
            else:
                x_coord = 17 - index
            for space in row:
                y_coord = space
                # special case for last row
                if index == 3:
                    if player.get_player() == "player1":
                        self._spaces[x_coord + 2][y_coord] = player
                    else:
                        self._spaces[x_coord - 2][y_coord] = player
                else:
                    self._spaces[x_coord][y_coord] = player

    def get_space(self, row, col):
        """
        returns the contents of a space on the board
        :param row: Row number (first row is 0, last row is 17) Integer
        :param col: Col Number (first col is 0, last col is 17) Integer
        :return: None if space is unoccupied, Piece if occupied
        """
        return self._spaces[row][col]

    def set_space(self, row, col, piece = None):
        """
        fills a row with piece, which is defaulted to None
        :param row: Row number (first row is 0, last row is 17) Integer
        :param col: Col Number (first col is 0, last col is 17) Integer
        """
        self._spaces[row][col] = piece

    def get_spaces(self):
        """
        returns the entire 2 dimensional board array
        """
        return self._spaces

    def set_spaces(self, spaces):
        """
        replaces the entire 2 dimensional board array
        :param spaces: a 2 dimensional 18x18 array
        """
        self._spaces = spaces

    def get_player(self, player):
        """
        returns the Piece object being used as player1 or player2
        :param player: "player1" or "player2"
        :return: Piece corresponding to player1 or player2
        """
        return self._player1 if player == "player1" else self._player2

    def print(self):
        """
        prints the board
        :return:
        """
        count = 2
        print("1 ", [None for _ in range(0, 20)])
        for row in self._spaces:
            print(str(count) + " " if count < 10 else count, [None] + row + [None])
            count += 1
        print("20", [None for _ in range(0, 20)])
        letters = " "
        for letter in range(97, 117):
            letters += "     " + chr(letter)
        print(letters)

    def clear_spaces(self, row, col):
        """
        clears a 3x3 space on the board
        :param row: row Integer
        :param col: col Integer
        """
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if 0 <= i <= 17 and 0 <= j <= 17:
                    self.set_space(i, j)

    def replace_space(self, row, col, piece):
        """
        replaces the 3x3 square at row, col with the squares of piece
        :param row: row Integer
        :param col: col Integer
        :param piece: 3x3 array represnting a 3x3 block on the board
        """
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if 0 <= i <= 17 and 0 <= j <= 17:
                    self.set_space(i, j, piece[1 + i - row][1 + j - col])


class Piece:
    """
    represents the piece on the board either player1 or player2
    """

    def __init__(self, player):
        """
        set the name of the player to either "player1" or "player2"
        :param player: String
        """
        self._player = player

    def get_player(self):
        """
        return the player name
        """
        return self._player

    def __str__(self):
        """ visual representation of the player """
        return " X " if self._player == "player1" else "  O "

    def __repr__(self):
        """ visual representation of the player """
        return "  X " if self._player == "player1" else "  O "


class GessGame:
    """
    represents the main mechanics of the game Gess
    creates a board with pieces at starting points, state is unfinished
    game is won when a player resigns or captures all teh rings of the other player
    """
    def __init__(self):
        """
        creates a board, sets initial state, records initial rings, initial player is player1
        """
        # make 18 x 18 board
        self._board = Board()
        self._state = "UNFINISHED"
        self._rings = {
            "player1": ["k1"],
            "player2": ["k16"]
        }
        self._turn = "player1"

    def get_game_state(self):
        """
        :return: "UNFINISHED" | "BLACK_WON" | "WHITE_WON"
        """
        return self._state

    def get_board(self):
        """
        :return: the Board object
        """
        return self._board

    def resign_game(self):
        """
        allows a player to resign from the game
        :param player: "player1" or "player2" String
        """
        if self._turn == "player1":
            self._state = "WHITE_WON"
        else:
            self._state = "BLACK_WON"

    def make_move(self, old_loc, new_loc):
        """
        attempts to move a 3x3 piece from old_loc to new_loc
        :param old_loc: center space, ie "f1" String
        :param new_loc: center space, ie "f2" String
        :return: True if move is successful, False if not
        """
        if self._state != "UNFINISHED":
            return False
        # validate user input, if not given a 2-3 letter string w a letter followed by 2 digits return false
        if 2 > len(old_loc) > 3 or 2 > len(new_loc) > 3:
            return False
        if not old_loc[0].isalpha() or not new_loc[0].isalpha():
            return False
        if not old_loc[1:].isnumeric() or not new_loc[1:].isnumeric():
            return False
        return self.is_valid_move(old_loc, new_loc)

    def create_piece(self, loc):
        """
        :param loc: center location of a piece on the board
        :return: returns a 2d array representing the 3x3 gamepiece
        """
        row, col = self.get_row_col(loc)
        # initialize empty piece to all None items
        pieces = [[None for x in range(0, 3)] for x in range(0, 3)]
        # loop from 1 row below to 1 row above
        for i in range(-1, 2):
            # loop from 1 col to left to 1 col to right
            for j in range(-1, 2):
                # if the row is off the board or the col is off the board the square is None
                if row + i < 0 or row + i > 17 or col + j < 0 or col + j > 17:
                    pieces[i + 1][j + 1] = None
                else:
                    # piece contains piece on board
                    pieces[i + 1][j + 1] = self._board.get_space(row + i, col + j)
        return pieces

    @staticmethod
    def get_row_col(center):
        """
        returns the coordinates of a center adjusted from 20x20 representation of 18x18 board
        :param center: center ex f3, String
        :return: a tuple of the corresponding row, col
        """
        col = ord(center[0]) - 98
        row = int(center[1:]) - 2
        return row, col

    def get_piece_from_row_col(self, row, col):
        """
        takes row, col and transforms it to center string, calls create_piece to return piece
        :param row: row Integer
        :param col: col Integer
        :return: 3x3 game piece with the center piece being row, col
        """
        return self.create_piece(self.get_center_from_row_col(row, col))

    @staticmethod
    def get_center_from_row_col(row, col):
        return chr(col + 98) + str(row + 2)

    def is_valid_move(self, old_loc, new_loc):
        """
        determines if a players piece can move from the old_loc to new_loc
        :param old_loc: starting point String
        :param new_loc: ending point String
        :return: true if valid move false if not Boolean
        """
        # convert spaces to rows and col to work with array
        old_row, old_col = self.get_row_col(old_loc)
        new_row, new_col = self.get_row_col(new_loc)
        if old_row > 17 or old_row < 0:
            return False
        elif new_row > 17 or new_row < 0:
            return False
        elif old_col > 17 or old_col < 0:
            return False
        elif new_col > 17 or new_col < 0:
            return False
        # what direction piece is moving in (ie, "S" | "N", "E", "SE", etc)
        direction = self.determine_direction(old_row, old_col, new_row, new_col)
        # number of spaces piece is moving
        spaces = abs(new_row - old_row) if new_row != old_row else abs(new_col - old_col)
        # create an array of possible directions
        possible_directions = self.analyze_piece(self.create_piece(old_loc))
        # trying to move in a direction that is not allowed:
        if direction not in possible_directions:
            return False
        # moving more than 3 spots in center is not C:
        if "C" not in possible_directions:
            if spaces > 3:
                return False
        # trying to choose a spaces that contains the other player:
        if not self.piece_contains_only_player(self.create_piece(old_loc), self._turn):
            return False

        # doesnt destroy users only ring AND doesnt continue after hitting the first instance of other player
        if not self.successful_move(old_row, old_col, direction, spaces):
            return False

        return self.move_completed(old_loc, new_loc)

    def successful_move(self, old_row, old_col, direction, spaces):
        """
        determines if the piece can get from old_loc to new_loc without overlapping
        :param old_row: row of 3x3 Piece Integer
        :param old_col: col of 3x3 piece Integer
        :param direction: directin, ie "N" | "S" | "E", etc String
        :param spaces: amount of spaces to move
        :return: True if piece doesn't overlap, False if it does overlap
        """
        x_dir = y_dir = 0
        # determine how to move piece based on direction
        if "S" in direction:
            y_dir = +1
        if "E" in direction:
            x_dir = +1
        if "N" in direction:
            y_dir = -1
        if "W" in direction:
            x_dir = -1
        for space in range(spaces - 1):
            old_row += y_dir
            old_col += x_dir
            piece = self.get_piece_from_row_col(old_row, old_col)
            # if the piece has moved to a new location that contains the other player return false
            if self.pieces_overlap(piece, direction):
                return False
        return True

    def move_completed(self, loc1, loc2):
        """
        simulate move, determine if player is left without a ring, revert to old state if not a valid move
        :param loc1: starting center String
        :param loc2: ending center String
        :return: returns True if the move was made, False if not made
        """
        # make a copy of the current state (board and rings)
        old_board = list(self._board.get_spaces())
        old_rings = dict(self._rings)

        # get piece that is being move d
        piece = self.create_piece(loc1)

        # clear the piece being moved
        old_row, old_col = self.get_row_col(loc1)
        self._board.clear_spaces(old_row, old_col)

        # move the piece to the new center
        new_row, new_col = self.get_row_col(loc2)
        self._board.replace_space(new_row, new_col, piece)

        # update rings
        self.analyze_rings()

        # if the move leaves the current player with no rings, its not valid
        # revert state and return false
        if len(self._rings[self._turn]) == 0:
            self._board.set_spaces(old_board)
            self._rings = old_rings
            return False
        # move was valid, keep changes, toggle current player and return True
        self.toggle_turn()

        # check to see if other player is left with no rings
        if len(self._rings[self._turn]) == 0:
            if len(self._rings["player1"]) == 0:
                self._state = "WHITE_WON"
            else:
                self._state = "BLACK_WON"
        return True

    @staticmethod
    def determine_direction(row1, col1, row2, col2):
        """
        determines the direction of a move
        :param row1: y_coord of original center
        :param col1: x_coord of original center
        :param row2: y_coord of new center
        :param col2: x_coord of new center
        :return: direction that piece is moving (String)
        """
        if row2 > row1:
            if col1 == col2:
                return "S"
            if col2 > col1:
                return "SE"
            if col2 < col1:
                return "SW"
        elif row2 == row1:
            if col2 < col1:
                return "W"
            if col2 > col1:
                return "E"
        elif row2 < row1:
            if col1 == col2:
                return "N"
            if col2 < col1:
                return "NW"
            if col2 > col1:
                return "NE"

    @staticmethod
    def analyze_piece(piece):
        """
        creates a list of coordinates that are occupied in the piece
        :param piece: 3x3 piece that is being moved
        :return: a list of possible directions that the piece can move
        """
        cardinals = [
            ["NW", "N", "NE"],
            ["W",  "C",  "E"],
            ["SW", "S",  "SE"]
        ]
        directions = []
        for i in range(3):
            for j in range(3):
                if piece[i][j] is not None:
                    directions.append(cardinals[i][j])
        return directions

    @staticmethod
    def pieces_overlap(piece, direction):
        """
        determines if the next move will cause overlap
        :param piece: 3x3 Piece that would be next location
        :param direction: String "N" | "W" | "E"| "S"|
        :return: True if moving to loc results in overlap False if not
        """
        if "S" in direction:
            if piece[2].count(None) != 3:
                return True
        if "N" in direction:
            if piece[0].count(None) != 3:
                return True
        if "E" in direction:
            if [piece[0][2], piece[1][2], piece[2][2]].count(None) != 3:
                return True
        if "W" in direction:
            if [piece[0][0], piece[1][0], piece[2][0]].count(None) != 3:
                return True
        return False

    @staticmethod
    def piece_contains_only_player(piece, player):
        """
        make sure a 3x3 gamepiece only contains the current player
        :param piece: 3x3 array of pieces corresponding to a center on the board
        :param player: name of player ("player1" or "player2")
        :return: True if only current player False is mix
        """
        for i in range(3):
            for j in range(3):
                if piece[i][j] is not None:
                    if piece[i][j].get_player() != player:
                        return False
        return True

    def analyze_rings(self):
        """
        updates the rings on board
        """
        self._rings["player1"] = []
        self._rings["player2"] = []
        for i in range(0, 17):
            for j in range(0, 17):
                if self._board.get_space(i, j) is None:
                    center = chr(j + 98) + str(i + 2)
                    piece = self.get_piece_from_row_col(i, j)
                    directions = self.analyze_piece(piece)
                    if len(directions) == 8 and directions.count("C") == 0:
                        if self.piece_contains_only_player(piece, "player1"):
                            self._rings["player1"] += [center]
                        if self.piece_contains_only_player(piece, "player2"):
                            self._rings["player2"] += [center]

    def toggle_turn(self):
        """ toggle between player1 and player2 to simulate taking turns """
        if self._turn == "player1":
            self._turn = "player2"
        else:
            self._turn = "player1"

    def play_game(self):
        """
        allows two players to play the game on the command line
        """
        while self._state == "UNFINISHED":
            self._board.print()
            # print which player turn it is
            print(f"it is {self._turn}'s turn")
            # ask player if they want to resign
            giveup = input("Would you like to give up?")
            giveup = giveup.lower()
            if giveup == "y" or giveup == "yes":
                self.resign_game()
                break
            while True:
                # get start finish
                start = input("What space would you like to move?")
                end = input("Where would you like to move to?")
                # if move was valid break from loop
                if not self.make_move(start, end):
                    print("Sorry, that move was not valid")
                else:
                    break
        print(f"{self.get_game_state()}")
        print(self._rings)

