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

#import traceback

from PySide.QtCore import Qt
from PySide.QtGui import QWidget, QVBoxLayout, QGridLayout, QLabel, QFrame, QButtonGroup

from src.Config import Config
#from src import Error
#from ReadXml import ReadXml
from src.Widgets.Components.CharaTrait import CharaTrait
from src.Debug import Debug




class AttributeWidget(QWidget):
	"""
	@brief Das Widget, in welchem sämtliche Attribute angeordnet sind.

	Die Attribute werden in diesem Widget angeordnet.

	\todo Bonusattribut als tatsächlichen Attributspunkt einfügen.
	"""

	def __init__(self, template, character, parent=None):
		QWidget.__init__(self, parent)
		
		self.__character = character
		self.__storage = template

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

		typ = "Attribute"

		categoryList = (
			"Mental",
			"Physical",
			"Social",
		)

		self.__labelStr = QLabel( self )
		self.__labelDex = QLabel( self )
		self.__labelSta = QLabel( self )
		self.__labelMan = QLabel( self )

		#connect( self, SIGNAL( speciesChanged( bool ) ), labelStr, SLOT( setHidden( bool ) ) )
		#connect( self, SIGNAL( speciesChanged( bool ) ), labelDex, SLOT( setHidden( bool ) ) )
		#connect( self, SIGNAL( speciesChanged( bool ) ), labelSta, SLOT( setHidden( bool ) ) )
		#connect( self, SIGNAL( speciesChanged( bool ) ), labelMan, SLOT( setHidden( bool ) ) )

		for item in categoryList:
			#Debug.debug(self.__character.traits)
			__list = self.__character.traits[typ][item]

			actualColumn += 1

			vLine = QFrame( self )
			vLine.setFrameStyle( QFrame.VLine)
			self.__layoutAttributes.addWidget( vLine, 1, actualColumn, len(__list), 1, Qt.AlignHCenter )

			#// 		layout.setColumnMinimumWidth(actualColumn, Config::traitCategorySpace)
			self.__layoutAttributes.setColumnStretch( actualColumn, 1 )

			# Jetzt sind wir in der Spalte für die tatsächlchen Attribute
			actualColumn += 1

			# Aber zuerst kommt die Überschrift für die einzelnen Kategorien.
			header = QLabel()
			header.setAlignment( Qt.AlignHCenter )
			header.setText( "<b>" + item + "</b>" )
			self.__layoutAttributes.addWidget( header, 0, actualColumn )

			# Einfügen der tatsächlichen Attribute
			j = 0
			for attrib in __list:
				#Debug.debug(id(attrib))
				# Anlegen des Widgets, das diese Eigenschaft repräsentiert.
				traitWidget = CharaTrait( attrib, self )
				traitWidget.setSpecialtiesHidden( True )
				traitWidget.setDescriptionHidden( True )

				self.__layoutAttributes.addWidget( traitWidget, j + 1, actualColumn )

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

				j += 1

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

		#connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), self, SLOT( filterBonusAttribute() ) )
		#connect( character, SIGNAL( breedChanged( QString ) ), self, SLOT( filterBonusAttribute() ) )
		#connect( buttonsBonus, SIGNAL( buttonClicked( int ) ), self, SLOT( addAttributeBonus( int ) ) )
		#connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), self, SLOT( emitSpeciesChanged( cv_Species::SpeciesFlag ) ) )


#void AttributeWidget::updateshapeValuesStr( int val ) {
	#"""
	#Aktualisiert die Anzeige der unterschiedlichen Gestalten eines Werwolfs für die Stärke.
	#"""

	#QStringList txt

	#// Die Hishu-Gestalt interessiert nicht, da diese ja direkt eingegeben wird.

	#for ( int i = 1; i < cv_Shape::getShapeList().count(); ++i ) {
		#txt.append( QString::number( CalcAdvantages::strength( val, cv_Shape::getShapeList().at( i ) ) ) );
	#}

	#labelStr.setText( txt.join( "/" ) );
#}

