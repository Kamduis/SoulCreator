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
from PySide.QtGui import QWidget, QVBoxLayout, QGridLayout, QLabel, QFrame, QButtonGroup

from src.Config import Config
#from src import Error
#from ReadXml import ReadXml
from src.Widgets.Components.CharaTrait import CharaTrait
from src.Debug import Debug




class TraitWidget(QWidget):
	"""
	@brief Grundlage der Widgets für alle Eigenschaften.
	"""


	maxTraitChanged = Signal(int)


	def __init__(self, template, character, parent=None):
		QWidget.__init__(self, parent)

		self._character = character
		self._storage = template

		# Wenn sich Spezies oder Powerstat ändert, kann sich der erlaubte Maximalwert ändern.
		self._character.powerstatChanged.connect(self.emitMaxTraitChanged)
		self._character.speciesChanged.connect(self.emitMaxTraitChanged)



	def emitMaxTraitChanged(self):
		"""
		Sendet ein Signal aus, das als Wert das neue Maximum der Eigenschaften enthält.
		"""

		maxTrait = self._storage.maxTrait(self._character.species, self._character.powerstat)
		self.maxTraitChanged.emit(maxTrait)

