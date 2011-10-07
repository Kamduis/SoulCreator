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

#include "Parser/StringBoolParser.h"
// #include "Exceptions/Exception.h"
#include "Widgets/Dialogs/MessageBox.h"

#include "CharaTrait.h"


CharaTrait::CharaTrait( QWidget* parent, Trait* trait, Trait* traitStorage ) : TraitLine( parent, trait->name(), trait->value() ) {
	// Vorsicht: Nullzeiger ist immer gefährlich!
	ptr_trait = 0;
	ptr_traitStorage = traitStorage;

	character = StorageCharacter::getInstance();

	setTraitPtr( trait );

	// Falls ich mit der Maus den Wert ändere, muß er auch entsprechend verändert werden.
	connect( this, SIGNAL( valueChanged( int ) ), this, SLOT( setTraitValue( int ) ) );
	connect( this, SIGNAL( textChanged( QString ) ), this, SLOT( setCustomText( QString ) ) );
	connect( this, SIGNAL( typeChanged( cv_AbstractTrait::Type ) ), this, SLOT( hideSpecialtyWidget( cv_AbstractTrait::Type ) ) );
	connect( this, SIGNAL( typeChanged( cv_AbstractTrait::Type ) ), this, SLOT( hideDescriptionWidget() ) );
	connect( this, SIGNAL( specialtiesClicked( bool ) ), this, SLOT( emitSpecialtiesClicked( bool ) ) );
	connect( traitPtr(), SIGNAL( detailsChanged(int)), this, SLOT( unclickButton( int ) ) );

	connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( hideTraitIfNotAvailable( cv_Species::SpeciesFlag ) ) );
	connect( traitPtr(), SIGNAL( valueChanged( int ) ), this, SLOT( setValue( int ) ) );

	// Die Signale hier zu verbinden funktioniert offensichtlich nicht. Vielleicht weil einige Fertigkeiten dann noch nicht existieren.
	connect( traitPtr(), SIGNAL( availabilityChanged(bool)), this, SLOT( setEnabled(bool)) );

	if ( !traitPtr()->possibleValues().isEmpty() ) {
		setPossibleValues( traitPtr()->possibleValues() );
	}

	hideSpecialtyWidget( trait->type() );
	hideDescriptionWidget();
}


Trait* CharaTrait::traitPtr() const {
	return ptr_trait;
}

void CharaTrait::setTraitPtr( Trait* trait ) {
	if ( ptr_trait != trait ) {
		ptr_trait = trait;
	}
}


// int CharaTrait2::value() const {
// 	return traitPtr()->value();
// }
// void CharaTrait2::setValue( int val ) {
// 	qDebug() << Q_FUNC_INFO << name() << val << value();
// 	if ( value() != val ) {
// 		TraitLine::setValue( val );
// 	}
// }

void CharaTrait::setTraitValue( int val ) {
// 	qDebug() << Q_FUNC_INFO << name() << val << value();
	if ( traitPtr()->value() != val ) {
		traitPtr()->setValue( val );
	}
}


QString CharaTrait::customText() const {
	return traitPtr()->customText();
}
void CharaTrait::setCustomText( QString txt ) {
	if ( traitPtr()->customText() != txt ) {
		traitPtr()->setCustomText( txt );

		TraitLine::setText( txt );

		emit traitChanged( traitPtr() );
	}
}


cv_AbstractTrait::Type CharaTrait::type() const {
	return ptr_trait->type();
}

void CharaTrait::setType( cv_AbstractTrait::Type type ) {
	if ( ptr_trait->type() != type ) {
		ptr_trait->setType( type );

		emit typeChanged( type );
		emit traitChanged( traitPtr() );
	}
}

cv_AbstractTrait::Category CharaTrait::category() const {
	return ptr_trait->category();
}

void CharaTrait::setCategory( cv_AbstractTrait::Category category ) {
	if ( ptr_trait->category() != category ) {
		ptr_trait->setCategory( category );

		emit traitChanged( traitPtr() );
	}
}

cv_Species::Species CharaTrait::species() const {
	return ptr_trait->species();
}

void CharaTrait::setSpecies( cv_Species::Species species ) {
	if ( ptr_trait->species() != species ) {
		ptr_trait->setSpecies( species );
// 		emit speciesChanged(species);

		emit traitChanged( traitPtr() );
	}
}


bool CharaTrait::custom() const {
	return ptr_trait->custom();
}

void CharaTrait::setCustom( bool sw ) {
	if ( ptr_trait->custom() != sw ) {
		ptr_trait->setCustom( sw );

		emit traitChanged( traitPtr() );
	}
}

void CharaTrait::hideSpecialtyWidget( cv_AbstractTrait::Type type ) {
	if ( type == cv_AbstractTrait::Skill ) {
		hideSpecialties( false );
	} else {
		hideSpecialties( true );
	}
}

void CharaTrait::hideDescriptionWidget() {
	if ( custom() ) {
		hideDescription( false );
	} else {
		hideDescription( true );
	}
}

void CharaTrait::emitSpecialtiesClicked( bool sw ) {
	if ( ptr_traitStorage != 0 ) {
		QList< cv_TraitDetail > listStora = ptr_traitStorage->details();
		QList< cv_TraitDetail > listChara = traitPtr()->details();

// 		qDebug() << Q_FUNC_INFO << traitPtr()->name() << ptr_traitStorage->name() << traitPtr()->details().count() << ptr_traitStorage->details().count();

		for ( int i = 0; i < listStora.count(); i++ ) {
			for ( int j = 0; j < listChara.count(); j++ ) {
				if ( listStora.at( i ).name == listChara.at( j ).name ) {
// 					qDebug() << Q_FUNC_INFO << sw << listStora.at( i ).name << listChara.at( j ).name << listChara.at( j ).value;
					cv_TraitDetail traitDetail = listChara.at( j );
					listStora.replace( i, traitDetail );
				}
			}
		}

		emit specialtiesClicked( sw, name(), listStora );
	}
}
void CharaTrait::unclickButton( int val )
{
// 	qDebug() << Q_FUNC_INFO << val;
	if (val < 1){
		setSpecialtyButtonChecked(false);
		emit specialtiesClicked( false, name(), ptr_traitStorage->details());
	}
}



void CharaTrait::hideTraitIfNotAvailable( cv_Species::SpeciesFlag sp ) {
	if ( species().testFlag( sp ) ) {
		setHidden( false );
	} else {
		setValue( 0 );
		setHidden( true );
	}
}

