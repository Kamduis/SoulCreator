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


#include "Config/Config.h"
#include "Exceptions/Exception.h"

#include "cv_CreationPoints.h"


const int cv_CreationPoints::creationPointsAttA = 5;
const int cv_CreationPoints::creationPointsAttB = 4;
const int cv_CreationPoints::creationPointsAttC = 3;
const int cv_CreationPoints::creationPointsSkillA = 11;
const int cv_CreationPoints::creationPointsSkillB = 7;
const int cv_CreationPoints::creationPointsSkillC = 5;
const int cv_CreationPoints::creationPointsSkillSpecialties = 3;
const int cv_CreationPoints::creationPointsMerits = 7;
const int cv_CreationPoints::creationPointsPowersVampire = 3;


cv_CreationPoints::cv_CreationPoints() {
	attributesA = cv_CreationPoints::creationPointsAttA;
	attributesB = cv_CreationPoints::creationPointsAttB;
	attributesC = cv_CreationPoints::creationPointsAttC;
	skillsA = cv_CreationPoints::creationPointsSkillA;
	skillsB = cv_CreationPoints::creationPointsSkillA;
	skillsC = cv_CreationPoints::creationPointsSkillA;
	skillSpecialties = cv_CreationPoints::creationPointsSkillSpecialties;
	merits = cv_CreationPoints::creationPointsMerits;
	powers = 0;
}


QString cv_CreationPoints::outputPoint( int val ) {
	if ( val < 0 ) {
		return "<font color='red'>" + QString::number( val ) + "</font>";
	}
	return QString::number(val);
}



QString cv_CreationPoints::attributesOut() {
	return outputPoint( attributesA ) + "/" + outputPoint( attributesB ) + "/" + outputPoint( attributesC );
}

QString cv_CreationPoints::skillsOut() {
	return outputPoint( skillsA ) + "/" + outputPoint( skillsB ) + "/" + outputPoint( skillsC );
}

QString cv_CreationPoints::meritsOut() {
	return outputPoint( merits );
}

QString cv_CreationPoints::powersOut() {
	return outputPoint( powers );
}


bool cv_CreationPoints::operator==( const cv_CreationPoints& points ) const {
	if ( this == &points ) {
		return true;
	}

	bool result = attributesA == points.attributesA &&

				  attributesB == points.attributesB &&
				  attributesC == points.attributesC &&
				  skillsA == points.skillsA &&
				  skillsB == points.skillsB &&
				  skillsC == points.skillsC &&
				  skillSpecialties == points.skillSpecialties &&
				  merits == points.merits &&
				  powers == points.powers;

	return result;
}

bool cv_CreationPoints::operator!=( const cv_CreationPoints& points ) const {
	if ( this == &points ) {
		return false;
	}

	bool result = attributesA != points.attributesA ||

				  attributesB != points.attributesB ||
				  attributesC != points.attributesC ||
				  skillsA != points.skillsA ||
				  skillsB != points.skillsB ||
				  skillsC != points.skillsC ||
				  skillSpecialties != points.skillSpecialties ||
				  merits != points.merits ||
				  powers != points.powers;

	return result;
}

