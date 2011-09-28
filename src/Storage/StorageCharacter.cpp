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

#include <QDebug>

#include "StorageTemplate.h"

#include "StorageCharacter.h"
#include "Config/Config.h"


StorageCharacter* StorageCharacter::p_instance = 0;

QString StorageCharacter::v_virtue = "";
QString StorageCharacter::v_vice = "";
QString StorageCharacter::v_breed = "";
QString StorageCharacter::v_faction = "";
int StorageCharacter::v_superTrait = 0;
int StorageCharacter::v_morality = 0;
int StorageCharacter::v_armorGeneral = 0;
int StorageCharacter::v_armorFirearms = 0;
bool StorageCharacter::v_modified = false;
cv_IdentityList StorageCharacter::v_identities;
QList< cv_Trait > StorageCharacter::v_traits;
QList< Trait* > StorageCharacter::v_traits2;
cv_Species::SpeciesFlag StorageCharacter::v_species;
QList< cv_Derangement > StorageCharacter::v_derangements;


StorageCharacter* StorageCharacter::getInstance( ) {
	if ( !p_instance )
		p_instance = new StorageCharacter( );

	return p_instance;
}

void StorageCharacter::destroy() {
	if ( p_instance )
		delete p_instance;
}


StorageCharacter::StorageCharacter( QObject* parent ) : QObject( parent ) {
	realIdentity = &v_identities[0];

	storage = new StorageTemplate( this );

	// Sobald irgendein Aspekt des Charakters verändert wird, muß festgelegt werden, daß sich der Charkater seit dem letzten Speichern verändert hat.
	// Es ist Aufgabe der Speicher-Funktion, dafür zu sorgen, daß beim Speichern diese Inforamtion wieder zurückgesetzt wird.
	connect( this, SIGNAL( identityChanged( cv_Identity ) ), this, SLOT( setModified() ) );
	connect( this, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( setModified() ) );
	connect( this, SIGNAL( traitChanged( cv_Trait* ) ), this, SLOT( setModified() ) );
	connect( this, SIGNAL( derangementsChanged() ), this, SLOT( setModified() ) );
	connect( this, SIGNAL( virtueChanged( QString ) ), this, SLOT( setModified() ) );
	connect( this, SIGNAL( viceChanged( QString ) ), this, SLOT( setModified() ) );
	connect( this, SIGNAL( breedChanged( QString ) ), this, SLOT( setModified() ) );
	connect( this, SIGNAL( factionChanged( QString ) ), this, SLOT( setModified() ) );
	connect( this, SIGNAL( superTraitChanged( int ) ), this, SLOT( setModified() ) );
	connect( this, SIGNAL( moralityChanged( int ) ), this, SLOT( setModified() ) );
	connect( this, SIGNAL( armorChanged( int, int ) ), this, SLOT( setModified() ) );
}

