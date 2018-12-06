=========================
:mod:`maze` module
=========================

Define classes and auxiliaries function for maze.


Class description
=================

A class to alert user if trying to generate on an already generated maze
or trying to solve an already solved maze.

Class :class:`CreationError`
----------------------------

.. autoclass:: maze.CreationError


Class to manage maze

Class :class:`Maze`
-------------------  

.. autoclass:: maze.Maze


Méthods
=======

.. automethod:: maze.Maze.get_height

.. automethod:: maze.Maze.get_width

.. automethod:: maze.Maze.get_square

.. automethod:: maze.Maze.neighbourhood

.. automethod:: maze.Maze.random_generation

.. automethod:: maze.Maze.hand_generation

.. automethod:: maze.Maze.text_representation

.. automethod:: maze.Maze.picture_representation

.. automethod:: maze.Maze.resolution_neighbours

.. automethod:: maze.Maze.resolution_path

.. automethod:: maze.Maze.build_maze_from_text


Special Methods
===============

.. automethod:: maze.Maze.__init__

.. automethod:: maze.Maze.__str__


Auxiliaries Function
====================

.. autofunction:: maze._pict_rep_html_header

.. autofunction:: maze._pict_rep_html_footer
