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

#include "cv_AbstractTrait.h"


const QList< cv_AbstractTrait::Category > cv_AbstractTrait::v_categoryListGeneral = QList< cv_AbstractTrait::Category >()
		<< cv_AbstractTrait::Mental
		<< cv_AbstractTrait::Physical
		<< cv_AbstractTrait::Social;

const QList< cv_AbstractTrait::Category > cv_AbstractTrait::v_categoryListExtended = QList< cv_AbstractTrait::Category >()
		<< cv_AbstractTrait::v_categoryListGeneral
		<< cv_AbstractTrait::Extraordinary;

const QList< cv_AbstractTrait::Category > cv_AbstractTrait::v_categoryListDerangements = QList< cv_AbstractTrait::Category >()
		<< cv_AbstractTrait::Mild
		<< cv_AbstractTrait::Severe;

const QList< cv_AbstractTrait::Category > cv_AbstractTrait::v_categoryListAll = QList< cv_AbstractTrait::Category >()
		<< cv_AbstractTrait::v_categoryListExtended
		<< cv_AbstractTrait::Item
		<< cv_AbstractTrait::FightingStyle
		<< cv_AbstractTrait::DebateStyle;


cv_AbstractTrait::cv_AbstractTrait( QString txt, cv_Species::Species spe, cv_AbstractTrait::Type ty, cv_AbstractTrait::Category ca ) {
	name = txt;
	species = spe;
	type = ty;
	category = ca;
}

QString cv_AbstractTrait::toXmlString( cv_AbstractTrait::Type type ) {
	switch ( type ) {
		case cv_AbstractTrait::TypeNo:
			return "TypeNo";
		case cv_AbstractTrait::Virtue:
			return "Virtue";
		case cv_AbstractTrait::Vice:
			return "Vice";
		case cv_AbstractTrait::Breed:
			return "Breed";
		case cv_AbstractTrait::Faction:
			return "Faction";
		case cv_AbstractTrait::Attribute:
			return "Attribute";
		case cv_AbstractTrait::Skill:
			return "Skill";
		case cv_AbstractTrait::Merit:
			return "Merit";
		case cv_AbstractTrait::Derangement:
			return "Derangement";
		case cv_AbstractTrait::Flaw:
			return "Flaw";
		case cv_AbstractTrait::Super:
			return "Super";
		case cv_AbstractTrait::Power:
			return "Power";
		default:
			throw eTraitType( type );
// 			return "ERROR";
	}
}

QString cv_AbstractTrait::toXmlString( cv_AbstractTrait::Category category ) {
	switch ( category ) {
		case cv_AbstractTrait::CategoryNo:
			return "CategoryNo";
		case cv_AbstractTrait::Mental:
			return "Mental";
		case cv_AbstractTrait::Physical:
			return "Physical";
		case cv_AbstractTrait::Social:
			return "Social";
		case cv_AbstractTrait::Item:
			return "Item";
		case cv_AbstractTrait::FightingStyle:
			return "FightingStyle";
		case cv_AbstractTrait::DebateStyle:
			return "DebateStyle";
		case cv_AbstractTrait::Extraordinary:
			return "Extraordinary";
		case cv_AbstractTrait::Mild:
			return "Mild";
		case cv_AbstractTrait::Severe:
			return "Severe";
		default:
			throw eTraitCategory( category );
// 			return "ERROR";
	}
}

QString cv_AbstractTrait::toString( cv_AbstractTrait::Type type, bool plural ) {
	if ( plural ) {
		switch ( type ) {
			case cv_AbstractTrait::TypeNo:
				return QObject::tr( "Without Types" );
			case cv_AbstractTrait::Virtue:
				return QObject::tr( "Virtues" );
			case cv_AbstractTrait::Vice:
				return QObject::tr( "Vices" );
			case cv_AbstractTrait::Breed:
				return QObject::tr( "Breeds" );
			case cv_AbstractTrait::Faction:
				return QObject::tr( "Factions" );
			case cv_AbstractTrait::Attribute:
				return QObject::tr( "Attributes" );
			case cv_AbstractTrait::Skill:
				return QObject::tr( "Skills" );
			case cv_AbstractTrait::Merit:
				return QObject::tr( "Merits" );
			case cv_AbstractTrait::Derangement:
				return QObject::tr( "Derangements" );
			case cv_AbstractTrait::Flaw:
				return QObject::tr( "Flaws" );
			case cv_AbstractTrait::Super:
				return QObject::tr( "Supertraits" );
			case cv_AbstractTrait::Power:
				return QObject::tr( "Powers" );
			default:
				throw eTraitType( type );
// 			return "ERROR";
		}
	} else {
		switch ( type ) {
			case cv_AbstractTrait::TypeNo:
				return QObject::tr( "Without Type" );
			case cv_AbstractTrait::Virtue:
				return QObject::tr( "Virtue" );
			case cv_AbstractTrait::Vice:
				return QObject::tr( "Vice" );
			case cv_AbstractTrait::Breed:
				return QObject::tr( "Breed" );
			case cv_AbstractTrait::Faction:
				return QObject::tr( "Faction" );
			case cv_AbstractTrait::Attribute:
				return QObject::tr( "Attribute" );
			case cv_AbstractTrait::Skill:
				return QObject::tr( "Skill" );
			case cv_AbstractTrait::Merit:
				return QObject::tr( "Merit" );
			case cv_AbstractTrait::Derangement:
				return QObject::tr( "Derangement" );
			case cv_AbstractTrait::Flaw:
				return QObject::tr( "Flaw" );
			case cv_AbstractTrait::Super:
				return QObject::tr( "Supertrait" );
			case cv_AbstractTrait::Power:
				return QObject::tr( "Power" );
			default:
				throw eTraitType( type );
// 			return "ERROR";
		}
	}
}

