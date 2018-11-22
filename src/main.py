#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
:script:`graphical_maze` script

:author: Coignion Tristan, Tayebi Ajwad, Becquembois Logan

:date:  15/11/2018

This script is used to display a Graphical interface of the Maze

Uses: 
    - graphical_maze
        - maze.py
            - square.py (Dependancy)
    - tkinter
"""
from graphical_maze import * #pylint: disable=W0614

def main(maze):
    maze_width = maze.get_width()
    maze_height = maze.get_height()
    win = Tk() # Creates a window object
    win.title(random_word('../ressources/anagrams.txt')) # DEBUG is only valid is Visual Code
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
    maze = Maze().build_maze_from_text("../Test/TestMaze/maze_20_20_0.txt") #DEBUG
    main(maze)
