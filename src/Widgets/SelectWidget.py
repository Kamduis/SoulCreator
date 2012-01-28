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

from PySide.QtCore import Qt, QSize
from PySide.QtGui import QListWidget, QListWidgetItem, QIcon, QColor
from PySide import QtSvg	# Damit auch unter Windows SVG-Dateien dargestellt werden.

from src.Config import Config
from src.Debug import Debug

from resources import rc_resource




class SelectWidget(QListWidget):
	"""
	@brief Das Widget, in welchem sämtliche berechneten Werte angeordnet sind.

	Die Werte, welche aus den Eigenschaften des Charakters berechnet werden, kommen allesamt in dieses Widget.
	"""
	
	def __init__(self, parent=None):
		QListWidget.__init__(self, parent)

		QListWidgetItem(QIcon(":types/images/svg/humans.svg"), self.tr("Information"), self)
		QListWidgetItem(QIcon(":types/images/svg/maleprofile.svg"), self.tr("Attributes"), self)
		QListWidgetItem(QIcon(":types/images/svg/high_jump.svg"), self.tr("Skills"), self)
		QListWidgetItem(QIcon(":types/images/svg/karate.svg"), self.tr("Merits"), self)
		QListWidgetItem(QIcon(":types/images/svg/knife.svg"), self.tr("Morality"), self)
		QListWidgetItem(QIcon(":types/images/svg/bolt.svg"), self.tr("Powers"), self)
		QListWidgetItem(QIcon(":types/images/svg/tail.svg"), self.tr("Flaws"), self)
		QListWidgetItem(QIcon(":types/images/svg/flail.svg"), self.tr("Items"), self)
		QListWidgetItem(QIcon(":types/images/svg/fairy.svg"), self.tr("Specials"), self)

		self.__stdBackgroundRole = self.item( 0 ).data(Qt.BackgroundRole)

		for i in xrange(self.count()):
			self.item(i).setTextAlignment(Qt.AlignVCenter)
			self.item(i).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

		self.setIconSize(Config.selectIconSize)

		self.setMaximumWidth(Config.selectWidgetWidth)


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


	def setItemColor( self, row, color ):
		"""
		Färbt dieses Item ein.
		"""

		self.item( row ).setData(Qt.BackgroundRole, color)


	def resetItemColor( self, row ):
		"""
		Stellt die ursprüngliche Färbung wieder her.

		\note Die durch enabled-hervorgerufene Farbe bleibt hiervon unberührt.
		"""

		self.item( row ).setData(Qt.BackgroundRole, self.__stdBackgroundRole)


	def disableItems( self, species ):
		"""
		Diese Funktion verbirgt die Anzeige übernatürlicher Kräfte, wenn keine zur Verfügung stehen.
		"""

		rowsToChange = (
			5,
			8,
		)
		for row in rowsToChange:
			if species == "Human":
				self.setItemEnabled(row, False)
			else:
				self.setItemEnabled(row, True)


	def changeIcons(self, species):
		"""
		Ändert die Icons abhängig von der Spezies des Charakters.
		"""

		rowsToChange = 8
		if species == "Changeling":
			self.item(rowsToChange).setIcon(QIcon(":types/images/svg/fairy.svg"))
		elif species == "Mage":
			self.item(rowsToChange).setIcon(QIcon(":types/images/svg/pentagram.svg"))
		elif species == "Vampire":
			self.item(rowsToChange).setIcon(QIcon(":types/images/svg/teeth.svg"))
		elif species == "Werewolf":
			self.item(rowsToChange).setIcon(QIcon(":types/images/svg/wolfhead.svg"))
		else:
			self.item(rowsToChange).setIcon(QIcon(":types/images/svg/oldwitch.svg"))

