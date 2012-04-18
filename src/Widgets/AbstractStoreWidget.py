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

from PySide.QtCore import Signal# as Signal
from PySide.QtCore import Qt
from PySide.QtGui import QWidget, QIcon, QTableWidgetItem, QStandardItemModel, QStandardItem

#from src.Config import Config
#from src import Error
#from src.Calc.CalcAdvantages import CalcAdvantages
#from src.Widgets.Components.TraitDots import TraitDots
from src.Debug import Debug

from ui.ui_AbstractStoreWidget import Ui_AbstractStoreWidget




class AbstractStoreWidget(QWidget):
	"""
	@brief Ein einfaches Widget, um das Inventar des Charakters zu füllen.
	"""


	itemBought = Signal(str, str)
	itemSold = Signal(str, str)


	def __init__(self, template, character, parent=None):
		super(AbstractStoreWidget, self).__init__(parent)

		self.ui = Ui_AbstractStoreWidget()
		self.ui.setupUi(self)

		self.__character = character
		self.__storage = template

		self.__modelInventory = QStandardItemModel()
		self.ui.view_inventory.setModel(self.__modelInventory)

		self.__modelStore = QStandardItemModel()
		self.ui.view_store.setModel(self.__modelStore)

		## Resources
		self.ui.traitDots_resources.valueChanged.connect(self.__character.traits["Merit"]["Social"]["Resources"].setValue)
		self.__character.traits["Merit"]["Social"]["Resources"].valueChanged.connect(self.ui.traitDots_resources.setValue)
		self.ui.traitDots_enhancedItem.valueChanged.connect(self.__character.traits["Merit"]["Item"]["Enhanced Item"].setValue)
		self.__character.traits["Merit"]["Item"]["Enhanced Item"].valueChanged.connect(self.ui.traitDots_enhancedItem.setValue)

		## Items
		self.ui.traitDots_token.maximum = 10
		self.ui.traitDots_imbuedItem.maximum = 10
		self.ui.traitDots_artifact.maximum = 10
		self.ui.traitDots_cursedItem.valueChanged.connect(self.__character.traits["Merit"]["Item"]["Cursed Item"].setValue)
		self.ui.traitDots_fetish.valueChanged.connect(self.__character.traits["Merit"]["Item"]["Fetish"].setValue)
		self.ui.traitDots_token.valueChanged.connect(self.__character.traits["Merit"]["Item"]["Token"].setValue)
		self.ui.traitDots_imbuedItem.valueChanged.connect(self.__character.traits["Merit"]["Item"]["Imbued Item"].setValue)
		self.ui.traitDots_artifact.valueChanged.connect(self.__character.traits["Merit"]["Item"]["Artifact"].setValue)
		self.__character.traits["Merit"]["Item"]["Cursed Item"].valueChanged.connect(self.ui.traitDots_cursedItem.setValue)
		self.__character.traits["Merit"]["Item"]["Fetish"].valueChanged.connect(self.ui.traitDots_fetish.setValue)
		self.__character.traits["Merit"]["Item"]["Token"].valueChanged.connect(self.ui.traitDots_token.setValue)
		self.__character.traits["Merit"]["Item"]["Imbued Item"].valueChanged.connect(self.ui.traitDots_imbuedItem.setValue)
		self.__character.traits["Merit"]["Item"]["Artifact"].valueChanged.connect(self.ui.traitDots_artifact.setValue)

		self.ui.pushButton_add.setIcon(QIcon(":/icons/images/actions/1leftarrow.png"))
		self.ui.pushButton_remove.setIcon(QIcon(":/icons/images/actions/1rightarrow.png"))

		self.__modelInventory.rowsInserted.connect(self.checkButtonState)
		self.__modelInventory.rowsRemoved.connect(self.checkButtonState)
		self.__modelStore.rowsInserted.connect(self.checkButtonState)
		self.__modelStore.rowsRemoved.connect(self.checkButtonState)

		self.ui.pushButton_add.clicked.connect(self.buyItem)
		self.ui.view_store.doubleClicked.connect(self.buyItem)
		self.ui.pushButton_remove.clicked.connect(self.sellItem)
		self.ui.view_inventory.doubleClicked.connect(self.sellItem)

		self.ui.lineEdit_custom.textChanged.connect(self.changeCustomButtonState)
		self.ui.pushButton_addCustom.clicked.connect(self.buyCustomItem)


	def setEnhancedItemTraitsVisible(self, sw=True):
		self.ui.label_enhancedItem.setVisible(sw)
		self.ui.traitDots_enhancedItem.setVisible(sw)


	def setMagicalItemTraitsVisible(self, sw=True):
		self.ui.label_cursedItem.setVisible(sw)
		self.ui.traitDots_cursedItem.setVisible(sw)
		self.ui.label_fetish.setVisible(sw)
		self.ui.traitDots_fetish.setVisible(sw)
		self.ui.label_token.setVisible(sw)
		self.ui.traitDots_token.setVisible(sw)
		self.ui.label_artifact.setVisible(sw)
		self.ui.traitDots_artifact.setVisible(sw)
		self.ui.label_imbuedItem.setVisible(sw)
		self.ui.traitDots_imbuedItem.setVisible(sw)


	def setAddCustomVisible(self, sw=True):
		self.ui.widget_custom.setVisible(sw)


	def addItemToStore(self, name, category=None, icon=None):
		newItem = QStandardItem(name)
		if icon:
			newItem.setIcon(icon)
		if category:
			newItem.setData(category)
		self.__modelStore.appendRow(newItem)


	def buyItem(self):
		"""
		Der besagte Gegenstand wird vom Laden in das Inventar übernommen.
		"""

		listOfItems = self.__modelStore.takeRow(self.ui.view_store.currentIndex().row())
		self.__modelInventory.appendRow(listOfItems)

		self.itemBought.emit(listOfItems[0].text(), listOfItems[0].data())


	def __customItem(self, name):
		"""
		Erzeugt einen vom Benutzer benannten Gegenstand.
		"""

		if name:
			existingItemInventory = self.__modelInventory.findItems(name)
			if not existingItemInventory:
				existingItem = self.__modelStore.findItems(name)
				if existingItem:
					listOfItems = self.__modelStore.takeRow(existingItem[0].index().row())
					self.__modelInventory.appendRow(listOfItems)
					self.itemBought.emit(listOfItems[0].text(), listOfItems[0].data())
				else:
					newItem = QStandardItem(name)
					self.__modelInventory.appendRow(newItem)
					self.itemBought.emit(newItem.text(), newItem.data())


	def buyCustomItem(self):
		"""
		Fügt dem Inventar des Charakters einen Gegenstand hinzu.

		\todo Nach dem Drücken des Hinzufügen.Knopfes, sollte der Fokus wieder auf das LineEdit gehen.
		"""

		newName = self.ui.lineEdit_custom.text()
		if newName:
			self.__customItem(newName)
			## Textzeile löschen
			self.ui.lineEdit_custom.setText("")



	def sellItem(self):
		"""
		Der besagte Gegenstand wird vom Inventar zurück in den Laden befördert.
		"""

		listOfItems = self.__modelInventory.takeRow(self.ui.view_inventory.currentIndex().row())
		self.__modelStore.appendRow(listOfItems)

		#for item in listOfItems:
			#Debug.debug(item.data())

		self.itemSold.emit(listOfItems[0].text(), listOfItems[0].data())


	def moveItemToInventory(self, name, category=None):
		"""
		Der besagte Gegenstand wird aus dem Laden ins Inventar bewegt. Gibt es keinen Gegenstand dieses Namens im Laden, wird er direkt im Inventar erzeugt.
		"""

		foundItems = self.__modelStore.findItems(name)
		if foundItems:
			for item in foundItems:
				if item.data() == category:
					listOfItems = self.__modelStore.takeRow(item.index().row())
					self.__modelInventory.appendRow(listOfItems)
		else:
			self.__customItem(name)


	def moveItemToStore(self, name, category=None):
		"""
		Der besagte Gegenstand wird aus dem Inventar in den Laden bewegt.
		"""

		foundItems = self.__modelInventory.findItems(name)
		for item in foundItems:
			if item.data() == category:
				listOfItems = self.__modelInventory.takeRow(item.index().row())
				self.__modelStore.appendRow(listOfItems)


	def checkButtonState(self):
		"""
		Aktiviert/Deaktiviert die Knöpfe für das Übertragen von Gegenständen.
		"""

		if self.__modelInventory.rowCount() > 0:
			self.ui.pushButton_remove.setEnabled(True)
		else:
			self.ui.pushButton_remove.setEnabled(False)

		if self.__modelStore.rowCount() > 0:
			self.ui.pushButton_add.setEnabled(True)
		else:
			self.ui.pushButton_add.setEnabled(False)


	def changeCustomButtonState(self):
		"""
		Aktiviert den Knopf zum Hinzufügen eines zusätzlichen Gegenstandes nur, wenn es etwas zum Hinzufügen gibt. Die zeile also nicht leer und der Gegnstand noch nicht vorhanden ist.
		"""

		self.ui.pushButton_addCustom.setEnabled(False)
		if self.ui.lineEdit_custom.text() and not self.__modelInventory.findItems(self.ui.lineEdit_custom.text()):
			self.ui.pushButton_addCustom.setEnabled(True)



