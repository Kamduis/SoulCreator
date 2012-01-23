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
from src.Widgets.Components.TraitLine import CharaTrait
from src.Widgets.Components.CheckTrait import CheckTrait
from src.Debug import Debug




class CategoryTraitWidget(QWidget):
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
				if not trait[1].custom:
					traitWidget.setDescriptionHidden(True)

				self._toolBoxPageList[item].append(trait[1])

				layoutCategory.addWidget( traitWidget )

				self.__character.speciesChanged.connect(traitWidget.hideOrShowTrait_species)

			# Stretch einfügen, damit die Eigenschaften besser angeordnet sind.
			layoutCategory.addStretch()
		#Debug.debug(self._toolBoxPageList)
		self.__character.speciesChanged.connect(self.hideOrShowToolPage)


	def hideOrShowToolPage(self, species):
		"""
		Verbirgt eine Seite der ToolBox, wenn alle darin enthaltenen Widgets versteckt sind. Ansonsten wird sie dargestellt.
		"""

		# Damit die Kategorien auch nach dem Entfernen und Hinzufügen von Eigenschaften alphapetisch sortiert bleiben.
		keys = self._toolBoxPageList.keys()
		keys.sort()

		for item in keys:
			available = False
			for subitem in self._toolBoxPageList[item][1:]:
				if (not subitem.species or subitem.species == species):
					available = True
					break
			if available:
				self._toolBox.addItem(self._toolBoxPageList[item][0], item)
				self._toolBoxPageList[item][0].setVisible(True)
			else:
				indexOfWidget = self._toolBox.indexOf(self._toolBoxPageList[item][0])
				if indexOfWidget != -1:
					self._toolBox.removeItem(indexOfWidget)
				self._toolBoxPageList[item][0].setVisible(False)




class PowerWidget(CategoryTraitWidget):
	"""
	@brief Das Widget, in welchem sämtliche Übernatürlichen Kräfte angeordnet sind.

	Hier tauchen die nur die übergeordneten Powers auf, in dem anderen Widget dann die speziellen Kräfte (Vampire-Rituale, Werwolf-Gaben + Rituale, Mage-Rotes, Changeling-???)
	"""


	def __init__(self, template, character, parent=None):
		CategoryTraitWidget.__init__(self, template, character, typ="Power", isCheckable=False, parent=parent)




class SubPowerWidget(CategoryTraitWidget):
	"""
	@brief In diesem Widget werden die "Zaubersprüche" (Wechselbalg-GoblinContracts, Magier-Rotes, Vampir-Rituale, Werwolf-Gaben etc.) untergebracht. Diese können abgehakt werden und haben als Voraussetzung in der Regel eine bestimmte Power (\ref PowerWidget), um überhaupt gewählt werden zu können.

	\todo Das obligatorisch transparent Setzen des Hintergrundes sollte nicht vom Betriebssystem, sondern vom verwendeten Style abhängen.
	"""


	def __init__(self, template, character, parent=None):
		CategoryTraitWidget.__init__(self, template, character, typ="Subpower", isCheckable=True, parent=parent)



