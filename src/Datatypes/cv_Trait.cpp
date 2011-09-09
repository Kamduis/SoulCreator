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


const QList< cv_Trait::Category > cv_Trait::v_categoryListGeneral = QList< cv_Trait::Category >()
		<< cv_Trait::Mental
		<< cv_Trait::Physical
		<< cv_Trait::Social;

const QList< cv_Trait::Category > cv_Trait::v_categoryListExtended = QList< cv_Trait::Category >()
		<< cv_Trait::v_categoryListGeneral
		<< cv_Trait::Extraordinary;

const QList< cv_Trait::Category > cv_Trait::v_categoryListAll = QList< cv_Trait::Category >()
		<< cv_Trait::v_categoryListExtended
		<< cv_Trait::Item
		<< cv_Trait::FightingStyle
		<< cv_Trait::DebateStyle;


cv_Trait::cv_Trait() {
	name = "";
	value = 0;
// 	possibleValues;
	type = cv_Trait::TypeNo;
	category = cv_Trait::CategoryNo;
	species = cv_Species::SpeciesNo;
	era = cv_Trait::EraNo;
	age = cv_Trait::AgeNo;
// 	details;
	prerequisites = "";
	custom = false;
	customText = "";
}



QString cv_Trait::toXmlString( cv_Trait::Type type ) {
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
		case cv_Trait::Derangement:
			return "Derangement";
		case cv_Trait::Flaw:
			return "Flaw";
		case cv_Trait::Super:
			return "Super";
		case cv_Trait::Power:
			return "Power";
		default:
			throw eTraitType( type );
// 			return "ERROR";
	}
}

QString cv_Trait::toXmlString( cv_Trait::Category category ) {
	switch ( category ) {
		case cv_Trait::CategoryNo:
			return "CategoryNo";
		case cv_Trait::Mental:
			return "Mental";
		case cv_Trait::Physical:
			return "Physical";
		case cv_Trait::Social:
			return "Social";
		case cv_Trait::Item:
			return "Item";
		case cv_Trait::FightingStyle:
			return "FightingStyle";
		case cv_Trait::DebateStyle:
			return "DebateStyle";
		case cv_Trait::Extraordinary:
			return "Extraordinary";
		default:
			throw eTraitCategory( category );
// 			return "ERROR";
	}
}

QString cv_Trait::toString( cv_Trait::Type type, bool plural ) {
	if ( plural ) {
		switch ( type ) {
			case cv_Trait::TypeNo:
				return QObject::tr( "Without Types" );
			case cv_Trait::Virtue:
				return QObject::tr( "Virtues" );
			case cv_Trait::Vice:
				return QObject::tr( "Vices" );
			case cv_Trait::Attribute:
				return QObject::tr( "Attributes" );
			case cv_Trait::Skill:
				return QObject::tr( "Skills" );
			case cv_Trait::Merit:
				return QObject::tr( "Merits" );
			case cv_Trait::Derangement:
				return QObject::tr( "Derangements" );
			case cv_Trait::Flaw:
				return QObject::tr( "Flaws" );
			case cv_Trait::Super:
				return QObject::tr( "Supertraits" );
			case cv_Trait::Power:
				return QObject::tr( "Powers" );
			default:
				throw eTraitType( type );
// 			return "ERROR";
		}
	} else {
		switch ( type ) {
			case cv_Trait::TypeNo:
				return QObject::tr( "Without Type" );
			case cv_Trait::Virtue:
				return QObject::tr( "Virtue" );
			case cv_Trait::Vice:
				return QObject::tr( "Vice" );
			case cv_Trait::Attribute:
				return QObject::tr( "Attribute" );
			case cv_Trait::Skill:
				return QObject::tr( "Skill" );
			case cv_Trait::Merit:
				return QObject::tr( "Merit" );
			case cv_Trait::Derangement:
				return QObject::tr( "Derangement" );
			case cv_Trait::Flaw:
				return QObject::tr( "Flaw" );
			case cv_Trait::Super:
				return QObject::tr( "Supertrait" );
			case cv_Trait::Power:
				return QObject::tr( "Power" );
			default:
				throw eTraitType( type );
// 			return "ERROR";
		}
	}
}

QString cv_Trait::toString( cv_Trait::Category category, bool plural ) {
	if ( plural ) {
		switch ( category ) {
			case cv_Trait::CategoryNo:
				return QObject::tr( "Without Category" );
			case cv_Trait::Mental:
				return QObject::tr( "Mental" );
			case cv_Trait::Physical:
				return QObject::tr( "Physical" );
			case cv_Trait::Social:
				return QObject::tr( "Social" );
			case cv_Trait::Item:
				return QObject::tr( "Items" );
			case cv_Trait::FightingStyle:
				return QObject::tr( "Fighting Styles" );
			case cv_Trait::DebateStyle:
				return QObject::tr( "Debate Styles" );
			case cv_Trait::Extraordinary:
				return QObject::tr( "Extraordinary" );
			default:
				throw eTraitCategory( category );
		}
	} else {
		switch ( category ) {
			case cv_Trait::CategoryNo:
				return QObject::tr( "Without Category" );
			case cv_Trait::Mental:
				return QObject::tr( "Mental" );
			case cv_Trait::Physical:
				return QObject::tr( "Physical" );
			case cv_Trait::Social:
				return QObject::tr( "Social" );
			case cv_Trait::Item:
				return QObject::tr( "Item" );
			case cv_Trait::FightingStyle:
				return QObject::tr( "Fighting Style" );
			case cv_Trait::DebateStyle:
				return QObject::tr( "Debate Style" );
			case cv_Trait::Extraordinary:
				return QObject::tr( "Extraordinary" );
			default:
				throw eTraitCategory( category );
		}
	}
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
	else if ( str == "Derangement" )
		return cv_Trait::Derangement;
	else if ( str == "Flaw" )
		return cv_Trait::Flaw;
// 	else if ( str == "Morale" )
// 		return cv_Trait::Morale;
	else if ( str == "Super" )
		return cv_Trait::Super;
	else if ( str == "Power" )
		return cv_Trait::Power;
	else
		return cv_Trait::TypeNo;
}

cv_Trait::Category cv_Trait::toCategory( QString str ) {
	if ( str == "Mental" )
		return cv_Trait::Mental;
	else if ( str == "Physical" )
		return cv_Trait::Physical;
	else if ( str == "Social" )
		return cv_Trait::Social;
	else if ( str == "Item" )
		return cv_Trait::Item;
	else if ( str == "FightingStyle" )
		return cv_Trait::FightingStyle;
	else if ( str == "DebateStyle" )
		return cv_Trait::DebateStyle;
	else if ( str == "Extraordinary" )
		return cv_Trait::Extraordinary;
	else
		return cv_Trait::CategoryNo;
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


QList< cv_Trait::Category > cv_Trait::getCategoryList( cv_Trait::Type type ) {
	if ( type == cv_Trait::Attribute || type == cv_Trait::Skill ) {
		return v_categoryListGeneral;
	} else if ( type == cv_Trait::Merit ) {
		return v_categoryListAll;
	} else if ( type == cv_Trait::Power || type == cv_Trait::Derangement ) {
		return QList< cv_Trait::Category >() << cv_Trait::CategoryNo;
	} else if ( type == cv_Trait::Flaw ) {
		return v_categoryListExtended;
	} else {
		throw eTraitType( type );
	}
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

	bool result = name < name;
}
