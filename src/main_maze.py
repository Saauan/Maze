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
import time

SETUP_WIDTH = 800
SETUP_HEIGHT = 600
SAVE_PATH = "../mazes/"
SPEED_VALUES = {"Very Slow": 1,
                "Slow" : 0.5,
                "Normal" : 0.2,
                "Fast" : 0.1,
                "Very Fast" : 0.05,
                "Extremely Fast" : 0.01,
                "GOTTA GO FAST M8" : 0.001}

global g_filename # global variable
global is_disp_res # True if the res is currently displayed, False otherwise
is_disp_res = False

####################
# SETUP FUNCTIONS #
####################

def invert_state(elems):
    """
    Toggles the state of a Tkinter Widget on the window

    :param elems: (list) a list of the Widget to toggle
    :side effect: Inverts the state of the Widgets from `disabled` to `normal` and vice-versa
    :return: None
    :UC: None
    :Examples:

    >>> root = Tk()
    >>> root.withdraw()
    ''
    >>> someObject = Button(root, state="normal")
    >>> anotherObject = Entry(root, textvariable="test", state="disabled")
    >>> invert_state([someObject, anotherObject])
    >>> someObject["state"] == "disabled"
    True
    >>> anotherObject["state"] == "normal"
    True
    """
    for elem in elems:
        if elem["state"] == "normal":
            elem["state"] = 'disabled'
        else:
            elem["state"] = "normal"

def toggle_state_on(elems):
    """
    Toggles on the state of a Tkinter Widget on the window

    :param elems: (list) a list of Widget to activate
    :side effect: sets the state of the Widget to `normal`
    :return: None
    :UC: None
    :Examples:

    >>> root = Tk()
    >>> root.withdraw()
    ''
    >>> someObject = Button(root, state="normal")
    >>> anotherObject = Entry(root, textvariable="test", state="disabled")
    >>> toggle_state_on([someObject, anotherObject])
    >>> someObject["state"] == "normal"
    True
    >>> anotherObject["state"] == "normal"
    True
    """
    for elem in elems:
        elem["state"] = "normal"

def toggle_state_off(elems):
    """
    Toggles off the state of a Tkinter Widget on the window

    :param elems: (list) a list of Widgets to activate
    :side effect: sets the state of the Widget to `disabled`
    :return: None
    :UC: Widget of elems must have a state attributes
    :Examples:

    >>> root = Tk()
    >>> root.withdraw()
    ''
    >>> someObject = Button(root, state="normal")
    >>> anotherObject = Entry(root, textvariable="test", state="disabled")
    >>> toggle_state_off([someObject, anotherObject])
    >>> someObject["state"] == "disabled"
    True
    >>> anotherObject["state"] == "disabled"
    True
    """
    for elem in elems:
        elem["state"] = "disabled"

def askfile():
    """
    Asks the user for a file and stores the result in the global variable `g_filename`
    
    :return: (str) an absolute path for a file chosen by the user
    :UC: `g_filename` must be a global variable
    """
    global g_filename
    temp_filename = str((filedialog.askopenfile(initialdir = os.getcwd(), title = "Select a txt file", filetypes = (("text file","*.txt"),("all files","*.*")))))
    temp_filename = temp_filename.lstrip("<_io.TextIOWrapper name='") #pylint: disable=E1310
    i = temp_filename.index(" mode='r'")
    g_filename.set(temp_filename[:i-1])

    # g_filename.set(strip_name(temp_filename, "<_io.TextIOWrapper name='", "' mode='r' encoding='UTF-8'>"))
    if g_filename.get() != None:
        print("This file has been selected", g_filename.get())

def toggleonoff(elemon, elemoff):
    """
    Sets the state of the Widgets of elemoff to `disabled` and of the elements of elemon to `normal`
    
    :param elemon: (tuple) tuple of tkinter Widgets to make normal
    :param elemoff: (tuple) tuple of tkinter Widgets to disable
    :side effect: See the description above
    :return: None
    :UC: None
    :Example:

    >>> root = Tk()
    >>> root.withdraw()
    ''
    >>> someObject = Button(root, state="normal")
    >>> anotherObject = Entry(root, textvariable="test", state="disabled")
    >>> toggleonoff([anotherObject], [someObject])
    >>> someObject["state"] == "disabled"
    True
    >>> anotherObject["state"] == "normal"
    True
    """
    toggle_state_on(elemon)
    toggle_state_off(elemoff)

