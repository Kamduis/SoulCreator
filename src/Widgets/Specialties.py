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

#import traceback

from PySide.QtCore import Qt, Signal
#from PySide.QtGui import QWidget, QVBoxLayout, QGridLayout, QLabel, QFrame, QButtonGroup

#from src.Config import Config
#from src import Error
#from ReadXml import ReadXml
from src.Widgets.Components.CheckedList import CheckedList
from src.Debug import Debug




class Specialties(CheckedList):
	"""
	@brief Diese Spezialisierungen werden direkt mit dem Charakter verknüpft.

	\todo Es wäre toll, wenn der Benutzer eigene Spezialisierungen eintragen könnte, zusätzlich zu denen, die schon angeboten werden.
	"""

	def __init__(self, template, parent=None):
		CheckedList.__init__(self, parent)

		#self.__character = character
		self.__storage = template

		self.__trait = None

		self.itemStateChanged.connect(self.modifyTrait)


	def setSpecialties( self, specialties ):
		for item in specialties:
			state = Qt.Unchecked
			if ( item in self.__trait.specialties ):
				state = Qt.Checked

			self.addCheckableItem( item, state )


	def showSpecialties(self, sw, trait):
		self.clear()
		if sw:
			#Debug.debug("Zeige Spezialisierungen von {}".format(trait.name))
			if self.__trait != trait:
				# Vorherige Verbindung lösen.
				if self.__trait:
					self.__trait.specialtiesChanged.disconnect(self.reshowSpecialties)
				self.__trait = trait
				# Neue Verbindung aufbauen, damit beim Laden des Charakters die angezeigten Spezialisierungen automatisch richtig abgehakt werden.
				self.__trait.specialtiesChanged.connect(self.reshowSpecialties)
			#Debug.debug(self.__trait)
			for item in self.__storage:
				for subitem in self.__storage[item].items():
					#Debug.debug(subitem)
					if subitem[0] == trait.name:
						self.setSpecialties(subitem[1]["specialties"])
						return


	def reshowSpecialties(self):
		self.clear()
		for item in self.__storage:
			for subitem in self.__storage[item].items():
				if subitem[0] == self.__trait.name:
					self.setSpecialties(subitem[1]["specialties"])
					return



	def modifyTrait(self, name, state):
		if state == Qt.Checked:
			if name not in self.__trait.specialties:
				self.__trait.appendSpecialty(name)
		elif name in self.__trait.specialties:
			self.__trait.removeSpecialty(name)

