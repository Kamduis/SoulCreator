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

import sys
import os

#from src.Config import Config




class PathTools():
	"""
	@brief Hilfsfunktionen beim Umgang mit Dateien und Pfaden.
	"""

	def __init__(self):
		pass


	@staticmethod
	def getPath():
		"""
		Bestimmt den Pfad zu diesem Skript, unabhängig davon, wie es ausgeführt wird.
		"""

		# Bestimmt, ob diese Anwednung eine normale Python-Ausfürhung ist oder ob es sich um eine "Frozen Executable" handelt.
		if hasattr(sys,  'frozen'):
			# Es wird eine "Frozen Executable" ausgeführt.
			dir_path = os.path.dirname(sys.executable)
		elif '__file__' in locals():
			# Es wird ein normales py-Skript ausgeführt.
			dir_path = os.path.dirname(__file__)
		else:
			# Es wird von der Kommandozeile gestartet.
			dir_path = sys.path[0]
		return dir_path





class ImageTools():
	"""
	@brief Hilfsfunktionen, im Umgang mit Bildern.
	"""

	def __init__(self):
		pass


	@staticmethod
	def genderSymbol(gender):
		"""
		Gibt das Symbol für das Übergebene Geschlecht aus.
		"""

		if gender.lower() == "female" or gender.lower() == "m" or gender.lower() == "w":
			return "♀"
		elif gender.lower() == "male" or gender.lower() == "m":
			return "♂"
		else:
			return "⚥"




class ListTools():
	"""
	@brief Hilfsfunktionen für den Umgang mit Listen.
	"""

	def __init__(self):
		pass


	@staticmethod
	def uniqify(seq):
		"""
		\brief Löscht alle Duplukate aus einer Liste.
		
		Garantiert /nicht/ das Beibnehalten der Reihenfolge der Original-Liste.

		\note Diese Methode kann etwas schneller sein, als \ref uniqifyOrdered
		"""
		
		keys = {}
		for e in seq:
			keys[e] = 1
		return keys.keys()


	@staticmethod
	def uniqifyOrdered(seq, idfun=None):
		"""
		\brief Löscht alle Duplukate aus einer Liste.

		Garantiert das Beibehalten der Reihenfolge der Original-Liste.

		\note Diese Methode kann etwas langsamer sein, als \ref uniqify

		>>> a=list('ABeeE')
		>>> f5(a)
		['A','B','e','E']
		>>> f5(a, lambda x: x.lower())
		['A','B','e']
		"""

		if idfun is None:
			def idfun(x): return x
		seen = {}
		result = []
		for item in seq:
			marker = idfun(item)
			if marker in seen:
				continue
			seen[marker] = 1
			result.append(item)
		return result


	@staticmethod
	def findKey(dictionary, item):
		"""
		Gibt den key des dictionarys zurück, wenn man das Item angibt.
		"""

		return [k for k, v in dictionary.iteritems() if v == item][0]

