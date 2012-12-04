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




import os

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget, QColor, QIcon, QListWidgetItem, QRadioButton, QButtonGroup

from src.Config import Config
from src.Widgets.AbstractStoreWidget import AbstractStoreWidget
from src.Debug import Debug

from ui.ui_ItemWidget import Ui_ItemWidget




class ItemWidget(QWidget):
	"""
	@brief Auflistung der Gegenstände.

	\todo Drag&Drop wäre auch nicht schlecht.

	\todo Momentan finde ich die Waffenkategorie über die Hintergrundfarbe heraus. Das ist nicht wirklich gut.
	"""

	def __init__(self, template, character, parent=None):
		super(ItemWidget, self).__init__(parent)

		self.ui = Ui_ItemWidget()
		self.ui.setupUi(self)

		self.__character = character
		self.__storage = template

		## Weapons
		weaponStore = AbstractStoreWidget(template, character)
		weaponStore.setEnhancedItemTraitsVisible(True)
		weaponStore.setMagicalItemTraitsVisible(False)
		weaponStore.setAddCustomVisible(False)
		self.ui.layout_weapons.addWidget(weaponStore)

		for category in self.__storage.weapons:
			for weapon in self.__storage.weapons[category]:
				weaponStore.addItemToStore(weapon, category, QIcon(Config.weaponIcons[category]))

		weaponStore.itemBought.connect(self.__character.addWeapon)
		weaponStore.itemSold.connect(self.__character.deleteWeapon)
		self.__character.weaponAdded.connect(weaponStore.moveItemToInventory)
		self.__character.weaponRemoved.connect(weaponStore.moveItemToStore)

		## Equipment
		equipmentStore = AbstractStoreWidget(template, character)
		equipmentStore.setEnhancedItemTraitsVisible(False)
		equipmentStore.setMagicalItemTraitsVisible(False)
		equipmentStore.setAddCustomVisible(True)
		self.ui.layout_equipment.addWidget(equipmentStore)

		for equipment in self.__storage.equipment:
			equipmentStore.addItemToStore(equipment)

		equipmentStore.itemBought.connect(self.__character.addEquipment)
		equipmentStore.itemSold.connect(self.__character.deleteEquipment)
		self.__character.equipmentAdded.connect(equipmentStore.moveItemToInventory)
		self.__character.equipmentRemoved.connect(equipmentStore.moveItemToStore)

		## Automobiles
		automobileStore = AbstractStoreWidget(template, character)
		automobileStore.setEnhancedItemTraitsVisible(False)
		automobileStore.setMagicalItemTraitsVisible(False)
		automobileStore.setAddCustomVisible(False)
		self.ui.layout_automobiles.addWidget(automobileStore)

		for category in self.__storage.automobiles:
			for automobile in self.__storage.automobiles[category]:
				automobileStore.addItemToStore(automobile, category, QIcon(Config.automobilesIcons[category]))

		automobileStore.itemBought.connect(self.__character.addAutomobile)
		automobileStore.itemSold.connect(self.__character.deleteAutomobile)
		self.__character.automobileAdded.connect(automobileStore.moveItemToInventory)
		self.__character.automobileRemoved.connect(automobileStore.moveItemToStore)

		## ExtraordinaryItems
		extraordinaryItemStore = AbstractStoreWidget(template, character)
		extraordinaryItemStore.setEnhancedItemTraitsVisible(False)
		extraordinaryItemStore.setMagicalItemTraitsVisible(True)
		extraordinaryItemStore.setAddCustomVisible(False)
		self.ui.layout_extraordinaryItems.addWidget(extraordinaryItemStore)

		for category in self.__storage.extraordinaryItems:
			for extraordinaryItem in self.__storage.extraordinaryItems[category]:
				extraordinaryItemStore.addItemToStore(extraordinaryItem, category, QIcon(Config.extraordinaryItemsIcons[category]))

		extraordinaryItemStore.itemBought.connect(self.__character.addExtraordinaryItem)
		extraordinaryItemStore.itemSold.connect(self.__character.deleteExtraordinaryItem)
		self.__character.extraordinaryItemAdded.connect(extraordinaryItemStore.moveItemToInventory)
		self.__character.extraordinaryItemRemoved.connect(extraordinaryItemStore.moveItemToStore)


		## \todo Sollte nicht vom Betriebssystem, sondern vom verwendeten Style abhängen.
		self.ui.tabWidget_items.setObjectName("transparentWidget")
		if os.name == "nt":
			self.ui.tabWidget_items.setStyleSheet( "QWidget#transparentWidget { background: transparent; }" )

		self.ui.tabWidget_items.setCurrentIndex(0)

		## Resources
		self.ui.traitDots_armorResources.valueChanged.connect(self.__character.traits["Merit"]["Social"]["Resources"].setValue)
		#self.ui.traitDots_equipmentResources.valueChanged.connect(self.__character.traits["Merit"]["Social"]["Resources"].setValue)
		self.__character.traits["Merit"]["Social"]["Resources"].valueChanged.connect(self.ui.traitDots_armorResources.setValue)
		#self.__character.traits["Merit"]["Social"]["Resources"].valueChanged.connect(self.ui.traitDots_equipmentResources.setValue)
		self.ui.traitDots_armorEnhancedItem.valueChanged.connect(self.__character.traits["Merit"]["Item"]["Enhanced Item"].setValue)
		#self.ui.traitDots_equipmentEnhancedItem.valueChanged.connect(self.__character.traits["Merit"]["Item"]["Enhanced Item"].setValue)
		self.__character.traits["Merit"]["Item"]["Enhanced Item"].valueChanged.connect(self.ui.traitDots_armorEnhancedItem.setValue)
		#self.__character.traits["Merit"]["Item"]["Enhanced Item"].valueChanged.connect(self.ui.traitDots_equipmentEnhancedItem.setValue)

		## Armor

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

		self.__buttonGroup_armor.buttonClicked.connect(self.takeArmor)
		self.ui.checkBox_armorDedicated.toggled.connect(self.takeArmor)

		self.__character.armorChanged.connect(self.selectArmor)
		self.__character.speciesChanged.connect(self.hideShowDedicated)

		### Equipment

		#self.ui.pushButton_equipmentAdd.setIcon(QIcon(":/icons/images/actions/1leftarrow.png"))
		#self.ui.pushButton_equipmentRemove.setIcon(QIcon(":/icons/images/actions/1rightarrow.png"))
		
		#for item in self.__storage.equipment:
			#listItem = QListWidgetItem()
			#listItem.setText(item)
			##listItem.setIcon(QIcon(Config.weaponIcons[category]))
			##listItem.setData(Qt.BackgroundRole, QColor(Config.weaponsColor[category]))
			#self.ui.listWidget_equipmentStore.addItem(listItem)

		#self.ui.pushButton_equipmentAdd.clicked.connect(self.addEquipment)
		#self.ui.listWidget_equipmentStore.itemDoubleClicked.connect(self.addEquipment)
		#self.ui.pushButton_equipmentRemove.clicked.connect(self.removeEquipment)
		#self.ui.listWidget_equipmentInventory.itemDoubleClicked.connect(self.removeEquipment)
		#self.ui.pushButton_equipmentAddCustom.clicked.connect(self.addCustomEquipment)
		#self.__character.equipmentChanged.connect(self.refillEquipmentInventory)
		#self.__character.equipmentChanged.connect(self.refillEquipmentStore)
		#self.__character.equipmentChanged.connect(self.checkButtonEnabledEquipment)

		## Magical Tool
		self.__character.speciesChanged.connect(self.hideShowMagicalTool)
		self.ui.lineEdit_magicalTool.textEdited.connect(self.__character.setMagicalTool)
		self.__character.magicalToolChanged.connect(self.ui.lineEdit_magicalTool.setText)


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


	#def addCustomEquipment(self):
		#"""
		#Fügt dem Inventar des Charakters einen Gegenstand hinzu.

		#\todo Nach dem Drücken des Hinzufügen.Knopfes, sollte der Fokus wieder auf das LineEdit gehen.
		#"""

		#newItem = self.ui.lineEdit_equipmentCustom.text()
		#if newItem:
			#self.__character.addEquipment(newItem)
			### Textzeile löschen
			#self.ui.lineEdit_equipmentCustom.setText("")


	#def addEquipment(self):
		#"""
		#Der Charakter erhält den in \ref listWidget_equipmentStore markierte Ausrüstungsgegenstand.
		#"""

		#item = self.ui.listWidget_equipmentStore.takeItem(self.ui.listWidget_equipmentStore.row(self.ui.listWidget_equipmentStore.currentItem()))
		#if item:
			#self.__character.addEquipment(item.text())


	#def removeEquipment(self):
		#"""
		#Entfernt einen Gegenstand aus dem Inventar des Charakters. Wenn er aus der Liste der vorgeschlagenen Ausrüsrtung stammt, wird er dort wieder hinzugefügt.
		#"""

		#if self.ui.listWidget_equipmentInventory.currentItem():
			#item = self.ui.listWidget_equipmentInventory.takeItem(self.ui.listWidget_equipmentInventory.row(self.ui.listWidget_equipmentInventory.currentItem()))
			#self.__character.delEquipment(item.text())


	#def refillEquipmentInventory(self, itemList):
		#"""
		#Schreibt alle Gegenstände aus dem Charakterspeicher in die Liste
		#"""

		#self.ui.listWidget_equipmentInventory.clear()
		#for item in itemList:
			#listItem = QListWidgetItem()
			#listItem.setText(item)
			##listItem.setIcon(QIcon(Config.weaponIcons[category]))
			##listItem.setFlags(listItem.flags() | Qt.ItemIsEditable)
			#self.ui.listWidget_equipmentInventory.addItem(listItem)


	#def refillEquipmentStore(self, itemList):
		#"""
		#Löschte alle Gegenstände, die im Inventar des Charakters sind aus dem Laden.
		#"""

		#self.ui.listWidget_equipmentStore.clear()
		#for item in self.__storage.equipment:
			#if item not in itemList:
				#listItem = QListWidgetItem()
				#listItem.setText(item)
				#listItem = self.ui.listWidget_equipmentStore.addItem(listItem)


	#def checkButtonEnabledEquipment(self):
		#"""
		#Aktiviert/Deaktiviert die Knöpfe für das Übertragen von Ausrüstung.
		#"""

		#if self.ui.listWidget_equipmentStore.count() < 1:
			#self.ui.pushButton_equipmentAdd.setEnabled(False)
		#else:
			#self.ui.pushButton_equipmentAdd.setEnabled(True)


	def hideShowMagicalTool(self, species):
		"""
		Nur bei Magiern wird ein Magische Werkzeug angeboten.
		"""

		if species == "Mage":
			self.ui.widget_magicalTool.setVisible(True)
		else:
			self.ui.widget_magicalTool.setVisible(False)





