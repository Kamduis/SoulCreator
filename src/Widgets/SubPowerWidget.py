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
#from src import Error
from src.Tools import ListTools
from src.Widgets.Components.CheckTrait import CheckTrait
from src.Debug import Debug




class SubPowerWidget(QWidget):
	"""
	@briefIn diesem Widget werden die "Zaubersprüche" (Wechselbalg-GoblinContracts, Magier-Rotes, Vampir-Rituale, Werwolf-Gaben etc.) untergebracht. Diese können abgehakt werden und haben als Voraussetzung in der Regel eine bestimmte Power (\ref PowerWidget), um überhaupt gewählt werden zu können.
	
	\todo Das obligatorisch transparent Setzen des Hintergrundes sollte nicht vom Betriebssystem, sondern vom verwendeten Style abhängen.
	"""


	def __init__(self, template, character, parent=None):
		QWidget.__init__(self, parent)

		self.__storage = template
		self.__character = character

		self.__layout = QVBoxLayout()
		self.setLayout( self.__layout )

		self.__toolBox = QToolBox()
		## Die Auflistung der Eigenschaften soll auch unter Windows einen transparenten Hintergrund haben.
		self.__toolBox.setObjectName("transparentWidget")
		## Sollte nicht vom Betriebssystem, sondern vom verwendeten Style abhängen.
		if os.name == "nt":
			self.__toolBox.setStyleSheet( "QScrollArea{ background: transparent; } QWidget#transparentWidget { background: transparent; }" )
		self.__layout.addWidget(self.__toolBox)

		self.__typ = "Subpower"
		categories = self.__storage.categories(self.__typ)
		#Debug.debug(categories)

		# Diese Liste speichert den Index der ToolBox-Seite bei den unterschiedlichen Kategorien
		self.__categoryIndex = {}

		# Diese Liste speichert den Index der ToolBox-Seite bei den unterschiedlichen Kategorien
		self.toolBoxPageList = {}

		for item in categories:
			# Für jede Kategorie wird ein eigener Abschnitt erzeugt.
			widgetSubpowerCategory = QWidget()
			## Dank des Namens übernimmt dieses Widget den Stil des Eltern-Widgets.
			widgetSubpowerCategory.setObjectName("transparentWidget")

			layoutSubpowerCategory = QVBoxLayout()
			widgetSubpowerCategory.setLayout( layoutSubpowerCategory )

			self.__toolBox.addItem( widgetSubpowerCategory, item )
			self.__categoryIndex[item] = self.__toolBox.count() - 1
			#Debug.debug(self.__categoryIndex)

			## In dieser Liste sammle ich die Widgets, damit sie später bei Bedarf in die ToolBox eingefügt werden können.
			self.toolBoxPageList[item] = [widgetSubpowerCategory]

			__list = self.__character.traits[self.__typ][item].items()
			__list.sort()
			for trait in __list:
				#Debug.debug(merit)
				# Anlegen des Widgets, das diese Eigenschaft repräsentiert.
				traitWidget = CheckTrait( trait[1], self )
				if not trait[1].custom:
					traitWidget.setDescriptionHidden(True)

				self.toolBoxPageList[item].append(trait[1])

				layoutSubpowerCategory.addWidget( traitWidget )

				trait[1].valueChanged.connect(self.countTraits)
				self.__character.speciesChanged.connect(traitWidget.hideOrShowTrait_species)


			# Stretch einfügen, damit die Eigenschaften besser angeordnet sind.
			layoutSubpowerCategory.addStretch()

		self.setMinimumWidth(Config.traitLineWidthMin)

		self.__character.speciesChanged.connect(self.countTraits)
		self.__character.speciesChanged.connect(self.hideOrShowToolPage)


	def hideOrShowToolPage(self, species):
		"""
		Verbirgt eine Seite der ToolBox, wenn alle darin enthaltenen Widgets versteckt sind. Ansonsten wird sie dargestellt.
		"""

		# Damit die Kategorien auch nach dem Entfernen und Hinzufügen von Eigenschaften alphapetisch sortiert bleiben.
		keys = self.toolBoxPageList.keys()
		keys.sort()

		for item in keys:
			available = False
			for subitem in self.toolBoxPageList[item][1:]:
				if (not subitem.species or subitem.species == species):
					available = True
					break
			if available:
				self.__toolBox.addItem(self.toolBoxPageList[item][0], item)
				self.toolBoxPageList[item][0].setVisible(True)
			else:
				indexOfWidget = self.__toolBox.indexOf(self.toolBoxPageList[item][0])
				if indexOfWidget != -1:
					self.__toolBox.removeItem(indexOfWidget)
				self.toolBoxPageList[item][0].setVisible(False)


	def countTraits(self):
		"""
		Zält die Subpowers in einer Kategorie, deren Wert größer 0 ist. Dieser Wert wird dann in die Überschrift der einzelnen ToolBox-Seiten angezeigt, um dem Benutzer die Übersicht zu bewahren.

		Es wird nur dann etwas angezeigt, wenn der Weert größer 0 ist.

		Versteckte Eigenschaften. also solche, die der Spezies nicht zur Verfügung stehen, können einen Wert > 0 haben, sollten aber nicht mitgezählt werden.
		"""

		for item in self.__character.traits[self.__typ]:
			numberInCategory = 0
			for subitem in self.__character.traits[self.__typ][item].values():
				if subitem.value > 0 and (not subitem.species or subitem.species == self.__character.species):
					numberInCategory += 1

			# ToolBox-Seite des entsprechenden Kategorie mit der Anzahl gewählter Subpowers beschriften.
			if numberInCategory > 0:
				self.__toolBox.setItemText( self.__categoryIndex[item], "{} ({})".format(item, numberInCategory) )
			else:
				self.__toolBox.setItemText( self.__categoryIndex[item], item )

