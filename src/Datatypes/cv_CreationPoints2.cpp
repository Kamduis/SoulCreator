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


#include "Config/Config.h"
#include "Exceptions/Exception.h"

#include "cv_CreationPoints2.h"


cv_CreationPoints2::cv_CreationPoints2() {
	attributes = QList<int>();
	skills = QList<int>();
	skillSpecialties = 0;
	merits = 0;
	powers = 0;
}


QString cv_CreationPoints2::outputPoint( int val ) {
	if ( val < 0 ) {
		return "<font color='red'>" + QString::number( val ) + "</font>";
	}
	return QString::number( val );
}


QString cv_CreationPoints2::attributesOut() {
	QStringList resultList;

	for ( int i = 0; i < attributes.count(); i++ ) {
		resultList.append( outputPoint( attributes.at( i ) ) );
	}

	return resultList.join( "/" );
}

QString cv_CreationPoints2::skillsOut() {
	QStringList resultList;

	for ( int i = 0; i < skills.count(); i++ ) {
		resultList.append( outputPoint( skills.at( i ) ) );
	}

	return resultList.join( "/" );
}

QString cv_CreationPoints2::skillSpecialtiesOut() {
	return outputPoint( skillSpecialties );
}

QString cv_CreationPoints2::meritsOut() {
	return outputPoint( merits );
}

QString cv_CreationPoints2::powersOut() {
	return outputPoint( powers );
}


bool cv_CreationPoints2::operator==( const cv_CreationPoints2& points ) const {
	if ( this == &points ) {
		return true;
	}

	bool result = species == points.species &&
				  attributes == points.attributes &&
				  skills == points.skills &&
				  skillSpecialties == points.skillSpecialties &&
				  merits == points.merits &&
				  powers == points.powers;

	return result;
}

bool cv_CreationPoints2::operator!=( const cv_CreationPoints2& points ) const {
	if ( this == &points ) {
		return false;
	}

	bool result = species != points.species ||
				  attributes != points.attributes ||
				  skills != points.skills ||
				  skillSpecialties != points.skillSpecialties ||
				  merits != points.merits ||
				  powers != points.powers;

	return result;
}
