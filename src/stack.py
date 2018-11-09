#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
:mod:`stack1` module

:author: `FIL - Faculté des Sciences et Technologies - 
          Univ. Lille <http://portail.fil.univ-lille1.fr>`_

:date: 2015, september
:last revision: 2017, october

A module for stack data structure.

:Provides:

* class Stack

and methods

* `push`
* `pop`
* `top`
* `is_empty`

:Examples:

>>> stack = Stack()
>>> stack.is_empty()
True
>>> stack.push(1)
>>> stack.is_empty()
False
>>> stack.push(2)
>>> stack.top()
2
>>> stack.pop()
2
>>> stack.top()
1
>>> stack.pop()
1
>>> stack.is_empty()
True
>>> stack.pop()
Traceback (most recent call last):
   ... 
StackEmptyError: empty stack, nothing to pop
"""

class StackEmptyError(Exception):
    """
    Exception for empty stacks
    """
    def __init__(self, msg):
        self.message = msg


class Stack():

    def __init__(self):
        """
        :build: a new empty stack
        :UC: none
        """
        self.__content = []

    def push(self, x):
        """
        :param x: a value
        :type x: any
        :return: None
        :rtype: Nonetype
        :Side effect: stack self contains a new value : x
        :UC: none
        """
        self.__content.append(x)

    def pop(self):
        """
        :return: element on top of self
        :Side effect: self contains an element less
        :UC: self must be non empty
        """
        try:
            return self.__content.pop()
        except IndexError:
            raise StackEmptyError('empty stack, nothing to pop')

    def top(self):
        """
        :return: element on top of self without removing it
        :UC: self must be non empty
        """
        try:
            return self.__content[-1]
        except IndexError:
            raise StackEmptyError('empty stack, nothing on the top')

    def is_empty(self):
        """
        :return: 
           * ``True`` if s is empty
           * ``False`` otherwise
        :rtype: bool
        :UC: none
        """
        return self.__content == []

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS, verbose=True)
