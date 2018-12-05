#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
:mod:`deadend` module

:author: Coignion Tristan, Tayebi Ajwad, Becquembois Logan

:date:  1/11/2018

This module provides functions for a 'deadend method' resolution of a maze.
"""

from maze import Maze, CreationError


def deadend_neighbours(maze, square, res):
    """
    Creates a list of possible neighbours for a selected square. They must not have the `wrong` or `crossed` state
    This will allow to not select them twice during the resolution_path
    
    :param maze: (Maze) - a generated maze
    :param square: (Square) - a square in the maze maze
    :param res: (list) the list of coordinates forming the path from start to end
    :return: neighbours (list) of possible neighbours for the square
    :CU: maze has to be already generated
    """
    potential_neighbours = [('Top', (0,-1)),
                            ('Left', (-1,0)),('Right', (1,0)),
                                        ('Bottom', (0,1))]
    neighbours = [0]
    for side, (Xs, Ys) in potential_neighbours:
        Xn, Yn = square.get_coordinates()[0] + Xs, square.get_coordinates()[1] + Ys
        if (0 <= Xn < maze.get_width()) and (0 <= Yn < maze.get_height()):
            neighbour = maze.get_square(Xn, Yn)
            neighbourState = neighbour.get_state()
            if not square.has_common_rampart(neighbour, side) and neighbourState != "wrong":
                neighbours[0] += 1
                if neighbour.get_coordinates() not in res:
                #if neighbourState != 'crossed':
                    neighbours.append(neighbour)
    return neighbours


def deadend_iterate(maze, square, res):
    """
    Change the states of cells if they are path of a dead end, and add cells
    that are in the resolution path to res.
    :param maze: (Maze) - a generated maze
    :param square: (Square) - a square in the maze maze
    :param res: (list) the list of coordinates forming the path from start to end
    :return: (list) param res, modified or not
    """
    neighbours = deadend_neighbours(maze, square, res)
    squareState = square.get_state()
    squareCoord = square.get_coordinates()
    validNeighbours = neighbours[0]
    blankNeighbours = len(neighbours) -1
    if (validNeighbours <= 1) and (squareState == 'blank') and (squareCoord not in res):
        if blankNeighbours == 0:
            square.state_modification('wrong')
            return res
        else:
            neighbour = neighbours[1]
            square.state_modification('wrong')
            return deadend_iterate(maze, neighbour, res)
    elif (blankNeighbours == 1) and (validNeighbours == 2):
        neighbour = neighbours[1]
        if (squareState == 'blank') and (squareCoord not in res):
            res += [squareCoord]
            #square.state_modification('crossed')
            return deadend_iterate(maze, neighbour, res)
        else:
            if neighbour.get_state() == 'finish':
                return res + [neighbour.get_coordinates()]
            else:
                #neighbour.state_modification('crossed')
                res += [neighbour.get_coordinates()]
                return deadend_iterate(maze, neighbour, res)
    else:
        return res
            

def deadend_pathfinder(maze):
    """
    Returns to the user the list corresponding to the path from the beginning square until the finish square.
    
    :param maze: (Maze) - a fresh new maze
    :return: (list(tuple(int, int))) A list of tuples of the coordinates of the resolution path in the correct order
                If more_path is set to True, return a tuple of two lists, with the second list being the path the function followed (see `more_path`)
    :effect: Change the values of some squares' state of maze
    """
    height = maze.get_height()
    width = maze.get_width()
    startSquare, finalSquare = maze.get_square(0, 0), maze.get_square(width-1, height-1)
    #startSquare.state_modification("crossed")
    finalSquare.state_modification("finish")
    res = [startSquare.get_coordinates()]
    while True:
        for y in range(height):
            print(maze)
            print(res)
            for x in range(width):
                square = maze.get_square(x, y)
                res = deadend_iterate(maze, square, res)
                if res[-1] == finalSquare.get_coordinates():
                    return res


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS, verbose=True)
