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

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QListWidget, QListWidgetItem, QIcon, QColor
#from PyQt4 import QtSvg	# Damit auch unter Windows SVG-Dateien dargestellt werden.

from src.Config import Config
#from src.Debug import Debug




class SelectWidget(QListWidget):
	"""
	@brief Das Widget, in welchem sämtliche berechneten Werte angeordnet sind.

	Die Werte, welche aus den Eigenschaften des Charakters berechnet werden, kommen allesamt in dieses Widget.
	"""
	
	def __init__(self, parent=None):
		super(SelectWidget, self).__init__(parent)

		self.pageList = [
			[ "Information", ":types/images/svg/humans.svg", ],
			[ "Attributes", ":types/images/svg/maleprofile.svg", ],
			[ "Skills", ":types/images/svg/high_jump.svg", ],
			[ "Template", ":types/images/svg/evolution.svg", ],
			[ "Merits", ":types/images/svg/karate.svg", ],
			[ "Morality", ":types/images/svg/knife.svg", ],
			[ "Powers", ":types/images/svg/bolt.svg", ],
			[ "Flaws", ":types/images/svg/tail.svg", ],
			[ "Items", ":types/images/svg/flail.svg", ],
			[ "Specials", ":types/images/svg/fairy.svg", ],
		]

		for page in self.pageList:
			QListWidgetItem(QIcon(page[1]), self.tr(page[0]), self)

		self.__stdBackgroundRole = self.item( 0 ).data(Qt.BackgroundRole)

		for i in range(self.count()):
			self.item(i).setTextAlignment(Qt.AlignVCenter)
			self.item(i).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

		self.setIconSize(Config.selectIconSize)

		self.setMaximumWidth(Config.selectWidgetWidth)


	def currentPage(self):
		"""
		Gibt den Namen der aktuellen Seite zurück.
		"""

		return self.pageList[self.currentRow()][0]


	def indexOf(self, page):
		"""
		Gibt den Index der Seite mit dem angegebenen Titel zurück.
		"""

		i = 0
		for item in self.pageList:
			if item[0] == page:
				return i
			i += 1


	def selectPrevious(self):
		if ( self.currentRow() > 0 ):
			self.setCurrentRow( self.currentRow() - 1 )

			if ( not self.item( self.currentRow() ).flags() & Qt.ItemIsEnabled ):
				if ( self.currentRow() > 0 ):
					self.selectPrevious()
				else:
					self.selectNext()


	def selectNext(self):
		if ( self.currentRow() < self.count() - 1 ):
			self.setCurrentRow( self.currentRow() + 1 )

			# Ist die neue Seite disabled, müssen wir noch eine Seite weiter springen.
			if ( not self.item( self.currentRow() ).flags() & Qt.ItemIsEnabled ):
				if ( self.currentRow() < self.count() - 1 ):
					self.selectNext()
				else:
					self.selectPrevious()


	def setItemEnabled(self, row, sw):
		"""
		Aktiviert oder deaktiviert das Item in Zeile row.
		"""

		if sw:
			self.item( row ).setFlags( Qt.ItemIsEnabled | Qt.ItemIsSelectable )
			self.item( row ).setData(Qt.ForegroundRole, QColor())
		else:
			self.item( row ).setFlags( Qt.NoItemFlags )
			self.item( row ).setData(Qt.ForegroundRole, QColor(Config.deactivatedTextColor))


	def setItemColor( self, item, color ):
		"""
		Färbt dieses Item ein.

		\param item Hier kann entweder der Index der Zeile oder aber der Name der Seite angegeben werden.
		"""

		row = None
		if type(item) == int:
			row = item
		else:
			for i in range(len(self.pageList)):
				if self.pageList[i][0] == item:
					row = i
					break
		self.item( row ).setData(Qt.BackgroundRole, color)


	def resetItemColor( self, item ):
		"""
		Stellt die ursprüngliche Färbung wieder her.

		\param item Hier kann entweder der Index der Zeile oder aber der Name der Seite angegeben werden.

		\note Die durch enabled-hervorgerufene Farbe bleibt hiervon unberührt.
		"""

		row = None
		if type(item) == int:
			row = item
		else:
			for i in range(len(self.pageList)):
				if self.pageList[i][0] == item:
					row = i
					break
		self.item( row ).setData(Qt.BackgroundRole, self.__stdBackgroundRole)


	def disableItems( self, species ):
		"""
		Diese Funktion verbirgt die Anzeige übernatürlicher Kräfte, wenn keine zur Verfügung stehen.
		"""

		for i in range(len(self.pageList)):
			if self.pageList[i][0] == "Powers" or self.pageList[i][0] == "Specials":
				if species == "Human":
					self.setItemEnabled(i, False)
				else:
					self.setItemEnabled(i, True)


	def changeIcons(self, species):
		"""
		Ändert die Icons abhängig von der Spezies des Charakters.
		"""

		for i in range(len(self.pageList)):
			if self.pageList[i][0] == "Specials":
				if species == "Changeling":
					self.item(i).setIcon(QIcon(":types/images/svg/fairy.svg"))
				elif species == "Mage":
					self.item(i).setIcon(QIcon(":types/images/svg/pentagram.svg"))
				elif species == "Vampire":
					self.item(i).setIcon(QIcon(":types/images/svg/teeth.svg"))
				elif species == "Werewolf":
					self.item(i).setIcon(QIcon(":types/images/svg/wolfhead.svg"))
				else:
					self.item(i).setIcon(QIcon(":types/images/svg/oldwitch.svg"))

