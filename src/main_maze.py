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
SAVE_PATH = "../mazes/"

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
    width.set("20")
    height = StringVar(winset)
    height.set("20")
    widthEntry = Entry(winset, textvariable=width, state="normal")
    heightEntry = Entry(winset, textvariable=height, state="normal")
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


    title.grid(row = 0, column = 0, padx=10) # Places the label in the grid
    exitButton.grid(row=100, column=0)
    okButton.grid(row=100, column=1)

    genLabel.grid(row = 10, column = 0, pady=(10, 0))
    handgenCheck.grid(row = 11, column = 0)
    textgenCheck.grid(row = 12, column = 0)
    randomgenCheck.grid(row = 13, column = 0)

    saveLabel.grid(row = 10, column = 1, pady=(10, 0))
    saveCheck.grid(row = 11, column = 1)
    saveresCheck.grid(row = 12, column = 1)
    savehtmlCheck.grid(row = 13, column = 1)

    widthLabel.grid(row=20, column=0, pady=(10, 0))
    widthEntry.grid(row=20, column=1, pady=(10, 0))
    heightLabel.grid(row=21, column=0)
    heightEntry.grid(row=21, column=1)

    fileLabel.grid(row=22, column=0, padx=(10,0))
    fileEntry.grid(row=22, column=1)
    fileButton.grid(row=22, column=2)

    graphicLabel.grid(row = 30, column = 0, pady=(10, 0))
    graphicCheck.grid(row = 31, column = 0)
    graphicresCheck.grid(row = 32, column = 0 )
    dynamicCheck.grid(row = 33, column = 0)


    winset.mainloop()
    return (width.get(), height.get(), filename.get(), varGen.get(), 
            is_save.get(), is_saveres.get(), is_savehtml.get(),
            is_graphic.get(), is_graphicres.get(), is_dynamic.get())

def parse_gen(width, height, filepath, varGen):
    """
    """
    if varGen == 1:
        maze = Maze().build_maze_from_text(filepath)
    else:
        try:
            width = int(width)
            height = int(height)
        except TypeError:
            raise TypeError("The width and height are not of the correct type !")
        if varGen == 2:
            maze = Maze().random_generation(width, height)
        else:
            # maze = Maze.hand_generation() #TODO
            pass
    return maze

def parse_save(maze, is_save, is_saveres, is_savehtml):
    """
    """
    if is_save:
        maze.text_representation(SAVE_PATH+"maze.txt")
    if is_saveres:
        # maze.text_representation(SAVE_PATH+"maze_res.txt", res=True)
        pass
    if is_savehtml:
        maze.picture_representation(SAVE_PATH+"maze_html.html")

def graph_disp(maze, is_graphicres, is_dynamic):
    """
    """
    width = maze.get_width()
    height = maze.get_height()
    win = Tk() # Creates a window object
    win.title(random_word('../ressources/anagrams.txt')) # DEBUG is only valid is Visual Code
    can = Canvas(win, bg=BG_COLOR, width=CAN_WIDTH, height=CAN_HEIGHT)
    can.bind('<Button-1>',
            lambda event: draw_circle(can, event))
    can.pack() # Allows the canvas to be handled as grid and columns
    draw_grid(can, width, height) 
    setup_wall(can, maze)
    if is_graphicres:
        if is_dynamic:
            pass
            # Display all the resolution progressively
        else:
            pass
            # Display all the resolution in one go
    win.mainloop()

def main():
    """
    """
    setup_var = setup_window()
    width, height, filepath, varGen, is_save, is_saveres, is_savehtml, is_graphic, is_graphicres, is_dynamic = setup_var
    
    maze = parse_gen(width, height, filepath, varGen)

    parse_save(maze, is_save, is_saveres, is_savehtml)

    if is_graphic:
        graph_disp(maze, is_graphicres, is_dynamic)

    
if __name__ == '__main__':
    main()
