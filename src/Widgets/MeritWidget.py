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

#from PyQt4.QtCore import pyqtSignal as Signal
#from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget, QVBoxLayout, QToolBox

from src.Config import Config
#from src import Error
from src.Tools import ListTools
from src.Widgets.TraitWidget import TraitWidget
from src.Widgets.Components.CharaTrait import CharaTrait
#from src.Debug import Debug




class MeritWidget(TraitWidget):
	"""
	@brief Das Widget, in welchem sämtliche Merits angeordnet sind.

	\todo Einen Knopf erstellen, über den der Benutzer angeben kann, welche Merits er denn wirklich alle angezeigt haben will.

	\todo Bei Merits mit Zusatztext (Language) in diesem men+ ein Zahlenfle dangeben, bei welchem der benutzer einstellen kann, wieviele verschiedene dieser scheinbar identischen merits er angezeigt haben will.
	"""


	def __init__(self, template, character, parent=None):
		super(MeritWidget, self).__init__(template, character, parent)

		self.__layout = QVBoxLayout()
		self.setLayout( self.__layout )

		self.__toolBox = QToolBox()
		## Die Auflistung der Merits soll auch unter Windows einen transparenten Hintergrund haben.
		self.__toolBox.setObjectName("transparentWidget")
		## \todo Sollte nicht vom Betriebssystem, sondern vom verwendeten Style abhängen.
		if os.name == "nt":
			self.__toolBox.setStyleSheet( "QScrollArea{ background: transparent; } QWidget#transparentWidget { background: transparent; }" )
		self.__layout.addWidget(self.__toolBox)

		self.__typ = "Merit"
		categories = []
		categories.extend(Config.meritCategories)
		categories.extend(self._storage.categories(self.__typ))
		# Duplikate werden entfernt. Dadurch wird die in der Config-Klasse vorgegebene Reihenfolge eingehalten und zusätzliche, dort nicht erwähnte Kategorien werden hinterher angehängt.
		categories = ListTools.uniqifyOrdered(categories)

		# Diese Liste speichert den Index der ToolBox-Seite bei den unterschiedlichen Kategorien
		self.__categoryIndex = {}

		# Merits werden in einer Spalte heruntergeschrieben, aber mit vertikalem Platz dazwischen.
		for item in categories:
			# Für jede Kategorie wird ein eigener Abschnitt erzeugt.
			widgetMeritCategory = QWidget()
			## Dank des Namens übernimmt dieses Widget den Stil des Eltern-Widgets.
			widgetMeritCategory.setObjectName("transparentWidget")

			layoutMeritCategory = QVBoxLayout()
			widgetMeritCategory.setLayout( layoutMeritCategory )

			self.__toolBox.addItem( widgetMeritCategory, item )
			self.__categoryIndex[item] = self.__toolBox.count() - 1
			#Debug.debug(self.__categoryIndex)

			__list = list( self._character.traits[self.__typ][item].items() )
			__list.sort()
			for merit in __list:
				#Debug.debug(merit)
				# Anlegen des Widgets, das diese Eigenschaft repräsentiert.
				traitWidget = CharaTrait( merit[1], self )
				traitWidget.setSpecialtiesHidden(True)
				if not merit[1].custom:
					traitWidget.setDescriptionHidden(True)

				# Bei Merits sind nur bestimmte Werte erlaubt.
				#Debug.debug(self._storage.traits[self.__typ][item][merit[0]])
				traitWidget.setPossibleValues(self._storage.traits[self.__typ][item][merit[1].identifier]["values"])

				# Es werden nur Eigenschaften der richtigen Alters- und Zeit-Kategorie angezeigt.
				self.hideReasonChanged.connect(traitWidget.hideOrShowTrait)

				layoutMeritCategory.addWidget( traitWidget )

				merit[1].valueChanged.connect(self.countMerits)
				#self._character.speciesChanged.connect(traitWidget.hideOrShowTrait_species)


			# Stretch einfügen, damit die Eigenschaften besser angeordnet sind.
			layoutMeritCategory.addStretch()

		self.setMinimumWidth(Config.traitLineWidthMin)

		self._character.speciesChanged.connect(self.countMerits)

	#// 	dialog = new SelectMeritsDialog( this );
	#//
	#// 	QHBoxLayout* layout_button = new QHBoxLayout();
	#// 	layoutTop.addLayout( layout_button );
	#//
	#// 	button = new QPushButton();
	#// 	button.setIcon( style().standardIcon( QStyle::SP_FileDialogStart ) );
	#//
	#// 	layout_button.addStretch();
	#// 	layout_button.addWidget( button );
	#//
	#// 	connect( button, SIGNAL( clicked( bool ) ), dialog, SLOT( exec() ) );


	def countMerits(self):
		"""
		Zält die Merits in einer Kategorie, deren Wert größer 0 ist. Dieser Wert wird dann in die Überschrift der einzelnen ToolBox-Seiten angezeigt, um dem Benutzer die Übersicht zu bewahren.

		Es wird nur dann etwas angezeigt, wenn der Weert größer 0 ist.

		Versteckte Eigenschaften. also solche, die der Spezies nicht zur Verfügung stehen, können einen Wert > 0 haben, sollten aber nicht mitgezählt werden.
		"""

		for item in self._character.traits[self.__typ]:
			numberInCategory = 0
			for subitem in self._character.traits[self.__typ][item].values():
				if subitem.value > 0 and (not subitem.species or subitem.species == self._character.species):
					numberInCategory += 1

			# ToolBox-Seite des entsprechenden Kategorie mit der Anzahl gewählter Merits beschriften.
			if numberInCategory > 0:
				self.__toolBox.setItemText( self.__categoryIndex[item], "{} ({})".format(item, numberInCategory) )
			else:
				self.__toolBox.setItemText( self.__categoryIndex[item], item )

