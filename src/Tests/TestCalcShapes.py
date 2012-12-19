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

import src.Config as Config

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
		Überprüft die Berechnung der Stärke.
		"""

		for val_1 in range(1, ATTRIBUTE_MAX + 1):
			for shape in SHAPES:
				self.assertGreaterEqual( CalcShapes.strength(val_1, shape), val_1 )


	def test__dexterity(self):
		"""
		Überprüft die Berechnung des Geschicks.
		"""

		for val_1 in range(1, ATTRIBUTE_MAX + 1):
			for shape in SHAPES:
				self.assertGreaterEqual( CalcShapes.dexterity(val_1, shape), val_1 )


	def test__stamina(self):
		"""
		Überprüft die Berechnung der Widerstandsfähigkeit.
		"""

		for val_1 in range(1, ATTRIBUTE_MAX + 1):
			for shape in SHAPES:
				self.assertGreaterEqual( CalcShapes.stamina(val_1, shape), val_1 )


	def test__manipulation(self):
		"""
		Überprüft ide Berechnung der Manipulation.
		"""

		for val_1 in range(1, ATTRIBUTE_MAX + 1):
			for shape in SHAPES:
				self.assertLessEqual( CalcShapes.manipulation(val_1, shape), val_1 )


	def test__manipulation(self):
		"""
		Überprüft ide Berechnung der Manipulation.
		"""

		for val_1 in range(1, ATTRIBUTE_MAX + 1):
			for shape in SHAPES:
				self.assertLessEqual( CalcShapes.manipulation(val_1, shape), val_1 )


	def test__manipulation(self):
		"""
		Überprüft ide Berechnung der Manipulation.
		"""

		for val_1 in range(1, ATTRIBUTE_MAX + 1):
			for shape in SHAPES:
				self.assertLessEqual( CalcShapes.manipulation(val_1, shape), val_1 )


	def test__size(self):
		"""
		Überprüft ide Berechnung der Größe.
		"""

		for val_1 in range(1, ATTRIBUTE_MAX + 1):
			for shape in SHAPES:
				self.assertIn( CalcShapes.size(val_1, shape), range( val_1 - 1, val_1 + 3 ) )


	def test__initiative(self):
		"""
		Überprüft die Berechnung der Initiative.
		"""

		for val_1 in range(1, ATTRIBUTE_MAX + 1):
			for shape in SHAPES:
				self.assertIn( CalcShapes.initiative(val_1, shape), range( val_1, val_1 + 3 ) )


	def test__speed(self):
		"""
		Überprüft die Berechnung der Geschwindigkeit.
		"""

		for val_1 in range(1, ATTRIBUTE_MAX + 1):
			for shape in SHAPES:
				self.assertIn( CalcShapes.speed(val_1, shape), range( val_1, val_1 + 8 ) )


	def test__defense(self):
		"""
		Überprüft die Berechnung der Defense.
		"""

		for val_1 in range(1, ATTRIBUTE_MAX + 1):
			for val_2 in range(1, ATTRIBUTE_MAX + 1):
				for shape in SHAPES:
					self.assertEqual( CalcShapes.defense(val_1, val_2, shape), min( val_1, CalcShapes.dexterity( val_2, shape ) ) )


	def test__health(self):
		"""
		Überprüft die Berechnung der Gesundheit.
		"""

		for val_1 in range(1, ATTRIBUTE_MAX + 1):
			for shape in SHAPES:
				self.assertGreaterEqual( CalcShapes.health(val_1, shape), val_1 )


	def test__height(self):
		"""
		Überprüft die Berechnung der Körpergröße.
		"""

		height = 1.70

		for val_1 in range(1, ATTRIBUTE_MAX + 1):
			for val_2 in range(1, ATTRIBUTE_MAX + 1):
				for shape in SHAPES:
					if shape == SHAPES[1]:
						## Zwischen 4 in bis 6 in Größe mehr
						self.assertGreaterEqual( CalcShapes.height(height, val_1, val_2, shape), height + 4 * Config.INCH_IN_METER )
						self.assertLessEqual( CalcShapes.height(height, val_1, val_2, shape), height + 6 * Config.INCH_IN_METER )
					elif shape == SHAPES[2]:
						## Zwischen 2 ft bis 3 ft Größe mehr
						self.assertGreaterEqual( CalcShapes.height(height, val_1, val_2, shape), height + 2 * Config.FOOT_IN_METER )
						self.assertLessEqual( CalcShapes.height(height, val_1, val_2, shape), height + 3 * Config.FOOT_IN_METER )
					elif shape == SHAPES[3]:
						## Zwischen 3 ft bis 5 ft Größe 1 ft = 0,3048
						self.assertGreaterEqual( CalcShapes.height(height, val_1, val_2, shape), 3 * Config.FOOT_IN_METER )
						self.assertLessEqual( CalcShapes.height(height, val_1, val_2, shape), 5 * Config.FOOT_IN_METER )
					elif shape == SHAPES[4]:
						## Zwischen 70 bis 90 cm Größe
						self.assertGreaterEqual( CalcShapes.height(height, val_1, val_2, shape), .7 )
						self.assertLessEqual( CalcShapes.height(height, val_1, val_2, shape), .9 )
					else:
						self.assertEqual( CalcShapes.height(height, val_1, val_2, shape), height )


	def test__weight(self):
		"""
		Überprüft die Berechnung der Körpergröße.
		"""

		weight = 70

		for val_1 in range(1, ATTRIBUTE_MAX + 1):
			for val_2 in range(1, ATTRIBUTE_MAX + 1):
				for shape in SHAPES:
					if shape in SHAPES[0]:
						self.assertEqual( CalcShapes.weight(weight, val_1, val_2, shape), weight )
					elif shape in SHAPES[1]:
						## 12.5 bis 25 kg zusätzliches Gewicht
						self.assertGreaterEqual( CalcShapes.weight(weight, val_1, val_2, shape), weight + 12.5 )
						self.assertLessEqual( CalcShapes.weight(weight, val_1, val_2, shape), weight + 25 )
					elif shape in SHAPES[2]:
						## 100 bis 150 kg zusätzliches Gewicht
						self.assertGreaterEqual( CalcShapes.weight(weight, val_1, val_2, shape), weight + 100 )
						self.assertLessEqual( CalcShapes.weight(weight, val_1, val_2, shape), weight + 150 )
					elif shape in SHAPES[3]:
						## 90% des Gauru-Gewichts
						self.assertAlmostEqual( CalcShapes.weight(weight, val_1, val_2, shape), .9 * CalcShapes.weight(weight, val_1, val_2, SHAPES[2]) )
					else:
						## Wölfe Wiegen 35 bis 67 kg
						self.assertGreaterEqual( CalcShapes.weight(weight, val_1, val_2, shape), 35 )
						self.assertLessEqual( CalcShapes.weight(weight, val_1, val_2, shape), 67 )
