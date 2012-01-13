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

#from PySide.QtCore import QObject, Signal
#from PySide.QtGui import QWidget, QVBoxLayout, QGridLayout, QLabel, QFrame, QButtonGroup

#from src.Config import Config
#from src import Error
from src.Debug import Debug




class CalcShapes(object):
	"""
	\brief Einfache Berechnungen.
	"""


	def __init__(self):
		pass


	@staticmethod
	def werewolfHeight( height, strength, stamina ):
		"""
		Berechnet die Körpergröße der übrigen vier Werwolfgestalten aus der Hishu-Gestalt und den körperlichen Attributen.

		\todo Möglicherweise noch einen Hauch Zufall einfügen, der aber bei einem Charakter immer gleich sein sollte, also vielelicht mit dem Namen seeden oder so ähnlich.

		\todo GEschlecht berücksichtigen? Weibchen sind um 2 bis 12 % kleiner als die Rüden und 20 bis 25 % leichter.
		"""

		## gewinnt 4 bis 6 in an Größe.
		heightDalu = height + 0.1 + 0.003125 * max(0, strength - 1) * max(0, stamina - 1)

		## gewinnt 2 bis 3 ft an Größe.
		heightGauru = height + 0.61 + 0.0381 * max(0, strength - 1) * max(0, stamina - 1)

		## 3 bis 5 ft Schulterhöhe. Hishu-Größe hat Einfluß, indem Durchschnittsgröße 1.7 m angenommen wird.
		heightUrshul = (height - .7) * 0.9144 + 0.038125 * max(0, strength - 1) * max(0, stamina - 1)

		## Wölfe haben Schulterhöhe von 70 bis 90 cm
		heightUrhan = (height - .7) * 0.8

		result =  [height, heightDalu, heightGauru, heightUrshul, heightUrhan]

		for i in xrange(len(result)):
			result[i] = round(result[i], 2)

		return result


	@staticmethod
	def werewolfWeight( weight, strength, stamina ):
		"""
		Berechnet das Körpergewicht der übrigen vier Werwolfgestalten aus der Hishu-Gestalt und den körperlichen Attributen.

		\todo Möglicherweise noch einen Hauch Zufall einfügen, der aber bei einem Charakter immer gleich sein sollte, also vielelicht mit dem Namen seeden oder so ähnlich.

		\todo GEschlecht berücksichtigen?
		"""

		## gewinnt 12.5 bis 25 kg an Gewicht.
		weightDalu = weight + 12.5 + 0.78125 * max(0, strength - 1) * max(0, stamina - 1)

		## gewinnt 100 bis 125 kg an Gewicht.
		weightGauru = weight + 100 + 1.5625 * max(0, strength - 1) * max(0, stamina - 1)

		weightUrshul = 0.9 * weightGauru

		## Wölfe Wiegen 35 bis 67 kg
		weightUrhan = 0.77 * weight

		result =  [weight, weightDalu, weightGauru, weightUrshul, weightUrhan]

		for i in xrange(len(result)):
			result[i] = round(result[i], 2)

		return result


