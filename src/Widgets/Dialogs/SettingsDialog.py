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

#from PySide.QtCore import Signal# as Signal
from PySide.QtGui import QDialog

from src.Config import Config
#from src.Error import ErrXmlTooOldVersion
#from src.Debug import Debug

from ui.ui_SettingsDialog import Ui_SettingsDialog




class SettingsDialog(QDialog):
	"""
	@brief Einstellungssdialog, in welchem die Einstellungen für das Programm geändert werden können.

	Die verschiedenen Einstellungen werden erst dann gespeichert, wenn der Dialog akzeptiert wird.
	"""


	#settingsChanged = Signal()


	def __init__(self, parent=None):
		super(SettingsDialog, self).__init__(parent)

		self.ui = Ui_SettingsDialog()
		self.ui.setupUi(self)

		self.ui.checkBox_autoSelectEra.setChecked(Config.autoSelectEra)

		self.ui.buttonBox.accepted.connect(self.saveChanges)
		self.ui.buttonBox.rejected.connect(self.reject)


	def saveChanges(self):
		"""
		Speichert die im Dialog vorgenommen Änderungen.
		"""

		Config.autoSelectEra = self.ui.checkBox_autoSelectEra.isChecked()

		self.accept()
