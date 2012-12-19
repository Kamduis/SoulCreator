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

	values = [wits, dexterity( dex, shape ), ]

	return min(values)


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


def werewolfHeight( value_height, str, sta ):
	"""
	Berechnet die Körpergröße der übrigen vier Werwolfgestalten aus der Hishu-Gestalt und den körperlichen Attributen.

	\todo Möglicherweise noch einen Hauch Zufall einfügen, der aber bei einem Charakter immer gleich sein sollte, also vielleicht mit dem Namen seeden oder so ähnlich.

	\todo Geschlecht berücksichtigen? Weibchen sind um 2 bis 12 % kleiner als die Rüden und 20 bis 25 % leichter.
	"""

	## gewinnt 4 bis 6 in an Größe.
	heightDalu = value_height + 0.1 + 0.003125 * max(0, str - 1) * max(0, sta - 1)

	## gewinnt 2 bis 3 ft an Größe.
	heightGauru = value_height + 0.61 + 0.0381 * max(0, str - 1) * max(0, sta - 1)

	## 3 bis 5 ft Schulterhöhe. Hishu-Größe hat Einfluß, indem Durchschnittsgröße 1.7 m angenommen wird.
	heightUrshul = (value_height - .7) * 0.9144 + 0.038125 * max(0, str - 1) * max(0, sta - 1)

	## Wölfe haben Schulterhöhe von 70 bis 90 cm
	heightUrhan = (value_height - .7) * 0.8

	result =  [value_height, heightDalu, heightGauru, heightUrshul, heightUrhan]

	for i in range(len(result)):
		result[i] = round(result[i], 2)

	return result


def werewolfWeight( weight, strength, stamina ):
	"""
	Berechnet das Körpergewicht der übrigen vier Werwolfgestalten aus der Hishu-Gestalt und den körperlichen Attributen.

	\todo Möglicherweise noch einen Hauch Zufall einfügen, der aber bei einem Charakter immer gleich sein sollte, also vielelicht mit dem Namen seeden oder so ähnlich.

	\todo Geschlecht berücksichtigen?
	"""

	## gewinnt 12.5 bis 25 kg an Gewicht.
	weightDalu = weight + 12.5 + 0.78125 * max(0, strength - 1) * max(0, stamina - 1)

	## gewinnt 100 bis 125 kg an Gewicht.
	weightGauru = weight + 100 + 1.5625 * max(0, strength - 1) * max(0, stamina - 1)

	weightUrshul = 0.9 * weightGauru

	## Wölfe Wiegen 35 bis 67 kg
	weightUrhan = 0.77 * weight

	result =  [weight, weightDalu, weightGauru, weightUrshul, weightUrhan]

	for i in range(len(result)):
		result[i] = round(result[i], 2)

	return result
