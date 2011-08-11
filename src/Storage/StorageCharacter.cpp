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


StorageCharacter* StorageCharacter::getInstance(  ) {
	if ( !p_instance )
		p_instance = new StorageCharacter(  );
	return p_instance;
}

void StorageCharacter::destroy() {
	if ( p_instance )
		delete p_instance;
}


// //Character::Species StorageCharacter::storedSpecies;
// //QList<Name> StorageCharacter::storedNames;
// QList<cv_Trait> StorageCharacter::storedTraits;
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

		qDebug() << Q_FUNC_INFO << "Spezies in Speicher verändert!";

		emit speciesChanged( species );
// 		emitSpeciesChanged( species );
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

QList< cv_Trait > StorageCharacter::traits( cv_Trait::Type type, cv_Trait::Category category ) const {
	QList< cv_Trait > traits = v_traits;
	QList< cv_Trait > list;

	for ( int i = 0; i < traits.count(); i++ ) {
		if ( traits.at( i ).type == type && traits.at( i ).category == category ) {
			list.append( traits.at( i ) );
		}
	}

	return list;
}

QList< cv_Trait > StorageCharacter::attributes( cv_Trait::Category category ) const {
	return traits( cv_Trait::Attribute, category );
}


void StorageCharacter::setValue( int value, cv_Trait::Type type, cv_Trait::Category category, QString name ) {
	bool trait_exists = false;

	// Es sind nicht von Anfang an alle Eigenschaften gespeichert. Wenn eine Eigenschaft also nicht in der Liste zu finden ist, muß sie angelegt werden.

	for ( int i = 0; i < v_traits.count(); i++ ) {
		qDebug() << Q_FUNC_INFO << "Vergleiche" << name << type << category << "mit" << v_traits.at( i ).name << v_traits.at( i ).type << v_traits.at( i ).category << ".";

		
		if ( v_traits.at( i ).type == type && v_traits.at( i ).category == category && v_traits.at( i ).name == name ) {
			trait_exists = true;

			qDebug() << Q_FUNC_INFO << "Sind identisch!";

			if ( v_traits.at( i ).value != value ) {
				// Ich kann den Inhalt in einer Liste nicht direkt ändern, also erst rauskopieren, die Kopie ändern und dann das Original mit der Kopie wieder überschreiben.
				cv_Trait trait = v_traits.at( i );
				trait.value = value;

				// Bei einem Fertigkeitswert von 0 werden alle Spezialisierungen gelöscht.

				if ( value < 1 ) {
					trait.details.clear();
				}

				v_traits.replace( i, trait );

				qDebug() << Q_FUNC_INFO << "Wert von" << name << "in Speicher verändert!";

				emit valueChanged( value, type, category, name );
			}

			break;
		}
	}

	if ( !trait_exists ) {
		qDebug() << Q_FUNC_INFO << "Sind verschieden!";

		StorageTemplate storage;

		cv_Trait trait = storage.trait( type, category, name );
		trait.value = value;
		// Alle /möglichen/ Spezialisierungen löschen.
		trait.details.clear();

		v_traits.append( trait );
		
		qDebug() << Q_FUNC_INFO << name << value << "in Speicher erzeugt!";

		emit valueChanged( value, type, category, name );
	}

// 	qDebug() << Q_FUNC_INFO << "In Speicher geändert:" << name << "zu" << value;
}

void StorageCharacter::setSkillSpecialties( QString name, QList< cv_TraitDetail > details ) {
	bool trait_exists = false;

	for ( int i = 0; i < v_traits.count(); i++ ) {
		// Spezialisieren gibt es nur bei Fertigkeiten.
		// Spezialisierungen gibt es nur bei Fertigkeiten, die hier schon existieren.
		// Spezialisierungen gibt es nur bei Fertigkeiten, die einen Wert größer 0 haben.
		if ( v_traits.at( i ).type == cv_Trait::Skill && v_traits.at( i ).name == name && v_traits.at( i ).value > 0 ) {
			trait_exists = true;

// 			qDebug() << Q_FUNC_INFO << "Füge Spezialisierung" << details.at(i).name << "zu Fertigkeit" << name << "hinzu";

			cv_Trait trait = v_traits.at( i );
			// Erst alle Spezialisieren löschen
			trait.details.clear();

			// Dann neu setzen.

			for ( int j = 0; j < details.count(); j++ ) {
				cv_TraitDetail specialty;
				specialty.name = details.at( j ).name;
				trait.details.append( specialty );
			}

			v_traits.replace( i, trait );

			break;
		}
	}

	// Existiert die Fertigkeit nicht, für die eine Spezialisierung eingetragen werden soll, muß etwas getan werden. Anlegen ist aber nicht dier richtige Lösung (welcher Wert denn?).
	if ( !trait_exists ) {
		qDebug() << Q_FUNC_INFO << "Spezialisierungen nicht angelegt, da Fertigkeit" << name << "nicht existiert.";
	}
}

// void StorageCharacter::emitSpeciesChanged( cv_Species::SpeciesFlag species ) {
// 	emit speciesChanged(species);
// }

