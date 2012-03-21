# -*- coding: utf-8 -*-

"""
\file
\author Victor von Rhein <victor@caern.de>

\section License

Copyright (C) Victor von Rhein, 2011, 2012

This file is part of SoulCreator.

SoulCreator is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SoulCreator is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with SoulCreator.  If not, see <http://www.gnu.org/licenses/>.
"""




from __future__ import division, print_function

#from PySide.QtCore import Signal# as Signal
#from PySide.QtCore import QObject
#from PySide.QtGui import QWidget, QVBoxLayout, QGridLayout, QLabel, QFrame, QButtonGroup

#from src.Config import Config
#from src import Error
#from ReadXml import ReadXml
#from src.Widgets.Components.CharaTrait import CharaTrait
#from src.Debug import Debug




class Calc(object):
	"""
	\brief Allgemeine Berechnungen.
	"""


	@staticmethod
	def years(date1, date2):
		"""
		Berechnet die Anzahl der Jahre zwischen den beiden Daten.
		"""

		#if date1 > date2:
			#cache = date1
			#date1 = date2
			#date2 = cache

		years = date2.year() - date1.year()
		if date2.month() < date1.month() or (date2.month() == date1.month() and date2.day() < date1.day()):
			years -= 1

		#Debug.debug(date1, date2, years)

		return years
