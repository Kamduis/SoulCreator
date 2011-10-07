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

// #include "Config/Config.h"
#include "Exceptions/Exception.h"

#include "StorageTemplate.h"


QList< cv_Species > StorageTemplate::v_species;
QList< cv_SpeciesTitle > StorageTemplate::v_titles;
QList< Trait* > StorageTemplate::v_traits;
QList< cv_SuperEffect > StorageTemplate::v_superEffects;
cv_CreationPointsList StorageTemplate::v_creationPointsList;

StorageTemplate::StorageTemplate( QObject *parent ) : QObject( parent ) {
}

StorageTemplate::~StorageTemplate() {
}


QList< cv_Species > StorageTemplate::species() const {
	return v_species;
}


QStringList StorageTemplate::traitNames( cv_AbstractTrait::Type type, cv_AbstractTrait::Category category, cv_Trait::EraFlag era, cv_Trait::AgeFlag age ) const {
	QList< Trait* > traits = v_traits;
	QStringList list;

	for ( int i = 0; i < traits.count(); i++ ) {
		if ( traits.at( i )->type() == type && traits.at( i )->category() == category ) {
			if ( traits.at( i )->era().testFlag( era ) ) {
				if ( traits.at( i )->age().testFlag( age ) ) {
					// Es kann vorkommen, daß mehrere Eigenschaften doppelt aufgeführt sind. Diese wollen wir natürlich nicht doppelt ausgeben.
					if ( !list.contains( traits.at( i )->name() ) ) {
// 						qDebug() << Q_FUNC_INFO << "Gib aus" << traits.at( i )->name;
						list.append( traits.at( i )->name() );
					}
				}
			}
		}
	}

	return list;
}

QStringList StorageTemplate::virtueNames( cv_Trait::AgeFlag age ) const {
	return traitNames( cv_AbstractTrait::Virtue, cv_AbstractTrait::CategoryNo, cv_Trait::EraAll, age );
}

