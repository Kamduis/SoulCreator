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

#import src.Config as Config
#from src import Error
#from src.Widgets.Components.CharaTrait import CharaTrait
import src.Debug as Debug




def years(date_1, date_2):
	"""
	Berechnet die Anzahl der Jahre zwischen den beiden Daten.

	Funktioniert mit QDate- oder datetime-date-Objekten.
	"""

	## QDate wird in datetime.date verwandelt
	dates_to_use = [ date_1, date_2 ]
	for idx, date in enumerate( dates_to_use ):
		try:
			dates_to_use[idx] = date.toPyDate()
		except AttributeError as e:
			## Existiert die Funktion toPyDate nicht, handelt es sich nicht um ein QDate-Objekt, also kann direkt weitergearbeitet werden.
			pass

	time_between_dates = date_2 - date_1
	years = time_between_dates.days // 365

	#Debug.debug(date_1, date_2, time_between_dates)

	return years
