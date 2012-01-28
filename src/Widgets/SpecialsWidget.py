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

import os

from PySide.QtCore import Qt
from PySide.QtGui import QWidget

from src.Config import Config
#from src.Tools import PathTools
#from src.Calc.Calc import Calc
#from src.Datatypes.Identity import Identity
#from src.Widgets.Dialogs.NameDialog import NameDialog
from src.Debug import Debug

from ui.ui_SpecialsWidget import Ui_SpecialsWidget




class SpecialsWidget(QWidget):
	"""
	@brief Dieses Widget beinahltet sämtliche Besundherheiten der verschiedenen Spezies.
	"""


	def __init__(self, template, character, parent=None):
		QWidget.__init__(self, parent)

		self.ui = Ui_SpecialsWidget()
		self.ui.setupUi(self)

		self.__storage = template
		self.__character = character

		self.__character.speciesChanged.connect(self.setPage)

		## Magier
		self.ui.textEdit_nimbus.focusLost.connect(self.changeNimbus)
		self.__character.nimbusChanged.connect(self.ui.textEdit_nimbus.setPlainText)


	def setPage(self, species):
		"""
		Zeit die der gewählten Spezies zugehörige Seite an.
		"""

		if species == "Changeling":
			self.ui.stackedWidget.setCurrentWidget(self.ui.page_changeling)
		elif species == "Mage":
			self.ui.stackedWidget.setCurrentWidget(self.ui.page_mage)


	def changeNimbus( self ):
		"""
		Verändert den Nimbustext im Speicher.
		"""

		self.__character.nimbus = self.ui.textEdit_nimbus.toPlainText()

