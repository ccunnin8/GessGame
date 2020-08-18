# Author: Corey Cunningham
# Date: 06-11-2020
# Description: Create a GUI implementation of Gess Game

import pygame
import sys

from GessGame import GessGame

# COLORS
brown = 123, 72, 45
blue = 0, 0, 255
green = 0, 255, 0
black = 0, 0, 0
white = 255, 255, 255

# SIZES
size = width, height = 550, 600
square_size = 20
offset_x = (width - 20 * square_size) // 2
offset_y = (height - 20 * square_size) // 2

# INITIALIZE
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Gess Game")
background = pygame.image.load("background.jpeg").convert()
game = GessGame()

# add text/background
# screen.fill(blue)
screen.blit(background, (0, 0), (0, 0, width, height))
screen.fill(brown, (offset_x, offset_y, 20 * square_size, 20 * square_size))
# screen.fill(brown)
font = pygame.font.SysFont(None, 24)
title = font.render("Gess Game", True, white)
player = font.render("BLACK'S TURN", True, white)
screen.blit(player, ((width - player.get_width()) / 2, 40))
screen.blit(title, (20, 20))
pygame.display.update()


def print_board(canvas, margin_x, margin_y, square_width):
    """
    displays the board
    :param canvas: screen object
    :param margin_x: margin x
    :param margin_y: margin y
    :param square_width: size of each square
    """
    radius = square_width / 2.3
    center_circle = square_width / 2
    board = game.get_board()
    spaces = board.get_spaces()
    col_label = 65
    row_label = 1

    # create labels for columns
    for x in range(20):
        label = font.render(chr(col_label), True, white)
        canvas.blit(label, (margin_x + 5 + square_width * x, margin_y - square_width))
        col_label += 1
    # print first row label
    label = font.render(str(row_label), True, white)
    canvas.blit(label, (margin_x - (square_width / 2), margin_y + 2))
    row_label += 1
    # print empty row (row 1)
    for x in range(20):
        pygame.draw.rect(canvas, black, (margin_x + (square_width * x), margin_y, square_width, square_width), 1)
    margin_y += square_width

    for index_row, board_row in enumerate(spaces):
        left = margin_x
        top = margin_y + (index_row * square_width)
        # draw initial square (col a)
        pygame.draw.rect(canvas, black, (left, top, square_width, square_width), 1)
        label = font.render(str(row_label), True, white)
        canvas.blit(label, (left - square_width if row_label >= 10 else left - (square_width / 2), top + 2))
        # draw cols b - s
        for index_col, board_col in enumerate(spaces):
            left += square_width
            fill = black
            border = 1
            space = board.get_space(index_row, index_col)
            pygame.draw.rect(canvas, fill, (left, top, square_width, square_width), border)
            # if the space is occupied draw a black or white piece depending on who owns the piece
            if space is not None:
                if space.get_player() == "player1":
                    fill = black
                else:
                    fill = white
                center = (left + center_circle, top + center_circle)
                pygame.draw.circle(canvas, fill, center, radius)
        # draw square for col t
        row_label += 1
        left += square_width
        pygame.draw.rect(canvas, black, (left, top, square_width, square_width), 1)
    margin_y += square_width * 18
    # last row label
    label = font.render(str(row_label), True, white)
    canvas.blit(label, (margin_x - square_width, margin_y + 2))
    for x in range(20):
        pygame.draw.rect(canvas, black, (margin_x + (square_width * x), margin_y, square_width, square_width), 1)


def convert_coords(loc, margin_x, margin_y, square_width):
    x, y = loc
    if margin_x < x < margin_x + (square_width * 20) and margin_y < y < margin_y + (square_width * 20):
        col = (x - margin_x) // square_width - 1
        row = (y - margin_y) // square_width - 1
        return row, col
    return None


def rerender(invalid=False):
    """
    redraw the board and pieces
    """
    screen.blit(background, (0, 0), (0, 0, width, height))
    screen.fill(brown, (offset_x, offset_y, 20 * square_size, 20 * square_size))
    screen.blit(title, (20, 20))
    if game.get_turn() == "player1":
        turn = font.render("BLACK'S TURN", True, white)
    else:
        turn = font.render("WHITE'S TURN", True, white)
    screen.blit(turn, ((width - turn.get_width()) / 2, 40))
    print_board(screen, offset_x, offset_y, square_size)
    if invalid:
        invalid = font.render("That move was not valid, please try again", True, white)
        screen.blit(invalid, ((width - invalid.get_width()) / 2, height - 50))
    pygame.display.update()


print_board(screen, offset_x, offset_y, square_size)
pygame.display.update()
start = end = None

# GAME LOOP
while 1:
    invalid = False
    for event in pygame.event.get():
        # quit if user exits
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # if the user clicks after the game has been finished, start the game up again
            if game.get_game_state() != "UNFINISHED":
                game = GessGame()
                rerender()
                break
            pressed = pygame.mouse.get_pos()
            # if the user clicks on the board get the x, y location of mouse click and convert to row, col on board
            coords = convert_coords(pressed, offset_x, offset_y, square_size)
            if coords is not None:
                row, col = coords
                if start is None:
                    # screen.fill(brown, (0, height - 75, width, height))
                    screen.blit(background, (0, height - 75), (0, height - 75, width, height))
                    start = game.get_center_from_row_col(row, col)
                    start_text = font.render(f"Start: {start}", True, white)
                    screen.blit(start_text, (width / 2 - 35, height - 50))
                    test = start_text.get_rect()
                    pygame.display.update()
                # allow user to reclick the same center to choose a different move
                elif start == game.get_center_from_row_col(row, col):
                    start = None
                    rerender()
                else:
                    # try to make the move, reset start and end, rerender
                    end = game.get_center_from_row_col(row, col)
                    # if the move wasn't valid let the user know
                    if not game.make_move(start, end):
                        invalid = True
                    start = None
                    end = None
                    rerender(invalid)
        if game.get_game_state() != "UNFINISHED":
            winner = game.get_game_state()
            if winner == "BLACK_WON":
                winner_text = "CONGRATULATIONS BLACK"
            else:
                winner_text = "CONGRATULATIONS WHITE"
            screen.blit(background, (0, 0), (0, 0, width, height))
            winner = font.render(winner_text, True, white)
            screen.blit(winner, ((width - winner.get_width()) / 2, height / 2))
            pygame.display.update()





