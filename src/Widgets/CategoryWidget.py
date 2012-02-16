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

#from src.Config import Config
#from src import Error
from src.Datatypes.StandardTrait import StandardTrait
#from src.Datatypes.SubPowerTrait import SubPowerTrait
from src.Widgets.Components.CharaTrait import CharaTrait
from src.Widgets.Components.CheckTrait import CheckTrait
#from src.Debug import Debug




class CategoryWidget(QWidget):
	"""
	@brief Dieses Widget kann in Kategorien aufgeteilte Widgets aufnehmen. Es werden nur jene Kategorien angezeigt, welche auch ein anzuzeigendes Widget enthalten.
	"""


	def __init__(self, template, character, typ, isCheckable=False, parent=None):
		QWidget.__init__(self, parent)

		self.__storage = template
		self.__character = character

		self._layout = QVBoxLayout()
		self.setLayout( self._layout )

		self._toolBox = QToolBox()
		## Die Auflistung der Widgets soll auch unter Windows einen transparenten Hintergrund haben.
		self._toolBox.setObjectName("transparentWidget")
		## \todo Sollte nicht vom Betriebssystem, sondern vom verwendeten Style abhängen.
		if os.name == "nt":
			self._toolBox.setStyleSheet( "QScrollArea{ background: transparent; } QWidget#transparentWidget { background: transparent; }" )

		self._layout.addWidget( self._toolBox )

		self._typ = typ
		categories = self.__storage.categories(self._typ)

		# Diese Liste speichert den Index der ToolBox-Seite bei den unterschiedlichen Kategorien
		# {
		# 	Index: [Widget, Eigenschaft1, Eigenschaft2, ...]
		# }
		self._toolBoxPageList = {}

		for item in categories:
			# Für jede Kategorie wird ein eigener Abschnitt erzeugt.
			widgetCategory = QWidget()
			## Dank des Namens übernimmt dieses Widget den Stil des Eltern-Widgets.
			widgetCategory.setObjectName("transparentWidget")

			layoutCategory = QVBoxLayout()

			widgetCategory.setLayout( layoutCategory )

			## In dieser Liste sammle ich die Widgets, damit sie später bei Bedarf in die ToolBox eingefügt werden können.
			self._toolBoxPageList[item] = [widgetCategory]

			__list = self.__character.traits[self._typ][item].items()
			__list.sort()
			for trait in __list:
				# Anlegen des Widgets, das diese Eigenschaft repräsentiert.
				traitWidget = None
				if isCheckable:
					traitWidget = CheckTrait( trait[1], self )
				else:
					traitWidget = CharaTrait( trait[1], self )
					traitWidget.setSpecialtiesHidden(True)
				if type(trait) != StandardTrait or not trait[1].custom:
					traitWidget.setDescriptionHidden(True)

				self._toolBoxPageList[item].append(trait[1])

				layoutCategory.addWidget( traitWidget )

				self.__character.speciesChanged.connect(traitWidget.hideOrShowTrait)

			# Stretch einfügen, damit die Eigenschaften besser angeordnet sind.
			layoutCategory.addStretch()
		#Debug.debug(self._toolBoxPageList)
		self.__character.speciesChanged.connect(self.hideOrShowToolPage)
		self.__character.breedChanged.connect(self.hideOrShowToolPage)
		self.__character.factionChanged.connect(self.hideOrShowToolPage)


	def hideOrShowToolPage(self, res):
		"""
		Verbirgt eine Seite der ToolBox, wenn alle darin enthaltenen Widgets versteckt sind oder diese Kategorie für die ausgewählte Brut/Fraktion nicht zur Verfügung steht. Ansonsten wird sie dargestellt.
		"""

		# Damit die Kategorien auch nach dem Entfernen und Hinzufügen von Eigenschaften alphapetisch sortiert bleiben.
		keys = self._toolBoxPageList.keys()
		keys.sort()

		for item in keys:
			available = False
			for subitem in self._toolBoxPageList[item][1:]:
				## Alles ausblenden, was nicht zur Spezies paßt.
				#if (not subitem.species or subitem.species == self.__character.species):
				if (not subitem.species or subitem.species == self.__character.species) and (not subitem.only or self.__character.breed in subitem.only or self.__character.faction in subitem.only):
					available = True
					break
			if available:
				# Nicht hinzufügen, was schon in der Liste steht.
				if self._toolBox.indexOf(self._toolBoxPageList[item][0]) < 0:
					self._toolBox.addItem(self._toolBoxPageList[item][0], item)
					self._toolBoxPageList[item][0].setVisible(True)
			else:
				indexOfWidget = self._toolBox.indexOf(self._toolBoxPageList[item][0])
				if indexOfWidget >= 0:
					self._toolBox.removeItem(indexOfWidget)
				self._toolBoxPageList[item][0].setVisible(False)



