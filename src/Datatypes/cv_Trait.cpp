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


#include "../Exceptions/Exception.h"

#include "cv_Trait.h"


QString cv_Trait::toString( cv_Trait::Type type ) {
	switch ( type ) {
		case cv_Trait::TypeNo:
			return "TypeNo";
		case cv_Trait::Virtue:
			return "Virtue";
		case cv_Trait::Vice:
			return "Vice";
		case cv_Trait::Attribute:
			return "Attribute";
		case cv_Trait::Skill:
			return "Skill";
		case cv_Trait::Merit:
			return "Merit";
		default:
			throw eTraitType( type );
// 			return "ERROR";
	}
}

QString cv_Trait::toString( cv_Trait::Category category ) {
	switch ( category ) {
		case cv_Trait::CategoryNo:
			return "CategoryNo";
		case cv_Trait::Mental:
			return "Mental";
		case cv_Trait::Physical:
			return "Physical";
		case cv_Trait::Social:
			return "Social";
		default:
			throw eTraitCategory( category );
// 			return "ERROR";
	}
}

cv_Trait::Category cv_Trait::toCategory( QString str ) {
	if ( str == "Mental" )
		return cv_Trait::Mental;
	else if ( str == "Physical" )
		return cv_Trait::Physical;
	else if ( str == "Social" )
		return cv_Trait::Social;
	else
		return cv_Trait::CategoryNo;
}

cv_Trait::Type cv_Trait::toType( QString str ) {
	if ( str == "Virtue" )
		return cv_Trait::Virtue;
	else if ( str == "Vice" )
		return cv_Trait::Vice;
	else if ( str == "Attribute" )
		return cv_Trait::Attribute;
	else if ( str == "Skill" )
		return cv_Trait::Skill;
	else if ( str == "Merit" )
		return cv_Trait::Merit;
	else if ( str == "Morale" )
		return cv_Trait::Morale;
	else if ( str == "Super" )
		return cv_Trait::Super;
	else if ( str == "Power" )
		return cv_Trait::Power;
	else
		return cv_Trait::TypeNo;
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
