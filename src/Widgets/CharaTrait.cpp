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

#include "CharaTrait.h"


CharaTrait::CharaTrait( QWidget* parent, cv_Trait::Type type, cv_Trait::Category category, QString name, int value ) : TraitLine( parent, name, value ) {
	character = StorageCharacter::getInstance();

	connect( this, SIGNAL( valueChanged( int ) ), this, SLOT( emitValueChanged( int ) ) );
// 	connect( this, SIGNAL( valueChanged( cv_Trait ) ), character, SLOT( addTrait( cv_Trait ) ) );
	connect( this, SIGNAL( typeChanged( cv_Trait::Type ) ), this, SLOT( hideSpecialtyWidget( cv_Trait::Type ) ) );
	connect( this, SIGNAL( specialtiesClicked( bool ) ), this, SLOT( emitSpecialtiesClicked( bool ) ) );
	// Änderungen am Charakter im Speicher müssen dieses Widget aber auch aktualisieren.
	connect( character, SIGNAL( traitChanged( cv_Trait ) ), this, SLOT( setTrait( cv_Trait ) ) );

	// Damit die Schaltfläche für die Spezialisierungen verborgen wird, wenn sie nicht nötig ist.
// 	hideSpecialtyWidget(cv_Trait::Skill);
	setType( type );
	setCategory( category );
}


cv_Trait::Type CharaTrait::type() const {
	return v_type;
}

void CharaTrait::setType( cv_Trait::Type type ) {
	if ( v_type != type ) {
		v_type = type;

		emit typeChanged( type );
	}
}

cv_Trait::Category CharaTrait::category() const {
	return v_category;
}

void CharaTrait::setCategory( cv_Trait::Category category ) {
	if ( v_category != category ) {
		v_category = category;
	}
}


void CharaTrait::addSpecialty( cv_TraitDetail specialty ) {
	v_specialties.append( specialty );
}



void CharaTrait::hideSpecialtyWidget( cv_Trait::Type type ) {
	if ( type == cv_Trait::Skill ) {
		hideSpecialties( false );
	} else {
		hideSpecialties( true );
	}
}

void CharaTrait::setTrait( cv_Trait trait ) {
	if ( type() == trait.type && category() == trait.category && name() == trait.name ) {
		setValue( trait.value );
	}
}






void CharaTrait::emitValueChanged( int value ) {
	cv_Trait trait;
	trait.type = type();
	trait.category = category();
	trait.name = name();
	trait.value = value;
	// Eigenschaften, die mit diesem Widget dargestellt werden, haben keinen erklärenden Text.
	trait.custom = false;
	
	emit traitChanged( trait );
}

void CharaTrait::emitSpecialtiesClicked( bool sw ) {
	QList< cv_TraitDetail > list = v_specialties;

	for ( int i = 0; i < list.count(); i++ ) {
		for ( int j = 0; j < character->traits( type(), category() ).count(); j++ ) {
			for ( int k = 0; k < character->traits( type(), category() ).at( j ).details.count(); k++ ) {
				if ( list.at( i ).name == character->traits( type(), category() ).at( j ).details.at( k ).name ) {
					cv_TraitDetail detail = list.at( i );
					detail.value = true;
					list.replace( i, detail );
				}
			}
		}
		qDebug() << Q_FUNC_INFO << list.at( i ).name << list.at( i ).value;
	}

	emit specialtiesClicked( sw, name(), list );
}

