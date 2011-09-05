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

#include "../Parser/StringBoolParser.h"
#include "../Exceptions/Exception.h"
#include "Dialogs/MessageBox.h"

#include "CharaTrait2.h"


CharaTrait2::CharaTrait2( QWidget* parent, cv_Trait* trait ) : TraitLine( parent, trait->name, trait->value ) {
	// Vorsicht: Nullzeiger ist immer gefährlich!
	ptr_trait = 0;

	character = StorageCharacter::getInstance();

	connect( this, SIGNAL( valueChanged( int ) ), this, SLOT( setValue( int ) ) );
	connect( character, SIGNAL( traitChanged( cv_Trait* ) ), this, SLOT( updateWidget() ) );

	setTraitPtr( trait );
}


cv_Trait* CharaTrait2::traitPtr() const {
	return ptr_trait;
}

void CharaTrait2::setTraitPtr( cv_Trait* trait ) {
	if ( ptr_trait != trait ) {
		ptr_trait = trait;
	}
}




int CharaTrait2::value() const {
	return traitPtr()->value;
}
void CharaTrait2::setValue( int value )
{
	if ( traitPtr()->value != value ) {
		traitPtr()->value = value;
	}
}


cv_Trait::Type CharaTrait2::type() const {
	return ptr_trait->type;
}

void CharaTrait2::setType( cv_Trait::Type type ) {
	if ( ptr_trait->type != type ) {
		ptr_trait->type = type;
	}
}

cv_Trait::Category CharaTrait2::category() const {
	return ptr_trait->category;
}

void CharaTrait2::setCategory( cv_Trait::Category category ) {
	if ( ptr_trait->category != category ) {
		ptr_trait->category = category;
	}
}

cv_Species::Species CharaTrait2::species() const {
	return ptr_trait->species;
}

void CharaTrait2::setSpecies( cv_Species::Species species ) {
	if ( ptr_trait->species != species ) {
		ptr_trait->species = species;
// 		emit speciesChanged(species);
	}
}


bool CharaTrait2::custom() const {
	return ptr_trait->custom;
}

void CharaTrait2::setCustom( bool sw ) {
	if ( ptr_trait->custom != sw ) {
		ptr_trait->custom = sw;
	}
}


void CharaTrait2::addSpecialty( cv_TraitDetail specialty ) {
	ptr_trait->details.append( specialty );
}



void CharaTrait2::updateWidget() {
	update();
}
