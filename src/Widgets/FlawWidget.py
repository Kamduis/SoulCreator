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

#from PySide.QtCore import Qt, Signal
from PySide.QtGui import QWidget, QVBoxLayout, QToolBox

from src.Config import Config
from src.Tools import ListTools
from src.Widgets.Components.CheckTrait import CheckTrait
from src.Debug import Debug




class FlawWidget(QWidget):
	"""
	@brief Das Widget, in welchem sämtliche Nachteile angeordnet sind.
	"""

	def __init__(self, template, character, parent=None):
		QWidget.__init__(self, parent)

		self.__storage = template
		self.__character = character

		self.__layout = QVBoxLayout()
		self.setLayout( self.__layout )

		self.__toolBox = QToolBox()
		## Die Auflistung der Merits soll auch unter Windows einen transparenten Hintergrund haben.
		self.__toolBox.setObjectName("transparentWidget")
		## \todo Sollte nicht vom Betriebssystem, sondern vom verwendeten Style abhängen.
		if os.name == "nt":
			self.__toolBox.setStyleSheet( "QScrollArea{ background: transparent; } QWidget#transparentWidget { background: transparent; }" )
		self.__layout.addWidget(self.__toolBox)

		self.__typ = "Flaw"
		categories = []
		categories.extend(Config.flawCategories)
		categories.extend(self.__storage.categories(self.__typ))
		# Duplikate werden entfernt. Dadurch wird die in der Config-Klasse vorgegebene Reihenfolge eingehalten und zusätzliche, dort nicht erwähnte Kategorien werden hinterher angehängt.
		categories = ListTools.uniqifyOrdered(categories)

		# Diese Liste speichert den Index der ToolBox-Seite bei den unterschiedlichen Kategorien
		self.__categoryIndex = {}

		# Flaws werden in einer Spalte heruntergeschrieben, aber mit vertikalem Platz dazwischen.
		for item in categories:
			# Für jede Kategorie wird ein eigener Abschnitt erzeugt.
			widgetFlawCategory = QWidget()
			## Dank des Namens übernimmt dieses Widget den Stil des Eltern-Widgets.
			widgetFlawCategory.setObjectName("transparentWidget")

			layoutFlawCategory = QVBoxLayout()

			widgetFlawCategory.setLayout( layoutFlawCategory )

			self.__toolBox.addItem( widgetFlawCategory, item )
			self.__categoryIndex[item] = self.__toolBox.count() - 1
			#Debug.debug(self.__categoryIndex)

			__list = self.__character.traits[self.__typ][item].items()
			__list.sort()
			for flaw in __list:
				# Anlegen des Widgets, das diese Eigenschaft repräsentiert.
				traitWidget = CheckTrait( flaw[1], self )
				if not flaw[1].custom:
					traitWidget.setDescriptionHidden(True)

				layoutFlawCategory.addWidget( traitWidget )

				flaw[1].valueChanged.connect(self.countItems)
				self.__character.speciesChanged.connect(traitWidget.hideOrShowTrait)


			# Stretch einfügen, damit die Eigenschaften besser angeordnet sind.
			layoutFlawCategory.addStretch()

		self.setMinimumWidth(Config.traitLineWidthMin)



	def countItems(self):
		"""
		Zält die Nachteile in einer Kategorie, deren Wert größer 0 ist. Dieser Wert wird dann in die Überschrift der einzelnen ToolBox-Seiten angezeigt, um dem Benutzer die Übersicht zu bewahren.

		Es wird nur dann etwas angezeigt, wenn der Weert größer 0 ist.
		"""

		for item in self.__character.traits[self.__typ]:
			numberInCategory = 0
			for subitem in self.__character.traits[self.__typ][item].values():
				if subitem.value > 0:
					numberInCategory += 1

			# ToolBox-Seite des entsprechenden Kategorie mit der Anzahl gewählter Merits beschriften.
			if numberInCategory > 0:
				self.__toolBox.setItemText( self.__categoryIndex[item], "{} ({})".format(item, numberInCategory) )
			else:
				self.__toolBox.setItemText( self.__categoryIndex[item], item )

