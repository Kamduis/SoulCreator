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




import sys
import os




def program_path():
	"""
	Gibt den Pfad des Programms aus, unabhängig davon, wie es ausgeführt wird.
	"""

	# Bestimmt, ob diese Anwednung eine normale Python-Ausfürhung ist oder ob es sich um eine "Frozen Executable" handelt.
	if hasattr(sys,  "frozen"):
		# Es wird eine "Frozen Executable" ausgeführt.
		dir_path = os.path.dirname(sys.executable)
	elif "__file__" in locals():
		# Es wird ein normales py-Skript ausgeführt.
		dir_path = os.path.dirname(__file__)
	else:
		# Es wird von der Kommandozeile gestartet.
		dir_path = sys.path[0]
	return dir_path
