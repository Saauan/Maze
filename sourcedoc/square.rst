====================
:mod:`square` module
====================


this module define a class to represent squares (or squares) of a maze
A square can

* have 0 to 4 ramparts (Top, Right, Bottom, Left)
* have a common rampart with a neighbour square
* be surrounded by 4 ramparts
* be blank, crossed, wrong or finish (end square)


Class description
=================
   
Class :class:`Square`
---------------------   

.. autoclass:: square.Square


Méthods
=======

.. automethod:: square.Square.get_coordinates

.. automethod:: square.Square.get_state

.. automethod:: square.Square.get_ramparts


Predicates
----------

.. automethod:: square.Square.has_left_rampart

.. automethod:: square.Square.has_top_rampart

.. automethod:: square.Square.has_right_rampart

.. automethod:: square.Square.has_bottom_rampart

.. automethod:: square.Square.has_common_rampart

.. automethod:: square.Square.is_surrounded


Modifiers
---------

.. automethod:: square.Square.rampart_deletion

.. automethod:: square.Square.square_modification

.. automethod:: square.Square.state_modification

		   
Special Methods
===============

.. automethod:: square.Square.__init__		
