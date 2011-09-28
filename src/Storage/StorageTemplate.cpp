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

#include "Config/Config.h"
#include "Exceptions/Exception.h"

#include "StorageTemplate.h"


QList< cv_Species > StorageTemplate::v_species;
QList< cv_SpeciesTitle > StorageTemplate::v_titles;
QList< cv_Trait > StorageTemplate::v_traits;
QList< Trait* > StorageTemplate::v_traits2;
QList< cv_SuperEffect > StorageTemplate::v_superEffects;
QList< cv_CreationPoints2 > StorageTemplate::v_creationPoints;

StorageTemplate::StorageTemplate( QObject *parent ) : QObject( parent ) {
}

StorageTemplate::~StorageTemplate() {
}

void StorageTemplate::sortTraits() {
	qSort( v_traits );
}


QList< cv_Species > StorageTemplate::species() const {
	return v_species;
}


QStringList StorageTemplate::traitNames( cv_Trait::Type type, cv_Trait::Category category, cv_Trait::EraFlag era, cv_Trait::AgeFlag age ) const {
	QList< cv_Trait > traits = v_traits;
	QStringList list;

	for ( int i = 0; i < traits.count(); i++ ) {
		if ( traits.at( i ).v_type == type && traits.at( i ).v_category == category ) {
			if ( traits.at( i ).v_era.testFlag( era ) ) {
				if ( traits.at( i ).v_age.testFlag( age ) ) {
					// Es kann vorkommen, daß mehrere Eigenschaften doppelt aufgeführt sind. Diese wollen wir natürlich nicht doppelt ausgeben.
					if ( !list.contains( traits.at( i ).v_name ) ) {
// 						qDebug() << Q_FUNC_INFO << "Gib aus" << traits.at( i ).name;
						list.append( traits.at( i ).v_name );
					}
				}
			}
		}
	}

	return list;
}

QStringList StorageTemplate::virtueNames( cv_Trait::AgeFlag age ) const {
	return traitNames( cv_Trait::Virtue, cv_Trait::CategoryNo, cv_Trait::EraAll, age );
}

QStringList StorageTemplate::viceNames( cv_Trait::AgeFlag age ) const {
	return traitNames( cv_Trait::Vice, cv_Trait::CategoryNo, cv_Trait::EraAll, age );
}

QString StorageTemplate::breedTitle( cv_Species::SpeciesFlag spe ) const {
	for ( int i = 0; i < v_titles.count(); i++ ) {
		if ( v_titles.at( i ).species.testFlag( spe ) && v_titles.at( i ).title == cv_SpeciesTitle::Breed ) {
			return v_titles.at( i ).name;
		}
	}

	return "Breed";
}

QString StorageTemplate::factionTitle( cv_Species::SpeciesFlag spe ) const {
	for ( int i = 0; i < v_titles.count(); i++ ) {
		if ( v_titles.at( i ).species.testFlag( spe ) && v_titles.at( i ).title == cv_SpeciesTitle::Faction ) {
			return v_titles.at( i ).name;
		}
	}

	return "Faction";
}

void StorageTemplate::appendTitle( cv_SpeciesTitle title ) {
	if ( !v_titles.contains( title ) ) {
		v_titles.append( title );
	}
}

QStringList StorageTemplate::breedNames( cv_Species::SpeciesFlag spe ) const {
	QList< cv_Trait > traits = v_traits;
	QStringList list;

	for ( int i = 0; i < traits.count(); i++ ) {
		if ( traits.at( i ).v_type == cv_Trait::Breed && traits.at( i ).v_category == cv_Trait::CategoryNo ) {
			if ( traits.at( i ).v_species == spe ) {
				// Es kann vorkommen, daß mehrere Eigenschaften doppelt aufgeführt sind. Diese wollen wir natürlich nicht doppelt ausgeben.
				if ( !list.contains( traits.at( i ).v_name ) ) {
					list.append( traits.at( i ).v_name );
				}
			}
		}
	}

	return list;
}

QStringList StorageTemplate::factionNames( cv_Species::SpeciesFlag spe ) const {
	QList< cv_Trait > traits = v_traits;
	QStringList list;

	for ( int i = 0; i < traits.count(); i++ ) {
		if ( traits.at( i ).v_type == cv_Trait::Faction && traits.at( i ).v_category == cv_Trait::CategoryNo ) {
			if ( traits.at( i ).v_species == spe ) {
				// Es kann vorkommen, daß mehrere Eigenschaften doppelt aufgeführt sind. Diese wollen wir natürlich nicht doppelt ausgeben.
				if ( !list.contains( traits.at( i ).v_name ) ) {
					list.append( traits.at( i ).v_name );
				}
			}
		}
	}

	return list;
}


