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

##include <QDebug>

##include "Exceptions/Exception.h"
#// #include "Config/Config.h"

##include "ReadXml.h"



from __future__ import division, print_function

from PySide.QtCore import Qt
from PySide.QtGui import QWidget, QGridLayout, QLabel, QPushButton, QComboBox, QIcon

#from src.Config import Config
from src.Storage.StorageTemplate import StorageTemplate
from src.Storage.StorageCharacter import StorageCharacter
from src.Widgets.Components.CharaSpecies import CharaSpecies
from src.Widgets.Dialogs.NameDialog import NameDialog




class InfoWidget(QWidget):
	"""
	@brief Das Widget, in welchem wichtige Informationen dargestellt werden.

	Spezies, Namen etc. des Charakters werden hier dargestellt.

	\todo Bei den Virtues und Vices wird bislang nur der erwachsene behrücksichtigt.
	"""

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		
		self.__storage = StorageTemplate(self)
		self.__character = StorageCharacter()

		self.__layout = QGridLayout()
		self.setLayout( self.__layout )

		self.__labelName = QLabel( "" )
		self.__namePushButton = QPushButton( self.tr( "Name:" ) )
		#// 	QLabel* labelNameFull = new QLabel()
		#// 	QLabel* labelNameDisplay = new QLabel()
		#// 	QLabel* labelNameHonorific = new QLabel()
		#// 	QLabel* labelNameSuper = new QLabel()

		self.__labelSpecies = QLabel( self.tr( "Species:" ) )
		self.__speciesComboBox = CharaSpecies( self)

		self.__labelGender = QLabel( self.tr( "Gender:" ) )
		self.__genderCombobox = QComboBox( self )
		self.__genderCombobox.addItem( QIcon( ":/icons/images/male.png" ), self.tr( "Male" ) )
		self.__genderCombobox.addItem( QIcon( ":/icons/images/female.png" ), self.tr( "Female" ) )

		self.__labelVirtue = QLabel( self.tr( "Virtue:" ) )
		self.__virtueCombobox = QComboBox( self )
		#self.__virtueCombobox.addItems( storage.virtueNames() )

		self.__labelVice = QLabel( self.tr( "Vice:" ) )
		self.__viceCombobox = QComboBox( self )
		#self.__viceCombobox.addItems( storage.viceNames() )

		self.__labelBreed = QLabel( self.tr( "Breed:" ) )
		self.__breedCombobox = QComboBox( self )
		#self.__breedCombobox.addItems( storage.breedNames() )

		self.__labelFaction = QLabel( self.tr( "Faction:" ) )
		self.__factionCombobox = QComboBox( self )
		#self.__factionCombobox.addItems( storage.factionNames() )

		self.__layout.addWidget( self.__namePushButton, 0, 0, Qt.AlignTop )
		self.__layout.addWidget( self.__labelName, 0, 1, 1, 2 )
		self.__layout.addWidget( self.__labelGender, 1, 0 )
		self.__layout.addWidget( self.__genderCombobox, 1, 1 )
		self.__layout.addWidget( self.__labelSpecies, 2, 0 )
		self.__layout.addWidget( self.__speciesComboBox, 2, 1 )
		self.__layout.addWidget( self.__labelVirtue, 3, 0 )
		self.__layout.addWidget( self.__virtueCombobox, 3, 1 )
		self.__layout.addWidget( self.__labelVice, 4, 0 )
		self.__layout.addWidget( self.__viceCombobox, 4, 1 )
		self.__layout.addWidget( self.__labelBreed, 5, 0 )
		self.__layout.addWidget( self.__breedCombobox, 5, 1 )
		self.__layout.addWidget( self.__labelFaction, 6, 0 )
		self.__layout.addWidget( self.__factionCombobox, 6, 1 )

