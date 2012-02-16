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

from PySide.QtCore import Qt#, Signal
from PySide.QtGui import QWidget, QVBoxLayout, QGridLayout, QLabel, QFrame, QButtonGroup

from src.Config import Config
#from src import Error
from src.Widgets.Components.CharaTrait import CharaTrait
from src.Widgets.TraitWidget import TraitWidget
#from src.Debug import Debug




class AttributeWidget(TraitWidget):
	"""
	@brief Das Widget, in welchem sämtliche Attribute angeordnet sind.

	Die Attribute werden in diesem Widget angeordnet.

	\todo Bonusattribut als tatsächlichen Attributspunkt einfügen.
	"""

	def __init__(self, template, character, parent=None):
		TraitWidget.__init__(self, template, character, parent)

		self.__layout = QVBoxLayout()
		self.setLayout( self.__layout )

		self.__layoutAttributes = QGridLayout()
		self.__layout.addLayout( self.__layoutAttributes )

		#// 	QFrame* frame = new QFrame( self )
		#// 	layout.addWidget( frame )
		#//
		#// 	QVBoxLayout* layoutHeader = new QVBoxLayout()
		#// 	frame.setLayout( layoutHeader )

		self.__labelPower = QLabel( "<b>" + self.tr( "Power" ) + "</b>" )
		self.__labelPower.setAlignment( Qt.AlignRight )

		self.__labelFinesse = QLabel( "<b>" + self.tr( "Finesse" ) + "</b>" )
		self.__labelFinesse.setAlignment( Qt.AlignRight )

		self.__labelResistance = QLabel( "<b>" + self.tr( "Resistance" ) + "</b>" )
		self.__labelResistance.setAlignment( Qt.AlignRight )

		actualRow = 1
		actualColumn = 0

		self.__layoutAttributes.addWidget( self.__labelPower, actualRow, actualColumn )
		actualRow += 1
		self.__layoutAttributes.addWidget( self.__labelFinesse, actualRow, actualColumn )
		actualRow += 1
		self.__layoutAttributes.addWidget( self.__labelResistance, actualRow, actualColumn )

		self.__labelStr = QLabel( self )
		self.__labelDex = QLabel( self )
		self.__labelSta = QLabel( self )
		self.__labelMan = QLabel( self )

		#connect( self, SIGNAL( speciesChanged( bool ) ), labelStr, SLOT( setHidden( bool ) ) )
		#connect( self, SIGNAL( speciesChanged( bool ) ), labelDex, SLOT( setHidden( bool ) ) )
		#connect( self, SIGNAL( speciesChanged( bool ) ), labelSta, SLOT( setHidden( bool ) ) )
		#connect( self, SIGNAL( speciesChanged( bool ) ), labelMan, SLOT( setHidden( bool ) ) )

		for item in Config.attributes:
			#Debug.debug(self._character.traits)

			actualColumn += 1

			vLine = QFrame( self )
			vLine.setFrameStyle( QFrame.VLine)
			self.__layoutAttributes.addWidget( vLine, 1, actualColumn, len(item[1]), 1, Qt.AlignHCenter )

			#// 		layout.setColumnMinimumWidth(actualColumn, Config::traitCategorySpace)
			self.__layoutAttributes.setColumnStretch( actualColumn, 1 )

			# Jetzt sind wir in der Spalte für die tatsächlchen Attribute
			actualColumn += 1

			# Aber zuerst kommt die Überschrift für die einzelnen Kategorien.
			header = QLabel()
			header.setAlignment( Qt.AlignHCenter )
			header.setText( "<b>" + item[0] + "</b>" )
			self.__layoutAttributes.addWidget( header, 0, actualColumn )

			# Einfügen der tatsächlichen Attribute
			i = 0
			for subitem in item[1]:
				attrib = self._character.traits["Attribute"][item[0]][subitem]
				#Debug.debug(attrib)
				# Anlegen des Widgets, das diese Eigenschaft repräsentiert.
				traitWidget = CharaTrait( attrib, self )
				traitWidget.setSpecialtiesHidden( True )
				traitWidget.setDescriptionHidden( True )

				# An welcher Position sitzt dieses Attribut in der Config.attributes-Liste?

				self.__layoutAttributes.addWidget( traitWidget, i + 1, actualColumn )

				self.maxTraitChanged.connect(traitWidget.setMaximum)

				#if ( item == "Physical" ):
					#if ( attrib["name"] == "Strength" ):
						#self.__layoutAttributes.addWidget( self.__labelStr, j + 1, actualColumn + 1 )
						#connect( trait, SIGNAL( valueChanged( int ) ), self, SLOT( updateshapeValuesStr( int ) ) )
					#} else if ( trait.name() == "Dexterity" ) {
						#layoutAttributes.addWidget( self.__labelDex, j + 1, actualColumn + 1 )
						#connect( trait, SIGNAL( valueChanged( int ) ), self, SLOT( updateshapeValuesDex( int ) ) )
					#} else if ( trait.name() == "Stamina" ) {
						#layoutAttributes.addWidget( self.__labelSta, j + 1, actualColumn + 1 )
						#connect( trait, SIGNAL( valueChanged( int ) ), self, SLOT( updateshapeValuesSta( int ) ) )
				#} else if ( trait.category() == cv_AbstractTrait::Social ) {
					#if ( self.__trait.name() == "Manipulation" ) {
						#layoutAttributes.addWidget( labelMan, j + 1, actualColumn + 1 )
						#connect( trait, SIGNAL( valueChanged( int ) ), self, SLOT( updateshapeValuesMan( int ) ) )

				i += 1

			# Bei Werwölfen erscheint hier Zusatztext. Und damit der Sparator richtig gesetzt wird, muß die aktuelle Spalte ein weitergezählt werden.
			actualColumn += 1

		self.__layout.addSpacing( Config.vSpace )

		self.__layoutBonus = QGridLayout()
		self.__layout.addLayout( self.__layoutBonus )

		self.__labelBonus = QLabel( self )
		self.__labelBonus.setText( self.tr( "Bonus Attribute:" ) )

		self.__layoutButtonsBonus = QVBoxLayout()

		self.__buttonsBonus = QButtonGroup( self )

		self.__layoutBonus.addWidget( self.__labelBonus, 0, 0, Qt.AlignTop | Qt.AlignLeft )
		self.__layoutBonus.addLayout( self.__layoutButtonsBonus, 0, 1 )
	#// 	layoutBonus.addItem(new QSpacerItem(0,0), 0, 2)
		self.__layoutBonus.addWidget( QWidget( self ), 0, 2 )
		self.__layoutBonus.setColumnStretch( 2, 1 )

