#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
:mod:`square` module

:author: Coignion Tristan, Ajwad Tayebi, Becquembois Logan

:date: 24/10/2018

This module provides functions and a class for maze's squares management.

"""
    
class Square():
    
    OPPOSITES = {'Left':'Right',
                 'Right':'Left',
                 'Top':'Bottom',
                 'Bottom':'Top'}

    STATES = {"blank", "crossed"}
    
    def __init__(self, x, y, state = "blank"):
        """
        :return: a new square of a maze's grid.
        :rtype: Square
        :UC: none
        :Examples:

        >>> square = Square(0,1)
        >>> square.has_leftRampart()
        True
        >>> square.has_topRampart()
        True
        >>> square.has_rightRampart()
        True
        >>> square.has_bottomRampart()
        True
        >>> square.is_surrounded()
        True
        >>> square.get_ramparts()
        {'Left': True, 'Top': True, 'Right': True, 'Bottom': True}
        >>> square.get_coordinates()
        (0, 1)
        >>> square.square_modification('Right', False)
        >>> square.has_rightRampart()
        False
        >>> square.is_surrounded()
        False
        >>> square.get_ramparts()
        {'Left': True, 'Top': True, 'Right': False, 'Bottom': True}
        """
        self.__is_finish = False
        self.__x, self.__y = x, y
        self.__ramparts = {'Left' : True, 'Top' : True, 'Right' : True, 'Bottom' : True}
        self.__state = state

    def has_leftRampart(self):
        """
        :return: True if self has a left-hand rampart, False otherwise
        :rtype: bool
        :UC: none
        :Example:

        >>> square = Square(0,1)
        >>> square.has_leftRampart()
        True
        """
        return self.__ramparts['Left'] == True

    def has_topRampart(self):
        """
        :return: True if self has an upper wall, False otherwise
        :rtype: bool
        :UC: none
        :Example:

        >>> square = Square(0,1)
        >>> square.has_topRampart()
        True
        """
        return self.__ramparts['Top'] == True
            
    def has_rightRampart(self):
        """
        :return: True if self has a right-hand wall, False otherwise
        :rtype: bool
        :UC: none
        :Example:

        >>> square = Square(0,1)
        >>> square.has_rightRampart()
        True
        """
        return self.__ramparts['Right'] == True

    def has_bottomRampart(self):
        """
        :return: True if self has a lower wall, False otherwise
        :rtype: bool
        :UC: none
        :Example:

        >>> square = Square(0,1)
        >>> square.has_bottomRampart()
        True
        """
        return self.__ramparts['Bottom'] == True

    def is_finish(self):
        """
        :return: True if self is finish square, False otherwise
        :rtype: bool
        :UC: none

        TODO
        """
        return self.__is_finish

    def set_finish(self):
        """
        :side effect: sets the square as a finish square
        :return: None

        TODO
        """
        self.__is_finish = True
    
    def is_surrounded(self):
        """
        :return: True if the square is surrounded, False otherwise
        :rtype: bool
        :UC: none
        :Example:

        >>> square = Square(0,1)
        >>> square.is_surrounded()
        True
        """
        return all(self.__ramparts.values())
    
    def rampart_deletion(self, neighbour, rampart):
        """
        Allows the 'destruction' of a rampart between 2 squares given as parameters.
        
        :param: self & neighbour (Square) - the two specific squares
                    rampart (str) - Must be 'Left', 'Top' 'Right' or 'Bottom'
        :return: None
        :effect: Inverse the bool one-sided wall between neighbour and rampart (only horizontal or vertical)
        """
        assert rampart in {'Left','Top','Right','Bottom'}, "The rampart has to be Left, Top, Right or Bottom"
        self.__ramparts[rampart] = False # Destroys the ramparts separating self and neighbour
        neighbour.__ramparts[Square.OPPOSITES[rampart]]  = False
   
    def get_coordinates(self):
        """
        :return: (tuple) containing the coordinates of the square
        
        :Example:
        
        >>> square = Square(0,1)
        >>> square.get_coordinates()
        (0, 1)
        """
        return (self.__x, self.__y)
    
    def get_ramparts(self):
        """
        :return: (dict) containing the ramparts of the square
        
        :Example:
        
        >>> square = Square(0,1)
        >>> square.get_ramparts()
        {'Left': True, 'Top': True, 'Right': True, 'Bottom': True}
        """
        return self.__ramparts
    
    def square_modification(self, rampart, value):
        """
        :param: rampart (str) - the rampart to modify
                    value (bool) - True if there is a rampart, False otherwise
        :return: None
        :effect: Change the value of one of the rampart
        
        :Example:
        
        >>> square = Square(0,1)
        >>> square.has_bottomRampart()
        True
        >>> square.square_modification("Bottom", False)
        >>> square.has_bottomRampart()
        False
        """
        assert (value == True) or (value == False), "The value of the rampart has to be a boolean."
        assert rampart in {'Left','Top','Right','Bottom'}, "The rampart has to be Left, Top, Right or Bottom"
        self.__ramparts[rampart] = value


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS, verbose=True)
