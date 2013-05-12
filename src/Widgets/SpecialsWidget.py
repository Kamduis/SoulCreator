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




#from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget, QHBoxLayout, QLineEdit, QMessageBox

import src.Config as Config
from src.Widgets.Components.TraitDots import TraitDots
from src.Widgets.CompanionWidget import CompanionWidget
#import src.Debug as Debug

from ui.ui_SpecialsWidget import Ui_SpecialsWidget




class SpecialsWidget(QWidget):
	"""
	@brief Dieses Widget beinahltet sämtliche Besundherheiten der verschiedenen Spezies.
	"""


	def __init__(self, template, character, parent=None):
		super(SpecialsWidget, self).__init__(parent)

		self.ui = Ui_SpecialsWidget()
		self.ui.setupUi(self)

		self.__storage = template
		self.__character = character

		self.__character.speciesChanged.connect(self.setPage)

		## Magier
		self.ui.textEdit_nimbus.textChanged.connect(self.changeNimbus)
		self.__character.nimbusChanged.connect(self.ui.textEdit_nimbus.setPlainText)
		self.ui.textEdit_paradoxMarks.textChanged.connect(self.changeParadoxMarks)
		self.__character.paradoxMarksChanged.connect(self.ui.textEdit_paradoxMarks.setPlainText)

		self.companionWidget = CompanionWidget(self.__storage, self.__character)
		self.ui.layout_companion.addWidget(self.companionWidget)

		## Vampir
		## Liste aller Vinculum-Widgets
		self.__vinculumWidgets = []
		for trait in self.__character.vinculi:
			vinculumLayout = QHBoxLayout()
			lineEdit = QLineEdit()
			lineEdit.textChanged.connect(trait.setName)
			traitDots = TraitDots()
			traitDots.setMaximum(Config.VINCULI_LEVEL_MAX)
			traitDots.valueChanged.connect(trait.setValue)
			vinculumLayout.addWidget(lineEdit)
			vinculumLayout.addWidget(traitDots)
			self.ui.layout_vinculi.addLayout(vinculumLayout)

			self.__vinculumWidgets.append([ lineEdit, traitDots ])

			trait.nameChanged.connect(lineEdit.setText)
			trait.valueChanged.connect(traitDots.setValue)
			traitDots.valueChanged.connect(self.checkMaxVinculum)

		## Werewolf
		self.totemWidget = CompanionWidget(self.__storage, self.__character)
		self.ui.layout_totem.addWidget(self.totemWidget)


	def setPage(self, species):
		"""
		Zeit die der gewählten Spezies zugehörige Seite an.
		"""

		if species == "Human":
			self.ui.stackedWidget.setCurrentWidget(self.ui.page_changeling)
		elif species == "Changeling":
			self.ui.stackedWidget.setCurrentWidget(self.ui.page_changeling)
		elif species == "Mage":
			self.ui.stackedWidget.setCurrentWidget(self.ui.page_mage)
		elif species == "Vampire":
			self.ui.stackedWidget.setCurrentWidget(self.ui.page_vampire)
		elif species == "Werewolf":
			self.ui.stackedWidget.setCurrentWidget(self.ui.page_werewolf)


	def changeNimbus( self ):
		"""
		Verändert den Nimbustext im Speicher.
		"""

		cursor = self.ui.textEdit_nimbus.textCursor()
		cursorPosition = cursor.position()

		self.__character.nimbus = self.ui.textEdit_nimbus.toPlainText()

		cursor.setPosition(cursorPosition)
		self.ui.textEdit_nimbus.setTextCursor(cursor)


	def changeParadoxMarks( self ):
		"""
		Verändert den Text der Paradox-Zeichen im Speicher.
		"""

		cursor = self.ui.textEdit_paradoxMarks.textCursor()
		cursorPosition = cursor.position()

		self.__character.paradoxMarks = self.ui.textEdit_paradoxMarks.toPlainText()

		cursor.setPosition(cursorPosition)
		self.ui.textEdit_paradoxMarks.setTextCursor(cursor)


	def checkMaxVinculum( self, value ):
		"""
		Erreicht ein Vinculum Stufe 3 werden alle anderen Vinculi gelöscht.
		"""

		if value > 2:
			## Nur warnen, wenn mehr als 1 vinculum vorhanden ist.
			numberOfVinculi = 0
			doProceed = True
			for vinculum in self.__vinculumWidgets:
				if vinculum[1].value > 0:
					numberOfVinculi += 1
					if numberOfVinculi > 1:
						doProceed = False
						break
			if not doProceed:
				ret = QMessageBox.warning(
					self,
					self.tr( "Maximal Vinculum level!" ),
					self.tr( "Maximzing a single Vinculum will reset all partial vinculums. Do you want to proceed?" ),
					QMessageBox.Yes | QMessageBox.No
				)
			if doProceed or ret == QMessageBox.StandardButton.Yes:
				for vinculum in self.__vinculumWidgets:
					if vinculum[1].value < 3:
						vinculum[0].setText("")
						vinculum[0].setEnabled(False)
						vinculum[1].value = 0
						vinculum[1].setEnabled(False)
			else:
				for vinculum in self.__vinculumWidgets:
					if vinculum[1] == self.sender():
						vinculum[1].value = 2
						break
		elif not any(x[1].value > 2 for x in self.__vinculumWidgets):
			for vinculum in self.__vinculumWidgets:
				vinculum[0].setEnabled(True)
				vinculum[1].setEnabled(True)



