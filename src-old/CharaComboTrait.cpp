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

	// Ich muß die Verbindung zu \ref StorageCharacter lösen, welche von der Elternklasse erstellt wurde, damit ich jetzt mit customText arbeit kann und eine neue Verbindung aufbaue.
	qDebug() << Q_FUNC_INFO << disconnect( SIGNAL( valueChanged( int ) ) );

	// Da ich eine neue Version von setTrait in diesem Kind erzeuge, muß ich die Verbindung zur Funktion der Elternklasse lösen.
	qDebug() << Q_FUNC_INFO << disconnect( SIGNAL( traitChanged( cv_Trait ) ) );

	connect( this, SIGNAL( valueChanged( int ) ), this, SLOT( emitTraitChanged() ) );
	connect( this, SIGNAL( traitChanged( cv_Trait ) ), this, SLOT( setTrait(cv_Trait)) );
	connect( customBox, SIGNAL( editingFinished( ) ), this, SLOT( emitTraitChanged() ) );
	connect( this, SIGNAL( traitChanged( cv_Trait ) ), character, SLOT( addTrait( cv_Trait ) ) );
// 	connect( nameBox, SIGNAL( currentIndexChanged( int ) ), this, SLOT( enableWidgets( int ) ) );
	connect( nameBox, SIGNAL( currentIndexChanged( QString ) ), this, SLOT( changeParameters( QString ) ) );
	connect( nameBox, SIGNAL( currentIndexChanged( QString ) ), this, SIGNAL( nameChanged( QString ) ) );
}

CharaComboTrait::~CharaComboTrait() {
	delete storage;
	delete customBox;
	delete nameBox;
}

bool CharaComboTrait::custom() const {
	return v_custom;
}
void CharaComboTrait::setCustom( bool sw ) {
	if ( v_custom != sw ) {
		v_custom = sw;
	}
}

QString CharaComboTrait::customText() const {
	return customBox->text();
}

void CharaComboTrait::setTrait( cv_Trait trait ) {
	qDebug() << Q_FUNC_INFO << "HIER!";

	if ( type() == trait.type && category() == trait.category && name() == trait.name ) {
		if ( !trait.custom || (trait.custom && customText() == trait.customText) ) {
			setValue( trait.value );
		}
	}
}


void CharaComboTrait::emitTraitChanged() {
	cv_Trait trait;
	trait.type = type();
	trait.category = category();
	trait.name = name();
	trait.value = value();
	// Eigenschaften, die mit diesem Widget dargestellt werden, haben keinen erklärenden Text.
	trait.custom = custom();
	trait.customText = customText();

	// Eigenschaften, die einen besonderen text haben, werden nur dann in den Speicher übertragen, wenn dieser Text auch existiert.
	if ( !custom() || !customText().isEmpty() ) {
		qDebug() << Q_FUNC_INFO << custom() << customText();
		emit traitChanged( trait );
	}
}



void CharaComboTrait::addName( QString name ) {
	QStringList names;

	for ( int i = 0; i < nameBox->count(); i++ ) {
		names.append( nameBox->itemText( i ) );
	}

	if ( !names.contains( name ) ) {
		nameBox->addItem( name );
	}
}

void CharaComboTrait::removeName( QString name ) {
	nameBox->removeItem( nameBox->findText( name ) );
}


// void CharaComboTrait::enableWidgets( int index ) {
// 	qDebug() << Q_FUNC_INFO << "Momentan hat diese Funktion keinerlei Effekt!";
// }


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
					setCustom( storage->traits( types.at( i ), categories.at( j ) ).at( k ).custom );

					// Wenn die Eigenschaft zusätzlichen erklärenden Text beinhalten kann, muß das Textfeld auch angezeigt werden.
					if ( custom() ) {
						customBox->setHidden( false );
					} else {
						customBox->setHidden( true );
					}

// 					cv_Trait trait = storage->traits( types.at( i ), categories.at( j ) ).at( k );
// 					trait.value = value();
// // 					trait.details.clear();
//
// 					emit traitChanged( trait );
				}
			}
		}
	}
}

