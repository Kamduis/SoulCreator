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

from pprint import *

from PyQt4.QtCore import QDate

import src.Config as Config

from src.Storage.StorageTemplate import StorageTemplate
from src.Storage.StorageCharacter import StorageCharacter
from src.IO.ReadXmlTemplate import ReadXmlTemplate
from src.Calc.CalcAdvantages import CalcAdvantages

from res import rc_resource




ATTRIBUTE_MAX = 10




class TestCalcAdvantages(unittest.TestCase):
	"""
	Testfunktionen für das CalcAdvantages-Modul.
	"""

	def setUp(self):
		## Konstanten

		## Dummy-Template anlegen
		self._storage = StorageTemplate()

		## Templete füllen
		reader = ReadXmlTemplate( self._storage )
		reader.read()

		## Einen Dummy-Charakter anlegen
		self._character = StorageCharacter( self._storage )

		## Klasse initialisieren.
		self._calc = CalcAdvantages( self._character )


	def tearDown(self):
		self._calc      = None
		self._character = None
		self._storage   = None


	def test__calc_size(self):
		"""
		Überprüft, daß die Funktion der Berechnung der Größe auch Ergebnisse im zu erwartenden Rahmen zurückgibt.
		"""

		for age in range( Config.AGE_ADULT - 1, Config.AGE_ADULT + 1 ):
			results_expected = tuple( range(Config.SIZE_DEFAULT["Adult"] - 1, Config.SIZE_DEFAULT["Adult"] + 2) )
			if age < Config.AGE_ADULT:
				results_expected = tuple( range(Config.SIZE_DEFAULT["Kid"] - 1, Config.SIZE_DEFAULT["Kid"] + 2) )

			self._character.dateBirth = self._character.dateGame.addYears( -age )
			for large_value in ( 0, 4, ):
				self._character.traits["Merit"]["Physical"]["Giant"].value = large_value
				self._character.traits["Merit"]["Physical"]["GiantKid"].value = large_value
				for small_value in ( 0, 1, ):
					self._character.traits["Flaw"]["Physical"]["Dwarf"].value = small_value
					self._character.traits["Merit"]["Physical"]["Tiny"].value = small_value
					self.assertIn( self._calc.calc_size(), results_expected )


	def test__calc_initiative(self):
		"""
		Überprüft die Berechnung der Initiative.
		"""

		for attr_1 in range( 1, ATTRIBUTE_MAX + 1 ):
			self._character.traits["Attribute"]["Physical"]["Dexterity"].value = attr_1
			for attr_2 in range( 1, ATTRIBUTE_MAX + 1 ):
				self._character.traits["Attribute"]["Social"]["Composure"].value = attr_2
				for merit_1 in range( 1, 4 ):
					self._character.traits["Merit"]["Physical"]["Fast Reflexes"].value = merit_1
					self.assertEqual( self._calc.calcInitiative(), attr_1 + attr_2 + merit_1 )


	def test__calc_speed(self):
		"""
		Überprüft die Berechnung der Geschwindigkeit.
		"""

		for attr_1 in range( 1, ATTRIBUTE_MAX + 1 ):
			self._character.traits["Attribute"]["Physical"]["Strength"].value = attr_1
			for attr_2 in range( 1, ATTRIBUTE_MAX + 1 ):
				self._character.traits["Attribute"]["Physical"]["Dexterity"].value = attr_2
				for merit_1 in range( 4 ):
					self._character.traits["Merit"]["Physical"]["Fleet of Foot"].value = merit_1
					self.assertEqual( self._calc.calcSpeed(), attr_1 + attr_2 + merit_1 + Config.SPEED_BASE_VALUE_HUMAN )


	def test__calc_defense(self):
		"""
		Überprüft die Berechnung der Geschwindigkeit.
		"""

		results_expected = tuple( range( 0, ATTRIBUTE_MAX + Config.SIZE_DEFAULT["Adult"] + 1 ) )

		for val_1 in range( 1, ATTRIBUTE_MAX + 1 ):
			self._character.traits["Attribute"]["Mental"]["Wits"].value = val_1
			for val_2 in range( 1, ATTRIBUTE_MAX + 1 ):
				self._character.traits["Attribute"]["Physical"]["Dexterity"].value = val_2
				for age in range( Config.AGE_ADULT - 1, Config.AGE_ADULT + 1 ):
					self._character.dateBirth = self._character.dateGame.addYears( -age )
					for val_4 in ( "small", "normal", "large", ):
						self._character.traits["Merit"]["Physical"]["Giant"].value = 0
						self._character.traits["Merit"]["Physical"]["GiantKid"].value = 0
						self._character.traits["Flaw"]["Physical"]["Dwarf"].value = 0
						self._character.traits["Merit"]["Physical"]["Tiny"].value = 0
						if val_4 == "small":
							self._character.traits["Flaw"]["Physical"]["Dwarf"].value = 1
							self._character.traits["Merit"]["Physical"]["Tiny"].value = 1
						elif val_4 == "large":
							self._character.traits["Merit"]["Physical"]["Giant"].value = 1
							self._character.traits["Merit"]["Physical"]["GiantKid"].value = 1
						self.assertIn( self._calc.calcDefense(), results_expected )


	def test__calc_health(self):
		"""
		Überprüft die Berechnung der Gesundheit.
		"""

		for val_1 in range( 1, ATTRIBUTE_MAX + 1 ):
			self._character.traits["Attribute"]["Physical"]["Stamina"].value = val_1
			for age in range( Config.AGE_ADULT - 1, Config.AGE_ADULT + 1 ):
				self._character.dateBirth = self._character.dateGame.addYears( -age )
				for val_2 in ( "small", "normal", "large", ):
					self._character.traits["Merit"]["Physical"]["Giant"].value = 0
					self._character.traits["Merit"]["Physical"]["GiantKid"].value = 0
					self._character.traits["Flaw"]["Physical"]["Dwarf"].value = 0
					self._character.traits["Merit"]["Physical"]["Tiny"].value = 0
					if val_2 == "small":
						self._character.traits["Flaw"]["Physical"]["Dwarf"].value = 1
						self._character.traits["Merit"]["Physical"]["Tiny"].value = 1
					elif val_2 == "large":
						self._character.traits["Merit"]["Physical"]["Giant"].value = 1
						self._character.traits["Merit"]["Physical"]["GiantKid"].value = 1
					self.assertEqual( self._calc.calcHealth(), val_1 + self._calc.calc_size() )


	def test__calc_willpower(self):
		"""
		Überprüft die Berechnung der Willenskraft.
		"""

		for val_1 in range( 1, ATTRIBUTE_MAX + 1 ):
			self._character.traits["Attribute"]["Mental"]["Resolve"].value = val_1
			for val_2 in range( 1, ATTRIBUTE_MAX + 1 ):
				self._character.traits["Attribute"]["Social"]["Composure"].value = val_2
				self.assertEqual( self._calc.calcWillpower(), val_1 + val_2 )