#// 	connect(nameLineEdit, SIGNAL(textChanged(QString)), self, SLOT(modifyRealIdentity()));
		self.__namePushButton.clicked.connect(self.openNameDialog)
	#connect( genderCombobox, SIGNAL( currentIndexChanged( int ) ), self, SLOT( changeGender( int ) ) );
	#connect( virtueCombobox, SIGNAL( currentIndexChanged( int ) ), self, SLOT( changeVirtue( int ) ) );
	#connect( viceCombobox, SIGNAL( currentIndexChanged( int ) ), self, SLOT( changeVice( int ) ) );
	#connect( breedCombobox, SIGNAL( currentIndexChanged( int ) ), self, SLOT( changeBreed( int ) ) );
	#connect( factionCombobox, SIGNAL( currentIndexChanged( int ) ), self, SLOT( changeFaction( int ) ) );
	#connect( character, SIGNAL( realIdentityChanged( cv_Identity ) ), self, SLOT( updateIdentity( cv_Identity ) ) );
	#connect( character, SIGNAL( virtueChanged( QString ) ), self, SLOT( updateVirtue( QString ) ) );
	#connect( character, SIGNAL( viceChanged( QString ) ), self, SLOT( updateVice( QString ) ) );
	#connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), self, SLOT( updateBreedTitle( cv_Species::SpeciesFlag ) ) );
	#connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), self, SLOT( updateFactionTitle( cv_Species::SpeciesFlag ) ) );
	#connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), self, SLOT( updateBreedBox( cv_Species::SpeciesFlag ) ) );
	#connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), self, SLOT( updateFactionBox( cv_Species::SpeciesFlag ) ) );
	#connect( character, SIGNAL( breedChanged( QString ) ), self, SLOT( updateBreed( QString ) ) );
	#connect( character, SIGNAL( factionChanged( QString ) ), self, SLOT( updateFaction( QString ) ) );
#}

	def openNameDialog(self):
		"""
		Ruft einen Dialog auf, in welchem die zahlreichen Namen des Charakters eingetragen werden können.
		"""
		
		dialog = NameDialog( self )
		dialog.exec_()
		#dialog.show()


#void InfoWidget::changeGender( int gen ) {
	#cv_Identity id = character->identities().at( 0 );

	#if( gen == 0 ) {
		#id.gender = cv_Identity::Male;
	#} else {
		#id.gender = cv_Identity::Female;
	#}

	#character->setRealIdentity( id );
#}

#void InfoWidget::changeVirtue( int idx ) {
	#character->setVirtue( virtueCombobox->currentText() );
#}

#void InfoWidget::changeVice( int idx ) {
	#character->setVice( viceCombobox->currentText() );
#}

#void InfoWidget::changeBreed( int idx ) {
	#character->setBreed( breedCombobox->currentText() );
#}

#void InfoWidget::changeFaction( int idx ) {
	#character->setFaction( factionCombobox->currentText() );
#}


#void InfoWidget::updateIdentity( cv_Identity id ) {
#// 	namePushButton->setText( cv_Name::displayNameDisplay( id.sureName, id.firstName(), id.nickName ) );

	#QString nameText = "";

	#if( !id.sureName.isEmpty() || !id.foreNames.isEmpty() ) {
		#nameText += cv_Name::displayNameFull( id.sureName, id.foreNames );
	#}

	#if( !id.nickName.isEmpty() ) {
		#if( !nameText.isEmpty() ) {
			#nameText += "\n";
		#}

		#nameText += cv_Name::displayNameDisplay( id.sureName, id.firstName(), id.nickName );
	#}

	#if( !id.honorificName.isEmpty() ) {
		#if( !nameText.isEmpty() ) {
			#nameText += "\n";
		#}

		#nameText += cv_Name::displayNameHonor( id.firstName(), id.honorificName );
	#}

	#if( !id.supernaturalName.isEmpty() ) {
		#if( !nameText.isEmpty() ) {
			#nameText += "\n";
		#}

		#nameText += id.supernaturalName;
	#}

	#labelName->setText( nameText );

	#if( id.gender == cv_Identity::Male ) {
		#genderCombobox->setCurrentIndex( 0 );
	#} else {
		#genderCombobox->setCurrentIndex( 1 );
	#}
#}

#void InfoWidget::updateVirtue( QString txt ) {
	#virtueCombobox->setCurrentIndex( virtueCombobox->findText( txt ) );
#}

#void InfoWidget::updateVice( QString txt ) {
	#viceCombobox->setCurrentIndex( viceCombobox->findText( txt ) );
#}

#void InfoWidget::updateBreed( QString txt ) {
	#breedCombobox->setCurrentIndex( breedCombobox->findText( txt ) );
#}

#void InfoWidget::updateFaction( QString txt ) {
	#factionCombobox->setCurrentIndex( factionCombobox->findText( txt ) );
#}

#void InfoWidget::updateBreedTitle( cv_Species::SpeciesFlag spe ) {
	#labelBreed->setText( storage->breedTitle( spe )  + ":" );
#}

#void InfoWidget::updateFactionTitle( cv_Species::SpeciesFlag spe ) {
	#labelFaction->setText( storage->factionTitle( spe )  + ":" );
#}

#void InfoWidget::updateBreedBox( cv_Species::SpeciesFlag spe ) {
	#breedCombobox->clear();
	#breedCombobox->addItems( storage->breedNames( spe ) );
#}

#void InfoWidget::updateFactionBox( cv_Species::SpeciesFlag spe ) {
	#factionCombobox->clear();
	#factionCombobox->addItems( storage->factionNames( spe ) );
#}
