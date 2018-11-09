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

##############################################
# Function for game's setup and management
##############################################
class CreationError(Exception):
    """
    Error created to warn the user that he can't generate a maze on a generated one.
    """
    def __init__(self, msg):
        self.__message = msg


class Maze():
    """
    """
    def __init__(self, width=10, height=8, x0 = 0, y0 = 0):
        """
        Build a maze grid of size width*height cells.

        :param: width (int) [optional] - horizontal size (int) of the maze (default = 10)
                    height (int) [optional] - vertical size (int) of the maze (default = 8)
        :return: an empty grid (Maze) of width*height squares
        :CU: width and height must be positive integers
        
        Example:
        >>> game = Maze(15,12)
        >>> game.get_width()
        15
        >>> game.get_height()
        12 
        """
        assert type(width) == int and type(height) == int, 'The width & the height of your maze have to be int numbers'
        self.__x0, self.__y0 = x0, y0
        self.__width = width
        self.__height = height
        self.maze = [[Square(X,Y) for Y in range(height)] for X in range(width)]
        
    def get_height(self):
        """
        Used to obtain the height of the maze self.
        
        :param: self (Maze) - your maze
        :return: height (int) of the maze
        :CU: none
        """
        return self.__height

    def get_width(self):
        """
        Used to obtain the width of the maze self.
        
        :param: self (Maze) - your maze
        :return: width (int) of the maze
        :CU: none
        """
        return self.__width
   
    def get_cell(self, x, y):
        """
        Used to obtain the specific square with the given coordinates.

        :param: self (Maze) - your maze
                    x (int) - x-coordinate of a square
                    y (int) - y-coordinate of a square
        :return: the square (Square) of coordinates (x,y) in the game's grid
        :CU: 0 <= x < self.get_width() and 0 <= y < self.get_height() of the maze
        """
        return self.maze[x][y]
    
    def hand_generation(self):
        """
        Allow the user to create a maze from a blank one by himself.
        
        :param: self (Maze) - a fresh new maze
        :return: None
        :effect: Launch a series of inputs which the user has to complete correctly
        :CU: self has to be a new, not modified.
                If already modified, CreationError raised.
        """
        if not self.get_cell(0,0).is_surrounded():
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
        :return: An external representation of the maze self
        :rtype: str
        :UC: none
        """
        Labyrinth = [ ('+-' * self.get_width()) + '+'] # We initiate the first line of the maze
        LastLine = Labyrinth[0]
        
        for Y in range(self.get_height()):
            
            Laby_Line = ['|'] # We initiate the leftmost rampart of a line
            for X in range(self.get_width()):
                if self.get_cell(X,Y).has_rightRampart():
                    Laby_Line.extend(' |') # We add a '|' if the left-hand square has a right-hand rampart
                else:
                    Laby_Line.extend('  ') # We don't add anything
            Labyrinth.append(''.join(Laby_Line))
            
            Laby_Line = ['+'] # We initiate the leftmost rampart of an interline
            for X in range(self.get_width()):
                if self.get_cell(X,Y).has_bottomRampart():
                    Laby_Line.extend('-+') # We add a '-' if the upper square has a bottom rampart
                else:                               
                    Laby_Line.extend(' +') # We don't add anything
            Labyrinth.append(''.join(Laby_Line))
        
        Labyrinth.pop() ; Labyrinth.append(LastLine)
        return '\n'.join(Labyrinth)

    def neighbourhood(self, square):
        """
        Create a list of possible neighbours for a selected square.
        
        :param: self (Maze) - a fresh new maze
                    square (Square) - a square in the maze self
        :return: neighbours (list) of possible neighbours for square
        :CU: None
        """
    #    (x,y) = square.get_coordinates()
    #    potential_neighbours = [('Top', (x,y-1)),
    #                        ('Left', (x-1, y)),         ('Right', (x+1, y)),
    #                                      ('Bottom', (x, y+1))]
    #    print(potential_neighbours, [(neigh[0], self.get_cell(x,y)) for neigh in potential_neighbours 
    #                  if (0 <= neigh[1][0] < self.get_width()
    #                  and 0 <= neigh[1][1] < self.get_height()
    #                  and self.get_cell(neigh[1][0], neigh[1][1]).is_surrounded())])
    #    return [(neigh[0], self.get_cell(x,y)) for neigh in potential_neighbours 
    #                  if (0 <= neigh[1][0] < self.get_width()
    #                  and 0 <= neigh[1][1] < self.get_height()
    #                  and self.get_cell(neigh[1][0], neigh[1][1]).is_surrounded())]
             
        potential_neighbours = [('Top', (0,-1)),
                                ('Left', (-1,0)),('Right', (1,0)),
                                         ('Bottom', (0,1))]
        neighbours = []
        for side, (Xs, Ys) in potential_neighbours:
            Xn, Yn = square.get_coordinates()[0] + Xs, square.get_coordinates()[1] + Ys
            if (0 <= Xn < self.get_width()) and (0 <= Yn < self.get_height()):
                neighbour = self.get_cell(Xn, Yn)
                if neighbour.is_surrounded():
                    neighbours.append((side, neighbour))
        return neighbours

    def random_generation(self, solutionChoice=0):
        """
        Allow the user to create a random maze from a blank one.
        
        :param: self (Maze) - a fresh new maze
                    solutionChoice (int) - 0 if the user doesn't want to see the resolutionPath
                                                    1 if the user wants to see the resolutionPath given to him
        :return: None
        :effect: Change the values of some walls of self
        :CU: self has to be a new, not modified.
                If already modified, CreationError raised.
        """
        if solutionChoice == 0:
            try:
                nbSquares, memoryPath = self.get_width()*self.get_height(), stack.Stack() # We initiate the total number of squares to check & a stack containing the last position
                actualSquare, checkedSquares = self.get_cell(self.__x0, self.__y0), 1 # We keep in memory in actualSquare our position, the resolutionPath and the maze and in cpt the number of squares already checked
                
                while checkedSquares < nbSquares:
                    NEIGHBOURS = self.neighbourhood(actualSquare)
                    if not NEIGHBOURS : # Which means no neighbours have been found, so we hit a dead end and we return in the previous square
                        actualSquare = memoryPath.pop()
                        continue
                    side, followingSquare = random.choice(NEIGHBOURS) # We go randomly in one direction depending on the possible NEIGHBOURS
                    actualSquare.rampart_deletion(followingSquare, side) # We take down the rampart between our initial position and the chosen neighbour
                    memoryPath.push(actualSquare) # We save our initial position in case we encounter a dead end
                    actualSquare = followingSquare # Our initial position is now the neighbour chosen before
                    checkedSquares += 1 # We increment the number of checked squares
            except:
                raise CreationError("Maze already generated, can't generate it again. Please create another variable to generate another one.")
        
        
        if solutionChoice == 1:
            try:
                nbSquares, memoryPath, resolutionPath = self.get_width()*self.get_height(), stack.Stack(), [(self.__x0, self.__y0)] # We initiate the total number of squares to check & a stack containing the last position
                actualSquare, checkedSquares = self.get_cell(self.__x0, self.__y0), 1 # We keep in memory in actualSquare our position, the resolutionPath and the maze and in cpt the number of squares already checked
                print("Starting at the position {0}.".format(actualSquare.get_coordinates()))
                
                while checkedSquares < nbSquares:
                    NEIGHBOURS = self.neighbourhood(actualSquare)
                    if not NEIGHBOURS : # Which means no neighbours have been found, so we hit a dead end and we return in the previous square
                        actualSquare = memoryPath.pop()
                    #    resolutionPath.pop()
                    #    if (self.get_width()-1, self.get_height()-1) not in resolutionPath:
                    #        print("Ugh, you just fell in a dead-end. Let's going back to the position {0}.".format(actualSquare.get_coordinates()))
                        continue
                    side, followingSquare = random.choice(NEIGHBOURS) # We go randomly in one direction depending on the possible NEIGHBOURS
                    actualSquare.rampart_deletion(followingSquare, side) # We take down the rampart between our initial position and the chosen neighbour
                    memoryPath.push(actualSquare) # We save our initial position in case we encounter a dead end
                    actualSquare = followingSquare # Our initial position is now the neighbour chosen before
                    
                #    if (self.get_width()-1, self.get_height()-1) not in resolutionPath:
                #        print("Moving to the {:s} side... ".format(side) + "now arrived in the position {0}.".format(actualSquare.get_coordinates()))
                #        resolutionPath += [actualSquare.get_coordinates()]
                        
                    checkedSquares += 1 # We increment the number of checked squares
                    
            #    Solution = input("\n\nDo you want the list containing the solution ? [Yes | No]")
            #    if Solution.rstrip() == "Yes" or Solution.rstrip() == "yes":
            #        print(resolutionPath)
            #    elif (Solution.rstrip() != "Yes") and (Solution.rstrip() != "No"):
            #        print("You didn't enter a right answer, unlucky you...")
            except:
                raise CreationError("Maze already generated, can't generate it again. Please create another variable to generate another one.")
            

M = Maze(8,5)
M.random_generation()
T = M.__str__().split("\n")
ListeLaby = []
LineLaby = []
for x in T[1:len(T)-1]:
    for elt in x[1:len(x)-1]:
        if elt == " ":
            LineLaby += [0]
        else:
            LineLaby += [1]
    ListeLaby.append(LineLaby)
    LineLaby = []
ListeLaby[2*(M.get_height() - 1)][2*M.get_width() - 2] = 2
 
def text_representation(self, filename, choice):
    """
    Create a new text file containing maze's informations.
    
    :param: self (Maze) - a fresh new maze
                filename (str) - the name of the file which will contain the maze self
                choice (int) - 0 if self has to be written as entered,
                                    1 if self is new and has to be randomly generated before
                                    2 if self is new and has to be created by the user
    :return: None
    :effect: Create a new text file in the folder containing the width, the height and the maze schematic.
    :CU: self has to be a new, not modified if choice == 1 or choice == 2
            If already modified, CreationError raised.
    """
    assert choice in {0,1,2}, "Your choice's number isn't a valid one."
    if choice == 0:
        with open("{:s}.txt".format(filename), "w") as mazeModel :
            mazeModel.write("{:d}\n{:d}\n{:s}".format(self.get_width(), self.get_height(), self.__str__()))
    elif choice == 1:
        self.random_generation()
        with open("{:s}.txt".format(filename), "w") as mazeModel :
            mazeModel.write("{:d}\n{:d}\n{:s}".format(self.get_width(), self.get_height(), self.__str__()))
    elif choice == 2:
        self.hand_generation()
        with open("{:s}.txt".format(filename), "w") as mazeModel :
            mazeModel.write("{:d}\n{:d}\n{:s}".format(self.get_width(), self.get_height(), self.__str__()))
        
if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS, verbose=True)


