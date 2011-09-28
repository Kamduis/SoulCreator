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


#include "Exceptions/Exception.h"

#include "Trait.h"


Trait::Trait( QString txt, int val, cv_Species::Species spe, cv_AbstractTrait::Type ty, cv_AbstractTrait::Category ca, QObject* parent ) : QObject(parent), cv_Trait( txt, val, spe, ty, ca ) {
}

Trait::Trait( cv_Trait trait, QObject* parent ): QObject(parent), cv_Trait( trait.v_name, trait.value(), trait.v_species, trait.v_type, trait.v_category ) {
	v_era = trait.v_era;
	v_age = trait.v_age;
	v_prerequisites = trait.v_prerequisites;
	v_custom = trait.v_custom;
	v_customText = trait.v_customText;
}

Trait::Trait( Trait* trait, QObject* parent ): QObject( parent ), cv_Trait( trait->v_name, trait->value(), trait->v_species, trait->v_type, trait->v_category ) {
	v_era = trait->v_era;
	v_age = trait->v_age;
	v_prerequisites = trait->v_prerequisites;
	v_custom = trait->v_custom;
	v_customText = trait->v_customText;
}


void Trait::setValue( int val ) {
	if ( value() != val){
		cv_Trait::setValue( val );
		emit valueChanged( val );
	}
}
