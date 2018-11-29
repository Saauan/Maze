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


def draw_circle(canvas, event):
    ray = 5
    x, y = event.x, event.y
    canvas.create_oval(x - ray, y - ray,
                       x + ray, y + ray,
                       fill = 'red')
    canvas.update()
    
def draw_grid(canvas, width, height, can_width=CAN_WIDTH, can_height=CAN_HEIGHT):
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
    :side effect: removes lines from the window
    :return: None
    :UC: the maze must be the same dimensions as the canvas
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

def set_circle(canvas, width, height, x, y, can_width=CAN_WIDTH, can_height=CAN_HEIGHT, fill_color = GOOD_CELL_COLOR):
    """
    draws a circle on the cell of coordinates (x,y)

    :param canvas: (Canvas)
    :param x,y: (int) the coordinates of the cell
    :side-effect: draws a circle
    :return: None
    :UC: 0<=x<=width-1, 0<=y<=height-1
    """
    DX = can_width // width 
    DY = can_height // height 
    canvas.create_oval((x*DX)+5, (y+1)*DY-5,
                       (x+1)*DX-5, (y)*DY+5,
                       fill = fill_color)

def remove_circle(canvas, width, height, x, y, can_width=CAN_WIDTH, can_height=CAN_HEIGHT, fill_color=BG_COLOR):
    """
    Removes a circle of the canvas by making its color the same as the background's
    """
    set_circle(canvas, width, height, x, y, can_width=CAN_WIDTH, can_height=CAN_HEIGHT, fill_color = BG_COLOR)
    
def set_bad_cell(canvas, width, height, x, y, can_width=CAN_WIDTH, can_height=CAN_HEIGHT):
    """
    TODO: change the name of the function

    Sets the cell as a cell which doesn't lead to the exit

    :param canvas: (Canvas)
    :param x,y: (int) the coordinates of the cell
    :side-effect: Does something on the cell
    :return: None
    :UC: 0<=x<=width-1, 0<=y<=height-1
    """
    DX = can_width // width # This is the width of a square
    DY = can_height // height # This is the height of a square
    canvas.create_rectangle(x*DX+5, y*DY+5,
                         (x+1)*DX-5, (y+1)*DY-5,
                         fill = BAD_CELL_COLOR)