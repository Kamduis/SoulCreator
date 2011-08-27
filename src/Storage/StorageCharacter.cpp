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

#include <QDebug>

#include "StorageTemplate.h"

#include "StorageCharacter.h"


StorageCharacter* StorageCharacter::p_instance = 0;

int StorageCharacter::v_superTrait = 0;
int StorageCharacter::v_morality = 0;

StorageCharacter* StorageCharacter::getInstance( ) {
	if ( !p_instance )
		p_instance = new StorageCharacter( );

	return p_instance;
}

void StorageCharacter::destroy() {
	if ( p_instance )
		delete p_instance;
}


cv_NameList StorageCharacter::v_identities;
QList< cv_Trait > StorageCharacter::v_traits;
cv_Species::SpeciesFlag StorageCharacter::v_species;


StorageCharacter::StorageCharacter( QObject* parent ) : QObject( parent ) {
}

StorageCharacter::~StorageCharacter() {
}

cv_Species::SpeciesFlag StorageCharacter::species() const {
	return v_species;
}

void StorageCharacter::setSpecies( cv_Species::SpeciesFlag species ) {
	if ( v_species != species ) {
		v_species = species;

// 		qDebug() << Q_FUNC_INFO << "Spezies in Speicher verändert!";

		emit speciesChanged( species );
	}
}

cv_NameList StorageCharacter::identities() const {
	return v_identities;
}

void StorageCharacter::insertIdentity( int index, cv_Name name ) {
	v_identities.insert( index, name );
}

void StorageCharacter::addIdentity( cv_Name name ) {
	int index = identities().count();
	insertIdentity( index, name );
}

QList< cv_Trait > StorageCharacter::traitsAll() const {
	return v_traits;
}

QList< cv_Trait > StorageCharacter::traits( cv_Trait::Type type, cv_Trait::Category category ) const {
	QList< cv_Trait > list;

	for ( int i = 0; i < v_traits.count(); i++ ) {
		if ( v_traits.at( i ).type == type && v_traits.at( i ).category == category ) {
			list.append( v_traits.at( i ) );
		}
	}

	return list;
}

QList< cv_Trait > StorageCharacter::attributes( cv_Trait::Category category ) const {
	return traits( cv_Trait::Attribute, category );
}

QList< cv_Trait > StorageCharacter::skills( cv_Trait::Category category ) const {
	return traits( cv_Trait::Skill, category );
}

QList< cv_Trait > StorageCharacter::merits( cv_Trait::Category category ) const {
	return traits( cv_Trait::Merit, category );
}

void StorageCharacter::addTrait( cv_Trait trait ) {
	bool exists = false;

	for ( int i = 0; i < v_traits.count(); i++ ) {
		if ( v_traits.at( i ).type == trait.type && v_traits.at( i ).category == trait.category && v_traits.at( i ).name == trait.name ) {
			if ( trait.custom ) {
				// Eigenschaften mit Zusatztext werden nur gespeichert, wenn dieser Text auch vorhanden ist.
				if ( trait.customText.isEmpty() ) {
// 					qDebug() << Q_FUNC_INFO << "Ersetze" << trait.name << "NICHT!";
					return;
				} else if ( v_traits.at( i ).customText == trait.customText ) {
// 					qDebug() << Q_FUNC_INFO << "Klicke" << trait.name << "mit" << trait.customText;
					exists = true;
				}
			} else {
				exists = true;
			}
		}

		// Wenn ich die Eigenschaft schon finde, muß ich natürlich nicht bis zum Ende der Schleife laufen, sondern ersetze sie sofort und fertig.
		if ( exists ) {
// 			qDebug() << Q_FUNC_INFO << "Ersetze:" << trait.name << trait.customText << "mit" << trait.value;
			v_traits.replace( i, trait );
			break;
		}
	}

	if ( !exists ) {
// 		qDebug() << Q_FUNC_INFO << "Füge hinzu:" << trait.name << "mit" << trait.custom << "und" << trait.customText;
		v_traits.append( trait );
	}

	emit traitChanged( trait );
}



void StorageCharacter::setSkillSpecialties( QString name, QList< cv_TraitDetail > details ) {
	bool trait_exists = false;

	for ( int i = 0; i < v_traits.count(); i++ ) {
		// Spezialisieren gibt es nur bei Fertigkeiten.
		// Spezialisierungen gibt es nur bei Fertigkeiten, die hier schon existieren.
		// Spezialisierungen gibt es nur bei Fertigkeiten, die einen Wert größer 0 haben.
		if ( v_traits.at( i ).type == cv_Trait::Skill && v_traits.at( i ).name == name && v_traits.at( i ).value > 0 ) {
			trait_exists = true;

			cv_Trait trait = v_traits.at( i );
			// Erst alle Spezialisieren löschen
			trait.details.clear();

			// Dann neu setzen.
			int detailsCount = details.count();

			for ( int j = 0; j < detailsCount; j++ ) {
				cv_TraitDetail specialty;
				specialty.name = details.at( j ).name;
				specialty.value = true;
// 				qDebug() << Q_FUNC_INFO << "Füge Spezialisierung" << specialty.name << "zu Fertigkeit" << name << "hinzu";
				trait.details.append( specialty );
			}

			v_traits.replace( i, trait );

			emit traitChanged( trait );

			break;
		}
	}

	// Existiert die Fertigkeit nicht, für die eine Spezialisierung eingetragen werden soll, muß etwas getan werden. Anlegen ist aber nicht dier richtige Lösung (welcher Wert denn?).
	if ( !trait_exists ) {
		qDebug() << Q_FUNC_INFO << "Spezialisierungen nicht angelegt, da Fertigkeit" << name << "nicht existiert.";
	}
}

int StorageCharacter::superTrait() const {
	return v_superTrait;
}
void StorageCharacter::setSuperTrait( int value ) {
	if ( v_superTrait != value ) {
		v_superTrait = value;
		emit superTraitChanged( value );
	}
}

int StorageCharacter::morality() const
{
	return v_morality;
}
void StorageCharacter::setMorality( int value )
{
	if (v_morality != value){
		v_morality = value;
		emit moralityChanged(value);
	}
}

