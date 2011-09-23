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


#include "Exceptions/Exception.h"

#include "cv_Trait.h"


cv_Trait::cv_Trait( QString txt, int val, cv_Species::Species spe, cv_AbstractTrait::Type ty, cv_AbstractTrait::Category ca ) : cv_AbstractTrait( txt, spe, ty, ca ) {
	value = val;
	era = cv_Trait::EraNo;
	age = cv_Trait::AgeNo;
// 	details;
	prerequisites = "";
	custom = false;
	customText = "";
}



cv_Trait::Era cv_Trait::toEra( QString str ) {
	if ( str == "Modern" )
		return cv_Trait::Modern;
	else if ( str == "Reason" )
		return cv_Trait::Reason;
	else if ( str == "Antique" )
		return cv_Trait::Antique;
	else
		return cv_Trait::EraAll;
}

cv_Trait::Age cv_Trait::toAge( QString str ) {
	if ( str == "Adult" )
		return cv_Trait::Adult;
	else if ( str == "Kid" )
		return cv_Trait::Kid;
	else
		return cv_Trait::AgeAll;
}


bool cv_Trait::operator==( const cv_Trait& trait ) const {
	if ( this == &trait ) {
		return true;
	}

	bool result = name == trait.name
				  && value == trait.value
				  && type == trait.type
				  && category == trait.category
				  && species == trait.species
				  && era == trait.era
				  && age == trait.age
				  && details == trait.details
				  && prerequisites == trait.prerequisites
				  && custom == trait.custom;

	return result;
}

bool cv_Trait::operator<( const cv_Trait& trait ) const {
	if ( this == &trait ) {
		return false;
	}

	bool result = value < trait.value;
}
