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

#from PySide.QtCore import Signal
from PySide.QtGui import QWidget, QVBoxLayout, QStandardItemModel, QStandardItem, QTreeView

#from src.Config import Config
#from src import Error
#from src.Widgets.CategoryWidget import CategoryWidget
#from src.Widgets.Components.CheckTrait import CheckTrait
from src.Debug import Debug




class SubPowerWidget(QWidget):
	"""
	@brief Zeigt alle Unterkräfte in einer Baumstruktur an.
	"""


	def __init__(self, template, character, parent=None):
		QWidget.__init__(self, parent)

		self.__storage = template
		self.__character = character

		self.__model = QStandardItemModel()
		# Das ungenutzte Model dient dazu, alle Unterkräfte aufzunehmen, die ich nicht darstellen möchte. Ist einfacher, als diese im View zu verstecken.
		self.__modelUnused = QStandardItemModel()

		self._layout = QVBoxLayout()
		self.setLayout( self._layout )

		self.__view = QTreeView()
		self.__view.setHeaderHidden(True)
		self.__view.setModel( self.__model)

		self._layout.addWidget(self.__view)

		self._typ = "Subpower"
		categories = self.__storage.categories(self._typ)

		self.__items = {}

		self.__rootItem = QStandardItem()
		self.__rootItem = self.__model.invisibleRootItem()

		self.__rootItemUnused = QStandardItem()
		self.__rootItemUnused = self.__modelUnused.invisibleRootItem()

		for item in categories:
			categoryItem = QStandardItem(item)
			self.__rootItem.appendRow(categoryItem)

			## Ich benötige diese Items auch im ungenutzten Model.
			categoryItemUnused = QStandardItem(item)
			self.__rootItemUnused.appendRow(categoryItemUnused)
			
			traitList = self.__character.traits[self._typ][item].items()
			traitList.sort()
			for trait in traitList:
				traitItem = QStandardItem(trait[1].name)
				traitItem.setCheckable(True)
				## Unhashable Type
				#self.__items[traitItem] = trait[1]
				categoryItem.appendRow(traitItem)

				## Funktioniert aus irgendeinem Grund nicht.
				#trait[1].availableChanged.connect(traitItem.setEnabled)

		self.__character.speciesChanged.connect(self.hideOrShowToolPage)
		self.__character.breedChanged.connect(self.hideOrShowToolPage)
		self.__character.factionChanged.connect(self.hideOrShowToolPage)


	#def test(self, sw):
		#Debug.debug(sw)


	def hideOrShowToolPage(self, res):
		"""
		Alle Eigenschaften, die nicht zur Verfügung stehen, werden verborgen, indem sie in ein anderes Model verschoben werden.

		\bug Möglicher Fehler in PySide: Der Aufruf von QStandardItem.model() führt beim Beenden des Programms zu einem Segmentation Fault.
		"""

		# Versteckt alle Unterkräfte, die zu gewähltem Charakter nicht passen.
		for item in self.__items.items():
			if (
				(
					item[0].species and
					item[0].species != self.__character.species
				) or (
					item[0].only and
					self.__character.breed not in item[0].only and
					self.__character.faction not in item[0].only
				)
			):
				#self.__view.setRowHidden(item[1].index().row(), item[1].parent().index(), True)
				#Debug.debug(item[1].model())
				## Hier wird beispielsweise besagter Aufruf getätigt, der zu einem segfault führt.
				if item[1].model() == self.__model:
					parent = item[1].parent()
					itemUnused = parent.takeRow(item[1].index().row())
					parentUnused = self.__modelUnused.findItems(parent.text())[0]
					parentUnused.appendRow(itemUnused)
			else:
				#self.__view.setRowHidden(item[1].index().row(), item[1].parent().index(), False)
				if item[1].model() == self.__modelUnused:
					parent = item[1].parent()
					itemUsed = parent.takeRow(item[1].index().row())
					parentUsed = self.__model.findItems(parent.text())[0]
					parentUsed.appendRow(itemUsed)

		## Versteckt alle Elternzeilen, wenn sie keine Kinder enthalten.
		for i in xrange(self.__model.rowCount()):
			categoryItem = self.__model.item(i)
			if categoryItem.hasChildren():
				self.__view.setRowHidden(categoryItem.index().row(), self.__rootItem.index(), False)
			else:
				self.__view.setRowHidden(categoryItem.index().row(), self.__rootItem.index(), True)




