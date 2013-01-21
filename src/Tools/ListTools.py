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


def uniqify_ordered(seq, idfun=None):
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


def find_key(dictionary, item):
	"""
	Gibt den key des dictionarys zurück, wenn man das Item angibt.
	"""

	return [k for k, v in dictionary.iteritems() if v == item][0]
