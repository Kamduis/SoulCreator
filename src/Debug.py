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
Erlaubt einfachen Zugriff auf Debug-Informationen.
"""




import inspect
import time

import src.Config as Config
import src.GlobalState as GlobalState




def debug( *args, level=Config.DEBUG_LEVEL_STD ):
	"""
	Gibt einen Text aus.

	Der vom Nutzer beim Programmaufruf gewählte Debug level bestimmt, wie ausfühlrich die Debug-Informationen sind und welche davon überhaupt angezeigt werden. Beispielsweise wird der Ort des Aufrufs dieser Funktion nur vorangestellt, wenn der gewählte Debug-Level hoch genug ist) Standardmäßig entfällt diese Anzeige.

	\param level Ab welchem debug-level diese debug-Nachricht angezeigt wird.
	"""

	if level <= Config.DEBUG_LEVEL_NONE:
		raise ValueError( "A level smaller than {} is not supported.".format(Config.DEBUG_LEVEL_NONE + 1) )

	if GlobalState.debug_level and GlobalState.debug_level > Config.DEBUG_LEVEL_NONE and GlobalState.debug_level >= level:
		## Dateiname und Zeilennummer der Debug-Ausgabe werden nur ausgegeben, wenn der Debug-Level hoch genug ist. Normalerweise wird darauf aufgrund der Übersichtlichkeit verzichtet.
		if GlobalState.debug_level > Config.DEBUG_LEVEL_STD:
			print("{:<78}\tl. {:<4}\t{:<18}".format(inspect.stack()[1][1], inspect.stack()[1][2], inspect.stack()[1][3]))
		for arg in args:
			print(arg)


#def stack( *args ):
	#"""
	#???
	#"""

	#if GlobalState.debug_level and GlobalState.debug_level > Config.DEBUG_LEVEL_NONE:
		#for item in inspect.stack():
			#print("{}\t{:<78}\t{}".format(item[0], item[1], item[3]))


def timehook( level=Config.DEBUG_LEVEL_STD + 1 ):
	if GlobalState.debug_level >= level:
		return time.time()


def timer( start, end, text=None, level=Config.DEBUG_LEVEL_STD + 1 ):
	_text = ""
	if text:
		if text[-1] == ".":
			_text = text[:-1]
		else:
			_text = text[:-1]
		_text += ": "
	debug( "{text}{time:.3f} seconds.".format(text=_text, time=(end - start) ), level=level )


def timesince( start, text=None, level=Config.DEBUG_LEVEL_STD + 1 ):
	if GlobalState.debug_level >= level:
		end = time.time()
		timer(start, end, text, level=level)
