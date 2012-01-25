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
#from ReadXml import ReadXml
from src.Debug import Debug
#from src.Error import ErrTraitType




class BasicTrait(QObject):
	"""
	@brief Speichert alle Eigenschaften einer einzigen Charaktereigenschaft.

	Simple Eigenschaften wie Attribute haben nur Name und Wert. Bei Fertigkeiten kommen bereits die Spezialisierungen hinzu, bei  Vorzügen noch die Einschränkungen etc.
	"""


	valueChanged = Signal(int)
	customTextChanged = Signal(str)
	availableChanged = Signal(bool)
	traitChanged = Signal(object)


	def __init__(self, character, name="", value=0, parent=None):
		"""
		Die Referenz auf character benötige ich nur, damit ich bei Eigenschaften mit Voraussetzungen diese auch überprüfen kann.

		\ref checkPrerequisites
		"""
		
		QObject.__init__(self, parent)

		self.__character = character

		self.__identifier = name
		self.__name = name
		self.__species = ""
		self.__value = value
		self.__prerequisites = False
		self.__prerequisitesText = ""
		self.__available = True

		# In dieser Liste werden Verweise auf alle Eigenschaften gespeichert, die in den Voraussetzungen erwähnung finden.
		self.__prerequisiteTraits = []


	@property
	def identifier(self):
		return self.__identifier

	@identifier.setter
	def identifier(self, identifier):
		self.__identifier = identifier


	@property
	def name(self):
		return self.__name

	@name.setter
	def name(self, name):
		self.__name = name


	def __getSpecies(self):
		return self.__species

	def __setSpecies(self, species):
		self.__species = species

	species = property(__getSpecies, __setSpecies)


	def __getValue(self):
		return self.__value

	def setValue(self, value):
		"""
		Verändert den Wert der Eigenschaft.
		"""
		
		if self.__value != value:
			self.__value = value
			#Debug.debug("Ändere Eigenschaft {} zu {}".format(self.name, self.value))
			self.valueChanged.emit(value)
			self.traitChanged.emit(self)

	value = property(__getValue, setValue)


	def __getPrerequisites(self):
		return self.__prerequisites

	def __setPrerequisites(self, prerequisites):
		self.__prerequisites = prerequisites

	hasPrerequisites = property(__getPrerequisites, __setPrerequisites)


	def __getPrerequisitesText(self):
		return self.__prerequisitesText

	def __setPrerequisitesText(self, text):
		if self.__prerequisitesText != text:
			self.__prerequisitesText = text
			#self.prerequisitesTextChanged.emit(text)

	prerequisitesText = property(__getPrerequisitesText, __setPrerequisitesText)


	def isAvailable(self):
		"""
		Gibt zurück, ob die Voraussetzungen der Eigenschaft erfüllt sind, ode rnicht.
		"""

		return self.__available

	def setAvailable( self, sw ):
		"""
		Legt fest, ob die Eigenschaft zur Verfügung steht oder nicht.
		"""

		if ( self.__available != sw ):
			self.__available = sw
			self.availableChanged.emit( sw )


	def checkPrerequisites(self, trait):
		self.__character.checkPrerequisites(self)


	@property
	def prerequisiteTraits(self):
		"""
		Eine Liste mit Verweisen auf alle Eigenschaften, die in den Voraussetzungen dieser Eigenschaft vorkommen.
		"""

		return self.__prerequisiteTraits

	@prerequisiteTraits.setter
	def prerequisiteTraits(self, prerequisites):
		if self.__prerequisiteTraits != prerequisites:
			self.__prerequisiteTraits = prerequisites

	def addPrerequisiteTrait(self, prerequisite):
		"""
		Fügt den Verweis auf eine Eigenschaft hinzu.
		"""

		self.__prerequisiteTraits.append(prerequisite)

