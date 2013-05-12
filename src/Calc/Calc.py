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
Allgemeine Berechnungen.
"""




from PyQt4.QtCore import QDate

import src.Config as Config
#from src import Error
#from src.Widgets.Components.CharaTrait import CharaTrait
import src.Debug as Debug




def years(date_1, date_2):
	"""
	Berechnet die Anzahl der Jahre zwischen den beiden Daten.

	Funktioniert nur mit QDate.
	"""

	days_between_dates = date_1.daysTo( date_2 )
	years = days_between_dates // 365

	#Debug.debug(date_1, date_2, time_between_dates)

	return years


def calc_size( age, is_giant=False, is_small=False ):
	"""
	Berechnet den abstrakten Größenwert.
	"""

	result = Config.SIZE_DEFAULT["Adult"]
	if age < Config.AGE_ADULT:
		result = Config.SIZE_DEFAULT["Kid"]

	if is_giant:
		result += 1
	elif is_small:
		result -= 1

	return result


def calc_initiative( *args ):
	"""
	Berechnet die Initiative.

	Monster (Finesse und Resistance), addieren keinen Basiswert hinzu. Humanoide (normale Attribute) schon.

	\todo Bislang nur von Dexterity, Composure und Fast Reflexes abhängig. Möglicherweise vorhandene übernatürliche Eigenschaften werden nicht berücksichtigt.
	"""

	result = sum( args )

	return result


def calc_speed( *args, monster=False ):
	"""
	Berechnet die abstrakte Geschwindigkeit.

	\todo Bislang nur von Dexterity, Composure und Fast Reflexes abhängig. Möglicherweise vorhandene übernatürliche Eigenschaften werden nicht berücksichtigt.
	"""

	result = sum( args )

	if not monster:
		result += Config.SPEED_BASE_VALUE_HUMAN

	return result


def calc_defense( *args, age=None, size=None, maximize=False):
	"""
	Berechnet die Defense.

	Einige Kreaturen (Tiere, Monster etc.) Nutzen die größte Eigenschaft als Defense, nicht die kleinste.
	"""

	result = min( args )
	if maximize:
		result = max( args )

	## Bei kindern gibt auch die Größe (bzw. deren Abwesenheit) einen Bonus auf Defense.
	if age and size and age < Config.AGE_ADULT:
		modificator = Config.SIZE_DEFAULT["Adult"] - size
		modificator = max(modificator, 0)
		result = result + modificator

	return result


def calc_health(stamina, size):
	"""
	Berechnet die Gesundheit.
	"""

	return stamina + size


def calc_willpower(resolve, composure):
	"""
	Berechnet die Willenskraft.
	"""

	return resolve + composure


def calc_rank_spirit(power, finesse, resistance):
	"""
	Berechnet den Rang eines Geistes aus dessen Attributen.
	"""

	result = power + finesse + resistance

	rank = 1
	if result > 25:
		rank = 5
	elif result > 19:
		rank = 4
	elif result > 13:
		rank = 3
	elif result > 7:
		rank = 2

	return rank
