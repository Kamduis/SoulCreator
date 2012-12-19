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




"""
Einfache Berechnungen betreffend des unterschiedlichen Werwolf-Gestalten.
"""




#from PyQt4.QtCore import pyqtSignal as Signal
#from PyQt4.QtCore import QObject
#from PyQt4.QtGui import QWidget, QVBoxLayout, QGridLayout, QLabel, QFrame, QButtonGroup

import src.Config as Config
#from src import Error
#import src.Debug as Debug




def strength( value, shape ):
	"""
	Berechnet die Strength des Charakters abhängig von den unterschiedlichen Gestalten.
	"""

	if shape == Config.SHAPES_WEREWOLF[1]:
		return value + 1
	elif shape == Config.SHAPES_WEREWOLF[2]:
		return value + 3
	elif shape == Config.SHAPES_WEREWOLF[3]:
		return value + 2
	else:
		return value


def dexterity( value, shape ):
	"""
	Berechnet die Dexterity des Charakters abhängig von den unterschiedlichen Gestalten.
	"""

	if shape == Config.SHAPES_WEREWOLF[2]:
		return value + 1
	elif shape == Config.SHAPES_WEREWOLF[3] or shape == Config.SHAPES_WEREWOLF[4]:
		return value + 2
	else:
		return value


def stamina( value, shape ):
	"""
	Berechnet die Stamina des Charakters abhängig von den unterschiedlichen Gestalten.
	"""

	if shape == Config.SHAPES_WEREWOLF[1] or shape == Config.SHAPES_WEREWOLF[4]:
		return value + 1
	elif shape == Config.SHAPES_WEREWOLF[2] or shape == Config.SHAPES_WEREWOLF[3]:
		return value + 2
	else:
		return value


def manipulation( value, shape ):
	"""
	Berechnet die Manipulation des Charakters abhängig von den unterschiedlichen Gestalten.
	"""

	if shape == Config.SHAPES_WEREWOLF[1]:
		return value - 1
	elif shape == Config.SHAPES_WEREWOLF[3]:
		return value - 3
	else:
		return value


def size( value, shape ):
	"""
	Berechnet die Größe des Charakters abhängig von den unterschiedlichen Gestalten.
	"""

	if shape == Config.SHAPES_WEREWOLF[1] or shape == Config.SHAPES_WEREWOLF[3]:
		return value + 1
	elif shape == Config.SHAPES_WEREWOLF[2]:
		return value + 2
	elif shape == Config.SHAPES_WEREWOLF[4]:
		return value - 1
	else:
		return value


def initiative( value, shape ):
	"""
	Berechnet die Initiative des Charakters abhängig von den unterschiedlichen Gestalten.
	"""

	if shape == Config.SHAPES_WEREWOLF[2]:
		return value + 1
	elif shape == Config.SHAPES_WEREWOLF[3] or shape == Config.SHAPES_WEREWOLF[4]:
		return value + 2
	else:
		return value


def speed( value, shape ):
	"""
	Berechnet die Geschwindigkeit des Charakters abhängig von den unterschiedlichen Gestalten.
	"""

	if shape == Config.SHAPES_WEREWOLF[1]:
		return value + 1
	elif shape == Config.SHAPES_WEREWOLF[2]:
		return value + 4
	elif shape == Config.SHAPES_WEREWOLF[3]:
		return value + 7
	elif shape == Config.SHAPES_WEREWOLF[4]:
		return value + 5
	else:
		return value


def defense( wits, dex, shape ):
	"""
	Berechnet die Verteidigung des Charakters abhängig von den unterschiedlichen Gestalten.
	"""

	return min( wits, dexterity( dex, shape ) )


def health( value, shape ):
	"""
	Berechnet die Geschwindigkeit des Charakters abhängig von den unterschiedlichen Gestalten.
	"""

	if shape == Config.SHAPES_WEREWOLF[1]:
		return value + 2
	elif shape == Config.SHAPES_WEREWOLF[2]:
		return value + 4
	elif shape == Config.SHAPES_WEREWOLF[3]:
		return value + 3
	else:
		return value


def height( value, strength, stamina, shape ):
	"""
	Berechnet die Körpergröße der jeweiligen Gestalt aus der Größe Hishu-Gestalt und den körperlichen Attributen.

	\todo Möglicherweise noch einen Hauch Zufall einfügen, der aber bei einem Charakter immer gleich sein sollte, also vielleicht mit dem Namen seeden oder so ähnlich.

	\todo Geschlecht berücksichtigen? Weibchen sind um 2 bis 12 % kleiner als die Rüden und 20 bis 25 % leichter.
	"""

	result = value

	if shape == Config.SHAPES_WEREWOLF[1]:
		## gewinnt 4 bis 6 in an Größe
		result = value + ( 4 + min(10, strength + stamina) / 5 ) * Config.INCH_IN_METER
	elif shape == Config.SHAPES_WEREWOLF[2]:
		## gewinnt 2 bis 3 ft an Größe
		result = value + ( 2 + min(10, strength + stamina) / 10 ) * Config.FOOT_IN_METER
	elif shape == Config.SHAPES_WEREWOLF[3]:
		## 3 bis 5 ft Schulterhöhe. Hishu-Größe hat auch Einfluß. Große Charaktere ergeben größere Wölfe.
		result = ( 3 + min( 10, strength + stamina ) / 10 + min( 2, value ) / 2 ) * Config.FOOT_IN_METER
	elif shape == Config.SHAPES_WEREWOLF[4]:
		## Wölfe haben Schulterhöhe von 70 bis 90 cm
		result = ( 7 + min( 10, strength + stamina ) / 10 + min( 2, value ) / 2 ) * 0.1

	return round(result, 2)


def weight( value, strength, stamina, shape ):
	"""
	Berechnet das Körpergewicht der jeweiligen Gestalt aus dem Gewicht Hishu-Gestalt und den körperlichen Attributen.

	\todo Möglicherweise noch einen Hauch Zufall einfügen, der aber bei einem Charakter immer gleich sein sollte, also vielelicht mit dem Namen seeden oder so ähnlich.

	\todo Geschlecht berücksichtigen?
	"""

	result = value

	if shape == Config.SHAPES_WEREWOLF[1]:
		## gewinnt 12.5 bis 25 kg an Gewicht
		result = value + ( 1 + min(10, strength + stamina) / 10 ) * 12.5
	elif shape == Config.SHAPES_WEREWOLF[2]:
		## gewinnt 100 bis 125 kg an Gewicht
		result = value + 100 + ( min(10, strength + stamina) / 10 ) * 25
	elif shape == Config.SHAPES_WEREWOLF[3]:
		## 90% des Gauru-Gewichts
		result = .9 * weight( value, strength, stamina, Config.SHAPES_WEREWOLF[2] )
	elif shape == Config.SHAPES_WEREWOLF[4]:
		## Wölfe wiegen 35 bis 67 kg
		result = 35 + ( min( 10, strength + stamina ) / 10 + min( 100, value ) / 100 ) * 16

	return round(result, 2)
