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
from PySide.QtGui import QWidget, QVBoxLayout, QToolBox#, QScrollArea, QGroupBox

#from src.Config import Config
#from src import Error
#from ReadXml import ReadXml
from src.Widgets.Components.CharaTrait import CharaTrait
from src.Debug import Debug




class MeritWidget(QWidget):
	"""
	@brief Das Widget, in welchem sämtliche Merits angeordnet sind.

	\todo Einen Knopf erstellen, über den der Benutzer angeben kann, welche Merits er denn wirklich alle angezeigt haben will.

	\todo Bei Merits mit Zusatztext (Language) in diesem men+ ein Zahlenfle dangeben, bei welchem der benutzer einstellen kann, wieviele verschiedene dieser scheinbar identischen merits er angezeigt haben will.
	"""


	def __init__(self, template, character, parent=None):
		QWidget.__init__(self, parent)

		self.__storage = template
		self.__character = character

		self.__layout = QVBoxLayout()
		self.setLayout( self.__layout )

		self.__toolBox = QToolBox()

		self.__layout.addWidget(self.__toolBox)

		self.__typ = "Merit"
		categories = self.__storage.categories(self.__typ)

		# Diese Liste speichert den Index der ToolBox-Seite bei den unterschiedlichen Kategorien
		self.__categoryIndex = {}

		# Merits werden in einer Spalte heruntergeschrieben, aber mit vertikalem Platz dazwischen.
		for item in categories:
			# Für jede Kategorie wird ein eigener Abschnitt erzeugt.
			widgetMeritCategory = QWidget()
			layoutMeritCategory = QVBoxLayout()

			widgetMeritCategory.setLayout( layoutMeritCategory )

			self.__toolBox.addItem( widgetMeritCategory, item )
			self.__categoryIndex[item] = self.__toolBox.count() - 1
			#Debug.debug(self.__categoryIndex)

			__list = self.__character.traits[self.__typ][item]

			for merit in __list.values():
				#Debug.debug(merit)
				# Anlegen des Widgets, das diese Eigenschaft repräsentiert.
				traitWidget = CharaTrait( merit, self )
				traitWidget.setSpecialtiesHidden(True)
				if not merit.custom:
					traitWidget.setDescriptionHidden(True)

				layoutMeritCategory.addWidget( traitWidget )

				merit.valueChanged.connect(self.countMerits)
				self.__character.speciesChanged.connect(traitWidget.hideOrShowTrait_species)


			# Stretch einfügen, damit die Eigenschaften besser angeordnet sind.
			layoutMeritCategory.addStretch()

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