QString cv_AbstractTrait::toString( cv_AbstractTrait::Category category, bool plural ) {
	if ( plural ) {
		switch ( category ) {
			case cv_AbstractTrait::CategoryNo:
				return QObject::tr( "Without Category" );
			case cv_AbstractTrait::Mental:
				return QObject::tr( "Mental" );
			case cv_AbstractTrait::Physical:
				return QObject::tr( "Physical" );
			case cv_AbstractTrait::Social:
				return QObject::tr( "Social" );
			case cv_AbstractTrait::Item:
				return QObject::tr( "Items" );
			case cv_AbstractTrait::FightingStyle:
				return QObject::tr( "Fighting Styles" );
			case cv_AbstractTrait::DebateStyle:
				return QObject::tr( "Debate Styles" );
			case cv_AbstractTrait::Extraordinary:
				return QObject::tr( "Extraordinary" );
			case cv_AbstractTrait::Mild:
				return QObject::tr( "Mild" );
			case cv_AbstractTrait::Severe:
				return QObject::tr( "Severe" );
			default:
				throw eTraitCategory( category );
		}
	} else {
		switch ( category ) {
			case cv_AbstractTrait::CategoryNo:
				return QObject::tr( "Without Category" );
			case cv_AbstractTrait::Mental:
				return QObject::tr( "Mental" );
			case cv_AbstractTrait::Physical:
				return QObject::tr( "Physical" );
			case cv_AbstractTrait::Social:
				return QObject::tr( "Social" );
			case cv_AbstractTrait::Item:
				return QObject::tr( "Item" );
			case cv_AbstractTrait::FightingStyle:
				return QObject::tr( "Fighting Style" );
			case cv_AbstractTrait::DebateStyle:
				return QObject::tr( "Debate Style" );
			case cv_AbstractTrait::Extraordinary:
				return QObject::tr( "Extraordinary" );
			case cv_AbstractTrait::Mild:
				return QObject::tr( "Mild" );
			case cv_AbstractTrait::Severe:
				return QObject::tr( "Severe" );
			default:
				throw eTraitCategory( category );
		}
	}
}


cv_AbstractTrait::Type cv_AbstractTrait::toType( QString str ) {
	if ( str == "Virtue" )
		return cv_AbstractTrait::Virtue;
	else if ( str == "Vice" )
		return cv_AbstractTrait::Vice;
	else if ( str == "Breed" )
		return cv_AbstractTrait::Breed;
	else if ( str == "Faction" )
		return cv_AbstractTrait::Faction;
	else if ( str == "Attribute" )
		return cv_AbstractTrait::Attribute;
	else if ( str == "Skill" )
		return cv_AbstractTrait::Skill;
	else if ( str == "Merit" )
		return cv_AbstractTrait::Merit;
	else if ( str == "Derangement" )
		return cv_AbstractTrait::Derangement;
	else if ( str == "Flaw" )
		return cv_AbstractTrait::Flaw;
// 	else if ( str == "Morale" )
// 		return cv_AbstractTrait::Morale;
	else if ( str == "Super" )
		return cv_AbstractTrait::Super;
	else if ( str == "Power" )
		return cv_AbstractTrait::Power;
	else
		return cv_AbstractTrait::TypeNo;
}

cv_AbstractTrait::Category cv_AbstractTrait::toCategory( QString str ) {
	if ( str == "Mental" )
		return cv_AbstractTrait::Mental;
	else if ( str == "Physical" )
		return cv_AbstractTrait::Physical;
	else if ( str == "Social" )
		return cv_AbstractTrait::Social;
	else if ( str == "Item" )
		return cv_AbstractTrait::Item;
	else if ( str == "FightingStyle" )
		return cv_AbstractTrait::FightingStyle;
	else if ( str == "DebateStyle" )
		return cv_AbstractTrait::DebateStyle;
	else if ( str == "Extraordinary" )
		return cv_AbstractTrait::Extraordinary;
	else if ( str == "Mild" )
		return cv_AbstractTrait::Mild;
	else if ( str == "Severe" )
		return cv_AbstractTrait::Severe;
	else
		return cv_AbstractTrait::CategoryNo;
}


QList< cv_AbstractTrait::Category > cv_AbstractTrait::getCategoryList( cv_Trait::Type type ) {
	if ( type == cv_Trait::Attribute || type == cv_Trait::Skill ) {
		return v_categoryListGeneral;
	} else if ( type == cv_Trait::Merit ) {
		return v_categoryListAll;
	} else if ( type == cv_Trait::Power ) {
		return QList< cv_Trait::Category >() << cv_Trait::CategoryNo;
	} else if ( type == cv_Trait::Flaw ) {
		return v_categoryListExtended;
	} else if ( type == cv_Trait::Derangement ) {
		return v_categoryListDerangements;
	} else {
		throw eTraitType( type );
	}
}


bool cv_AbstractTrait::operator==( const cv_AbstractTrait& trait ) const {
	if ( this == &trait ) {
		return true;
	}

	bool result = name == trait.name &&
				  type == trait.type &&
				  category == trait.category &&
				  species == trait.species;

	return result;
}
