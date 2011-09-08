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
 * along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <QGridLayout>
#include <QLabel>
#include <QDebug>

#include "../Exceptions/Exception.h"
#include "../Config/Config.h"

#include "InfoWidget.h"


InfoWidget::InfoWidget( QWidget *parent ) : QWidget( parent )  {
	character = StorageCharacter::getInstance();
	
	layout = new QGridLayout( this );
	setLayout( layout );

	QLabel* labelName = new QLabel( tr( "Name:" ) );
	nameLineEdit = new QLineEdit( this );

	QLabel* labelGender = new QLabel( tr( "Gender:" ) );
	speciesComboBox = new CharaSpecies( this );

	QLabel* labelSpecies = new QLabel( tr( "Species:" ) );
	genderCombobox = new QComboBox( this );

	QLabel* labelVirtue = new QLabel( tr( "Virtue:" ) );
	virtueCombobox = new QComboBox( this );

	QLabel* labelVice = new QLabel( tr( "Vice:" ) );
	viceCombobox = new QComboBox( this );

	QLabel* labelBreed = new QLabel( tr( "Breed:" ) );
	breedCombobox = new QComboBox( this );

	QLabel* labelFaction = new QLabel( tr( "Faction:" ) );
	factionCombobox = new QComboBox( this );

	layout->addWidget( labelName, 0, 0 );
	layout->addWidget( nameLineEdit, 0, 1 );
	layout->addWidget( labelGender, 0, 2 );
	layout->addWidget( genderCombobox, 0, 3 );
	layout->addWidget( labelSpecies, 0, 4 );
	layout->addWidget( speciesComboBox, 0, 5 );
	layout->addWidget( labelVirtue, 1, 0 );
	layout->addWidget( virtueCombobox, 1, 1 );
	layout->addWidget( labelBreed, 1, 2 );
	layout->addWidget( breedCombobox, 1, 3 );
	layout->addWidget( labelVice, 2, 0 );
	layout->addWidget( viceCombobox, 2, 1 );
	layout->addWidget( labelFaction, 2, 2 );
	layout->addWidget( factionCombobox, 2, 3 );

	connect(nameLineEdit, SIGNAL(textChanged(QString)), this, SLOT(modifyRealIdentity()));
	connect(character, SIGNAL(identityChanged(cv_Identity)), this, SLOT(updateIdentity(cv_Identity)));
}

InfoWidget::~InfoWidget() {
	delete genderCombobox;
	delete nameLineEdit;
	delete speciesComboBox;
	delete layout;
}

void InfoWidget::modifyRealIdentity() {
	character->realIdentity->foreName[0] = nameLineEdit->text();

	qDebug() << Q_FUNC_INFO << character->identities().realName();
}

void InfoWidget::updateIdentity( cv_Identity )
{
	QString txt = character->identities().realName();
	int doubleSpaceIndex = txt.indexOf("  ");
	txt.truncate(doubleSpaceIndex);
	
	nameLineEdit->setText(txt);
}