def setup_winentries(winset, default_width, default_height, default_path):
    """
    Returns the entries Widget sused for the setup_window.
    These includes:
        * Entries and Labels for the width and height
        * Entry, label and button for the file's path

    :param winset: (Tk) a window
    :param default_width: (int) The default width for the maze
    :param default_height: (int) The default height for the maze
    :param default_path: (str) The default path for the file
    :return: (Label, Label, StringVar, StringVar, Entry, Entry, Label, str, Entry, Button)
    width Label, height Label, width , height, width Entry, height Entry, fileLabel, the file's path, file Entry, the browse button
    :UC: None
    """
    # Maze's width
    widthLabel = Label(winset, text="Width of the maze (integer)")
    width = StringVar(winset)
    width.set(str(default_width))
    widthEntry = Entry(winset, textvariable=width, state="normal")

    # Maze's height
    heightLabel = Label(winset, text="Height of the maze (integer)")
    height = StringVar(winset)
    height.set(str(default_height))
    heightEntry = Entry(winset, textvariable=height, state="normal")

    # Maze's base filename
    global g_filename
    fileLabel = Label(winset, text="Generate from which file ? ")
    g_filename = StringVar(winset)
    g_filename.set(default_path)
    fileEntry = Entry(winset, textvariable=g_filename, state="disabled")
    fileButton = Button(winset, text="Browse", command=askfile, state="disabled")

    return widthLabel, heightLabel, width, height, widthEntry, heightEntry, fileLabel, g_filename, fileEntry, fileButton

def setup_wingen(winset, widthEntry, heightEntry, fileEntry, fileButton, default_gen):
    """
    Returns the generation Widgets used for the setup_window, includes:
        Three radio buttons for the generation
        The label for the generation
        The generation Variable


    :param winset: (Tk) a window
    :param widthEntry: (Entry) The Entry for the width
    :param heightEntry: (Entry) the Entry for the height
    :param fileEntry: (Entry) the Entry for the file's path
    :param fileButton: (Button) the Button for browsing files
    :param default_gen: (int) The default generation:
            * 0 : Hand generation
            * 1 : Generate from a text file
            * 2 : Generate randomly
    :return: (Label, IntVar, Radiobutton, Radiobutton, Radiobutton)
    The label, the generation variable, the handgen check, the textgen check, the randomgen check
    :UC: default_gen must be either 0, 1 or 2
    """
    genLabel = Label(winset, text="Generation Options (Chose only one)")
    varGen = IntVar()
    varGen.set(default_gen)

    # When handgen or randomgen is selected, the width and height entries will be activated, and the file entry and button are disabled
    # When texgen is selected, the reverse operation is done
    handgenCheck = Radiobutton(winset, variable=varGen, value=0, text="Hand generation", command=partial(toggleonoff, (widthEntry, heightEntry), (fileEntry, fileButton)))
    textgenCheck = Radiobutton(winset, variable=varGen, value=1, text="Generate from text file", command=partial(toggleonoff, (fileEntry, fileButton), (widthEntry, heightEntry)))
    randomgenCheck = Radiobutton(winset, variable=varGen, value=2, text="Generate randomly", command=partial(toggleonoff, (widthEntry, heightEntry), (fileEntry, fileButton)))

    return genLabel, varGen, handgenCheck, textgenCheck, randomgenCheck

