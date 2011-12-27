# -*- coding: utf-8 -*-

"""
\file
\author Victor von Rhein <victor@caern.de>

\section License

Copyright (C) 2011 by Victor von Rhein

This file is part of SoulCreator.

SoulCreator is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SoulCreator is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with SoulCreator.  If not, see <http://www.gnu.org/licenses/>.
"""




from __future__ import division, print_function

#import traceback

#from PySide.QtCore import QObject, QFile

#from src.Config import Config
#from src import Error
#from ReadXml import ReadXml
#from src.Debug import Debug




class cv_CreationPoints(object):
	"""
	@brief Datentyp für die freien Erschaffungspunkte.

	In dieser Klasse werden die freien Erschaffungspunkte eines einzigen Eigenschaftstyps gespeichert, natürlich abhängig von der Spezies.
	"""

	# Für welche Spezies diese Punkte zählen.
	species = ""

	# Für welchen Eigenscahftstyp diese Punkte zählen.
	typ = ""

	# Punkte.
	#
	# Bei Attributen und Fertigkeiten:
	#
	# Index 0 -> primär.
	#
	# Index 1 -> sekundär.
	#
	# Index 2 -> tertiär.
	#
	# Bei Fertigkeiten:
	# Index 3 -> Spezialisierungen
	points = []


	def __eq__(self, other):
		if id(self) == id(other):
			return True
		else:
			return ((self.species == other.species) and (self.typ == other.typ) and (self.points == other.points))



