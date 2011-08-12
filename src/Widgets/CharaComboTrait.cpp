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

#include <QDebug>

// #include "Storage.h"

#include "CharaComboTrait.h"


CharaComboTrait::CharaComboTrait( QWidget* parent, cv_Trait::Type type, int value ) : CharaTrait( parent, type, cv_Trait::CategoryNo, "", value ) {
	character = StorageCharacter::getInstance();

	nameBox = new QComboBox( this );
	nameBox->setInsertPolicy( QComboBox::InsertAlphabetically );
	nameBox->addItem( "" );
	customBox = new QLineEdit( this );
	customBox->setHidden( true );

	storage = new StorageTemplate( this );

	layout()->insertWidget( 0, nameBox );
	layout()->insertWidget( 1, customBox );
	labelName()->setHidden( true );

	connect( nameBox, SIGNAL( currentIndexChanged( int ) ), this, SLOT( enableWidget( int ) ) );
	connect( nameBox, SIGNAL( currentIndexChanged( QString ) ), this, SLOT( changeParameters( QString ) ) );
	connect( customBox, SIGNAL( editingFinished( ) ), this, SLOT( changeCustomText( ) ) );
}

CharaComboTrait::~CharaComboTrait() {
	delete storage;
	delete customBox;
	delete nameBox;
}

void CharaComboTrait::addName( QString name ) {
	nameBox->addItem( name );
}

void CharaComboTrait::enableWidgets( int index ) {
	qDebug() << Q_FUNC_INFO << "Momentan hat diese Funktion keinerlei Effekt!";
}


void CharaComboTrait::changeParameters( QString name ) {
	setName( name );

	QList< cv_Trait::Type > types;
	types.append( cv_Trait::Merit );
	types.append( cv_Trait::Power );

	QList< cv_Trait::Category > categories;
	categories.append( cv_Trait::Mental );
	categories.append( cv_Trait::Physical );
	categories.append( cv_Trait::Social );

	for ( int i = 0; i < types.count(); i++ ) {
		for ( int j = 0; j < categories.count(); j++ ) {
			for ( int k = 0; k < storage->traits( types.at( i ), categories.at( j ) ).count(); k++ ) {
				if ( name == storage->traits( types.at( i ), categories.at( j ) ).at( k ).name ) {
					setType( storage->traits( types.at( i ), categories.at( j ) ).at( k ).type );
					setCategory( storage->traits( types.at( i ), categories.at( j ) ).at( k ).category );

					// Wenn die Eigenschaft zusätzlichen erklärenden Text beinhalten kann, muß das Textfeld auch angezeigt werden.
					if ( storage->traits( types.at( i ), categories.at( j ) ).at( k ).custom ) {
						customBox->setHidden( false );
					} else {
						customBox->setHidden( true );
					}
				}
			}
		}
	}
}

void CharaComboTrait::changeCustomText( ) {
	QList< cv_Trait::Type > types;
	types.append( cv_Trait::Merit );
	types.append( cv_Trait::Power );

	QList< cv_Trait::Category > categories;
	categories.append( cv_Trait::Mental );
	categories.append( cv_Trait::Physical );
	categories.append( cv_Trait::Social );

	for ( int i = 0; i < types.count(); i++ ) {
		for ( int j = 0; j < categories.count(); j++ ) {
			for ( int k = 0; k < storage->traits( types.at( i ), categories.at( j ) ).count(); k++ ) {
				if ( name() == storage->traits( types.at( i ), categories.at( j ) ).at( k ).name && storage->traits( types.at( i ), categories.at( j ) ).at( k ).custom ) {
					// Eigenschaft aus Vorlage übernehmen und dann entsprechend des Widgets abändern.
					cv_Trait trait = storage->traits( types.at( i ), categories.at( j ) ).at( k );
					trait.customText = customBox->text();
					trait.value = value();
					character->addTrait( trait );
				}
			}
		}
	}
}