def setup_winsave(winset, default_save, default_saveres, default_savehtml):
    """
    Returns the save widget used for the setup_window

    :param: (Tk) a window
    :param default_save: (int) 1 if the program saves the maze, 0 otherwise
    :param default_saveres: (int) 1 if the program saves the resolution, 0 otherwise
    :param default_savehtml: (int) 1 if the program saves the maze in an html file, 0 otherwise
    :return: (Label, IntVar, Checkbutton, IntVar, Checkbutton, IntVar, Checkbutton)
    The save label, is_save, saveCheck, is_saveres, saveresCheck, is_savehtml, savehtmlCheck
    :UC: None
    """
    saveLabel = Label(winset, text="Save Options")

    # Save in file
    is_save = IntVar(winset, default_save)
    saveCheck = Checkbutton(winset, variable= is_save, text="Save into a file")

    # Save resolution in file
    is_saveres = IntVar(winset, default_saveres)
    saveresCheck = Checkbutton(winset, variable= is_saveres, text="Save into a file with the resolution [WIP]")

    # Save in HTML file
    is_savehtml = IntVar(winset, default_savehtml)
    savehtmlCheck = Checkbutton(winset, variable= is_savehtml, text="Save into a html file")

    return saveLabel, is_save, saveCheck, is_saveres, saveresCheck, is_savehtml, savehtmlCheck

def setup_wingraphic(winset, default_graphic, default_speed):
    """
    Returns the graphic items used for the setup_window

    :param: (Tk) a window
    :param default_graphic: (int) the default graphic display option:
            * 0 : Do not display the maze
            * 1 : Display the maze
            * 2 : Display the maze and its resolution
            * 3 : Display the maze and its resolution dynamicaly
            * 4 : Display the maze textually
            * 5 : Display the maze textually with the resolution
    :param default_speed: (str) the speed of the dynamic resolution
    :return: (Label, IntVar, CheckButton, Checkbutton, Checkbutton, Checkbutton, Label, StringVar, Spinbox)
    graphicLabel, varGraph, notgraphicCheck, graphicresCheck, dynamicCheck, graphicCheck, speedLabel, varSpeed, speedSpinbox
    :UC: default_speed must be in SPEED_VALUES.keys()
    """
    graphicLabel = Label(winset, text="Graphic Options")
    varGraph = IntVar(winset, default_graphic)

    # Speed of dynamic resolution
    speedLabel = Label(winset, text="Speed for dynamic")
    varSpeed = StringVar(winset, default_speed)
    speedSpinbox = Spinbox(winset, values=(list(SPEED_VALUES.keys())), wrap="True", textvariable=varSpeed)
    for i in range(list(SPEED_VALUES.keys()).index(default_speed)): # Moves the current speed to the default one
        speedSpinbox.invoke("buttonup")



    # Not displaying the Maze
    notgraphicCheck = Radiobutton(winset, variable=varGraph, value=0, text="Do not display the maze on a window", command=partial(toggle_state_off, [speedSpinbox]))

    # Displaying the Maze textually
    textCheck = Radiobutton(winset, variable=varGraph, value=4, text="Display the maze textually", command=partial(toggle_state_off, [speedSpinbox]))

    # Same but with the resolution
    textresCheck = Radiobutton(winset, variable=varGraph, value=5, text="Display the maze textually with the resolution", command=partial(toggle_state_off, [speedSpinbox]))

    # Displaying the Maze
    graphicCheck = Radiobutton(winset, variable=varGraph, value=1, text="Display the maze on a window", command=partial(toggle_state_off, [speedSpinbox]))

    # Graphic resolution
    graphicresCheck = Radiobutton(winset, variable=varGraph, value=2, text="Display the resolution on the maze", command=partial(toggle_state_off, [speedSpinbox]))

    # Dynamic resolution
    dynamicCheck = Radiobutton(winset, variable=varGraph, value=3, text="Display the resolution dynamically", command=partial(toggle_state_on, [speedSpinbox]))

    return graphicLabel, varGraph, notgraphicCheck, textCheck, textresCheck, graphicresCheck, dynamicCheck, graphicCheck, speedLabel, varSpeed, speedSpinbox

def is_convertible_to_integer(a):
    """
    Checks if a (any type) can be converted to an integer, if it can, returns True, otherwise, False

    :Examples:
    >>> is_convertible_to_integer("10")
    True
    >>> is_convertible_to_integer([10])
    False
    >>> is_convertible_to_integer("k")
    False
    """
    try:
        int(a)
        return True
    except TypeError:
        return False
    except ValueError:
        return False

