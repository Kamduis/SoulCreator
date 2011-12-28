# -*- coding: utf-8 -*-

"""
\file
\author Victor von Rhein <victor@caern.de>

\section License

Copyright (C) 2011 by Victor von Rhein

This file is part of SoulCreator.

SoulCreator is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SoulCreator is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with SoulCreator.  If not, see <http://www.gnu.org/licenses/>.
"""




from __future__ import division, print_function

from PySide.QtCore import Qt
from PySide.QtGui import QWidget, QVBoxLayout, QScrollArea, QGroupBox

from src.Config import Config
#from src import Error
#from ReadXml import ReadXml
from src.Widgets.Components. CharaTrait import CharaTrait
from src.Debug import Debug




class SkillWidget(QWidget):
	"""
	@brief Das Widget, in welchem sämtliche Fertigkeiten angeordnet sind.

	Wird bei irgendeiner Fertigkeit der Spazialisierungen-Knopf gedrückt, werden alle anderen Spezialisierungs-Knöpfe ausgeschalten.
	"""

	def __init__(self, template, character, parent=None):
		QWidget.__init__(self, parent)
		
		self.__character = character
		self.__storage = template

		self.__layout = QVBoxLayout()
		self.setLayout( self.__layout )

		self.__scrollArea = QScrollArea()
		self.__layout.addWidget( self.__scrollArea)

		self.__scrollLayout = QVBoxLayout()

		self.__scrollWidget = QWidget()
		#scrollWidget.setMinimumSize(this.width(), 400);
		self.__scrollWidget.setLayout(self.__scrollLayout)

		typ = "Skill"

		categoryList = (
			"Mental",
			"Physical",
			"Social",
		)

		for item in categoryList:
			#Debug.debug(self.__character.traits)
			__list = self.__character.traits[typ][item]

			# Für jede Kategorie wird ein eigener Abschnitt erzeugt.
			widgetSkillCategory = QGroupBox()
			widgetSkillCategory.setTitle(item)
			widgetSkillCategory.setFlat(True)
			
			layoutSkillCategory = QVBoxLayout()
			widgetSkillCategory.setLayout( layoutSkillCategory );

			self.__scrollLayout.addWidget( widgetSkillCategory )

			for skill in __list:
				print (skill.name)
				# Anlegen des Widgets, das diese Eigenschaft repräsentiert.
				traitWidget = CharaTrait( skill, self )
				traitWidget.buttonText = 0

				## Fertigkeiten haben Spezialisierungen.
				#connect( traitPtr, SIGNAL( detailsChanged( int )), charaTrait, SLOT( setButtonText(int)) );
				#connect( character, SIGNAL( characterResetted()), this, SLOT( uncheckButtons()) );
				#connect( charaTrait, SIGNAL( specialtiesClicked( bool, QString, QList< cv_TraitDetail > ) ), this, SLOT( toggleOffSpecialties( bool, QString, QList< cv_TraitDetail > ) ) );
				#connect( charaTrait, SIGNAL( specialtiesClicked( bool, QString, QList< cv_TraitDetail > ) ), this, SIGNAL( specialtiesClicked( bool, QString, QList< cv_TraitDetail > ) ) );

				layoutSkillCategory.addWidget( traitWidget )

			# Stretch einfügen, damit die Eigenschaften besser angeordnet sind.
			self.__scrollLayout.addStretch()

		self.__scrollArea.setWidget(self.__scrollWidget)
		self.__scrollArea.setWidgetResizable(True)
		self.__scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.__scrollArea.setMinimumWidth(self.__scrollArea.viewport().minimumWidth())

#void AttributeWidget::updateshapeValuesStr( int val ) {
	#QStringList txt

	#// Die Hishu-Gestalt interessiert nicht, da diese ja direkt eingegeben wird.

	#for ( int i = 1; i < cv_Shape::getShapeList().count(); ++i ) {
		#txt.append( QString::number( CalcAdvantages::strength( val, cv_Shape::getShapeList().at( i ) ) ) );
	#}

	#labelStr.setText( txt.join( "/" ) );
#}

#void AttributeWidget::updateshapeValuesDex( int val ) {
	#QStringList txt;

	#// Die Hishu-Gestalt interessiert nicht, da diese ja direkt eingegeben wird.

	#for ( int i = 1; i < cv_Shape::getShapeList().count(); ++i ) {
		#txt.append( QString::number( CalcAdvantages::dexterity( val, cv_Shape::getShapeList().at( i ) ) ) );
	#}

	#labelDex.setText( txt.join( "/" ) );
#}

#void AttributeWidget::updateshapeValuesSta( int val ) {
	#QStringList txt;

	#// Die Hishu-Gestalt interessiert nicht, da diese ja direkt eingegeben wird.

	#for ( int i = 1; i < cv_Shape::getShapeList().count(); ++i ) {
		#txt.append( QString::number( CalcAdvantages::stamina( val, cv_Shape::getShapeList().at( i ) ) ) );
	#}

	#labelSta.setText( txt.join( "/" ) );
#}

#void AttributeWidget::updateshapeValuesMan( int val ) {
	#QStringList txt;

	#// Die Hishu-Gestalt interessiert nicht, da diese ja direkt eingegeben wird.

	#for ( int i = 1; i < cv_Shape::getShapeList().count(); ++i ) {
		#txt.append( QString::number( CalcAdvantages::manipulation( val, cv_Shape::getShapeList().at( i ) ) ) );
	#}

	#labelMan.setText( txt.join( "/" ) );
#}

#void AttributeWidget::emitSpeciesChanged( cv_Species::SpeciesFlag spe ) {
	#if ( spe == cv_Species::Werewolf ) {
		#emit speciesChanged( false );
	#} else {
		#emit speciesChanged( true );
	#}
#}


#void AttributeWidget::filterBonusAttribute() {
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
