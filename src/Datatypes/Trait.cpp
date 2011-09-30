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

#include "Trait.h"


Trait::Trait( QString txt, int val, cv_Species::Species spe, cv_AbstractTrait::Type ty, cv_AbstractTrait::Category ca, QObject* parent ) : QObject( parent ), cv_Trait( txt, val, spe, ty, ca ) {
	construct();
}

Trait::Trait( cv_Trait trait, QObject* parent ) : QObject( parent ), cv_Trait( trait.name(), trait.value(), trait.species(), trait.type(), trait.category() ) {
	construct();

	setEra( trait.era() );
	setAge( trait.age() );
	setPrerequisites( trait.prerequisites() );
	setCustom( trait.custom() );
	setCustomText( trait.customText() );
	setDetails( trait.details() );
	setPossibleValues( trait.possibleValues() );
}

Trait::Trait( Trait* trait, QObject* parent ) : QObject( parent ), cv_Trait( trait->name(), trait->value(), trait->species(), trait->type(), trait->category() ) {
	construct();

	setEra( trait->era() );
	setAge( trait->age() );
	setPrerequisites( trait->prerequisites() );
	setCustom( trait->custom() );
	setCustomText( trait->customText() );
	setDetails( trait->details() );
	setPossibleValues( trait->possibleValues() );
}

void Trait::construct() {
	connect( this, SIGNAL( valueChanged( int ) ), this, SLOT( emitTraitChanged() ) );
	connect( this, SIGNAL( detailsChanged() ), this, SLOT( emitTraitChanged() ) );
}



void Trait::setValue( int val ) {
// 	qDebug() << Q_FUNC_INFO << name() << val << value();
	if ( value() != val ) {
		cv_Trait::setValue( val );

		emit valueChanged( val );
	}
}

void Trait::setDetails( QList< cv_TraitDetail > list ) {
	if ( details() != list ) {
		cv_Trait::setDetails( list );

		emit detailsChanged();
	}
}
void Trait::addDetail( cv_TraitDetail det ) {
	if ( !details().contains( det ) ) {
		cv_Trait::addDetail( det );

		emit detailsChanged();
	}
}
void Trait::clearDetails() {
	if ( !details().isEmpty() ) {
		cv_Trait::clearDetails();

		emit detailsChanged();
	}
}

void Trait::setType( cv_AbstractTrait::Type typ ) {
	if ( type() != typ ) {
		cv_AbstractTrait::setType( typ );

		emit typeChanged( typ );
	}
}




void Trait::emitTraitChanged() {
	emit traitChanged( this );
}