def exit_setup(winset, width, height, varGen, g_filename):
    """
    Makes the finals checks before closing the setup window
    Checks if the width and height are integers
    Checks if the file the user entered exists

    :param winset: (Tkinter Window)
    :param width: (varInt)
    :param height: (varInt)
    :param varGen: (varInt)
    :param g_filename: (varStr)
    :side effect:
    :return: None
    :UC: 
    """
    # Checking for the width and height
    if not all(map(is_convertible_to_integer,(width.get(), height.get()))) and varGen.get() in {0,2}:
        winwarning = Tk()
        winwarning.title("Warning")
        warningLabel = Label(winwarning, text="The values you have entered are not correct, please try again. (Width and height must be integer)")
        warningOkButton = Button(winwarning, text="OK", command=winwarning.destroy)
        warningLabel.grid()
        warningOkButton.grid()

    # Checking for the existence of the file 
    elif not os.path.exists(g_filename.get()) and varGen.get() == 1:
        winwarning = Tk()
        winwarning.title("Warning")
        warningLabel = Label(winwarning, text="The path you entered for the file is not a valid path")
        warningOkButton = Button(winwarning, text="OK", command=winwarning.destroy)
        warningLabel.grid()
        warningOkButton.grid()

    # Everything's okay, we can close the setup window
    else:
        winset.destroy()
        

#########################
# GRAPHICMAZE FUNCTIONS #
#########################

def adjust_dimensions(width, height, can_width=CAN_WIDTH, can_height=CAN_HEIGHT, ratio=40):
    """
    Returns adjusted dimensions for the canvas to use so that its content is not stretched

    :param can_width: (int or float) the width of the current canvas
    :param can_height: (int or float) the height of the current canvas
    :param width: (int) the width of the maze
    :param height: (int) the height of the maze
    :ratio: (int or float)
    :return: (tuple of two floats) the adjusted dimensions
    :UC: ratio != 0
    """
    adj_can_width = can_width//ratio*width
    adj_can_height = can_height//ratio*height
    if adj_can_width > 1600 or adj_can_height > 900: # Prevents the canvas to be too big
        adj_can_width = can_width
        adj_can_height = can_height
    return adj_can_width, adj_can_height

def restart(win, setup_var):
    """
    Restarts the program by closing the maze's window and reseting the setup values to the last ones (not necessarly the default ones)

    :param win: (Tkinter Window)
    :param setup_var: (tuple) a tuple with all the setup variables (see setup_window)
    :side effect: restarts the program
    :return: None
    :UC: setup_var must have as many elements as there are variables in setup_window
    """
    win.destroy()
    main(setup_var)

def toggle_graphic_res(can, maze, can_width, can_height):
    """
    Toggles on and off the resolution on the graphicmaze.
    Uses the global variable `is_disp_res`

    :param can: (Canvas)
    :param maze: (Maze)
    :param can_width: (Int or float) the width of the canvas
    :param can_height: (Int or float) the width of the canvas
    :side effect: Inverts the value of is_disp_res (bool)
    :return: None
    :UC: `is_disp_res` must be a global variable
    """
    width = maze.get_width()
    height = maze.get_height()
    trace = maze.resolution_path(trace=True) # The complete process of the resolution
    global is_disp_res # True if the resolution is displayed
    if is_disp_res: 
        for (x,y), state in trace:
                if state == "crossed": # We erase the good path
                    remove_circle(can, width, height, x, y, can_width=can_width, can_height=can_height)
                elif state == "wrong": # We erase the bad cells
                    remove_bad_cell(can, width, height, x, y, can_width=can_width, can_height=can_height)
        # We also erase the finish cell
        remove_circle(can, width, height, width-1, height-1, can_width=can_width, can_height=can_height)
        is_disp_res = False

    else:
        for (x,y), state in trace:
                if state == "crossed": # We draw the good path
                    set_circle(can, width, height, x, y, can_width=can_width, can_height=can_height)
                elif state == "wrong": # We draw the bad cells
                    set_bad_cell(can, width, height, x, y, can_width=can_width, can_height=can_height)
        # We also draw the finish cell
        set_circle(can, width, height, width-1, height-1, can_width=can_width, can_height=can_height)
        is_disp_res = True

    # Note: Will draw/erase over same cell a maximum of 2 times