StorageCharacter::~StorageCharacter() {
	delete storage;
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

cv_IdentityList StorageCharacter::identities() const {
	return v_identities;
}

void StorageCharacter::insertIdentity( int index, cv_Identity id ) {
	v_identities.insert( index, id );

	emit identityChanged( id );
}

void StorageCharacter::addIdentity( cv_Identity id ) {
	int index = identities().count();
	insertIdentity( index, id );

	emit identityChanged( id );
}

void StorageCharacter::setRealIdentity( cv_Identity id ) {
	if ( v_identities.count() > 0 ) {
		v_identities.replace( 0, id );
	} else {
		insertIdentity( 0, id );
	}

	emit identityChanged( id );

	emit realIdentityChanged( id );
}




QList< cv_Trait >* StorageCharacter::traits() const {
	return &v_traits;
}

QList< cv_Trait* > StorageCharacter::traits( cv_Trait::Type type ) const {
	QList< cv_Trait* > list;

	for ( int i = 0; i < v_traits.count(); i++ ) {
		if ( v_traits.at( i ).v_type == type ) {
			list.append( &v_traits[i] );
		}
	}

	return list;
}

QList< cv_Trait* > StorageCharacter::traits( cv_Trait::Type type, cv_Trait::Category category ) const {
	QList< cv_Trait* > list;

	for ( int i = 0; i < v_traits.count(); i++ ) {
		if ( v_traits.at( i ).v_type == type && v_traits.at( i ).v_category == category ) {
			list.append( &v_traits[i] );
		}
	}

	return list;
}


cv_Trait* StorageCharacter::addTrait( cv_Trait trait ) {
	cv_Trait* traitPtr;

// 	qDebug() << Q_FUNC_INFO << "Füge hinzu:" << trait.name << "mit" << trait.custom << "und" << trait.customText;
	v_traits.append( trait );
	traitPtr = &v_traits[ v_traits.count() - 1 ];

// 	Q_CHECK_PTR(traitPtr);

// 	emit traitChanged( trait );
// 	emit traitChanged( traitPtr );

	return traitPtr;
}
Trait* StorageCharacter::addTrait( Trait* trait ) {
	Trait* lcl_trait = new Trait(trait);

	v_traits2.append( lcl_trait );

	return lcl_trait;
}

void StorageCharacter::modifyTrait( cv_Trait trait ) {
	for ( int i = 0; i < v_traits.count(); i++ ) {
		if ( trait.v_type == v_traits.at( i ).v_type && trait.v_category == v_traits.at( i ).v_category && trait.v_name == v_traits.at( i ).v_name ) {
			if ( !v_traits.at( i ).v_custom || trait.v_customText == v_traits.at( i ).v_customText || v_traits.at( i ).v_customText.isEmpty() ) {
				// Custom bleibt immer gleich.
				v_traits[i].setValue ( trait.value() );
				v_traits[i].v_customText = trait.v_customText;
				v_traits[i].v_details = trait.v_details;
// 				qDebug() << Q_FUNC_INFO << v_traits.at( i ).name << "Adresse:" << &v_traits[i] << "verändert zu" << v_traits.at( i ).value << "Und zusatztext:" << v_traits.at( i ).customText << v_traits.at( i ).custom;

				emit traitChanged( &v_traits[i] );

				// Wenn der Eintrage geschrieben ist, wird die Schleife abgebrochen.
// 				qDebug() << Q_FUNC_INFO << "breche ab";
				break;
			}
		}
	}
}


QList< cv_Derangement >* StorageCharacter::derangements() const {
	return &v_derangements;
}

QList< cv_Derangement* > StorageCharacter::derangements( cv_Trait::Category category ) const {
	QList< cv_Derangement* > list;

	for ( int i = 0; i < v_derangements.count(); i++ ) {
		if ( v_derangements.at( i ).v_category == category ) {
			list.append( &v_derangements[i] );
		}
	}

	return list;
}

void StorageCharacter::addDerangement( cv_Derangement derang ) {
	if ( derang.v_name != "" && !v_derangements.contains( derang ) ) {
// 		qDebug() << Q_FUNC_INFO << derang.name << derang.morality;
		v_derangements.append( derang );

		emit derangementsChanged();
	}
}

void StorageCharacter::removeDerangement( cv_Derangement derang ) {
	if ( v_derangements.contains( derang ) ) {
		v_derangements.removeAll( derang );
		emit derangementsChanged();
	}
}






void StorageCharacter::setSkillSpecialties( QString name, QList< cv_TraitDetail > details ) {
	bool trait_exists = false;

	for ( int i = 0; i < v_traits.count(); i++ ) {
		// Spezialisieren gibt es nur bei Fertigkeiten.
		// Spezialisierungen gibt es nur bei Fertigkeiten, die hier schon existieren.
		// Spezialisierungen gibt es nur bei Fertigkeiten, die einen Wert größer 0 haben.
		if ( v_traits.at( i ).v_type == cv_Trait::Skill && v_traits.at( i ).v_name == name && v_traits.at( i ).value() > 0 ) {
			trait_exists = true;

			cv_Trait trait = v_traits.at( i );
			// Erst alle Spezialisieren löschen
			trait.v_details.clear();

			// Dann neu setzen.
			int detailsCount = details.count();

			for ( int j = 0; j < detailsCount; j++ ) {
				cv_TraitDetail specialty;
				specialty.name = details.at( j ).name;
				specialty.value = true;
// 				qDebug() << Q_FUNC_INFO << "Füge Spezialisierung" << specialty.name << "zu Fertigkeit" << name << "hinzu";
				trait.v_details.append( specialty );
			}

			v_traits.replace( i, trait );

// 			emit traitChanged( trait );
// 			emit traitChanged( &v_traits[ i ] );

			break;
		}
	}

	// Existiert die Fertigkeit nicht, für die eine Spezialisierung eingetragen werden soll, muß etwas getan werden. Anlegen ist aber nicht dier richtige Lösung (welcher Wert denn?).
	if ( !trait_exists ) {
		qDebug() << Q_FUNC_INFO << "Spezialisierungen nicht angelegt, da Fertigkeit" << name << "nicht existiert.";
	}
}

QString StorageCharacter::virtue() const {
	return v_virtue;
}

void StorageCharacter::setVirtue( QString txt ) {
	if ( v_virtue != txt ) {
		v_virtue = txt;
		emit virtueChanged( txt );
	}
}

QString StorageCharacter::vice() const {
	return v_vice;
}

void StorageCharacter::setVice( QString txt ) {
	if ( v_vice != txt ) {
		v_vice = txt;
		emit viceChanged( txt );
	}
}

QString StorageCharacter::breed() const {
	return v_breed;
}

void StorageCharacter::setBreed( QString txt ) {
	if ( v_breed != txt ) {
		v_breed = txt;
		emit breedChanged( txt );
	}
}

QString StorageCharacter::faction() const {
	return v_faction;
}

void StorageCharacter::setFaction( QString txt ) {
	if ( v_faction != txt ) {
		v_faction = txt;
		emit factionChanged( txt );
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

int StorageCharacter::morality() const {
	return v_morality;
}

void StorageCharacter::setMorality( int value ) {
	if ( v_morality != value ) {
		v_morality = value;

		emit moralityChanged( value );
	}
}

int StorageCharacter::armorGeneral() const {
	return v_armorGeneral;
}

int StorageCharacter::armorFirearms() const {
	return v_armorFirearms;
}

void StorageCharacter::setArmor( int general, int firearms ) {
	if ( v_armorGeneral != general || v_armorFirearms != firearms ) {
		v_armorGeneral = general;
		v_armorFirearms = firearms;

		emit armorChanged( general, firearms );
	}
}


void StorageCharacter::resetCharacter() {
	v_identities.reset();

	emit realIdentityChanged( v_identities.at( 0 ) );

	setSpecies( cv_Species::Human );

	setVirtue( storage->virtueNames().at( 0 ) );
	setVice( storage->viceNames().at( 0 ) );

	// Menschen haben eine Leere liste, also kann ich auch die Indizes nicht ändern.
// 	setBreed(storage->breedNames(species()).at(0));
// 	setFaction(storage->breedNames(species()).at(0));

	for ( int i = 0; i < v_traits.count();i++ ) {
		if ( v_traits[i].v_type == cv_Trait::Attribute ) {
			v_traits[i].setValue( 1 );
		} else {
			v_traits[i].setValue( 0 );
		}

		v_traits[i].v_details.clear();

		v_traits[i].v_customText = "";

		emit traitChanged( &v_traits[i] );
	}

	v_derangements.clear();

	setMorality( Config::derangementMoralityTraitMax );
}



bool StorageCharacter::isModifed() const {
	return v_modified;
}

void StorageCharacter::setModified( bool sw ) {
	if ( v_modified != sw ) {
		v_modified = sw;
	}
}



