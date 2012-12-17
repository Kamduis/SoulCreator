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

import datetime

from pprint import *

from PyQt4.QtCore import QDate

import src.Calc.Calc as Calc




class TestCalc(unittest.TestCase):
	"""
	Testfunktionen für das Calc-Modul.
	"""

	def setUp(self):
		DATE_STEP = 1
		DATE_YEAR = {
			"min": -1,
			"max": 2,
		}

		## Eine Liste mit Daten anlegen
		self.dates_QDate = []

		## Von ...
		self.year_min = DATE_YEAR["min"]
		## ... bis
		self.year_max = DATE_YEAR["max"]

		## Startdatum
		date_store = QDate(self.year_min, 1, 1)
		date_max = QDate(self.year_max, 1, 1)

		## Die Listen tatsächlich anlegen
		while date_store < date_max:
			self.dates_QDate.append( date_store )
			date_store = date_store.addDays( DATE_STEP )


	def test_years_QDate(self):
		"""
		Überprüft, daß die Funktion der Berechnung der Jahre auch Ergebnisse im zu erwartenden Rahmen zurückgibt.
		"""

		dates_to_compare = self.dates_QDate[:]
		results_expected = list( range( self.year_max - self.year_min + 1 ) )

		for date_1 in self.dates_QDate:
			dates_to_compare.remove( date_1 )
			for date_2 in dates_to_compare:
				self.assertIn( Calc.years(date_1, date_2), results_expected )




if __name__ == '__main__':
	unittest.main()

