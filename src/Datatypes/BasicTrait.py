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

from PyQt4.QtCore import pyqtSignal as Signal

#from src.Config import Config
from src.Datatypes.AbstractTrait import AbstractTrait
#from src.Error import ErrTraitType
#from src.Debug import Debug




class BasicTrait(AbstractTrait):
	"""
	@brief Speichert alle Eigenschaften einer einzigen Charaktereigenschaft.

	Simple Eigenschaften wie Attribute haben nur Name und Wert. Bei Fertigkeiten kommen bereits die Spezialisierungen hinzu, bei  Vorzügen noch die Einschränkungen etc.
	"""


	availableChanged = Signal(bool)


	def __init__(self, character, name="", value=0, parent=None):
		"""
		Die Referenz auf character benötige ich nur, damit ich bei Eigenschaften mit Voraussetzungen diese auch überprüfen kann.

		\ref checkPrerequisites
		"""
		
		super(BasicTrait, self).__init__(name, value, parent)

		self.__character = character
		self.__species = ""
		self.__prerequisites = False
		self.__prerequisitesText = ""
		self.__available = True
		## Die Breeds, Factions für welche diese Unterkraft besonders günstig ist.
		self.cheap = []
		## Die Breeds, Factions welche diese Unterkraft überhaupt erwerben dürfen.
		self.only = []

		# In dieser Liste werden Verweise auf alle Eigenschaften gespeichert, die in den Voraussetzungen erwähnung finden.
		self.__prerequisiteTraits = []


	def __getSpecies(self):
		return self.__species

	def __setSpecies(self, species):
		self.__species = species

	species = property(__getSpecies, __setSpecies)


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

