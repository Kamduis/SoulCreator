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
from PyQt4.QtGui import QWidget

import src.Config as Config
#from src import Error
#from src.Debug import Debug




class TraitWidget(QWidget):
	"""
	@brief Grundlage der Widgets für alle Eigenschaften.
	"""


	maxTraitChanged = Signal(int)
	hideReasonChanged = Signal(str, str, str)


	def __init__(self, template, character, parent=None):
		super(TraitWidget, self).__init__(parent)

		self._character = character
		self._storage = template

		# Wenn sich Spezies oder Powerstat ändert, kann sich der erlaubte Maximalwert ändern.
		self._character.powerstatChanged.connect(self.emitMaxTraitChanged)
		self._character.speciesChanged.connect(self.emitMaxTraitChanged)
		# Ändert sich alterskategorie oder die Ära, Wird ein paasendes Signal gesandt.
		self._character.eraChanged.connect(self.emitHideReasonChanged)
		self._character.ageChanged[str].connect(self.emitHideReasonChanged)
		self._character.speciesChanged.connect(self.emitHideReasonChanged)



	def emitMaxTraitChanged(self):
		"""
		Sendet ein Signal aus, das als Wert das neue Maximum der Eigenschaften enthält.
		"""

		maxTrait = self._storage.maxTrait(self._character.species, self._character.powerstat)
		self.maxTraitChanged.emit(maxTrait)


	def emitHideReasonChanged(self):
		#Debug.debug(Config.getAge(self._character.age), self._character.era)
		#ageStr = Config.AGES[0]
		#if self._character.age < Config.AGE_ADULT:
			#ageStr = Config.AGES[1]
		ageStr = Config.getAge(self._character.age)
		eraStr = self._character.era
		self.hideReasonChanged.emit(self._character.species, ageStr, eraStr)

