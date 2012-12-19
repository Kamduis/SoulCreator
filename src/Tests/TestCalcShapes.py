#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
# Copyright

Copyright (C) 2012 by Victor
victor@caern.de

# License

This file is part of SoulCreator.

SoulCreator is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

SoulCreator is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
SoulCreator.  If not, see <http://www.gnu.org/licenses/>.
"""




import unittest

import src.Calc.CalcShapes as CalcShapes




ATTRIBUTE_MAX = 10
SHAPES = (
	"Hishu",
	"Dalu",
	"Gauru",
	"Urshul",
	"Urhan",
)




class TestCalcShapes(unittest.TestCase):
	"""
	Testfunktionen für das CalcShapes-Modul.
	"""

	def setUp(self):
		pass


	def test__strength(self):
		"""
		Überprüft ide Berechnung der Stärke.
		"""

		for val_1 in range(1, ATTRIBUTE_MAX + 1):
			for val_2 in SHAPES:
				self.assertGreaterEqual( CalcShapes.strength(val_1, val_2), val_1 )


	def test__dexterity(self):
		"""
		Überprüft ide Berechnung des Geschicks.
		"""

		for val_1 in range(1, ATTRIBUTE_MAX + 1):
			for val_2 in SHAPES:
				self.assertGreaterEqual( CalcShapes.dexterity(val_1, val_2), val_1 )


	def test__stamina(self):
		"""
		Überprüft ide Berechnung der Widerstandsfähigkeit.
		"""

		for val_1 in range(1, ATTRIBUTE_MAX + 1):
			for val_2 in SHAPES:
				self.assertGreaterEqual( CalcShapes.stamina(val_1, val_2), val_1 )


	def test__manipulation(self):
		"""
		Überprüft ide Berechnung der Manipulation.
		"""

		for val_1 in range(1, ATTRIBUTE_MAX + 1):
			for val_2 in SHAPES:
				self.assertLesserEqual( CalcShapes.stamina(val_1, val_2), val_1 )
