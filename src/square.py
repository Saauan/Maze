#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
:mod:`square` module

:author: Coignion Tristan, Ajwad Tayebi, Becquembois Logan

:date: 24/10/2018

This module provides functions and a class for maze's squares management.

:Provides:

* class Square

and methods

* `has_left_rampart`
* `has_top_rampart`
* `has_right_rampart`
* `has_bottom_rampart`
* `has_common_rampart`
* `is_surrounded`
* `rampart_deletion`
* `get_coordinates`
* `get_state`
* `get_ramparts`
* `square_modification`
* `state_modification`
"""
    
class Square():
    
    OPPOSITES = {'Left':'Right',
                 'Right':'Left',
                 'Top':'Bottom',
                 'Bottom':'Top'}

    STATES = {"blank", "crossed", "wrong", "finish"}
    
    def __init__(self, x, y, state = "blank"):
        """
        Creates a cell of a Maze.

        :return: (Square) - a new square of a maze's grid.
        :UC: None
        :Examples:

        >>> square = Square(0,1)
        >>> square.has_left_rampart()
        True
        >>> square.has_top_rampart()
        True
        >>> square.has_right_rampart()
        True
        >>> square.has_bottom_rampart()
        True
        >>> square.is_surrounded()
        True
        >>> square.get_ramparts()
        {'Left': True, 'Top': True, 'Right': True, 'Bottom': True}
        >>> square.get_coordinates()
        (0, 1)
        >>> square.square_modification('Right', False)
        >>> square.has_right_rampart()
        False
        >>> square.is_surrounded()
        False
        >>> square.get_ramparts()
        {'Left': True, 'Top': True, 'Right': False, 'Bottom': True}
        """
        self.__x, self.__y = x, y
        self.__ramparts = {'Left' : True, 'Top' : True, 'Right' : True, 'Bottom' : True}
        self.__state = state
        
    def has_left_rampart(self):
        """
        Returns the status of `self`'s left rampart.

        :return: (bool) - True if self has a left-hand rampart, False otherwise
        :UC: None
        :Examples:

        >>> square = Square(0,1)
        >>> square.has_left_rampart()
        True
        """
        return self.__ramparts['Left'] == True

    def has_top_rampart(self):
        """
        Returns the status of `self`'s top rampart.

        :return: (bool) - True if self has an upper wall, False otherwise
        :UC: none
        :Examples:

        >>> square = Square(0,1)
        >>> square.has_top_rampart()
        True
        """
        return self.__ramparts['Top'] == True
            
    def has_right_rampart(self):
        """
        Returns the status of `self`'s right rampart.

        :return: (bool) - True if self has a right-hand wall, False otherwise
        :UC: None
        :Examples:

        >>> square = Square(0,1)
        >>> square.has_right_rampart()
        True
        """
        return self.__ramparts['Right'] == True

    def has_bottom_rampart(self):
        """
        Returns the status of `self`'s bottom rampart.

        :return: (bool) - True if self has a lower wall, False otherwise
        :UC: None
        :Examples:

        >>> square = Square(0,1)
        >>> square.has_bottom_rampart()
        True
        """
        return self.__ramparts['Bottom'] == True
    
    def has_common_rampart(self, neighbour, rampart):
        """
        Returns the status of `self`'s and `neighbour`'s common rampart.

        :return: (bool) - True if self and neighbour have a rampart between them, False otherwise
        :UC: None
        :Examples:

        >>> square = Square(0,1)
        >>> square2 = Square(0,2)
        >>> square.has_common_rampart(square2, "Bottom")
        True
        >>> square.square_modification("Bottom", False)
        >>> square.has_common_rampart(square2, "Bottom")
        False
        """
        return self.__ramparts[rampart] == neighbour.__ramparts[Square.OPPOSITES[rampart]]  == True 
    
    def is_surrounded(self):
        """
        Returns the status of `self`'s encirclement.

        :return: (bool) - True if the square is surrounded, False otherwise
        :UC: None
        :Examples:

        >>> square = Square(0,1)
        >>> square.is_surrounded()
        True
        """
        return all(self.__ramparts.values())
    
    def rampart_deletion(self, neighbour, rampart):
        """
        Allows the 'destruction' of the `rampart` between `self` and his `neighbour`.
        
        :param self: (Square) - the first square
        :param neighbour: (Square) - the second
        :param rampart: (str) - Must be 'Left', 'Top' 'Right' or 'Bottom'
        :return: None
        :effect: Inverse the bool one-sided wall between neighbour and rampart (only horizontal or vertical)
        """
        assert rampart in {'Left','Top','Right','Bottom'}, "The rampart has to be Left, Top, Right or Bottom"
        self.__ramparts[rampart] = False # Destroys the ramparts separating self and neighbour
        neighbour.__ramparts[Square.OPPOSITES[rampart]]  = False
   
    def get_coordinates(self):
        """
        Returns `self`'s coordinates.

        :return: (tuple) - containing the coordinates of the square
        :Examples:
        
        >>> square = Square(0,1)
        >>> square.get_coordinates()
        (0, 1)
        """
        return (self.__x, self.__y)
    
    def get_state(self):
        """
        Returns `self`'s state.

        :return: (str) - representing the square's state
        :Examples:
        
        >>> square = Square(0,1)
        >>> square.get_state()
        'blank'
        """
        return self.__state
    
    def get_ramparts(self):
        """
        Returns `self`'s ramparts.

        :return: (dict) - containing the ramparts of the square
        :Examples:
        
        >>> square = Square(0,1)
        >>> square.get_ramparts()
        {'Left': True, 'Top': True, 'Right': True, 'Bottom': True}
        """
        return self.__ramparts
    
    def square_modification(self, rampart, value):
        """
        Set `self`'s `rampart` to the `value` given.

        :param rampart: (str) - the rampart to modify
        :param value: (bool) - True if there is a rampart, False otherwise
        :return: None
        :effect: Change the value of one of the rampart
        :Examples:
        
        >>> square = Square(0,1)
        >>> square.has_bottom_rampart()
        True
        >>> square.square_modification("Bottom", False)
        >>> square.has_bottom_rampart()
        False
        """
        assert value in {True, False}, "The value of the rampart has to be a boolean."
        assert rampart in {'Left','Top','Right','Bottom'}, "The rampart has to be Left, Top, Right or Bottom"
        self.__ramparts[rampart] = value
        
    def state_modification(self, value):
        """
        Set `self`'s state to the `value` given.

        :param self: (Square) - the Square to modify
        :param value: (str) - the state of the Square can be {'blank', 'crossed', 'wrong'}
        :return: None
        :effect: Change the state of the square
        :Examples:
        
        >>> square = Square(0,1)
        >>> square.get_state()
        'blank'
        >>> square.state_modification('crossed')
        >>> square.get_state()
        'crossed'
        """
        assert value in Square.STATES, "The state's value isn't right. Has to be blank, crossed, wrong or finish."
        self.__state = value

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS, verbose=True)

