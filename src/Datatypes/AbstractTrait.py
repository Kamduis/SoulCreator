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




from PyQt4.QtCore import pyqtSignal as Signal
from PyQt4.QtCore import QObject

#from src.Config import Config
#from ReadXml import ReadXml
#from src.Debug import Debug
#from src.Error import ErrTraitType




class AbstractTrait(QObject):
	"""
	@brief Grundgerüst eines Datentyps für eine Charaktereigenschaft.
	"""


	nameChanged = Signal(str)
	valueChanged = Signal(int)
	totalvalueChanged = Signal(int)
	traitChanged = Signal(object)


	def __init__(self, name="", value=0, parent=None):
		"""
		Die Referenz auf character benötige ich nur, damit ich bei Eigenschaften mit Voraussetzungen diese auch überprüfen kann.

		\ref checkPrerequisites
		"""
		
		super(AbstractTrait, self).__init__(parent)

		self.__identifier = name
		self.__name = name
		self.__value = value

		self.valueChanged.connect(self.totalvalueChanged)


	def __lt__(self, other):
		return self.name < other.name


	@property
	def identifier(self):
		return self.__identifier

	@identifier.setter
	def identifier(self, identifier):
		self.__identifier = identifier


	def __getName(self):
		return self.__name

	def setName(self, name):
		if self.__name != name:
			self.__name = name
			self.nameChanged.emit(name)
			self.traitChanged.emit(self)

	name = property(__getName, setName)


	def _getValue(self):
		return self.__value

	def setValue(self, value):
		"""
		Verändert den Wert der Eigenschaft.
		"""
		
		if self.__value != value:
			self.__value = value
			#Debug.debug(u"Ändere Eigenschaft {} zu {}".format(self.name, self.__value))
			self.valueChanged.emit(self.__value)
			self.traitChanged.emit(self)

	value = property(_getValue, setValue)

	totalvalue = property(_getValue)

