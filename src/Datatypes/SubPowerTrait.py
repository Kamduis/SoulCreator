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




#from PyQt4.QtCore import pyqtSignal as Signal
from PyQt4.QtCore import Qt

#import src.Config as Config
from src.Datatypes.BasicTrait import BasicTrait
from src.Debug import Debug
#from src.Error import ErrTraitType




class SubPowerTrait(BasicTrait):
	"""
	@brief Speichert alle Eigenschaften einer einzigen Charaktereigenschaft.

	Simple Eigenschaften wie Attribute haben nur Name und Wert. Bei Fertigkeiten kommen bereits die Spezialisierungen hinzu, bei  Vorzügen noch die Einschränkungen etc.
	"""


	#specialtiesChanged = Signal(object)


	def __init__(self, character, name="", value=0, level=0, parent=None):
		super(SubPowerTrait, self).__init__(character, name, value, parent)

		self.__level = level
		self.__powers = {}


	def _getValue(self):
		return super(SubPowerTrait, self)._getValue()

	def setValue(self, value):
		"""
		Verändert den Wert der Eigenschaft.
		"""

		checkValue = value
		if type(value) != int:
			checkValue = 0
			if value == Qt.Checked:
				checkValue = 2
			elif value == Qt.PartiallyChecked:
				checkValue = 1

		#Debug.debug(checkValue)

		super(SubPowerTrait, self).setValue(checkValue)

	value = property(_getValue, setValue)


	@property
	def level(self):
		return self.__level

	@level.setter
	def level(self, level):
		if self.__level != level:
			self.__level = level
			self.traitChanged.emit(self)


	@property
	def powers(self):
		return self.__powers

	@powers.setter
	def powers(self, powers):
		self.__powers = powers