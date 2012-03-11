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

#from PySide.QtCore import Qt, Signal
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

		self._layout = QVBoxLayout()
		self.setLayout( self._layout )

		self.__view = QTreeView()
		self.__view.setModel( self.__model)

		self._layout.addWidget(self.__view)

		self._typ = "Subpower"
		categories = self.__storage.categories(self._typ)

		self.__items = []

		parentItem = QStandardItem()
		parentItem = self.__model.invisibleRootItem()

		for item in categories:
			categoryItem = QStandardItem(item)
			parentItem.appendRow(categoryItem)

			traitList = self.__character.traits[self._typ][item].items()
			traitList.sort()
			for trait in traitList:
				traitItem = QStandardItem(trait[1].name)
				traitItem.setCheckable(True)
				self.__items.append([ trait[1], traitItem, ])
				categoryItem.appendRow(traitItem)

		self.__character.speciesChanged.connect(self.hideOrShowToolPage)
		self.__character.breedChanged.connect(self.hideOrShowToolPage)
		self.__character.factionChanged.connect(self.hideOrShowToolPage)


	def hideOrShowToolPage(self, res):
		"""
		Verbirgt eine Seite der ToolBox, wenn alle darin enthaltenen Widgets versteckt sind oder diese Kategorie für die ausgewählte Brut/Fraktion nicht zur Verfügung steht. Ansonsten wird sie dargestellt.
		"""

		# Versteckt alle Unterkräfte, die zu gewähltem Charakter nicht passen.
		for item in self.__items:
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
				self.__view.setRowHidden(item[1].index().row(), item[1].parent().index(), True)
			else:
				self.__view.setRowHidden(item[1].index().row(), item[1].parent().index(), False)

		




