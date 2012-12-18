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

from PyQt4.QtCore import QDate

import src.Config as Config

import src.Calc.Calc as Calc




ATTRIBUTE_MAX = 10




class TestCalc(unittest.TestCase):
	"""
	Testfunktionen für das Calc-Modul.
	"""

	def setUp(self):
		pass


	def test__years_QDate(self):
		"""
		Überprüft, daß die Funktion der Berechnung der Jahre auch Ergebnisse im zu erwartenden Rahmen zurückgibt.
		"""
		
		DATE_STEP = 1
		DATE_YEAR = {
			"min": -1,
			"max": 2,
		}

		## Eine Liste mit Daten anlegen
		dates_all = []

		## Von ...
		year_min = DATE_YEAR["min"]
		## ... bis
		year_max = DATE_YEAR["max"]

		## Startdatum
		date_store = QDate(year_min, 1, 1)
		date_max = QDate(year_max, 1, 1)

		## Die Listen tatsächlich anlegen
		while date_store < date_max:
			dates_all.append( date_store )
			date_store = date_store.addDays( DATE_STEP )

		dates_to_compare = dates_all[:]
		results_expected = tuple( range( year_max - year_min + 1 ) )

		for date_1 in dates_all:
			dates_to_compare.remove( date_1 )
			for date_2 in dates_to_compare:
				self.assertIn( Calc.years(date_1, date_2), results_expected )


	def test__calc_size(self):
		"""
		Überprüft die Berechnung der Größen-Eigenschaft.
		"""

		for age in range( Config.AGE_ADULT - 1, Config.AGE_ADULT + 1 ):
			results_expected = tuple( range(Config.SIZE_DEFAULT["Adult"] - 1, Config.SIZE_DEFAULT["Adult"] + 2) )
			if age < Config.AGE_ADULT:
				results_expected = tuple( range(Config.SIZE_DEFAULT["Kid"] - 1, Config.SIZE_DEFAULT["Kid"] + 2) )

			for large in ( False, True, ):
				for small in ( False, True, ):
					self.assertIn( Calc.calc_size( age, is_giant=large, is_small=small ), results_expected )


	def test__calc_initiative_humanoid(self):
		"""
		Überprüft die Berechnung der Initiative bei Humanoiden (normale Attribute).
		"""

		for dex in range( 1, ATTRIBUTE_MAX + 1 ):
			for com in range( 1, ATTRIBUTE_MAX + 1 ):
				for fast in range( 4 ):
					self.assertEqual( Calc.calc_initiative( dex, com, fast ), dex + com + fast )


	def test__calc_initiative_monster(self):
		"""
		Überprüft die Berechnung der Initiative bei Monstren (Power, Finesse & Resistance).
		"""

		for fin in range( 1, ATTRIBUTE_MAX + 1 ):
			for res in range( 1, ATTRIBUTE_MAX + 1 ):
				self.assertEqual( Calc.calc_initiative( fin, res ), fin + res )


	def test__calc_speed_humanoid(self):
		"""
		Überprüft die Berechnung der Geschwindigkeit bei Humanoiden (normale Attribute).
		"""

		for val_1 in range( 1, ATTRIBUTE_MAX + 1 ):
			for val_2 in range( 1, ATTRIBUTE_MAX + 1 ):
				for val_3 in range( 4 ):
					self.assertEqual( Calc.calc_speed( val_1, val_2, val_3 ), val_1 + val_2 + val_3 + Config.SPEED_BASE_VALUE_HUMAN )


	def test__calc_speed_monster(self):
		"""
		Überprüft die Berechnung der Geschwindigkeit bei Monstren (Power, Finesse & Resistance).
		"""

		for val_1 in range( 1, ATTRIBUTE_MAX + 1 ):
			for val_2 in range( 1, ATTRIBUTE_MAX + 1 ):
				for val_3 in range( ATTRIBUTE_MAX + 1 ):
					self.assertEqual( Calc.calc_speed( val_1, val_2, val_3, monster=True ), val_1 + val_2 + val_3 )


	def test__calc_defense_humanoid(self):
		"""
		Überprüft die Berechnung der Defense.
		"""

		results_expected = tuple( range( 0, ATTRIBUTE_MAX + Config.SIZE_DEFAULT["Adult"] + 1 ) )

		for val_1 in range( 1, ATTRIBUTE_MAX + 1 ):
			for val_2 in range( 1, ATTRIBUTE_MAX + 1 ):
				for age in range( Config.AGE_ADULT - 1, Config.AGE_ADULT + 1 ):
					for val_3 in range( 1, 6 ):
						self.assertIn( Calc.calc_defense( val_1, val_2, age=age, size=val_3 ), results_expected )


	def test__calc_defense_monster(self):
		"""
		Überprüft die Berechnung der Defense.
		"""

		results_expected = tuple( range( 0, ATTRIBUTE_MAX + Config.SIZE_DEFAULT["Adult"] + 1 ) )

		for val_1 in range( 1, ATTRIBUTE_MAX + 1 ):
			for val_2 in range( 1, ATTRIBUTE_MAX + 1 ):
				self.assertEqual( Calc.calc_defense( val_1, val_2, maximize=True ), max( val_1, val_2 ) )


	def test__calc_health(self):
		"""
		Überprüft die Berechnung der Gesundheit.
		"""

		for val_1 in range( 1, ATTRIBUTE_MAX + 1 ):
			for val_2 in range( 3, 7 ):
				self.assertEqual( Calc.calc_health( val_1, val_2 ), val_1 + val_2 )


	def test__calc_willpower(self):
		"""
		Überprüft die Berechnung der Willenskraft.
		"""

		for val_1 in range( 1, ATTRIBUTE_MAX + 1 ):
			for val_2 in range( 1, ATTRIBUTE_MAX + 1 ):
				self.assertEqual( Calc.calc_willpower( val_1, val_2 ), val_1 + val_2 )