QStringList StorageTemplate::viceNames( cv_Trait::AgeFlag age ) const {
	return traitNames( cv_AbstractTrait::Vice, cv_AbstractTrait::CategoryNo, cv_Trait::EraAll, age );
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
QStringList StorageTemplate::powerHeaders( cv_Species::SpeciesFlag spe ) const {
	QStringList list;
	
	for ( int i = 0; i < v_titles.count(); i++ ) {
		if ( v_titles.at( i ).species.testFlag( spe ) && v_titles.at( i ).title == cv_SpeciesTitle::Power ) {
			list.append(v_titles.at( i ).name);
		}
	}

	return list;
}

void StorageTemplate::appendTitle( cv_SpeciesTitle title ) {
	if ( !v_titles.contains( title ) ) {
		v_titles.append( title );
	}
}

QStringList StorageTemplate::breedNames( cv_Species::SpeciesFlag spe ) const {
	QList< Trait* > traits = v_traits;
	QStringList list;

	for ( int i = 0; i < traits.count(); i++ ) {
		if ( traits.at( i )->type() == cv_AbstractTrait::Breed && traits.at( i )->category() == cv_AbstractTrait::CategoryNo ) {
			if ( traits.at( i )->species() == spe ) {
				// Es kann vorkommen, daß mehrere Eigenschaften doppelt aufgeführt sind. Diese wollen wir natürlich nicht doppelt ausgeben.
				if ( !list.contains( traits.at( i )->name() ) ) {
					list.append( traits.at( i )->name() );
				}
			}
		}
	}

	return list;
}
QStringList StorageTemplate::factionNames( cv_Species::SpeciesFlag spe ) const {
	QList< Trait* > traits = v_traits;
	QStringList list;

	for ( int i = 0; i < traits.count(); i++ ) {
		if ( traits.at( i )->type() == cv_AbstractTrait::Faction && traits.at( i )->category() == cv_AbstractTrait::CategoryNo ) {
			if ( traits.at( i )->species() == spe ) {
				// Es kann vorkommen, daß mehrere Eigenschaften doppelt aufgeführt sind. Diese wollen wir natürlich nicht doppelt ausgeben.
				if ( !list.contains( traits.at( i )->name() ) ) {
					list.append( traits.at( i )->name() );
				}
			}
		}
	}

	return list;
}



QList< Trait* > StorageTemplate::traits( cv_AbstractTrait::Type type, cv_AbstractTrait::Category category, cv_Trait::EraFlag era, cv_Trait::AgeFlag age ) const {
	QList< Trait* > traitsPtr;

	for ( int i = 0; i < v_traits.count(); i++ ) {
		if ( v_traits.at( i )->type() == type &&
				v_traits.at( i )->category() == category &&
				v_traits.at( i )->era().testFlag( era ) &&
				v_traits.at( i )->age().testFlag( age )
		   ) {
			traitsPtr.append( v_traits[i] );
		}
	}

// 	if ( traitsPtr.isEmpty() ) {
// // 		qDebug() << Q_FUNC_INFO << "Trait Typ" << cv_AbstractTrait::toString( type ) << "mit Kategorie" << cv_AbstractTrait::toString( category ) << "existiert nicht!";
// 		throw eTraitNotExisting();
// 	}

	return traitsPtr;
}

QList< Trait* > StorageTemplate::traits( cv_AbstractTrait::Type type, cv_Species::SpeciesFlag species ) const {
	QList< Trait* > traitsPtr;

// 	qDebug() << Q_FUNC_INFO << "Wird aufgerufen!";

	for ( int i = 0; i < v_traits.count(); i++ ) {
		if ( v_traits.at( i )->type() == type && v_traits.at( i )->species().testFlag( species ) ) {
			traitsPtr.append( v_traits[i] );
// 			qDebug() << Q_FUNC_INFO << "Füge hinzu:" << v_traits.at(i)->name();
		}
	}

	if ( traitsPtr.isEmpty() ) {
// 		qDebug() << Q_FUNC_INFO << "Trait Typ" << cv_AbstractTrait::toString( type ) << "mit Kategorie" << cv_AbstractTrait::toString( category ) << "existiert nicht!";
		throw eTraitNotExisting();
	}

	return traitsPtr;
}


// cv_Trait StorageTemplate::trait( cv_AbstractTrait::Type type, cv_AbstractTrait::Category category, QString name ) {
// 	bool trait_exists = false;
// 
// 	cv_Trait trait;
// 
// 	for ( int i = 0; i < v_traits.count(); i++ ) {
// 		if ( v_traits.at( i ).type() == type && v_traits.at( i ).category() == category && v_traits.at( i ).name() == name ) {
// 			trait = v_traits.at( i );
// 			trait_exists = true;
// 
// 			break;
// 		}
// 	}
// 
// 	if ( !trait_exists ) {
// // 		qDebug() << Q_FUNC_INFO << "Trait" << type << category << name << "existiert nicht!";
// // 		throw eTraitNotExisting();
// 	}
// 
// 	return trait;
// }



// void StorageTemplate::setTraits( QList< cv_Trait > traits ) {
// 	v_traits = traits;
// }

void StorageTemplate::appendSpecies( cv_Species species ) {
	v_species.append( species );
}


void StorageTemplate::appendTrait( cv_Trait trait ) {
	bool exists = false;

	Trait* lcl_trait = new Trait( trait );

	for ( int i = 0; i < v_traits.count(); i++ ) {
		if ( v_traits.at( i )->type() == lcl_trait->type() && v_traits.at( i )->name() == lcl_trait->name() ) {
			exists = true;
			break;
		}
	}
	if ( !exists ) {
		v_traits.append( lcl_trait );
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


cv_CreationPointsList* StorageTemplate::creationPoints() {
	return &v_creationPointsList;
}
void StorageTemplate::appendCreationPoints( cv_CreationPoints points ) {
// 	qDebug() << Q_FUNC_INFO << "Füge creationPoints hinzu!";
	if ( !v_creationPointsList.contains( points ) ) {
		v_creationPointsList.append( points );
	} else {
		qDebug() << Q_FUNC_INFO << "Gibt es schon!";
	}
}
