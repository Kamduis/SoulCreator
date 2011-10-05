/**
 * \file
 * \author Victor von Rhein <goliath@caern.de>
 *
 * \section License
 *
 * Copyright (C) 2011 by Victor von Rhein
 *
 * This file is part of SoulCreator.
 *
 * SoulCreator is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * SoulCreator is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with SoulCreator.  If not, see <http://www.gnu.org/licenses/>.
 */

// #include <QLabel>
#include <QDebug>

// #include "Exceptions/Exception.h"
// #include "Config/Config.h"
#include "Dialogs/NameDialog.h"

#include "InfoWidget.h"


InfoWidget::InfoWidget( QWidget *parent ) : QWidget( parent )  {
	storage = new StorageTemplate( this );
	character = StorageCharacter::getInstance();

	layout = new QGridLayout( this );
	setLayout( layout );

	labelName = new QLabel( "" );
	namePushButton = new QPushButton( tr( "Name:" ) );
// 	QLabel* labelNameFull = new QLabel();
// 	QLabel* labelNameDisplay = new QLabel();
// 	QLabel* labelNameHonorific = new QLabel();
// 	QLabel* labelNameSuper = new QLabel();

	QLabel* labelSpecies = new QLabel( tr( "Species:" ) );
	speciesComboBox = new CharaSpecies( this );

	QLabel* labelGender = new QLabel( tr( "Gender:" ) );
	genderCombobox = new QComboBox( this );
	genderCombobox->addItem( QIcon( ":/icons/images/male.png" ), tr( "Male" ) );
	genderCombobox->addItem( QIcon( ":/icons/images/female.png" ), tr( "Female" ) );

	QLabel* labelVirtue = new QLabel( tr( "Virtue:" ) );
	virtueCombobox = new QComboBox( this );
	virtueCombobox->addItems( storage->virtueNames() );

	QLabel* labelVice = new QLabel( tr( "Vice:" ) );
	viceCombobox = new QComboBox( this );
	viceCombobox->addItems( storage->viceNames() );

	labelBreed = new QLabel( tr( "Breed:" ) );
	breedCombobox = new QComboBox( this );
	breedCombobox->addItems( storage->breedNames() );

	labelFaction = new QLabel( tr( "Faction:" ) );
	factionCombobox = new QComboBox( this );
	factionCombobox->addItems( storage->factionNames() );

	layout->addWidget( namePushButton, 0, 0, Qt::AlignTop );
	layout->addWidget( labelName, 0, 1, 1, 2 );
	layout->addWidget( labelGender, 1, 0 );
	layout->addWidget( genderCombobox, 1, 1 );
	layout->addWidget( labelSpecies, 2, 0 );
	layout->addWidget( speciesComboBox, 2, 1 );
	layout->addWidget( labelVirtue, 3, 0 );
	layout->addWidget( virtueCombobox, 3, 1 );
	layout->addWidget( labelVice, 4, 0 );
	layout->addWidget( viceCombobox, 4, 1 );
	layout->addWidget( labelBreed, 5, 0 );
	layout->addWidget( breedCombobox, 5, 1 );
	layout->addWidget( labelFaction, 6, 0 );
	layout->addWidget( factionCombobox, 6, 1 );

// 	connect(nameLineEdit, SIGNAL(textChanged(QString)), this, SLOT(modifyRealIdentity()));
	connect( namePushButton, SIGNAL( clicked( bool ) ), this, SLOT( openNameDialog() ) );
	connect( genderCombobox, SIGNAL( currentIndexChanged( int ) ), this, SLOT( changeGender( int ) ) );
	connect( virtueCombobox, SIGNAL( currentIndexChanged( int ) ), this, SLOT( changeVirtue( int ) ) );
	connect( viceCombobox, SIGNAL( currentIndexChanged( int ) ), this, SLOT( changeVice( int ) ) );
	connect( breedCombobox, SIGNAL( currentIndexChanged( int ) ), this, SLOT( changeBreed( int ) ) );
	connect( factionCombobox, SIGNAL( currentIndexChanged( int ) ), this, SLOT( changeFaction( int ) ) );
	connect( character, SIGNAL( realIdentityChanged( cv_Identity ) ), this, SLOT( updateIdentity( cv_Identity ) ) );
	connect( character, SIGNAL( virtueChanged( QString ) ), this, SLOT( updateVirtue( QString ) ) );
	connect( character, SIGNAL( viceChanged( QString ) ), this, SLOT( updateVice( QString ) ) );
	connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( updateBreedTitle( cv_Species::SpeciesFlag ) ) );
	connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( updateFactionTitle( cv_Species::SpeciesFlag ) ) );
	connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( updateBreedBox( cv_Species::SpeciesFlag ) ) );
	connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( updateFactionBox( cv_Species::SpeciesFlag ) ) );
	connect( character, SIGNAL( breedChanged( QString ) ), this, SLOT( updateBreed( QString ) ) );
	connect( character, SIGNAL( factionChanged( QString ) ), this, SLOT( updateFaction( QString ) ) );
}

