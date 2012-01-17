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

from PySide.QtCore import Qt
from PySide.QtGui import QWidget, QColor, QIcon, QListWidgetItem, QRadioButton, QButtonGroup

from src.Config import Config
from src.Debug import Debug

from ui.ui_ItemWidget import Ui_ItemWidget




class ItemWidget(QWidget):
	"""
	@brief Auflistung der Gegenstände.

	\todo Drag&Drop wäre auch nicht schlecht.

	\todo Momentan finde ich die Waffenkategorie über die Hintergrundfarbe heraus. Das ist nicht wirklich gut.
	"""

	def __init__(self, template, character, parent=None):
		QWidget.__init__(self, parent)

		self.ui = Ui_ItemWidget()
		self.ui.setupUi(self)

		self.__character = character
		self.__storage = template

		self.ui.pushButton_take.setIcon(QIcon(":/icons/images/actions/1leftarrow.png"))
		self.ui.pushButton_give.setIcon(QIcon(":/icons/images/actions/1rightarrow.png"))

		for category in self.__storage.weapons:
			for weapon in self.__storage.weapons[category]:
				listItem = QListWidgetItem()
				listItem.setText(weapon)
				listItem.setIcon(QIcon(Config.weaponIcons[category]))
				listItem.setData(Qt.BackgroundRole, QColor(Config.weaponsColor[category]))
				self.ui.listWidget_store.addItem(listItem)

		self.__noArmorText = "None"
		self.__buttonArmorDict = {}
		self.__buttonGroup_armor = QButtonGroup(self)
		## Natürlich muß auch die Wahl bestehen, keine Rüstung zu tragen. Dies ist zu Anfang gewählt.
		radioButton = QRadioButton(self.__noArmorText)
		self.ui.layout_armor.addWidget(radioButton)
		self.__buttonGroup_armor.addButton(radioButton)
		radioButton.setChecked(True)
		self.__buttonArmorDict[radioButton.text()] = radioButton
		for armor in self.__storage.armor:
			radioButton = QRadioButton(armor)
			self.ui.layout_armor.addWidget(radioButton)
			self.__buttonGroup_armor.addButton(radioButton)
			self.__buttonArmorDict[radioButton.text()] = radioButton

		self.ui.pushButton_give.setEnabled(False)

		self.ui.pushButton_take.clicked.connect(self.takeWeapon)
		self.ui.listWidget_store.itemDoubleClicked.connect(self.takeWeapon)
		self.ui.pushButton_give.clicked.connect(self.giveWeapon)
		self.ui.listWidget_inventory.itemDoubleClicked.connect(self.giveWeapon)
		self.__buttonGroup_armor.buttonClicked.connect(self.takeArmor)
		self.ui.checkBox_armorDedicated.toggled.connect(self.takeArmor)

		self.__character.weaponAdded.connect(self.moveToInventory)
		self.__character.weaponRemoved.connect(self.moveToStore)
		self.__character.armorChanged.connect(self.selectArmor)
		self.__character.speciesChanged.connect(self.hideShowDedicated)


	def takeWeapon(self):
		"""
		Der Charakter erhält die in der in listWidget_store markierte Waffe.
		"""

		item = self.ui.listWidget_store.takeItem(self.ui.listWidget_store.row(self.ui.listWidget_store.currentItem()))
		if item:
			self.ui.listWidget_inventory.addItem(item)
			## Knöpfe aktivieren/deaktivieren
			self.ui.pushButton_give.setEnabled(True)
			if self.ui.listWidget_store.count() < 1:
				self.ui.pushButton_take.setEnabled(False)

			for category in Config.weaponsColor.items():
				if item.data(Qt.BackgroundRole).name() == QColor(category[1]).name():
					self.saveWeapon(category[0], item.text())
					break


	def giveWeapon(self):
		"""
		Der Charakter verliert die in der in listWidget_inventory markierte Waffe.
		"""

		item = self.ui.listWidget_inventory.takeItem(self.ui.listWidget_inventory.row(self.ui.listWidget_inventory.currentItem()))
		if item:
			self.ui.listWidget_store.addItem(item)
			## Knöpfe aktivieren/deaktivieren
			self.ui.pushButton_take.setEnabled(True)
			if self.ui.listWidget_inventory.count() < 1:
				self.ui.pushButton_give.setEnabled(False)

			for category in Config.weaponsColor.items():
				if item.data(Qt.BackgroundRole).name() == QColor(category[1]).name():
					self.deleteWeapon(category[0], item.text())
					break


	def moveToInventory(self, category, weapon):
		"""
		Bewegt besagte Waffe vom Laden zum Inventar.
		"""

		item = None
		for i in xrange(self.ui.listWidget_store.count()):
			if self.ui.listWidget_store.item(i).text() == weapon and self.ui.listWidget_store.item(i).data(Qt.BackgroundRole).name() == QColor(Config.weaponsColor[category]).name():
				item = self.ui.listWidget_store.takeItem(i)
				self.ui.listWidget_inventory.addItem(item)
				break


	def moveToStore(self, category, weapon):
		"""
		Bewegt besagte Waffe vom Laden zum Inventar.
		"""

		item = None
		for i in xrange(self.ui.listWidget_inventory.count()):
			if self.ui.listWidget_inventory.item(i).text() == weapon and self.ui.listWidget_inventory.item(i).data(Qt.BackgroundRole).name() == QColor(Config.weaponsColor[category]).name():
				item = self.ui.listWidget_inventory.takeItem(i)
				self.ui.listWidget_store.addItem(item)
				break


	def saveWeapon(self, category, weapon):
		"""
		Speichert die Waffe im Charakter-Speicher.
		"""

		self.__character.addWeapon(category, weapon)


	def deleteWeapon(self, category, weapon):
		"""
		Speichert die Waffe im Charakter-Speicher.
		"""

		self.__character.deleteWeapon(category, weapon)


	def takeArmor(self):
		"""
		Speichert die gewählte Rüstung im Charakter-Speicher.
		"""

		armorName = self.__buttonGroup_armor.checkedButton().text()
		if armorName == self.__noArmorText:
			armorName = ""
		dedicated = False
		if self.ui.checkBox_armorDedicated.isChecked():
			dedicated = True
		self.__character.setArmor(armorName, dedicated=dedicated)


	def selectArmor(self, armor, dedicated):
		"""
		Wählt den Knopf mit der Passenden Bezeichnung aus.
		"""

		armorName = armor
		if not armorName:
			armorName = self.__noArmorText

		if armorName in self.__buttonArmorDict:
			self.__buttonArmorDict[armorName].setChecked(True)
			if dedicated:
				self.ui.checkBox_armorDedicated.setChecked(True)
			else:
				self.ui.checkBox_armorDedicated.setChecked(False)


	def hideShowDedicated(self, species):
		"""
		Nur bei Werwölfen macht es Sinn, eine Rüstung zuzueignen. Entsprechendes Widget wird für alle anderen Spezies versteckt.
		"""

		if species == "Werewolf":
			self.ui.checkBox_armorDedicated.setVisible(True)
		else:
			self.ui.checkBox_armorDedicated.setVisible(False)