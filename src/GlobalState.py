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




class GlobalState(object):
	"""
	@brief Diese Klasse speichert alle globalen Einstellungen für das Programm.

	\note Diese Klasse folgt dem Borg-Pattern.
	"""

	_isDebug = False
	_isDevelop = False
	_isFallback = False
	isVerbose = False

	_shared = {}
	def __new__(cls, *args, **kwargs):
		inst = object.__new__(cls, *args, **kwargs)
		inst.__dict__ = cls._shared
		return inst


	@property
	@staticmethod
	def isDebug():
		return GlobalState._isDebug

	@isDebug.setter
	@staticmethod
	def isDebug(sw):
		GlobalState._isDebug = sw


	@property
	@staticmethod
	def isDevelop():
		return GlobalState._isDevelop

	@isDebug.setter
	@staticmethod
	def isDevelop(sw):
		GlobalState._isDevelop = sw


	@property
	@staticmethod
	def isFallback():
		return GlobalState._isFallback

	@isDebug.setter
	@staticmethod
	def isFallback(sw):
		GlobalState._isFallback = sw









