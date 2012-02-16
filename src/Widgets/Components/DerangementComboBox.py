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

from PySide.QtCore import Qt, Signal
from PySide.QtGui import QComboBox, QColor

from src.Config import Config
#from src import Error
#from src.Debug import Debug




class DerangementComboBox(QComboBox):
	"""
	@brief Eine Combobox für Geistesstörungen.

	Diese ComboBox zeigt milde und schwere Geistesstörungen in unterschiedlichen Farben an und bietet spezielle Signale.
	"""


	derangementChanged = Signal(str, bool, object)


	def __init__(self, parent=None):
		QComboBox.__init__(self, parent)

		self.__severeDerangements = []

		self.currentIndexChanged[str].connect(self.emitDerangementChanged)


	def addItems(self, items, severe=False):
		"""
		Fügt der Box eine Liste von Geistesstörungen einer bestimmten Kategorie hinzu.
		"""

		if severe:
			for item in items:
				self.addItem(item)
				self.__severeDerangements.append(item)
				self.setItemData(self.count()-1, QColor(Config.severeDerangementsColor), Qt.BackgroundRole)
		else:
			QComboBox.addItems(self, items)


	def emitDerangementChanged(self, text):
		"""
		Ändert sich der ausgewählte Text der combobox, wird dieses Signal gesendet, welches als Zusatzfunktion noch mitteilt, ob es sich bei der gewählten Geistesstörung um eine schwere handelt, oder nicht.
		"""

		severe = False
		if text in self.__severeDerangements:
			severe = True

		self.derangementChanged.emit(text, severe, self)



