#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
:script:`main_maze` script

:author: Coignion Tristan, Tayebi Ajwad, Becquembois Logan

:date:  22/11/2018

This script is used to display a maze on a screen

Uses: 
    - graphical_maze
        - tkinter
        - maze.py
            - square.py (Dependancy)
"""
from graphical_maze import * #pylint: disable=W0614
from maze import Maze, CreationError
from tkinter import * #pylint: disable=W0614
from tkinter import filedialog
from functools import partial
import os

SETUP_WIDTH = 800
SETUP_HEIGHT = 600

global filename # global variable

def toggle_check(elems):
    """
    Toggles the state of a Tkinter item on the window

    :param elems: (list) a list of the items to toggle
    :side effect: sets the state of the objects to `disable` or `normal`
    :return: None
    """
    for elem in elems:
        if elem["state"] == "normal":
            elem["state"] = 'disabled'
        else:
            elem["state"] = "normal"

def toggle_state_on(elems):
    """
    toggles on the state of a Tkinter item on the window

    :param elems: (list) a list of items to activate
    :side effect: sets the state of the objects to `normal`
    :return: None
    """
    for elem in elems:
        elem["state"] = "normal"

def toggle_state_off(elems):
    """
    toggles off the state of a Tkinter item on the window

    :param elems: (list) a list of items to activate
    :side effect: sets the state of the objects to `disabled`
    :return: None
    """
    for elem in elems:
        elem["state"] = "disabled"

def strip_filename(c):
    """
    """
    c = c.lstrip("<_io.TextIOWrapper name='")
    c = c.rstrip("' mode='r' encoding='UTF-8'>")
    return c

def askfile():
    """
    asks the user for a file and stores the result in filename
    """
    global filename
    print("test")
    filename.set((filedialog.askopenfile(initialdir = os.getcwd(), title = "Select a txt file", filetypes = (("text file","*.txt"),("all files","*.*")))))
    filename.set(strip_filename(filename.get()))
    if filename.get() != None:
        print("This file has been selected", filename.get())


def setup_window():
    """
    Opens a window for the user to input parameters and then returns those parameters
    """
    winset = Tk()
    winset.title("Maze setup")
    title = Label(winset, text="Please, select options in order to continue")
    exitButton = Button(winset, text='Exit', command=quit)
    okButton = Button(winset, text="OK", command=winset.destroy)

    widthLabel = Label(winset, text="Width of the maze (integer)")
    heightLabel = Label(winset, text="Height of the maze (integer)")
    width = StringVar(winset)
    height = StringVar(winset)
    widthEntry = Entry(winset, textvariable=width, state="disabled")
    heightEntry = Entry(winset, textvariable=height, state="disabled")
    fileLabel = Label(winset, text="Generate from which file ? ")
    global filename
    filename = StringVar(winset)
    fileEntry = Entry(winset, textvariable=filename, state="normal")
    fileButton = Button(winset, text="Browse", command=askfile)

    genLabel = Label(winset, text="Generation Options (Chose only one)")
    varGen = IntVar()
    varGen.set(2)
    handgenCheck = Radiobutton(winset, variable=varGen, value=0, text="Hand generation", command=partial(toggle_state_on, [widthEntry, heightEntry]))
    textgenCheck = Radiobutton(winset, variable=varGen, value=1, text="Generate from text file", command=partial(toggle_state_off, [widthEntry, heightEntry]))
    randomgenCheck = Radiobutton(winset, variable=varGen, value=2, text="Generate randomly", command=partial(toggle_state_on, [widthEntry, heightEntry]))

    saveLabel = Label(winset, text="Save Options")
    is_save = IntVar(winset, 1)
    saveCheck = Checkbutton(winset, variable= is_save, text="Save into a file")
    is_saveres = IntVar(winset, 0)
    saveresCheck = Checkbutton(winset, variable= is_saveres, text="Save into a file with the resolution")
    is_savehtml = IntVar(winset, 0)
    savehtmlCheck = Checkbutton(winset, variable= is_savehtml, text="Save into a html file")

    graphicLabel = Label(winset, text="Graphic Options")
    is_graphicres = IntVar(winset, 1)
    graphicresCheck = Checkbutton(winset, variable=is_graphicres, text="Display the resolution on the maze")
    is_dynamic = IntVar(winset, 1)
    dynamicCheck = Checkbutton(winset, variable=is_dynamic, text="Display the resolution dynamically")
    is_graphic = IntVar(winset, 1)
    graphicCheck = Checkbutton(winset, variable=is_graphic, text="Display the maze on a window", command=partial(toggle_check, [graphicresCheck, dynamicCheck]))


    title.grid(row = 0, column = 0, padx=10) # Positions the label in the grid
    exitButton.grid(row=12, column=0)
    okButton.grid(row=12, column=1)
    widthLabel.grid(row=1, column=0, pady=(10, 0))
    widthEntry.grid(row=1, column=1, pady=(10, 0))
    heightLabel.grid(row=2, column=0)
    heightEntry.grid(row=2, column=1)

    genLabel.grid(row = 3, column = 0, pady=(10, 0))
    handgenCheck.grid(row = 4, column = 0)
    textgenCheck.grid(row = 5, column = 0)
    randomgenCheck.grid(row = 6, column = 0)

    saveLabel.grid(row = 3, column = 1, pady=(10, 0))
    saveCheck.grid(row = 4, column = 1)
    saveresCheck.grid(row = 5, column = 1)
    savehtmlCheck.grid(row = 6, column = 1)

    graphicLabel.grid(row = 7, column = 0, pady=(10, 0))
    graphicCheck.grid(row = 8, column = 0)
    graphicresCheck.grid(row = 9, column = 0 )
    dynamicCheck.grid(row = 10, column = 0)


    fileLabel.grid()
    fileEntry.grid()
    fileButton.grid()

    winset.mainloop()
    return (width.get(), height.get(), filename.get(), varGen.get(), 
            is_save.get(), is_saveres.get(), is_savehtml.get(),
            is_graphic.get(), is_graphicres.get(), is_dynamic.get())

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

def new_main(width, height, varGen, is_save, is_saveres, is_savehtml, is_graphic, is_graphicres, is_dynamic):
    pass

    
if __name__ == '__main__':
    # We shall parse command line arguments here
    # HERE We shall build a maze according to some arguments we have passed in the command line

    setup_var = setup_window()
    width, height, filepath, varGen, is_save, is_saveres, is_savehtml, is_graphic, is_graphicres, is_dynamic = setup_var
    print(setup_var)

    maze = Maze().build_maze_from_text(filepath) #DEBUG
    main(maze)
