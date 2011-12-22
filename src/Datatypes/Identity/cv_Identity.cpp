/**
 * \file
 * \author Victor von Rhein <victor@caern.de>
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

#include "cv_Identity.h"


cv_Identity::cv_Identity( QString surename, QString firstname, cv_Identity::Gender gen ): cv_Name( surename, firstname ) {
	gender = gen;
}


QString cv_Identity::toXmlString( cv_Identity::Gender gen ) {
	switch ( gen ) {
		case cv_Identity::GenderNo:
			return "GenderNo";
		case cv_Identity::Male:
			return "Male";
		case cv_Identity::Female:
			return "Female";
		default:
			throw eGenderNotExisting( gen );
// 			return "ERROR";
	}
}

QString cv_Identity::toString( cv_Identity::Gender gen ) {
	switch ( gen ) {
		case cv_Identity::GenderNo:
			return QObject::tr( "GenderNo" );
		case cv_Identity::Male:
			return QObject::tr( "Male" );
		case cv_Identity::Female:
			return QObject::tr( "Female" );
		default:
			throw eGenderNotExisting( gen );
// 			return "ERROR";
	}
}

cv_Identity::Gender cv_Identity::toGender( QString text ) {
	if ( text == "Male" )
		return cv_Identity::Male;
	else if ( text == "Female" )
		return cv_Identity::Female;
	else
		return cv_Identity::GenderNo;
}
