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

#include <QDebug>

#include "Exceptions/Exception.h"
#include "Config/Config.h"

#include "CheckTrait2.h"


CheckTrait2::CheckTrait2( QWidget* parent, Trait* trait, Trait* traitStorage ) : QWidget( parent ) {
	// Vorsicht: Nullzeiger ist immer gefährlich!
	ptr_trait = 0;
	ptr_traitStorage = traitStorage;

	character = StorageCharacter::getInstance();

	layout = new QHBoxLayout( this );
	setLayout( layout );

	checkBox = new QCheckBox( this );
	checkBox->setText( trait->name() );
	checkBox->setMaximumHeight(Config::inlineWidgetHeightMax);

	lineEdit = new QLineEdit( this );
	lineEdit->setMinimumWidth(Config::traitCustomTextWidthMin);
	lineEdit->setMaximumHeight(Config::inlineWidgetHeightMax);

	layout->addWidget( checkBox );
	layout->addStretch();
	layout->addWidget( lineEdit );

	setTraitPtr( trait );

	connect( checkBox, SIGNAL( stateChanged( int ) ), this, SLOT( setValue( int ) ) );
	connect( lineEdit, SIGNAL( textChanged( QString ) ), this, SLOT( setCustomText( QString ) ) );
	connect( traitPtr(), SIGNAL( typeChanged( cv_Trait::Type ) ), this, SLOT( hideDescriptionWidget() ) );
	connect( checkBox, SIGNAL( stateChanged( int ) ), this, SIGNAL( stateChanged( int ) ) );
	connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( hideTraitIfNotAvailable( cv_Species::SpeciesFlag ) ) );

	hideDescriptionWidget();
}

CheckTrait2::~CheckTrait2() {
	delete checkBox;
}



Trait* CheckTrait2::traitPtr() const {
	return ptr_trait;
}

void CheckTrait2::setTraitPtr( Trait* trait ) {
	if ( ptr_trait != trait ) {
		ptr_trait = trait;
	}
}




int CheckTrait2::value() const {
	return checkBox->checkState();
}
void CheckTrait2::setValue( int val ) {
	if ( traitPtr()->value() != val ) {
		traitPtr()->setValue( val );
	}
}


QString CheckTrait2::customText() const {
	return traitPtr()->customText();
}

void CheckTrait2::setCustomText( QString txt ) {
	if ( traitPtr()->customText() != txt ) {
		traitPtr()->setCustomText( txt );
	}
}


cv_Trait::Type CheckTrait2::type() const {
	return ptr_trait->type();
}

void CheckTrait2::setType( cv_Trait::Type type ) {
	if ( ptr_trait->type() != type ) {
		ptr_trait->setType(type);
	}
}

cv_Trait::Category CheckTrait2::category() const {
	return ptr_trait->category();
}

void CheckTrait2::setCategory( cv_Trait::Category category ) {
	if ( ptr_trait->category() != category ) {
		ptr_trait->setCategory(category);
	}
}

cv_Species::Species CheckTrait2::species() const {
	return ptr_trait->species();
}

void CheckTrait2::setSpecies( cv_Species::Species species ) {
	if ( ptr_trait->species() != species ) {
		ptr_trait->setSpecies(species);
	}
}


bool CheckTrait2::custom() const {
	return ptr_trait->custom();
}

void CheckTrait2::setCustom( bool sw ) {
	if ( ptr_trait->custom() != sw ) {
		ptr_trait->setCustom(sw);
	}
}

void CheckTrait2::hideDescriptionWidget() {
	if ( custom() ) {
		lineEdit->setHidden( false );
	} else {
		lineEdit->setHidden( true );
	}
}


void CheckTrait2::hideTraitIfNotAvailable( cv_Species::SpeciesFlag sp ) {
	if ( species().testFlag( sp ) ) {
		setHidden( false );
	} else {
		setValue( 0 );
		setHidden( true );
	}
}
