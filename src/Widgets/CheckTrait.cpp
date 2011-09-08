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

#include "../Exceptions/Exception.h"

#include "CheckTrait.h"


CheckTrait::CheckTrait( QWidget* parent, cv_Trait* trait, cv_Trait* traitStorage ) : QWidget( parent ) {
	// Vorsicht: Nullzeiger ist immer gefährlich!
	ptr_trait = 0;
	ptr_traitStorage = traitStorage;

	character = StorageCharacter::getInstance();

	layout = new QHBoxLayout(this);
	setLayout(layout);
	
	checkBox = new QCheckBox(this);
	checkBox->setText(trait->name);

	lineEdit = new QLineEdit(this);
	
	layout->addWidget(checkBox);
	layout->addStretch();
	layout->addWidget(lineEdit);

	

// 	connect( this, SIGNAL( valueChanged( int ) ), this, SLOT( setValue( int ) ) );
// 	connect( this, SIGNAL( textChanged( QString ) ), this, SLOT( setCustomText( QString ) ) );
// 	connect( this, SIGNAL( typeChanged( cv_Trait::Type ) ), this, SLOT( hideSpecialtyWidget( cv_Trait::Type ) ) );
// 	connect( this, SIGNAL( typeChanged( cv_Trait::Type ) ), this, SLOT( hideDescriptionWidget() ) );
// 	connect( this, SIGNAL( specialtiesClicked( bool ) ), this, SLOT( emitSpecialtiesClicked( bool ) ) );
// 	connect( character, SIGNAL( traitChanged( cv_Trait* ) ), this, SLOT( updateWidget( cv_Trait* ) ) );
// 	connect( this, SIGNAL( traitChanged( cv_Trait* ) ), character, SIGNAL( traitChanged( cv_Trait* ) ) );
// 	connect( character, SIGNAL( traitChanged( cv_Trait* ) ), this, SLOT( checkTraitPrerequisites( cv_Trait* ) ) );
// 	connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( hideTraitIfNotAvailable( cv_Species::SpeciesFlag ) ) );

	setTraitPtr( trait );

	hideDescriptionWidget();
}
CheckTrait::~CheckTrait()
{
	delete checkBox;
}



cv_Trait* CheckTrait::traitPtr() const {
	return ptr_trait;
}

void CheckTrait::setTraitPtr( cv_Trait* trait ) {
	if ( ptr_trait != trait ) {
		ptr_trait = trait;
	}
}




int CheckTrait::value() const {
	return traitPtr()->value;
}
void CheckTrait::setValue( int val ) {
	if ( traitPtr()->value != val ) {
		traitPtr()->value = val;
// 		TraitLine::setValue( val );

		emit traitChanged( traitPtr() );
	}
}


QString CheckTrait::customText() const {
	return traitPtr()->customText;
}
void CheckTrait::setCustomText( QString txt ) {
	if ( traitPtr()->customText != txt ) {
		traitPtr()->customText = txt;
// 		TraitLine::setText( txt );

		emit traitChanged( traitPtr() );
	}
}


cv_Trait::Type CheckTrait::type() const {
	return ptr_trait->type;
}

void CheckTrait::setType( cv_Trait::Type type ) {
	if ( ptr_trait->type != type ) {
		ptr_trait->type = type;

		emit typeChanged( type );
		emit traitChanged( traitPtr() );
	}
}

cv_Trait::Category CheckTrait::category() const {
	return ptr_trait->category;
}

void CheckTrait::setCategory( cv_Trait::Category category ) {
	if ( ptr_trait->category != category ) {
		ptr_trait->category = category;

		emit traitChanged( traitPtr() );
	}
}

cv_Species::Species CheckTrait::species() const {
	return ptr_trait->species;
}

void CheckTrait::setSpecies( cv_Species::Species species ) {
	if ( ptr_trait->species != species ) {
		ptr_trait->species = species;
// 		emit speciesChanged(species);

		emit traitChanged( traitPtr() );
	}
}


bool CheckTrait::custom() const {
	return ptr_trait->custom;
}

void CheckTrait::setCustom( bool sw ) {
	if ( ptr_trait->custom != sw ) {
		ptr_trait->custom = sw;

		emit traitChanged( traitPtr() );
	}
}

void CheckTrait::hideDescriptionWidget() {
	if ( custom() ) {
		lineEdit->setHidden(false);
	} else {
		lineEdit->setHidden(true);
	}
}


void CheckTrait::hideTraitIfNotAvailable( cv_Species::SpeciesFlag sp ) {
	if ( species().testFlag( sp ) ) {
		setHidden( false );
	} else {
		setValue( 0 );
		setHidden( true );
	}
}




void CheckTrait::updateWidget( cv_Trait* trait ) {
	if ( traitPtr() == trait ) {
// 		TraitLine::setValue( value() );
// 		TraitLine::setText( customText() );
	}
}