#void AttributeWidget::updateshapeValuesDex( int val ) {
	#"""
	#Aktualisiert die Anzeige der unterschiedlichen Gestalten eines Werwolfs für die Geschicklichkeit.
	#"""

	#QStringList txt;

	#// Die Hishu-Gestalt interessiert nicht, da diese ja direkt eingegeben wird.

	#for ( int i = 1; i < cv_Shape::getShapeList().count(); ++i ) {
		#txt.append( QString::number( CalcAdvantages::dexterity( val, cv_Shape::getShapeList().at( i ) ) ) );
	#}

	#labelDex.setText( txt.join( "/" ) );
#}

#void AttributeWidget::updateshapeValuesSta( int val ) {
	#"""
	#Aktualisiert die Anzeige der unterschiedlichen Gestalten eines Werwolfs für die Widerstandsfähigkeit.
	#"""

	#QStringList txt;

	#// Die Hishu-Gestalt interessiert nicht, da diese ja direkt eingegeben wird.

	#for ( int i = 1; i < cv_Shape::getShapeList().count(); ++i ) {
		#txt.append( QString::number( CalcAdvantages::stamina( val, cv_Shape::getShapeList().at( i ) ) ) );
	#}

	#labelSta.setText( txt.join( "/" ) );
#}

#void AttributeWidget::updateshapeValuesMan( int val ) {
	#"""
	#Aktualisiert die Anzeige der unterschiedlichen Gestalten eines Werwolfs für die Manipulation.
	#"""

	#QStringList txt;

	#// Die Hishu-Gestalt interessiert nicht, da diese ja direkt eingegeben wird.

	#for ( int i = 1; i < cv_Shape::getShapeList().count(); ++i ) {
		#txt.append( QString::number( CalcAdvantages::manipulation( val, cv_Shape::getShapeList().at( i ) ) ) );
	#}

	#labelMan.setText( txt.join( "/" ) );
#}

#void AttributeWidget::emitSpeciesChanged( cv_Species::SpeciesFlag spe ) {
	#"""
	#Sorgt dafür, daß das Signal speciesChanged() mit dem richtigen Argument ausgesandt wird.
	#"""

	#"""
	#
	#"""
	
	#if ( spe == cv_Species::Werewolf ) {
		#emit speciesChanged( false );
	#} else {
		#emit speciesChanged( true );
	#}
#}


#void AttributeWidget::filterBonusAttribute() {
	#"""
	#Ein Bonusattributs wird nur manchmal dargestellt.
	#"""

	#cv_AbstractTrait::Type type = cv_AbstractTrait::Attribute;

	#QList< TraitBonus* > listBonus = storage.traitsBonus( type, character.species() );

	#// Bereits platzierte Knöpfe löschen, bevor wir sie wieder neu einfügen.
	#int listCount = buttonsBonus.buttons().count();
	#for ( int i = listCount; i > 0; --i ) {

		#delete buttonsBonus.buttons().at( i - 1 );
	#}

	#for ( int i = 0; i < listBonus.count(); ++i ) {
		#if ( listBonus.at( i ).breedDependant() == character.breed() ) {
			#// Füge neue Knöpfe hinzu
			#QRadioButton* button = new QRadioButton( listBonus.at( i ).name() );
			#buttonsBonus.addButton( button );
			#layoutButtonsBonus.addWidget( button );

			#if ( i == 0 ) {
				#button.click();
			#}
		#}
	#}
#}


#void AttributeWidget::addAttributeBonus( int id ) {
	#"""
	#Der Bonusattributspunkt wird an die tatsächlichen Attribute angefügt.
	#"""

	#QList< Trait* > list = character.traits( cv_AbstractTrait::Attribute );

	#for ( int i = 0; i < list.count(); ++i ) {
		#list.at( i ).setBonus( false );

#// 		qDebug() << Q_FUNC_INFO << buttonsBonus.button( id ).text();
		#if ( buttonsBonus.button( id ).text() == list.at( i ).name() ) {
			#list.at( i ).setBonus( true );
#// 			qDebug() << Q_FUNC_INFO << "Lege Bonuseigenschaft von" << list.at(i).name() << "auf" << list.at(i).isBonus();
		#}
	#}
#}