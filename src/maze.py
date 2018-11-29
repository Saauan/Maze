#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
:mod:`maze` module

:author: Coignion Tristan, Tayebi Ajwad, Becquembois Logan

:date:  1/11/2018

This module provides functions and a class for hand-maze's game's management.
"""

from square import Square
import stack
import random


class CreationError(Exception):
    """
    Error created to warn the user that he can't generate a maze on a generated one or resolve a maze already resolved.
    """
    def __init__(self, msg):
        self.__message = msg

def _pict_rep_html_header(stream, W, H, p, style_path):
    """
    """
    stream.write('<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr" lang="fr">\n\n')
    stream.write('  <head>\n')
    stream.write('    <meta charset="UTF-8" />\n')
    stream.write('    <title> Votre Labyrinthe </title>\n')
    stream.write('    <link rel="stylesheet" type="text/css" href="{:s}maze.css"/>\n'.format(style_path))
    stream.write('    <link rel="icon" href="{:s}pictures/maze.ico"/>\n'.format(style_path))
    stream.write('    <meta name="author" content="TAYEBI Ajwad, COIGNION Tristan, BECQUEMBOIS Logan" />\n')
    stream.write('    <meta name="keywords" content="HTML, CSS, SVG" />\n')
    stream.write('  </head>\n\n')
    stream.write('  <body>\n')
    stream.write('    <svg xmlns="http://www.w3.org/2000/svg"\n')
    stream.write('         xmlns:xlink="http://www.w3.org/1999/xlink"\n')
    stream.write('         width="{:d}" height="{:d}" viewBox="{} {} {} {}">\n'.format(W+2*p, H+2*p, -p, -p, W+2*p, H+2*p))

def _pict_rep_html_footer(stream):
    """
    """
    stream.write('    </svg>\n')
    stream.write('  </body>\n\n')
    stream.write('</html>')

class Maze():
    """
    """

    STYLE_PATH = "../ressources/styles/"

    def __init__(self, width=10, height=8, x0 = 0, y0 = 0):
        """
        Build a maze grid of size `width`*`height` cells.

        :param width: (int) [optional] - horizontal size (int) of the maze (default = 10)
        :param height: (int) [optional] - vertical size (int) of the maze (default = 8)
        :param x0: (int) [optional] - the x-coordinate of the starting point (default = 0)
        :param y0: (int) [optional] - the y-coordinate of the starting point (default = 0)
        :return: (Maze) - an empty grid of `width`*`height` Squares
        :UC: `width` and `height` must be positive integers
        :Examples:
        
        >>> game = Maze(15,12)
        >>> game.get_width()
        15
        >>> game.get_height()
        12 
        """
        assert type(width) == int and type(height) == int and width>0 and height>0, 'The width & the height of your maze have to be positive integers'
        self.__x0, self.__y0 = x0, y0
        self.__width, self.__height = width, height
        self.maze = [[Square(X,Y) for Y in range(height)] for X in range(width)]
        
    def get_height(self):
        """
        Returns `self`'s height.
        
        :param self: (Maze) - your maze
        :return: (int) - height of the maze
        :UC: None
        :Examples:
        
        >>> M = Maze(10,5)
        >>> M.get_height()
        5
        """
        return self.__height

    def get_width(self):
        """
        Returns `self`'s width.
        
        :param self: (Maze) - your maze
        :return: (int) - width of the maze
        :UC: None
        :Examples:
        
        >>> M = Maze(9,15)
        >>> M.get_width()
        9
        """
        return self.__width
   
    def get_square(self, x, y):
        """
        Returns the `self`'s square which has as coordinates (`x`, `y`).

        :param self: (Maze) - your maze
        :param x: (int) - x-coordinate of a square
        :param y: (int) - y-coordinate of a square
        :return: (Square) - the square of coordinates (x,y) in the game's grid
        :UC: 0 <= `x` < self.get_width() and 0 <= `y` < self.get_height() of the maze and `x` and `y` have to be positive integers
        """
        assert 0 <= x < self.get_width() and 0 <= y < self.get_width(), "Your coordinates are out of the maze's boundaries."
        assert type(x) == int and type(y) == int, 'The x-coordinate & the y-coordinate of your square have to be positive integers'
        return self.maze[x][y]
    
    def hand_generation(self):
        """
        Allow the user to create a maze from a blank one `self` by himself.
        
        :param self: (Maze) - a fresh new maze
        :return: None
        :effect: Launch a series of inputs which the user has to complete correctly
        :UC: self has to be a new, not modified.
                If already modified, CreationError raised.
        """
        if not self.get_square(0,0).is_surrounded():
            raise CreationError("Maze already generated, can't generate it again. Please create another variable to generate another one.")
 
        for linesSquares in self.maze :
            for sqr in linesSquares:
                
                R = input("Enter the walls for the square at the position  {0}  like this :\nLeftOne, TopOne, RightOne, BottomOne. \n".format(sqr.get_coordinates()))
                R = [r.strip() for r in R.split(',') if r != ''] 
                for boo in range(len(R)):
                    if R[boo] == 'True':
                        R[boo] = True              # After the input's processing, R will contain the values of the 4 ramparts of the square
                    else:
                        R[boo] = False 
                
                for i,k in enumerate(sqr.get_ramparts()):
                    sqr.square_modification(k, R[i])     # Apply the square's modifications
                
                print("\n")
                print(self)
                          
    def __str__(self):
        """
        Gives a textual representation of `self` by printing it.

        :return: (str) - An external representation of the maze self
        :UC: None
        """
        Labyrinth = [ ('+-' * self.get_width()) + '+'] # We initiate the first line of the maze
        LastLine = Labyrinth[0]
        
        for Y in range(self.get_height()):
            
            Laby_Line = ['|'] # We initiate the leftmost rampart of a line
            for X in range(self.get_width()):
                if self.get_square(X,Y).has_right_rampart() and self.get_square(X,Y).get_state() == "blank":
                    Laby_Line.extend(' |') # We add a '|' if the left-hand square has a right-hand rampart
                elif not self.get_square(X,Y).has_right_rampart() and self.get_square(X,Y).get_state() == "blank":
                    Laby_Line.extend('  ') # We don't add anything
                elif self.get_square(X,Y).has_right_rampart() and self.get_square(X,Y).get_state() == "crossed":
                    Laby_Line.extend('✔|')
                elif not self.get_square(X,Y).has_right_rampart() and self.get_square(X,Y).get_state() == "crossed":
                    Laby_Line.extend('✔ ')
                elif self.get_square(X,Y).has_right_rampart() and self.get_square(X,Y).get_state() == "wrong":
                    Laby_Line.extend('✖|')
                elif not self.get_square(X,Y).has_right_rampart() and self.get_square(X,Y).get_state() == "wrong":
                    Laby_Line.extend('✖ ')
                elif self.get_square(X,Y).has_right_rampart() and self.get_square(X,Y).get_state() == "finish":
                    Laby_Line.extend('⚑|')
                elif not self.get_square(X,Y).has_right_rampart() and self.get_square(X,Y).get_state() == "finish":
                    Laby_Line.extend('⚑ ')
            Labyrinth.append(''.join(Laby_Line))
            
            Laby_Line = ['+'] # We initiate the leftmost rampart of an interline
            for X in range(self.get_width()):
                if self.get_square(X,Y).has_bottom_rampart():
                    Laby_Line.extend('-+') # We add a '-' if the upper square has a bottom rampart
                else:                               
                    Laby_Line.extend(' +') # We don't add anything
            Labyrinth.append(''.join(Laby_Line))
        
        Labyrinth.pop() ; Labyrinth.append(LastLine)
        return '\n'.join(Labyrinth)

    def neighbourhood(self, square):
        """
        Create a list of possible neighbours for `square` in `self`. Used for random_generation.
        
        :param self (Maze) - a fresh new maze
        :param square: (Square) - a square in the maze self
        :return: (list(tuple(str, Square))) - list of possible neighbours for `square`
        :UC: None
        """
        potential_neighbours = [('Top', (0,-1)),
                                ('Left', (-1,0)),('Right', (1,0)),
                                         ('Bottom', (0,1))]
        neighbours = []
        for side, (Xs, Ys) in potential_neighbours:
            Xn, Yn = square.get_coordinates()[0] + Xs, square.get_coordinates()[1] + Ys
            if (0 <= Xn < self.get_width()) and (0 <= Yn < self.get_height()):
                neighbour = self.get_square(Xn, Yn)
                if neighbour.is_surrounded():
                    neighbours.append((side, neighbour))
        return neighbours

    @staticmethod
    def random_generation(width, height):
        """
        Allow the user to create a random maze of `width`*`height` squares.
        
        :param width: (int) - the width of your maze
        :param height: (int) - the height of your maze
        :return: None
        :effect: Change the values of some walls of self
        :UC: `width` and `height` must be positive integers
        """
        assert type(width) == int and type(height) == int and width>0 and height>0, 'The width & the height of your maze have to be positive integers'
        maze = Maze(width, height)
        try:
            nbSquares, memoryPath = maze.get_width()*maze.get_height(), stack.Stack() # We initiate the total number of squares to check & a stack containing the last position
            actualSquare, checkedSquares = maze.get_square(maze.__x0, maze.__y0), 1 # We keep in memory in actualSquare our position, the resolutionPath and the maze and in cpt the number of squares already checked
                
            while checkedSquares < nbSquares:
                NEIGHBOURS = maze.neighbourhood(actualSquare)
                if not NEIGHBOURS : # Which means no neighbours have been found, so we hit a dead end and we return in the previous square
                    actualSquare = memoryPath.pop()
                    continue
                side, followingSquare = random.choice(NEIGHBOURS) # We go randomly in one direction depending on the possible NEIGHBOURS
                actualSquare.rampart_deletion(followingSquare, side) # We take down the rampart between our initial position and the chosen neighbour
                memoryPath.push(actualSquare) # We save our initial position in case we encounter a dead end
                actualSquare = followingSquare # Our initial position is now the neighbour chosen before
                checkedSquares += 1 # We increment the number of checked squares
            return maze
        except:
            raise CreationError("Maze already generated, can't generate it again. Please create another variable to generate another one.")

 
    def text_representation(self, filename):
        """
        Create a new text file, named `filename`, containing the maze `self`s informations.
        
        :param self: (Maze) - a fresh new maze
        :param filename: (str) - the name of the file which will contain the maze self
        :return: None
        :effect: Create a new text file in the folder containing the width, the height and the maze schematic.
        :UC: the maze self has to be already generated.
        """
        with open(filename, "w") as mazeModel :
            mazeModel.write("{:d}\n{:d}\n{:s}".format(self.get_width(), self.get_height(), self.__str__()))

    def picture_representation(self, fichier, style_path=STYLE_PATH):
        """
        Write an HTML file, named `fichier`, containing a SVG representation of the maze `self`.
        
        :param self: (Maze) - the Maze to represent in an HTML file
        :param fichier: (str) - the name of the file you want to get your picture representation
        :param style_path: (str) [optional] - the path to the directory of the styles sheets (default = "../ressources/styles/")
        :return: None
        :effect: Create a new HTML file in the folder containing the SVG representation of the maze
        :UC: the maze self has to be already generated
        """
        H = 650 ; W = int(H * (self.get_width() / self.get_height())) ; p = 20 # Size of the Maze in pixels & the padding (used later)
        # To draw the maze's lines, we consider the following scales :
        sX = H / self.get_height() ; sY = W / self.get_width()
        with open("{:s}".format(fichier), 'w') as output:
            _pict_rep_html_header(output, W, H, p, style_path)
            
            #First of all, we draw all the top ramparts of the first line and the left ramparts of the first column
            output.write('      <line x1="0" y1="0" x2="{}" y2="0"/>\n'.format(W))
            output.write('      <line x1="0" y1="0" x2="0" y2="{}"/>\n'.format(H))
            
            #Then, square by square, we check if they have a bottom or/and a right rampart, if they do, we draw it/them
            for X in range(self.get_width()):
                for Y in range(self.get_height()):
                    if self.get_square(X,Y).has_bottom_rampart(): 
                        output.write('      <line x1="{}" y1="{}" x2="{}" y2="{}"/>\n'.format(X*sX, (Y+1)*sY, (X+1)*sX, (Y+1)*sY))
                    if self.get_square(X,Y).has_right_rampart():
                        output.write('      <line x1="{}" y1="{}" x2="{}" y2="{}"/>\n'.format((X+1)*sX, Y*sY, (X+1)*sX, (Y+1)*sY))
                        
            _pict_rep_html_footer(output)     
    
    def resolution_neighbours(self, square):
        """
        Creates a list of possible neighbours for `square`. Used for resolution_path.
        They must not have the 'wrong' or 'crossed' state to not repeat the selection of a square during the resolution.
        
        :param self: (Maze) - a generated maze
        :param square: (Square) - a square in the maze self
        :return: (list(tuple(str, Square))) - list of possible neighbours for the square
        :UC: self has to be already generated
        """
        potential_neighbours = [('Bottom', (0,1)), ('Right', (1,0)), ('Top', (0,-1)), ('Left', (-1,0))]
        neighbours = []
        for side, (Xs, Ys) in potential_neighbours:
            Xn, Yn = square.get_coordinates()[0] + Xs, square.get_coordinates()[1] + Ys
            if (0 <= Xn < self.get_width()) and (0 <= Yn < self.get_height()):
                neighbour = self.get_square(Xn, Yn)
                if not square.has_common_rampart(neighbour, side) and neighbour.get_state() != "crossed" and neighbour.get_state() != "wrong":
                    neighbours.append((side, neighbour))
        return neighbours
        
    def resolution_path(self, more_path=False, talkative=False):
        """
        Returns to the user the list corresponding to the path from the beginning square until the finish square.
        
        :param self: (Maze) - a fresh new maze
        :param more_path: (bool) - if True, the function returns the path of all cells it went through (even the wrong ones). If False, it returns only the list of correct squares
        :param talkative: (bool) - True if we want to have more informations on the process of the function
        :return: (list(tuple(int, int))) A list of tuples of the coordinates of the resolution path in the correct order
                 If more_path is set to True, return a tuple of two lists, with the second list being the path the function followed (see `more_path`)
        :effect: Change the values of some squares' state of self
        :UC: self has to be already generated but not already resolved.
        """
        try:
            memoryPath, resolutionPath = stack.Stack(), [(self.__x0, self.__y0)] # We initiate a stack containing the last position & the list of the positions' solution.
            actualSquare, finalSquare = self.get_square(self.__x0, self.__y0), self.get_square(self.get_width()-1, self.get_height()-1)
            finalSquare.state_modification("finish")
            if talkative:
                print("Starting at the position {0}.".format(actualSquare.get_coordinates()))
            allPath = []
            while actualSquare.get_coordinates() != (self.get_width() - 1, self.get_height() - 1):
                NEIGHBOURS = self.resolution_neighbours(actualSquare) # All neighbours which are neither 'wrong' nor 'crossed'
                allPath.append(actualSquare.get_coordinates)
                if not NEIGHBOURS : # Which means no neighbours have been found, so we hit a dead end and we return in the previous square
                    actualSquare.state_modification("wrong")
                    actualSquare = memoryPath.pop() ; resolutionPath.pop()
                    if talkative:
                        print("Ugh, you just fell in a dead-end. Let's go back to the position {0}.".format(actualSquare.get_coordinates()))
                    continue
                
                side, followingSquare = NEIGHBOURS[0] # We go randomly in one direction depending on the possible NEIGHBOURS
                memoryPath.push(actualSquare) # We save our initial position in case we encounter a dead end
                actualSquare.state_modification("crossed")
                actualSquare = followingSquare # Our initial position is now the neighbour chosen before
                if talkative:
                    print("Moving to the {:s} side... ".format(side) + "now arrived in the position {0}.".format(actualSquare.get_coordinates()))
                resolutionPath.append(actualSquare.get_coordinates())
            if more_path:
                return resolutionPath, allPath
            
            return resolutionPath
        
        except stack.StackEmptyError:
            raise CreationError("Maze already resolved, can't resolve it again.")
        
    @staticmethod
    def build_maze_from_text(filename):
        """
        Build a Maze object from a text file
        The two first lines of the text file are the width and the height of the labyrinth (integers)
        The following lines describes the corridors of the maze using the symbols:
        - "+" for the corners of the squares
        - "-" and "|" for the walls separating adjacent squares
        - " " for the squares and the passages between them

        :param filename: (str) - a valid name of a text file
        :return: (Maze) - A maze built from the text file
        :UC: None
        """
        with open(filename, "r") as instream:
            lines = []
            for line in instream.readlines():
                lines.append(line.rstrip("\n"))

        try:
            width = int(lines.pop(0))
            height = int(lines.pop(0))
        except TypeError:
            print("build_maze_from_text: The width and height are not written correctly")
            raise TypeError
        
        maze = Maze(width, height)
        for i, line in enumerate(lines):
            for j, c in enumerate(line):
                if c == " ":
                    if i % 2 == 0: # We are on the "+" line.
                        x = j // 2
                        y = i // 2
                        if y <= height - 1: # We are not on the bottom edge.
                            maze.get_square(x,y).square_modification("Top", False)
                        if y >= 2: # We are not on the top squares.
                            maze.get_square(x, y-1).square_modification("Bottom", False)

                    elif j % 2 == 0: # We are on the "|" line and not inside a square.
                        x = j // 2
                        y = i // 2
                        if x <= width -1: # We are not on the far right edge.
                            maze.get_square(x, y).square_modification("Left", False)
                        if x >= 2 : # We are not on the far left squares.
                            maze.get_square(x-1, y).square_modification("Right", False)
        return maze

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS, verbose=True)