InfoWidget::~InfoWidget() {
	delete genderCombobox;
	delete namePushButton;
	delete labelBreed;
	delete breedCombobox;
	delete labelFaction;
	delete factionCombobox;
	delete viceCombobox;
	delete virtueCombobox;
	delete labelName;
	delete speciesComboBox;
	delete layout;
	delete storage;
}

void InfoWidget::openNameDialog() {
	NameDialog* dialog = new NameDialog( this );
	dialog->exec();
	delete dialog;
}

void InfoWidget::changeGender( int gen ) {
	cv_Identity id = character->identities().at( 0 );

	if ( gen == 0 ) {
		id.gender = cv_Identity::Male;
	} else {
		id.gender = cv_Identity::Female;
	}

	character->setRealIdentity( id );
}

void InfoWidget::changeVirtue( int idx ) {
	character->setVirtue( virtueCombobox->currentText() );
}

void InfoWidget::changeVice( int idx ) {
	character->setVice( viceCombobox->currentText() );
}

void InfoWidget::changeBreed( int idx ) {
	character->setBreed( breedCombobox->currentText() );
}

void InfoWidget::changeFaction( int idx ) {
	character->setFaction( factionCombobox->currentText() );
}


void InfoWidget::updateIdentity( cv_Identity id ) {
// 	namePushButton->setText( cv_Name::displayNameDisplay( id.sureName, id.firstName(), id.nickName ) );

	QString nameText = "";

	if ( !id.sureName.isEmpty() || !id.foreNames.isEmpty() ) {
		nameText += cv_Name::displayNameFull( id.sureName, id.foreNames );
	}

	if ( !id.nickName.isEmpty() ) {
		if ( !nameText.isEmpty() ) {
			nameText += "\n";
		}

		nameText += cv_Name::displayNameDisplay( id.sureName, id.firstName(), id.nickName );
	}

	if ( !id.honorificName.isEmpty() ) {
		if ( !nameText.isEmpty() ) {
			nameText += "\n";
		}

		nameText += cv_Name::displayNameHonor( id.firstName(), id.honorificName );
	}

	if ( !id.supernaturalName.isEmpty() ) {
		if ( !nameText.isEmpty() ) {
			nameText += "\n";
		}

		nameText += id.supernaturalName;
	}

	labelName->setText( nameText );

	if ( id.gender == cv_Identity::Male ) {
		genderCombobox->setCurrentIndex( 0 );
	} else {
		genderCombobox->setCurrentIndex( 1 );
	}
}

void InfoWidget::updateVirtue( QString txt ) {
	virtueCombobox->setCurrentIndex( virtueCombobox->findText( txt ) );
}

void InfoWidget::updateVice( QString txt ) {
	viceCombobox->setCurrentIndex( viceCombobox->findText( txt ) );
}

void InfoWidget::updateBreed( QString txt ) {
	breedCombobox->setCurrentIndex( breedCombobox->findText( txt ) );
}

void InfoWidget::updateFaction( QString txt ) {
	factionCombobox->setCurrentIndex( factionCombobox->findText( txt ) );
}

void InfoWidget::updateBreedTitle( cv_Species::SpeciesFlag spe ) {
	labelBreed->setText( storage->breedTitle(spe)  + ":" );
}

void InfoWidget::updateFactionTitle( cv_Species::SpeciesFlag spe ) {
	labelFaction->setText( storage->factionTitle(spe)  + ":");
}

void InfoWidget::updateBreedBox( cv_Species::SpeciesFlag spe ) {
	breedCombobox->clear();
	breedCombobox->addItems( storage->breedNames( spe ) );
}

void InfoWidget::updateFactionBox( cv_Species::SpeciesFlag spe ) {
	factionCombobox->clear();
	factionCombobox->addItems( storage->factionNames( spe ) );
}
