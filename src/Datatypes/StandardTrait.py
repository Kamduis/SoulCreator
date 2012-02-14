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

from PySide.QtCore import QObject, Signal

#from src.Config import Config
from src.Datatypes.BasicTrait import BasicTrait
from src.Debug import Debug
#from src.Error import ErrTraitType




class StandardTrait(BasicTrait):
	"""
	@brief Speichert alle Eigenschaften einer einzigen Charaktereigenschaft.

	Simple Eigenschaften wie Attribute haben nur Name und Wert. Bei Fertigkeiten kommen bereits die Spezialisierungen hinzu, bei  Vorzügen noch die Einschränkungen etc.
	"""


	customTextChanged = Signal(str)
	specialtiesChanged = Signal(object)
	totalspecialtiesChanged = Signal(object)


	def __init__(self, character, name="", value=0, parent=None):
		BasicTrait.__init__(self, character, name, value, parent)

		self.__specialties = []
		self.__age = ""
		self.__era = ""
		self.__custom = False
		self.__customText = ""

		self.specialtiesChanged.connect(self.totalspecialtiesChanged)


	def __getSpecialties(self):
		return self.__specialties

	def __setSpecialties(self, specialties):
		if self.__specialties != specialties:
			self.__specialties = specialties
			self.specialtiesChanged.emit(specialties)
			self.traitChanged.emit(self)

	specialties = property(__getSpecialties, __setSpecialties)

	totalspecialties = property(__getSpecialties)

	def appendSpecialty(self, name):
		"""
		Fügt der Liste von SPezialisierungen eine hinzu.

		\note Diese Methode muß verwendet werden, wenn man das Signal \ref specialtyChanged nutzen möchte.
		"""

		self.__specialties.append(name)
		self.specialtiesChanged.emit(self.specialties)
		self.traitChanged.emit(self)

	def removeSpecialty(self, name):
		"""
		Fügt der Liste von SPezialisierungen eine hinzu.

		\note Diese Methode muß verwendet werden, wenn man das Signal \ref specialtyChanged nutzen möchte.
		"""

		self.__specialties.remove(name)
		self.specialtiesChanged.emit(self.specialties)
		self.traitChanged.emit(self)


	def __getEra(self):
		return self.__era

	def __setEra(self, era):
		self.__era = era

	era = property(__getEra, __setEra)


	def __getAge(self):
		return self.__age

	def __setAge(self, age):
		self.__age = age

	age = property(__getAge, __setAge)


	def isCustom(self):
		return self.__custom

	def setCustom(self, custom):
		self.__custom = custom


	def __getCustomText(self):
		return self.__customText

	def __setCustomText(self, text):
		if self.__customText != text:
			self.__customText = text
			self.customTextChanged.emit(text)

	customText = property(__getCustomText, __setCustomText)