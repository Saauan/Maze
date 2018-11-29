==================
:mod:`square` module
==================


this module define a class to represent cells (or squares) of a maze
A cell can

* have 0 to 4 ramparts (Top, Right, Bottom, Left)
* have a common rampart with a neighbour cell
* be surrounded by 4 ramparts
* be blank, crossed, wrong or finish (end cell)


Class description
=================
   
Class :class:`Square`
------------------------------   

.. autoclass:: square.Square


Méthods
======

.. automethod:: cell.Square.get_coordinates

.. automethod:: cell.Square.get_state

.. automethod:: cell.Square.get_ramparts


Predicates
----------

.. automethod:: cell.Square.has_left_rampart

.. automethod:: cell.Square.has_top_rampart

.. automethod:: cell.Square.has_right_rampart

.. automethod:: cell.Square.has_bottom_rampart

.. automethod:: cell.Square.has_common_rampart

.. automethod:: cell.Square.is_surrounded


Modifiers
---------

.. automethod:: cell.Square.rampart_deletion

.. automethod:: cell.Square.square_modification

.. automethod:: cell.Square.state_modification

		   
Special Methods
===============

.. automethod:: square.Square.__init__		