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
#include <QStringList>
#include <QDebug>

#include "../../Datatypes/cv_Identity.h"
#include "../../Exceptions/Exception.h"

#include "NameDialog.h"
#include "ui_NameDialog.h"


NameDialog::NameDialog( QWidget *parent ) : QDialog( parent ), ui( new Ui::NameDialog )  {
	ui->setupUi( this );

	character = StorageCharacter::getInstance();

	connect( ui->lineEdit_firstName, SIGNAL( textChanged( QString ) ), this, SLOT( showNames() ) );
	connect( ui->lineEdit_additionalForenames, SIGNAL( textChanged( QString ) ), this, SLOT( showNames() ) );
	connect( ui->lineEdit_surename, SIGNAL( textChanged( QString ) ), this, SLOT( showNames() ) );
	connect( ui->lineEdit_honorificName, SIGNAL( textChanged( QString ) ), this, SLOT( showNames() ) );
	connect( ui->lineEdit_nickname, SIGNAL( textChanged( QString ) ), this, SLOT( showNames() ) );
	connect( ui->lineEdit_specialName, SIGNAL( textChanged( QString ) ), this, SLOT( showNames() ) );
	connect( ui->buttonBox, SIGNAL( accepted() ), this, SLOT( saveNames() ) );
	connect( ui->buttonBox, SIGNAL( rejected() ), this, SLOT( reject() ) );

	// Der Erste Name in der Liste ist der firstName() und damit schon abgehandelt.
	QString foreNames;
	for ( int i = 1; i < character->identities().at( 0 ).foreNames.count();i++ ) {
		foreNames.append( character->identities().at( 0 ).foreNames.at( i ) );
		if ( i < character->identities().at( 0 ).foreNames.count() - 1 ) {
			foreNames.append( " " );
		}
	}

	ui->lineEdit_firstName->setText( character->identities().at( 0 ).firstName() );
	ui->lineEdit_additionalForenames->setText( foreNames );
	ui->lineEdit_surename->setText( character->identities().at( 0 ).sureName );
	ui->lineEdit_honorificName->setText( character->identities().at( 0 ).honorificName );
	ui->lineEdit_nickname->setText( character->identities().at( 0 ).nickName );
	ui->lineEdit_specialName->setText( character->identities().at( 0 ).supernaturalName );

	showNames();
}

NameDialog::~NameDialog() {
}


void NameDialog::showNames() {
	QStringList forenames = ui->lineEdit_additionalForenames->text().split( " " );
	forenames.insert( 0, ui->lineEdit_firstName->text() );

	ui->label_displayFull->setText( cv_Name::displayNameFull( ui->lineEdit_surename->text(), forenames ) );
	ui->label_displayDisplay->setText( cv_Name::displayNameDisplay( ui->lineEdit_surename->text(), ui->lineEdit_firstName->text(), ui->lineEdit_nickname->text() ) );
	ui->label_displayHonorific->setText( cv_Name::displayNameHonor(ui->lineEdit_firstName->text(), ui->lineEdit_honorificName->text() ) );
	ui->label_displaySuper->setText( ui->lineEdit_specialName->text() );
}

void NameDialog::saveNames() {
	character->realIdentity->foreNames.clear();

	QString foreNames = ui->lineEdit_additionalForenames->text();
	QStringList foreNameList;
	if ( !foreNames.isEmpty() ) {
		foreNameList = foreNames.split( " " );
	}

	foreNameList.insert( 0, ui->lineEdit_firstName->text() );

	cv_Identity id;
	id.foreNames = foreNameList;
	id.sureName = ui->lineEdit_surename->text();
	id.honorificName = ui->lineEdit_honorificName->text();
	id.nickName = ui->lineEdit_nickname->text();
	id.supernaturalName = ui->lineEdit_specialName->text();

	character->setRealIdentity( id );

	accept();
}

