#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
:script:`graphical_maze` script

:author: Coignion Tristan, Tayebi Ajwad, Becquembois Logan

:date:  15/11/2018

This script is used to display a Graphical interface of the Maze

Uses: 
    - maze.py
        - square.py (Dependancy)
    - tkinter
"""
from tkinter import *
from maze import *
from random import choice

CAN_WIDTH = 800
CAN_HEIGHT = 800
BG_COLOR = 'black'
GRID_COLOR = 'yellow'


def draw_circle(canvas, event):
    ray = 5
    x, y = event.x, event.y
    canvas.create_oval(x - ray, y - ray,
                       x + ray, y + ray,
                       fill = 'red')
    canvas.update()
    
def draw_grid(canvas, width, height):
    DX = CAN_WIDTH // width # Width of a square
    DY = CAN_HEIGHT // height
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

def remove_wall(canvas, x, y, side, width, height):
    """
    removes a wall from a side of a cell on the canvas

    :param canvas: (Canvas)
    :param x, y: (int) the coordinates of the cell
    :side: (str) the side we want to remove, must be "Left" or "Top"
    :side-effect: removes a line from the canvas
    :return: None
    :UC: 0<=x<=width-1, 0<=y<=height-1
    """
    DX = CAN_WIDTH // width # This is the width of a square
    DY = CAN_HEIGHT // height # This is the height of a square
    if side == "Left":
        canvas.create_line(x * DX, y * DY, (x) * DX, (y + 1) * DY, fill=BG_COLOR, width=1)
    if side == "Top":
        canvas.create_line(x * DX, y * DY, (x+1) * DX, y * DY, fill=BG_COLOR, width=1)

def setup_wall(canvas, maze):
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
            cell = maze.get_cell(x, y)
            if not cell.has_leftRampart():
                remove_wall(canvas, x, y, "Left", width, height)
            if not cell.has_topRampart():
                remove_wall(canvas, x, y, "Top", width, height)

def set_circle(canvas, width, height, x, y):
    """
    draws a circle on the cell of coordinates (x,y)

    :param canvas: (Canvas)
    :param x,y: (int) the coordinates of the cell
    :side-effect: draws a circle
    :return: None
    :UC: 0<=x<=width-1, 0<=y<=height-1
    """
    DX = CAN_WIDTH // width 
    DY = CAN_HEIGHT // height 
    canvas.create_oval(x*DX*1.02, y*DY*0.98,
                       (x+1)*DX*0.98, (y-1)*DY*1.02,
                       fill = "red")
    
def set_bad_cell(canvas, width, height, x, y):
    """
    TODO: change the name of the function

    Sets the cell as a cell which doesn't lead to the exit

    :param canvas: (Canvas)
    :param x,y: (int) the coordinates of the cell
    :side-effect: Does something on the cell
    :return: None
    :UC: 0<=x<=width-1, 0<=y<=height-1
    """
    DX = CAN_WIDTH // width # This is the width of a square
    DY = CAN_HEIGHT // height # This is the height of a square
    canvas.create_rectangle(x*DX+1, y*DY-1,
                         (x+1)*DX-1, (y+1)*DY+1,
                         fill = "gray")

def main(maze):
    maze_width = maze.get_width()
    maze_height = maze.get_height()
    win = Tk() # Creates a window object
    win.title(random_word('ressources/anagrams.txt')) # DEBUG is only valid is Visual Code
    can = Canvas(win, bg=BG_COLOR, width=CAN_WIDTH, height=CAN_HEIGHT)
    can.bind('<Button-1>',
             lambda event: draw_circle(can, event))
    can.pack() # Allows the canvas to be handled as grid and columns
    draw_grid(can, maze_width, maze_height) 
    setup_wall(can, maze)
    win.mainloop()
    
if __name__ == '__main__':
    # We shall parse command line arguments here
    # HERE We shall build a maze according to some arguments we have passed in the command line
    maze = Maze().build_maze_from_text("Test/TestMaze/maze_20_20_0.txt") #DEBUG
    main(maze)