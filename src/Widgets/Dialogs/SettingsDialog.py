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
from PyQt4.QtGui import QDialog

import src.Config as Config
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

		self.ui.checkBox_autoSelectEra.setChecked(Config.era_auto_select)
		self.ui.checkBox_compressSaves.setChecked(Config.compress_saves)

		self.ui.buttonBox.accepted.connect(self.saveChanges)
		self.ui.buttonBox.rejected.connect(self.reject)


	def saveChanges(self):
		"""
		Speichert die im Dialog vorgenommen Änderungen.
		"""

		Config.era_auto_select = self.ui.checkBox_autoSelectEra.isChecked()
		Config.compress_saves = self.ui.checkBox_compressSaves.isChecked()

		self.accept()