def setup_buttons(win, setup_var):
    """
    Adds buttons to the window.
    Adds the restart button and the quit button.
    
    :param win: (Tkitner window)
    :param setup_var: (Tuple) see `setup_window` for the default values
    :side effect: puts two buttons on the window `win`
    :return: None
    :UC: setup_var must have as many elements as there are parameters in `setup_window`
    """
    restartButton = Button(win, text="Restart", command=partial(restart, win, setup_var))
    restartButton.pack(side="left")
    quitButton = Button(win, text="Quit", command=exit)
    quitButton.pack(side="right")

def draw_res_cell(can, width, height, x, y, state, can_width=CAN_WIDTH, can_height=CAN_HEIGHT):
    """
    Draws a resolution cell of the maze of dimensions `width` and `height` on the canvas
    `can` of dimensions `can_width` and `can_height` at the coordinate `x`, `y`.
    If the cell is a a good one (on the path to the finish), it will draw a circle over it.
    Else, it will draw a square over it

    :param can: (Canvas)
    :param width: (int) the width of the maze
    :param height: (int) the height of the maze
    :param x: (int) the x coordinate of the cell
    :param y: (int) the y coordinate of the cell
    :param state: (str) a state of the cell (see the `square` module)
    :param can_width: (int or float) the width of the canvas
    :param can_height: (int or float) the height of the canvas
    :side effect: draws a cell on the canvas
    :return: None
    :UC: x and y must be within the dimension width and height
    """
    if state == "crossed":
        set_circle(can, width, height, x, y, can_width=can_width, can_height=can_height)
    elif state == "wrong":
        remove_circle(can, width, height, x, y, can_width=can_width, can_height=can_height)
        set_bad_cell(can, width, height, x, y, can_width=can_width, can_height=can_height)

##################
# MAIN FUNCTIONS #
##################

