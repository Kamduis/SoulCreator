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

#include "../Config/Config.h"
#include "../Exceptions/Exception.h"

#include "StorageTemplate.h"


QList< cv_Species > StorageTemplate::v_species;
QList< cv_Trait > StorageTemplate::v_traits;
QList< cv_SuperEffect > StorageTemplate::v_superEffects;


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
		if ( traits.at( i ).type == type && traits.at( i ).category == category ) {
			if ( traits.at( i ).era.testFlag( era ) ) {
				if ( traits.at( i ).age.testFlag( age ) ) {
					// Es kann vorkommen, daß mehrere Eigenschaften doppelt aufgeführt sind. Diese wollen wir natürlich nicht doppelt ausgeben.
					if ( !list.contains( traits.at( i ).name ) ) {
// 						qDebug() << Q_FUNC_INFO << "Gib aus" << traits.at( i ).name;
						list.append( traits.at( i ).name );
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

QList< cv_Trait > StorageTemplate::attributes( cv_Trait::Category category, cv_Trait::EraFlag era, cv_Trait::AgeFlag age ) const {
	return traits( cv_Trait::Attribute, category, era, age );
}

// QStringList StorageTemplate::attributeNames( cv_Trait::Category category ) const {
// 	return traitNames( cv_Trait::Attribute, category, cv_Trait::EraAll, cv_Trait::AgeAll );
// }

QList< cv_Trait > StorageTemplate::skills( cv_Trait::Category category, cv_Trait::EraFlag era, cv_Trait::AgeFlag age ) const {
	return traits( cv_Trait::Skill, category, era, age );
}

// QStringList StorageTemplate::skillNames( cv_Trait::Category category, cv_Trait::EraFlag era, cv_Trait::AgeFlag age ) const {
// 	return traitNames( cv_Trait::Skill, category, era, age );
// }

QList< cv_TraitDetail > StorageTemplate::skillSpecialties( QString skillName ) const {
	QList< cv_TraitDetail > list;

	for ( int i = 0; i < v_traits.count(); i++ ) {
		if ( v_traits.at( i ).name == skillName ) {
			for ( int j = 0; j < v_traits.at( i ).details.count(); j++ ) {
				// Es kann vorkommen, daß mehrere Spezialisierungen doppelt aufgeführt sind. Diese wollen wir natürlich nicht doppelt ausgeben.
				if ( !list.contains( v_traits.at( i ).details.at( j ) ) ) {
					list.append( v_traits.at( i ).details.at( j ) );
				}
			}
		}
	}

	return list;
}

// QStringList StorageTemplate::meritNames( cv_Trait::Category category ) const {
// 	return traitNames( cv_Trait::Merit, category, cv_Trait::EraAll, cv_Trait::AgeAll );
// }


QList< cv_Trait > StorageTemplate::merits( cv_Trait::Category category ) const {
	QList< cv_Trait > list;

	for ( int i = 0; i < v_traits.count(); i++ ) {
		if ( v_traits.at( i ).type == cv_Trait::Merit && v_traits.at( i ).category == category ) {
			// Es kann vorkommen, daß mehrere Eigenschaften doppelt aufgeführt sind. Diese wollen wir natürlich nicht doppelt ausgeben.
			if ( !list.contains( v_traits.at( i ) ) ) {
				list.append( v_traits.at( i ) );
			}
		}
	}

	return list;
}

QList< int > StorageTemplate::meritValues( QString meritName ) const {
	QList< cv_Trait > traits = v_traits;
	QList< int > list;

	for ( int i = 0; i < traits.count(); i++ ) {
		if ( traits.at( i ).type == cv_Trait::Merit && traits.at( i ).name == meritName ) {
			for ( int j = 0; j < traits.at( i ).possibleValues.count(); j++ ) {
				// Es kann vorkommen, daß mehrere Werte doppelt aufgeführt sind. Diese wollen wir natürlich nicht doppelt ausgeben.
				if ( !list.contains( traits.at( i ).possibleValues.at( j ) ) ) {
					list.append( traits.at( i ).possibleValues.at( j ) );
				}
			}
		}
	}

	return list;
}

QString StorageTemplate::meritPrerequisites( QString meritName ) const {
	QList< cv_Trait > traits = v_traits;
	QString text = "";

	for ( int i = 0; i < traits.count(); i++ ) {
		if ( traits.at( i ).type == cv_Trait::Merit && traits.at( i ).name == meritName ) {
			text.append( traits.at( i ).prerequisites );
		}
	}

	return text;
}

QList< cv_Trait > StorageTemplate::powers( cv_Trait::Category category ) const {
	QList< cv_Trait > list;

	for ( int i = 0; i < v_traits.count(); i++ ) {
		if ( v_traits.at( i ).type == cv_Trait::Power && v_traits.at( i ).category == category ) {
			// Es kann vorkommen, daß mehrere Eigenschaften doppelt aufgeführt sind. Diese wollen wir natürlich nicht doppelt ausgeben.
			if ( !list.contains( v_traits.at( i ) ) ) {
				list.append( v_traits.at( i ) );
			}
		}
	}

	return list;
}

QList< cv_Trait > StorageTemplate::traits( cv_Trait::Type type, cv_Trait::Category category, cv_Trait::EraFlag era, cv_Trait::AgeFlag age ) const {
	QList< cv_Trait > traits;
	cv_Trait trait;

	for ( int i = 0; i < v_traits.count(); i++ ) {
		if ( v_traits.at( i ).type == type && v_traits.at( i ).category == category && v_traits.at( i ).era.testFlag( era ) && v_traits.at( i ).age.testFlag( age ) ) {
			trait = v_traits.at( i );
			traits.append( trait );
		}
	}

	if ( traits.isEmpty() ) {
// 		qDebug() << Q_FUNC_INFO << "Trait Typ" << type << "mit Kategorie" << category << "existiert nicht!";
// 		throw eTraitNotExisting();
	}

	return traits;
}



cv_Trait StorageTemplate::trait( cv_Trait::Type type, cv_Trait::Category category, QString name ) {
	bool trait_exists = false;

	cv_Trait trait;

	for ( int i = 0; i < v_traits.count(); i++ ) {
		if ( v_traits.at( i ).type == type && v_traits.at( i ).category == category && v_traits.at( i ).name == name ) {
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
		if ( v_traits.at( i ).type == trait.type && v_traits.at( i ).name == trait.name ) {
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





// QStringList StorageTemplate::speciesNames(){
// 	cv_Species species;
// 	QStringList list;
//
// 	for (int i = 0; i < readTemplate->speciesList.count(); i++){
// 		list.append(readTemplate->speciesList.at(i).name);
// 	}
//
// 	return list;
// }
//
// //QStringList StorageTemplate::virtueNames(Character::Age age){
// //	QStringList list;
// //	QList<Trait> traits = readTemplate->traitList;
// //
// //	for (int i = 0; i < traits.count(); i++){
// //		if (traits.at(i).type == Trait::Virtue && traits.at(i).age == age){
// //			list.append(traits.at(i).name);
// //		}
// //	}
// //
// //	return list;
// //}
//
// //QStringList StorageTemplate::viceNames(Character::Age age){
// //	QStringList list;
// //	QList<Trait> traits = readTemplate->traitList;
// //
// //	for (int i = 0; i < traits.count(); i++){
// //		if (traits.at(i).type == Trait::Vice && traits.at(i).age == age){
// //			list.append(traits.at(i).name);
// //		}
// //	}
// //
// //	return list;
// //}
//
// QList<cv_Trait> StorageTemplate::attributes(cv_Trait::Categories categories){
// //	Trait::Categories chooseCategories;
// //
// //	if (categories == Trait::CategoryAll)
// //		chooseCategory = Trait::Category(Trait::Mental | Trait::Physical | Trait::Social);
// //	else
// //		chooseCategory = category;
//
//
// 	QList<cv_Trait> list;
// 	QList<cv_Trait> traits = readTemplate->traitList;
//
// 	for (int i = 0; i < traits.count(); i++){
// 		if (traits.at(i).type == cv_Trait::Attribute && traits.at(i).categories == categories){
// //			qDebug() << "Attribut: " << traits.at(i).name;
// 			cv_Trait trait;
// 			trait = traits.at(i);
// 			list.append(trait);
// 		}
// 	}
//
// 	return list;
// }
//
// QStringList StorageTemplate::attributeNames(cv_Trait::Categories categories){
// 	QStringList list;
// 	QList<cv_Trait> traits = attributes(categories);
//
// 	for (int i = 0; i < traits.count(); i++){
// 		list.append(traits.at(i).name);
// 	}
//
// 	return list;
//
// //	QStringList list;
// //	QList<Trait> traits = readTemplate->traitList;
// //
// //	for (int i = 0; i < traits.count(); i++){
// //		if (traits.at(i).type == Trait::Attribute && traits.at(i).categories == categories){
// //			list.append(traits.at(i).name);
// //		}
// //	}
// //
// //	return list;
// }
//
// QStringList StorageTemplate::skillNames(cv_Trait::Categories categories){
// 	QStringList list;
// 	QList<cv_Trait> traits = readTemplate->traitList;
//
// 	for (int i = 0; i < traits.count(); i++){
// 		if (traits.at(i).type == cv_Trait::Skill && traits.at(i).categories == categories){
// 			list.append(traits.at(i).name);
// 		}
// 	}
//
// 	return list;
// }
//
// QStringList StorageTemplate::skillNames(cv_Trait::Categories categories, cv_Trait::Era era, cv_Trait::Age age){
// 	QStringList list;
// 	QList<cv_Trait> traits = readTemplate->traitList;
//
// 	for (int i = 0; i < traits.count(); i++){
// //		if (traits.at(i).type == cv_Trait::Skill && traits.at(i).categories == categories && traits.at(i).era == era && traits.at(i).age == age){
// 		if (traits.at(i).type == cv_Trait::Skill && traits.at(i).categories == categories && traits.at(i).era == era){
// 			list.append(traits.at(i).name);
// 		}
// 	}
//
// 	return list;
// }
//
// QStringList StorageTemplate::skillSpecialties(QString skillName, cv_Species::Species species){
// 	QStringList list;
// 	QList<cv_Trait> traits = readTemplate->traitList;
//
// 	for (int i = 0; i < traits.count(); i++){
// 		if (traits.at(i).type == cv_Trait::Skill && traits.at(i).name == skillName){
// 			for (int j = 0; j < traits.at(i).details.count(); j++){
// 				if (traits.at(i).details.at(j).species == species)
// 					list.append(traits.at(i).details.at(j).name);
// 			}
// 		}
// 	}
//
// 	return list;
// }
//
// //QStringList StorageTemplate::meritNames(Character::Species species){
// //	QStringList list;
// //	QList<Trait> traits = readTemplate->traitList;
// //
// //	for (int i = 0; i < traits.count(); i++){
// //		if (traits.at(i).type == Trait::Merit && (traits.at(i).species == species || traits.at(i).species == Character::SpeciesAll)){
// //			list.append(traits.at(i).name);
// //		}
// //	}
// //
// //	return list;
// //}
//
// //QString StorageTemplate::showName(Name::Category category){
// //	for (int i = 0; i < storedNames.count(); i++){
// //		if (storedNames.at(i).category == category){
// ////			qDebug() << "Speichere den Namen";
// //			return storedNames.at(i).name;
// //		}
// //	}
// //
// ////	qDebug() << "Speichere den Namen NICHT!";
// //	return "";
// //}
//
// //void StorageTemplate::storeName(QString name, Name::Category category){
// //	for (int i = 0; i < storedNames.count(); i++){
// //		if (storedNames.at(i).category == category){
// //			storedNames[i].name = name;
// //			return;
// //		}
// //	}
// //
// //	Name newName;
// //	newName.category = category;
// //	newName.name = name;
// //	storedNames.append(newName);
// //}
//
// void StorageTemplate::storeTrait(cv_Trait trait, bool replace){
// 	bool traitExists = false;
//
// 	for (int i = 0; i < StorageTemplate::storedTraits.count(); i++){
// 		if ((replace || StorageTemplate::storedTraits.at(i).name == trait.name) && StorageTemplate::storedTraits.at(i).type == trait.type){
// //			qDebug() << "Verändere bereits vorhandene Eigenschaft zu Wert " << value();
// 			StorageTemplate::storedTraits.replace(i, trait);
// //			qDebug() << "Im Speicher steht damit: " << StorageTemplate::storedTraits.at(i).value;
// 			traitExists = true;
// 			break;
// 		}
// 	}
//
// 	if (!traitExists){
// //		qDebug() << "Ergänze neue Eigenschaft mit Wert: " << value();
// 		StorageTemplate::storedTraits.append(trait);
// //		qDebug() << "Im Speicher steht damit: " << StorageTemplate::storedTraits.at(StorageTemplate::storedTraits.count()-1).value;
// 	}
// }