QList< cv_Trait* > StorageTemplate::traits( cv_Trait::Type type, cv_Trait::Category category, cv_Trait::EraFlag era, cv_Trait::AgeFlag age ) const {
	QList< cv_Trait* > traitsPtr;

	for ( int i = 0; i < v_traits.count(); i++ ) {
		if ( v_traits.at( i ).v_type == type && v_traits.at( i ).v_category == category && v_traits.at( i ).v_era.testFlag( era ) && v_traits.at( i ).v_age.testFlag( age ) ) {
			traitsPtr.append( &v_traits[i] );
		}
	}

	if ( traitsPtr.isEmpty() ) {
// 		qDebug() << Q_FUNC_INFO << "Trait Typ" << cv_Trait::toString( type ) << "mit Kategorie" << cv_Trait::toString( category ) << "existiert nicht!";
		throw eTraitNotExisting();
	}

	return traitsPtr;
}
QList< Trait* > StorageTemplate::traits2( cv_Trait::Type type, cv_Trait::Category category, cv_Trait::EraFlag era, cv_Trait::AgeFlag age ) const {
	QList< Trait* > traitsPtr;

	for ( int i = 0; i < v_traits2.count(); i++ ) {
		if ( v_traits2.at( i )->v_type == type &&
				v_traits2.at( i )->v_category == category &&
				v_traits2.at( i )->v_era.testFlag( era ) &&
				v_traits2.at( i )->v_age.testFlag( age )
		   ) {
			traitsPtr.append( v_traits2[i] );
		}
	}

	if ( traitsPtr.isEmpty() ) {
// 		qDebug() << Q_FUNC_INFO << "Trait Typ" << cv_Trait::toString( type ) << "mit Kategorie" << cv_Trait::toString( category ) << "existiert nicht!";
		throw eTraitNotExisting();
	}

	return traitsPtr;
}

QList< cv_Trait* > StorageTemplate::traits( cv_Trait::Type type, cv_Species::SpeciesFlag species ) const {
	QList< cv_Trait* > traitsPtr;

	for ( int i = 0; i < v_traits.count(); i++ ) {
		if ( v_traits.at( i ).v_type == type && v_traits.at( i ).v_species.testFlag( species ) ) {
			traitsPtr.append( &v_traits[i] );
		}
	}

	if ( traitsPtr.isEmpty() ) {
// 		qDebug() << Q_FUNC_INFO << "Trait Typ" << cv_Trait::toString( type ) << "mit Kategorie" << cv_Trait::toString( category ) << "existiert nicht!";
		throw eTraitNotExisting();
	}

	return traitsPtr;
}



cv_Trait StorageTemplate::trait( cv_Trait::Type type, cv_Trait::Category category, QString name ) {
	bool trait_exists = false;

	cv_Trait trait;

	for ( int i = 0; i < v_traits.count(); i++ ) {
		if ( v_traits.at( i ).v_type == type && v_traits.at( i ).v_category == category && v_traits.at( i ).v_name == name ) {
			trait = v_traits.at( i );
			trait_exists = true;

			break;
		}
	}

	if ( !trait_exists ) {
// 		qDebug() << Q_FUNC_INFO << "Trait" << type << category << name << "existiert nicht!";
// 		throw eTraitNotExisting();
	}

	return trait;
}



// void StorageTemplate::setTraits( QList< cv_Trait > traits ) {
// 	v_traits = traits;
// }

void StorageTemplate::appendSpecies( cv_Species species ) {
	v_species.append( species );
}


void StorageTemplate::appendTrait( cv_Trait trait ) {
	bool exists = false;

	for ( int i = 0; i < v_traits.count(); i++ ) {
		if ( v_traits.at( i ).v_type == trait.v_type && v_traits.at( i ).v_name == trait.v_name ) {
			exists = true;
			break;
		}
	}

	if ( !exists ) {
// 		if (trait.custom){
// 			qDebug() << Q_FUNC_INFO << trait.name << "ist besonders";
// 		}
// 		qDebug() << Q_FUNC_INFO << "Füge" << trait.name << "hinzu." << trait.category;
		v_traits.append( trait );
	}

	bool exists2 = false;

	Trait* lcl_trait = new Trait( trait );

	for ( int i = 0; i < v_traits2.count(); i++ ) {
		if ( v_traits2.at( i )->v_type == lcl_trait->v_type && v_traits2.at( i )->v_name == lcl_trait->v_name ) {
			exists2 = true;
			break;
		}
	}
	if ( !exists2 ) {
		v_traits2.append( lcl_trait );
	}
}



void StorageTemplate::appendSuperEffect( cv_SuperEffect effect ) {
	v_superEffects.append( effect );
}

int StorageTemplate::traitMax( cv_Species::Species species, int value ) {
	if ( species == cv_Species::Human ) {
		return Config::traitMax;
	} else {
		for ( int i = 0; i < v_superEffects.count(); i++ ) {
			if ( v_superEffects.at( i ).species == species && v_superEffects.at( i ).value == value ) {
				return v_superEffects.at( i ).traitMax;
			}
		}
	}
}

int StorageTemplate::fuelMax( cv_Species::Species species, int value ) {
	if ( species == cv_Species::Human ) {
		return 0;
	} else {
		for ( int i = 0; i < v_superEffects.count(); i++ ) {
			if ( v_superEffects.at( i ).species == species && v_superEffects.at( i ).value == value ) {
				return v_superEffects.at( i ).fuelMax;
			}
		}
	}
}

int StorageTemplate::fuelPerTurn( cv_Species::Species species, int value ) {
	if ( species == cv_Species::Human ) {
		return 0;
	} else {
		for ( int i = 0; i < v_superEffects.count(); i++ ) {
			if ( v_superEffects.at( i ).species == species && v_superEffects.at( i ).value == value ) {
				return v_superEffects.at( i ).fuelPerTurn;
			}
		}
	}
}


cv_CreationPoints2 StorageTemplate::creationPoints( cv_Species::Species species ) {
	for ( int i = 0; i < v_creationPoints.count(); i++ ) {
		if ( species == v_creationPoints.at( i ).species ) {
			return v_creationPoints.at( i );
		}
	}
}
void StorageTemplate::appendCreationPoints( cv_CreationPoints2 points ) {
	if ( !v_creationPoints.contains( points ) ) {
		v_creationPoints.append( points );
	}
}