def setup_window(default_width=20, default_height=20, default_path="", default_gen=2, default_save=1, default_saveres=0, 
                 default_savehtml=0, default_graphic=3, default_speed="Normal"):
    """
    Opens a window for the user to input parameters and then returns those parameters

    :param default_width: (int) [default=20] The default_width of the maze
    :param default_height: (int) [default=20] The default height of the maze
    :param default_path: (str) [default=""] The default path for the file from which the maze is generated
    :param default_gen: (int) [default=2] The default generation option:
            * 0 : Hand generation
            * 1 : Generate from a text file
            * 2 : Generate randomly
    :param default_save: (int) [default=1] 1 if the program saves in a text file, 0 otherwise
    :param default_saveres: (int) [default=0] 1 if the resolution is saved too, 0 otherwise
    :param default_savehtml: (int) [default=0] 1 if the program saves in an html file, 0 otherwise
    :param default_graphic: (int) [default=3] The default graphical display option:
            * 0 : Do not display the maze
            * 1 : Display the maze
            * 2 : Display the maze and its resolution
            * 3 : Display the maze and its resolution dynamicaly
            * 4 : Display the maze textually
            * 5 : Display the maze textually with the resolution
    :param default_speed: (str) [default="Normal] The speed of the resolution
    :side effect: Opens a Tkinter window on which the user has to input the parameters of the program

    :return: The function returns 10 values in a tuple listed below:
        - (int) The width of the maze
        - (int) The height of the maze
        - (str) The path of the text file from which we can build a maze
        - (int) The generation the user has chosen
            * 0 : Hand generation
            * 1 : Generate from a text file
            * 2 : Generate randomly
        - (int) 1 if the user wants to save in a text file, 0 otherwise
        - (int) 1 if the user wants the resolution to be saved too, 0 otherwise
        - (int) 1 if the user wants the maze to be saved into a html file, 0 otherwise
        - (int) The display option:
            * 0 : Do not display the maze
            * 1 : Display the maze
            * 2 : Display the maze and its resolution
            * 3 : Display the maze and its resolution dynamicaly
            * 4 : Display the maze textually
            * 5 : Display the maze textually with the resolution
        - (str) The speed at which the resolution is displayed(key in SPEED_VALUES)
    :UC: None
    """
    # Setup of the window
    winset = Tk()
    winset.title("Maze setup")
    title = Label(winset, text="Please, select options in order to continue")
    exitButton = Button(winset, text='Exit', command=exit)
    okButton = Button(winset, text="OK")

    # Entries (width, height and filepath) setup
    entries_var = setup_winentries(winset, default_width, default_height, default_path)
    widthLabel, heightLabel, width, height, widthEntry, heightEntry, fileLabel, g_filename, fileEntry, fileButton = entries_var

    # Generation setup
    gen_var = setup_wingen(winset, widthEntry, heightEntry, fileEntry, fileButton, default_gen)
    genLabel, varGen, handgenCheck, textgenCheck, randomgenCheck = gen_var

    # Save setup
    save_var = setup_winsave(winset, default_save, default_saveres, default_savehtml)
    saveLabel, is_save, saveCheck, is_saveres, saveresCheck, is_savehtml, savehtmlCheck = save_var

    # Graphic setup
    graphic_var = setup_wingraphic(winset, default_graphic, default_speed)
    graphicLabel, varGraph, notgraphicCheck, textCheck, textresCheck, graphicresCheck, dynamicCheck, graphicCheck, speedLabel, varSpeed, speedSpinbox = graphic_var

    okButton["command"] = partial(exit_setup, winset, width, height, varGen, g_filename)

    # Placement
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

    graphicLabel.grid(row = 25, column = 0, pady=(10, 0))
    notgraphicCheck.grid(row = 26, column = 0)
    textCheck.grid(row = 27, column = 0)
    textresCheck.grid(row = 28, column = 0)
    graphicCheck.grid(row = 32, column = 0)
    graphicresCheck.grid(row = 33, column = 0 )
    dynamicCheck.grid(row = 34, column = 0)
    speedLabel.grid(row=35, column=0)
    speedSpinbox.grid(row=35, column=1)

    winset.mainloop()

    return (int(width.get()), int(height.get()), g_filename.get(), varGen.get(), 
            is_save.get(), is_saveres.get(), is_savehtml.get(),
            varGraph.get(), varSpeed.get())

def parse_gen(width, height, filepath, varGen):
    """
    Returns a maze generated accordingly to the arguments of the function
    
    :param width: (int) the width of the maze
    :param height: (int) the height of the maze
    :param filepath: (str) a path of a file we want to generate a maze from
    :param varGen: (int) The generation the user has chosen
            * 0 : Hand generation
            * 1 : Generate from a text file
            * 2 : Generate randomly
    :return: (Maze) a maze
    :UC: None
    :Examples:

    >>> maze_test = parse_gen(20, 20, "", 2)
    >>> maze_test.get_height()
    20
    >>> maze_test.get_width()
    20
    """
    # Generate from a text file
    if varGen == 1:
        maze = Maze().build_maze_from_text(filepath)
    else:
        try:
            width = int(width)
            height = int(height)
        except TypeError as err:
            print("The width and height are not of the correct type !, There's might be a bug in `exit_setup`", err)
            raise
    # Generate randomly
    if varGen == 2:
        maze = Maze().random_generation(width, height)
    # Generate by hand
    else:
        maze = Maze.hand_generation(width, height)
    return maze

def parse_save(maze, is_save, is_saveres, is_savehtml, save_path=SAVE_PATH):
    """
    Saves the maze into different files depending on the arguments of the function

    :param maze: (Maze)
    :param is_save: (bool) if True, the maze will be saved as is in a text file
    :param is_saveres: (bool) if True, the maze and its resolution will be saved in a text file
    :param is_savehtml: (bool) if True, the maze and its resolution will be saved in an html file
    :param save_path: (str) [default SAVE_PATH] the path to the directory where the maze will be saved
    :side effect: save
    :return: None
    :UC: None
    """
    if is_save:
        maze.text_representation(SAVE_PATH+"maze.txt")
    if is_saveres:
        maze.text_representation(SAVE_PATH+"maze_res.txt", disp_res = True)
        pass
    if is_savehtml:
        maze.picture_representation(SAVE_PATH+"maze_html.html")

