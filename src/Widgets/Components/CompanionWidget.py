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

from PySide.QtCore import Qt
from PySide.QtGui import QGroupBox, QHBoxLayout, QLineEdit

from src.Config import Config
#from src import Error
from src.Widgets.Components.TraitDots import TraitDots
from src.Debug import Debug

from ui.ui_CompanionWidget import Ui_CompanionWidget




class CompanionWidget(QGroupBox):
	"""
	@brief Ein Widget mit allen nötigen Feldern für einen Companion.
	"""


	#powerChanged = Signal(int)
	#finesseChanged = Signal(int)
	#resistanceChanged = Signal(int)


	def __init__(self, character, parent=None):
		QGroupBox.__init__(self, parent)

		self.ui = Ui_CompanionWidget()
		self.ui.setupUi(self)

		self.__character = character

		self.ui.lineEdit_name.textChanged.connect(self.__character.setCompanionName)
		self.ui.traitDots_power.valueChanged.connect(self.__character.setCompanionPower)
		self.ui.traitDots_finesse.valueChanged.connect(self.__character.setCompanionFinesse)
		self.ui.traitDots_resistance.valueChanged.connect(self.__character.setCompanionResistance)
		self.ui.spinBox_size.valueChanged[int].connect(self.__character.setCompanionSize)
		self.ui.spinBox_speedFactor.valueChanged[int].connect(self.__character.setCompanionSpeedFactor)
		self.ui.listWidget_numina.itemStateChanged.connect(self.modifyNumen)

		self.__character.companionNameChanged.connect(self.ui.lineEdit_name.setText)
		self.__character.companionPowerChanged.connect(self.ui.traitDots_power.setValue)
		self.__character.companionFinesseChanged.connect(self.ui.traitDots_finesse.setValue)
		self.__character.companionResistanceChanged.connect(self.ui.traitDots_resistance.setValue)
		self.__character.companionSizeChanged.connect(self.ui.spinBox_size.setValue)
		self.__character.companionSpeedFactorChanged.connect(self.ui.spinBox_speedFactor.setValue)
		self.__character.companionNuminaChanged.connect(self.updateNumina)

		self.ui.traitDots_power.minimum = Config.traitSpiritMin
		self.ui.traitDots_finesse.minimum = Config.traitSpiritMin
		self.ui.traitDots_resistance.minimum = Config.traitSpiritMin
		self.ui.traitDots_power.maximum = Config.traitSpiritMax
		self.ui.traitDots_finesse.maximum = Config.traitSpiritMax
		self.ui.traitDots_resistance.maximum = Config.traitSpiritMax

		## Liste aller Einflüsse
		self.__influenceWidgets = []
		for trait in self.__character.companionInfluences:
			influencesLayout = QHBoxLayout()
			lineEdit = QLineEdit()
			lineEdit.textChanged.connect(trait.setName)
			traitDots = TraitDots()
			traitDots.setMaximum(5)
			traitDots.valueChanged.connect(trait.setValue)
			influencesLayout.addWidget(lineEdit)
			influencesLayout.addWidget(traitDots)
			self.ui.layout_influences.addLayout(influencesLayout)

			self.__influenceWidgets.append([ lineEdit, traitDots ])

			trait.nameChanged.connect(lineEdit.setText)
			trait.valueChanged.connect(traitDots.setValue)


	def modifyNumen(self, name, state):
		"""
		Wenn sich ein Numina in der Liste verändert, wird selbiges im Charakter-Speicher aktualisiert.
		"""

		#Debug.debug("Test")
		if state == Qt.Checked:
			if name not in self.__character.companionNumina:
				self.__character.appendCompanionNumen(name)
		elif name in self.__character.companionNumina:
			self.__character.removeCompanionNumen(name)


	def updateNumina(self, listOfNumina):
		for i in xrange(self.ui.listWidget_numina.count()):
			item = self.ui.listWidget_numina.item(i)
			if item.text() in listOfNumina:
				item.setCheckState(Qt.Checked)
			else:
				item.setCheckState(Qt.Unchecked)
