#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
:mod:`graphical_maze` module

:author: Coignion Tristan, Tayebi Ajwad, Becquembois Logan

:date:  15/11/2018

This module provides function which help display the maze from the Maze module in a window

Uses: 
    - maze.py
        - square.py (Dependancy)
    - tkinter
"""
from tkinter import * #pylint: disable=W0614
from maze import * #pylint: disable=W0614
from random import choice

CAN_WIDTH = 800
CAN_HEIGHT = 800
BG_COLOR = 'black'
GRID_COLOR = 'medium blue'
GOOD_CELL_COLOR = "yellow"
BAD_CELL_COLOR = "crimson"
CIRCLE_SCALE = 0.6
RECTANGLE_SCALE = 0.8


def draw_circle(canvas, event):
    """
    Draws a circle of ray 5 at the location of `event` on the `canvas`
    """
    ray = 5
    x, y = event.x, event.y
    canvas.create_oval(x - ray, y - ray,
                       x + ray, y + ray,
                       fill = 'red')
    canvas.update()
    
def draw_grid(canvas, width, height, can_width=CAN_WIDTH, can_height=CAN_HEIGHT):
    """
    Draws a grid on the `canvas`. The dimensions of the grid are `width` and `height`.
    The dimensions of the canvas are `can_width` and `can_height` and are by default
    `CAN_WIDTH` and `CAN_HEIGHT`
    """
    DX = can_width // width # Width of a square
    DY = can_height // height
    for y in range(height):
        for x in range(width):
            canvas.create_line(x * DX, y * DY,
                               (x + 1) * DX, y * DY,
                               fill=GRID_COLOR, width=1)
            canvas.create_line(x * DX, y * DY,
                               x * DX, (y + 1) * DY,
                               fill=GRID_COLOR, width=1)
    canvas.create_line(0, height * DY - 1,  width * DX - 1, height * DY - 1,
                       fill=GRID_COLOR, width=1)
    canvas.create_line(width * DX - 1, 0,  width * DX - 1, height * DY - 1,
                       fill=GRID_COLOR, width=1)
    
def random_word(filename):
    """
    returns a random word taken from a file `filename`

    :param filename: (str) the words have to be separated by backspaces
    :return: (str) a word
    """
    with open(filename, 'r') as stream:
        lines = stream.readlines()
        
    return choice(lines).rstrip('\n')

def remove_wall(canvas, x, y, side, width, height, can_width=CAN_WIDTH, can_height=CAN_HEIGHT):
    """
    removes a wall from a side of a cell on the canvas

    :param canvas: (Canvas)
    :param x, y: (int) the coordinates of the cell
    :side: (str) the side we want to remove, must be "Left" or "Top"
    :param width: (int) the width of the maze
    :param height: (int) the height of the maze
    :param can_width: (int) the width of the canvas
    :param can_height: (int) the height of the canvas
    :side-effect: removes a line from the canvas
    :return: None
    :UC: 0<=x<=width-1, 0<=y<=height-1
    """
    DX = can_width // width # This is the width of a square
    DY = can_height // height # This is the height of a square
    if side == "Left":
        canvas.create_line(x * DX, y * DY, (x) * DX, (y + 1) * DY, fill=BG_COLOR, width=1)
    if side == "Top":
        canvas.create_line(x * DX, y * DY, (x+1) * DX, y * DY, fill=BG_COLOR, width=1)

def setup_wall(canvas, maze, can_width=CAN_WIDTH, can_height=CAN_HEIGHT):
    """
    removes all the walls of the graphical maze according to the ones on the maze object

    :param canvas: (Canvas)
    :param maze: (Maze)
    :param can_width: (int) the width of the canvas
    :param can_height: (int) the height of the canvas
    :side effect: removes lines from the canvas
    :return: None
    :UC: None
    """
    height = maze.get_height()
    width = maze.get_width()
    for y in range(height):
        for x in range(width):
            cell = maze.get_square(x, y)
            if not cell.has_left_rampart():
                remove_wall(canvas, x, y, "Left", width, height, can_width, can_height)
            if not cell.has_top_rampart():
                remove_wall(canvas, x, y, "Top", width, height, can_width, can_height)

def set_circle(canvas, width, height, x, y, can_width=CAN_WIDTH, can_height=CAN_HEIGHT, fill_color = GOOD_CELL_COLOR, scale=CIRCLE_SCALE):
    """
    draws a circle on the cell of coordinates (x,y)

    :param canvas: (Canvas)
    :param x,y: (int) the coordinates of the cell
    :param width: (int) the width of the maze
    :param height: (int) the height of the maze
    :param can_width: (int) the width of the canvas
    :param can_height: (int) the height of the canvas
    :param fill_color: (str) [default = GOOD_CELL_COLOR] the color of the circle
    :param scale: (int) [default = CIRCLE_SCALE] the scale of the circle
    :side-effect: draws a circle
    :return: None
    :UC: 0<=x<=width-1, 0<=y<=height-1 0<= scale <= 1
    """
    DX = can_width // width 
    DY = can_height // height 
    scale = scale/2 + 0.5
    canvas.create_oval(DX*(x+scale), DY*(y+scale),
                       DX*(x+1-scale), DY*(y+1-scale),
                       fill = fill_color)

def remove_circle(canvas, width, height, x, y, can_width=CAN_WIDTH, can_height=CAN_HEIGHT, fill_color=BG_COLOR, scale=CIRCLE_SCALE):
    """
    Removes a circle of the canvas by making its color the same as the background's

    :param canvas: (Canvas)
    :param x,y: (int) the coordinates of the cell
    :param width: (int) the width of the maze
    :param height: (int) the height of the maze
    :param can_width: (int) the width of the canvas
    :param can_height: (int) the height of the canvas
    :param fill_color: (str) [default = BG_COLOR] the color of the circle
    :param scale: (int) [default = CIRCLE_SCALE] the scale of the circle
    :side-effect: erase a circle
    :return: None
    :UC: 0<=x<=width-1, 0<=y<=height-1  0<= scale <= 1
    """
    set_circle(canvas, width, height, x, y, can_width=can_width, can_height=can_height, fill_color=fill_color, scale=scale)
    
def set_bad_cell(canvas, width, height, x, y, can_width=CAN_WIDTH, can_height=CAN_HEIGHT, fill_color=BAD_CELL_COLOR, scale=RECTANGLE_SCALE):
    """
    Draws a cell as a cell which doesn't lead to the exit

    :param canvas: (Canvas)
    :param x,y: (int) the coordinates of the cell
    :param width: (int) the width of the maze
    :param height: (int) the height of the maze
    :param can_width: (int) the width of the canvas
    :param can_height: (int) the height of the canvas
    :param fill_color: (str) [default = BAD_CELL_COLOR] the color of the cell
    :param scale: (int) [default = RECTANGLE_SCALE] the scale of the square
    :side-effect: Draws a square on the cell
    :return: None
    :UC: 0<=x<=width-1, 0<=y<=height-1 0<= scale <= 1
    """
    scale = scale/2 + 0.5
    DX = can_width // width # This is the width of a square
    DY = can_height // height # This is the height of a square
    canvas.create_rectangle(DX*(x+scale), DY*(y+scale),
                            DX*(x+1-scale), DY*(y+1-scale),
                            fill = fill_color)

def remove_bad_cell(canvas, width, height, x, y, can_width=CAN_WIDTH, can_height=CAN_HEIGHT, fill_color=BG_COLOR, scale=RECTANGLE_SCALE):
    """
    Erase a cell as a cell which doesn't lead to the exit

    :param canvas: (Canvas)
    :param x,y: (int) the coordinates of the cell
    :param width: (int) the width of the maze
    :param height: (int) the height of the maze
    :param can_width: (int) the width of the canvas
    :param can_height: (int) the height of the canvas
    :param fill_color: (str) [default = BG_COLOR] the color of the cell
    :param scale: (int) [default = RECTANGLE_SCALE] the scale of the square
    :side-effect: Draws a square on the cell
    :return: None
    :UC: 0<=x<=width-1, 0<=y<=height-1 0<= scale <= 1
    """
    set_bad_cell(canvas, width, height, x, y, can_width=can_width, can_height=can_height, fill_color=fill_color, scale=scale)

def create_canvas(win, adjusted_can_width, adjusted_can_height):
    """
    Creates and returns a canvas with a scrolling bar

    :param win: (Window) A tkinter window parent to the canvas
    :param adjusted_can_width: (int) the width of the canvas
    :param adjusted_can_height: (int) the height of the canvas
    """
    can = Canvas(win, bg=BG_COLOR, width=adjusted_can_width, height=adjusted_can_height)
    can.bind('<Button-1>',
            lambda event: draw_circle(can, event))

    defilY = Scrollbar(win, orient="vertical", command=can.yview)
    defilY.pack(side="right")
    defilX = Scrollbar(win, orient="horizontal", command=can.xview)
    defilX.pack(side="bottom")

    can["yscrollcommand"] = defilY.set
    can["xscrollcommand"] = defilX.set
    can.pack(fill="both", expand=True) # Allows the canvas to be handled as grid and columns
    return can