def graph_disp(maze, varGraph, speed, setup_var):
    """
    Displays a `maze` on a Tkinter window and eventually its solution (dynamicaly or not)

    :param maze: (Maze)
    :param varGraph: (int) the display option, can be:
            * 1 : Display the maze on a window
            * 2 : Display the maze and its resolution
            * 3 : Display the maze and its resolution dynamicaly
    :param speed: (str) a key of the dictionnary SPEED_VALUES
    :param setup_var: (tuple) see `setup_window` for the default values
    :side effect: Displays a graph on a window
    :return: None
    :UC: varGraph in {1, 2, 3}
    """
    assert varGraph in {1, 2, 3}
    global is_disp_res  # True if the resolution is currently displayed, False otherwise
    width = maze.get_width()
    height = maze.get_height()

    adj_can_width, adj_can_height = adjust_dimensions(width, height) # We adjust the dimension

    win = Tk() # Creates a window object
    win.title(random_word('../ressources/anagrams.txt'))
    can = create_canvas(win, adj_can_width, adj_can_height)

    draw_grid(can, width, height, can_width=adj_can_width, can_height=adj_can_height) 
    setup_wall(can, maze, can_width=adj_can_width, can_height=adj_can_height)
    setup_buttons(win, setup_var)

    if varGraph in {2, 3}:
        trace = maze.resolution_path(trace=True)
        
        # Display the resolution in one go
        if varGraph == 2:
            for (x, y), state in trace:
                draw_res_cell(can, width, height, x, y, state, adj_can_width, adj_can_height)

        # Display all the resolution progressively
        else: 
            speed_val = SPEED_VALUES[speed]
            for (x, y), state in trace:
                draw_res_cell(can, width, height, x, y, state, adj_can_width, adj_can_height)
                win.update()
                time.sleep(speed_val)

        # Draw the finish cell
        set_circle(can, width, height, width-1, height-1, can_width=adj_can_width, can_height= adj_can_height)
        is_disp_res = True

        


    toggleresButton = Button(win, text="Toggle Resolution",
                            command=partial(toggle_graphic_res, can, maze, adj_can_width, adj_can_height))
    toggleresButton.pack(side="left")
    win.mainloop()

def text_disp(maze, varGraph):
    """
    Displays the maze textually

    :param maze: (Maze)
    :param varGraph: (int) the display option, can be:
            * 4 : Display the maze textually
            * 5 : Display the maze textually with the resolution
    :side effect: Prints the maze on the console
    :return: None
    :UC: varGraph in {4,5}
    """
    assert varGraph in {4,5}
    if varGraph == 4:
        print(maze)
    else:
        maze.resolution_path()
        print(maze)
        


def main(old_var=()):
    """
    Main function of main_maze.py.
    Will in this order:
        * Display a setup window
        * Generate a maze according to the setup parameters
        * May save it into different files (depends on the parameters)
        * May display the maze in a window with the resolution (depends on the parameters)

    :param old_var: (tuple) [default = ()] the setup variable used by the user the last time the main function was ran (Used in setup_var)
    :side effect: (see above)
    :return: None
    :UC: None
    """
    # We get all the setup variable from the user using a GUI
    setup_var = setup_window(*old_var)
    width, height, filepath, varGen, is_save, is_saveres, is_savehtml, varGraph, speed = setup_var
    # We generate the maze
    maze = parse_gen(width, height, filepath, varGen)
    # If we must, we save it in files
    parse_save(maze, is_save, is_saveres, is_savehtml)

    # Displays the maze on a window
    if varGraph in {1, 2, 3}:
        graph_disp(maze, varGraph, speed, setup_var)
    # Displays the maze textually
    elif varGraph in {4, 5}:
        text_disp(maze, varGraph)

    
if __name__ == '__main__':
    main()
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS, verbose=False)
