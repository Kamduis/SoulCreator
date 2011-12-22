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


#include <QDebug>

// #include "Exceptions/Exception.h"

#include "cv_Trait.h"


cv_Trait::cv_Trait( QString txt, int val, cv_Species::Species spe, cv_AbstractTrait::Type ty, cv_AbstractTrait::Category ca ) : cv_AbstractTrait( txt, spe, ty, ca ) {
	v_value = val;
	v_era = cv_Trait::EraNo;
	v_age = cv_Trait::AgeNo;
// 	details;
	v_prerequisites = "";
	v_custom = false;
	v_customText = "";
	v_bonus = false;
}

cv_Trait::~cv_Trait() {
}


int cv_Trait::value() const {
	return v_value;
}
void cv_Trait::setValue( int val ) {
	v_value = val;
}

QList< int > cv_Trait::possibleValues() const {
	return v_possibleValues;
}
void cv_Trait::setPossibleValues( QList< int > list ) {
	v_possibleValues = list;
}
void cv_Trait::addPossibleValue( int val ) {
	v_possibleValues.append( val );
}


cv_Trait::Era cv_Trait::era() const {
	return v_era;
}

void cv_Trait::setEra( cv_Trait::Era er ) {
	v_era = er;
}

cv_Trait::Age cv_Trait::age() const {
	return v_age;
}

void cv_Trait::setAge( cv_Trait::Age ag ) {
	v_age = ag;
}

QList< cv_TraitDetail > cv_Trait::details() const {
	return v_details;
}

void cv_Trait::setDetails( QList< cv_TraitDetail > list ) {
	if ( v_details != list ) {
		v_details = list;
	}
}
void cv_Trait::addDetail( cv_TraitDetail det ) {
	if ( !v_details.contains( det ) ) {
		v_details.append( det );
	}
}
void cv_Trait::clearDetails() {
	if ( !v_details.isEmpty() ) {
		v_details.clear();
	}
}


QString cv_Trait::prerequisites() const {
	return v_prerequisites;
}

void cv_Trait::setPrerequisites( QString txt ) {
	v_prerequisites = txt;
}

bool cv_Trait::custom() const {
	return v_custom;
}

void cv_Trait::setCustom( bool sw ) {
	v_custom = sw;
}

QString cv_Trait::customText() const {
	if ( custom() ) {
		return v_customText;
	} else {
		return "";
	}
}

void cv_Trait::setCustomText( QString txt ) {
	if ( !txt.isEmpty() ) {
		v_custom = true;
	}

	v_customText = txt;
}

bool cv_Trait::isBonus() const {
	return v_bonus;
}
void cv_Trait::setBonus( bool sw ) {
// 	qDebug() << Q_FUNC_INFO << "Wird aufgerufen!";
	if (v_bonus != sw){
		v_bonus = sw;
	}
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

	bool result = name() == trait.name()

				  && v_value == trait.v_value
				  && type() == trait.type()
				  && category() == trait.category()
				  && species() == trait.species()
				  && v_era == trait.v_era
				  && v_age == trait.v_age
				  && v_details == trait.v_details
				  && v_prerequisites == trait.v_prerequisites
				  && v_custom == trait.v_custom;

	return result;
}

bool cv_Trait::operator<( const cv_Trait& trait ) const {
	if ( this == &trait ) {
		return false;
	}

	bool result = v_value < trait.v_value;
}
