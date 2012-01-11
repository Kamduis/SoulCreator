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
#from src.Tools import ListTools
from src.Widgets.Components.CharaTrait import CharaTrait
from src.Debug import Debug




class PowerWidget(QWidget):
	"""
	@brief Das Widget, in welchem sämtliche Übernatürlichen Kräfte angeordnet sind.

	\bug Da ich die Eigenschaften, welche für die jeweilige Spezies nicht gelten nur verstecke, nehmen sie doch ein klein wenig Platz weg. Und das fällt tatsächlich auf!

	\todo Ein gesondertes Widget für die Sonderkräfte machen. Hier tauchen die Übergeordneten Powers auf, in dem anderen Widget dann die speziellen Kräfte (Vampire-Rituale, Werwolf-Gaben + Rituale, Mage-Rotes, Changeling-???)
	"""


	def __init__(self, template, character, parent=None):
		QWidget.__init__(self, parent)

		self.__storage = template
		self.__character = character

		self.__layout = QVBoxLayout()
		self.setLayout( self.__layout )

		self.__toolBox = QToolBox()
		## Die Auflistung der Kräfte soll auch unter Windows einen transparenten Hintergrund haben.
		self.__toolBox.setObjectName("transparentWidget")
		## \todo Sollte nicht vom Betriebssystem, sondern vom verwendeten Style abhängen.
		if os.name == "nt":
			self.__toolBox.setStyleSheet( "QScrollArea{ background: transparent; } QWidget#transparentWidget { background: transparent; }" )

		self.__layout.addWidget( self.__toolBox )

		self.__typ = "Power"
		categories = self.__storage.categories(self.__typ)

		# Diese Liste speichert den Index der ToolBox-Seite bei den unterschiedlichen Kategorien
		self.toolBoxPageList = {}

		# Powers werden in einer Spalte heruntergeschrieben.
		for item in categories:
			# Für jede Kategorie wird ein eigener Abschnitt erzeugt.
			widgetPowerCategory = QWidget()
			## Dank des Namens übernimmt dieses Widget den Stil des Eltern-Widgets.
			widgetPowerCategory.setObjectName("transparentWidget")

			layoutPowerCategory = QVBoxLayout()

			widgetPowerCategory.setLayout( layoutPowerCategory )

			#self.__toolBox.addItem( widgetPowerCategory, item )

			## In dieser Liste sammle ich die Widgets, damit sie später bei Bedarf in die ToolBox eingefügt werden können.
			self.toolBoxPageList[item] = [widgetPowerCategory]

			__list = self.__character.traits[self.__typ][item].items()
			__list.sort()
			for power in __list:
				# Anlegen des Widgets, das diese Eigenschaft repräsentiert.
				traitWidget = CharaTrait( power[1], self )
				traitWidget.setSpecialtiesHidden(True)
				if not power[1].custom:
					traitWidget.setDescriptionHidden(True)

				self.toolBoxPageList[item].append(power[1])

				layoutPowerCategory.addWidget( traitWidget )

				#power[1].valueChanged.connect(self.countMerits)
				self.__character.speciesChanged.connect(traitWidget.hideOrShowTrait_species)

			# Stretch einfügen, damit die Eigenschaften besser angeordnet sind.
			layoutPowerCategory.addStretch()
		#Debug.debug(self.toolBoxPageList)
		self.__character.speciesChanged.connect(self.hideOrShowToolPage)


	def hideOrShowToolPage(self, species):
		"""
		Verbirgt eine Seite der ToolBox, wenn alle darin enthaltenen Widgets versteckt sind. Ansonsten wird sie dargestellt.
		"""

		for item in self.toolBoxPageList:
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


