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


	#specialtiesActivated = Signal(bool, object)
	#hideReasonChanged = Signal(str, str)


	def __init__(self, template, character, parent=None):
		QWidget.__init__(self, parent)

		self.__storage = template
		self.__character = character

		self.__layout = QVBoxLayout()
		self.setLayout( self.__layout )

		self.__toolBox = QToolBox()

		self.__layout.addWidget(self.__toolBox)

		typ = "Merit"
		categories = self.__storage.categories(typ)

		# Merits werden in einer Spalte heruntergeschrieben, aber mit vertikalem Platz dazwischen.
		for item in categories:
			# Für jede Kategorie wird ein eigener Abschnitt erzeugt.
			widgetMeritCategory = QWidget()
			layoutMeritCategory = QVBoxLayout()

			widgetMeritCategory.setLayout( layoutMeritCategory )

			self.__toolBox.addItem( widgetMeritCategory, item )

			__list = self.__character.traits[typ][item]

			#try {
				#list = storage.traits( type, v_category.at( i ) );
			#} catch (eTraitNotExisting &e) {
				#MessageBox::exception(this, e.message(), e.description());
			#}

			for merit in __list:
				Debug.debug(merit)
				# Anlegen des Widgets, das diese Eigenschaft repräsentiert.
				traitWidget = CharaTrait( merit, self )
				traitWidget.setSpecialtiesHidden(True)
				traitWidget.setDescriptionHidden( True )

				#for ( int k = 0; k < Config::traitMultipleMax; ++k ) {
					#// Anlegen der Eigenschaft im Speicher
					#Trait* traitPtr = character.addTrait( list[j] );

					#// Anlegen des Widgets, das diese Eigenschaft repräsentiert.
					#CharaTrait* charaTrait = new CharaTrait( this, traitPtr, list[j] );
					#charaTrait.setValue( 0 );
				layoutMeritCategory.addWidget( traitWidget )

					#connect( charaTrait, SIGNAL( valueChanged( int ) ), this, SLOT( countMerits() ) );

					#// Eigenschaften mit Beschreibungstext werden mehrfach dargestellt, da man sie ja auch mehrfach erwerben kann. Alle anderen aber immer nur einmal.

					#if ( !list.at( j ).custom() ) {
						#break;
					#}
				#}
			#}

			# Stretch einfügen, damit die Eigenschaften besser angeordnet sind.
			layoutMeritCategory.addStretch()
		#}

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
	#}


#void MeritWidget::countMerits() {
	#"""
	#Zält die Merits in einer Kategorie, deren Wert größer 0 ist. Dieser Wert wird dann in die Überschrift der einzelnen ToolBox-Seiten angezeigt, um dem Benutzer die Übersicht zu bewahren.
	
	#Es wird nur dann etwas angezeigt, wenn der Weert größer 0 ist.
	
	#\bug Merits mit Zusatztext werden nicht gezählt. Kann sein, daß das nur auftritt wenn nichts in der Textbox steht. Ist dann kein Problem, da es ohnehin nicht möglich sein dürfte, Werte einzugeben, wenn Zusatext nicht angegeben ist.
	
	#\todo Momentan wird eine Liste mit allen Merits des Charakters erstellt und dann alle gezählt, deren Wert größer 0 ist. Das muß doch besser gehen.
	#"""
	
	#for (int i = 0; i < v_category.count(); ++i){
		#QList< Trait* > list = character.traits( cv_AbstractTrait::Merit, v_category.at(i) );

		#int numberInCategory = 0;

		#for ( int j = 0; j < list.count(); ++j ) {
			#if ( list.at( j ).value() > 0 ) {
				#numberInCategory++;
			#}
		#}

		#// Index der veränderten Kategorie in Liste suchen und dann die toolBox-Seite mit der identischen Indexzahl anpassen.
		#int categoryIndex = v_category.indexOf( v_category.at(i) );

		#if ( numberInCategory > 0 ) {
			#toolBox.setItemText( categoryIndex, cv_AbstractTrait::toString( v_category.at( categoryIndex ), true ) + " (" + QString::number( numberInCategory ) + ")" );
		#} else {
			#toolBox.setItemText( categoryIndex, cv_AbstractTrait::toString( v_category.at( categoryIndex ), true ) );
		#}
	#}
#}

