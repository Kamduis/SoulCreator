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

#include "../Datatypes/cv_SuperEffect.h"
#include "../Exceptions/Exception.h"
#include "../Config/Config.h"

#include "ReadXmlTemplate.h"


const QString ReadXmlTemplate::templateFile_base = ":/template/xml/base.xml";
const QString ReadXmlTemplate::templateFile_human = ":/template/xml/human.xml";
const QString ReadXmlTemplate::templateFile_changeling = ":/template/xml/changeling.xml";
const QString ReadXmlTemplate::templateFile_mage = ":/template/xml/mage.xml";
const QString ReadXmlTemplate::templateFile_vampire = ":/template/xml/vampire.xml";
const QString ReadXmlTemplate::templateFile_werewolf = ":/template/xml/werewolf.xml";
// const QString ReadXmlTemplate::templateFile_base = "../resources/xml/base.xml";
// const QString ReadXmlTemplate::templateFile_human = "../resources/xml/human.xml";
// const QString ReadXmlTemplate::templateFile_changeling = "../resources/xml/changeling.xml";
// const QString ReadXmlTemplate::templateFile_mage = "../resources/xml/mage.xml";
// const QString ReadXmlTemplate::templateFile_vampire = "../resources/xml/vampire.xml";
// const QString ReadXmlTemplate::templateFile_werewolf = "../resources/xml/werewolf.xml";

//const QString ReadXmlTemplate::templateFile = "../test.dat";

// QList< cv_Trait > ReadXmlTemplate::traitList;

// QList<cv_Species> ReadXmlTemplate::speciesList;


ReadXmlTemplate::ReadXmlTemplate() : ReadXml() {
	storage = new StorageTemplate();

	file_base = new QFile( ReadXmlTemplate::templateFile_base );
	file_human = new QFile( ReadXmlTemplate::templateFile_human );
	file_changeling = new QFile( ReadXmlTemplate::templateFile_changeling );
	file_mage = new QFile( ReadXmlTemplate::templateFile_mage );
	file_vampire = new QFile( ReadXmlTemplate::templateFile_vampire );
	file_werewolf = new QFile( ReadXmlTemplate::templateFile_werewolf );
}

ReadXmlTemplate::~ReadXmlTemplate() {
	delete file_base;
	delete file_human;
	delete file_changeling;
	delete file_mage;
	delete file_vampire;
	delete file_werewolf;
	delete storage;
}


bool ReadXmlTemplate::read() {
	process( file_base );
	process( file_human );
	process( file_changeling );
	process( file_mage );
	process( file_vampire );
	process( file_werewolf );
}

void ReadXmlTemplate::process( QFile *device ) {
// 	qDebug() << "Lese aus Datei: " << device->fileName();
	readXml( device );
}

void ReadXmlTemplate::readXml( QFile *device ) {
	openFile( device );
	setDevice( device );

	while ( !atEnd() ) {
		readNext();

		if ( isStartElement() ) {
			QString elementName = name().toString();
			QString elementVersion = attributes().value( "version" ).toString();

			if ( checkXmlVersion( elementName, elementVersion ) ) {
				readSoulCreator();
			}
		}
	}

	if ( hasError() ) {
		qDebug() << Q_FUNC_INFO << "Error!";
		throw eXmlError( device->fileName(), errorString() );
	}

	closeFile( file_base );
}

void ReadXmlTemplate::readSoulCreator() {
	while ( !atEnd() ) {
		readNext();

		if ( isEndElement() )
			break;

		if ( isStartElement() ) {
			if ( name() == "traits" ) {
				QString tmp = attributes().value( "species" ).toString();
				cv_Species::SpeciesFlag speciesFlag = cv_Species::toSpecies( tmp );

				if ( speciesFlag != cv_Species::SpeciesNo ) {
// 					qDebug() << "Spezies " << speciesFlag << " gefunden.";

					cv_Species species;
					species.name = tmp;
					species.morale = attributes().value( "morale" ).toString();
					species.supertrait = attributes().value( "supertrait" ).toString();
					species.fuel = attributes().value( "fuel" ).toString();

					// Füge die gerade in der xml-Datei gefundene Spezies einer Liste zu, die später zur Auswahl verwendet werden wird.
					storage->appendSpecies( species );

					readTree( speciesFlag );
				}
			} else
				readUnknownElement();
		}
	}
}

void ReadXmlTemplate::readTree( cv_Species::Species sp ) {
	while ( !atEnd() ) {
		readNext();

		if ( isEndElement() )
			break;

		if ( isStartElement() ) {
			cv_Trait::Type type = cv_Trait::toType( name().toString() );

			if ( type != cv_Trait::TypeNo ) {
// 				qDebug() << "Typ " << type << " gefunden.";
				// Virtues und Vices haben keine Kategorie, also darf ich dort auch nicht so tief den Baum hinuntersteigen. Bei allen anderen aber muß ich erst die Kategorie einlesen.

				if ( type == cv_Trait::Virtue || type == cv_Trait::Vice || type == cv_Trait::Power ) {
					readTraits( sp, type, cv_Trait::CategoryNo );
				} else if ( type == cv_Trait::Super ) {
					readSuperTrait( sp );
				} else {
					readTraits( sp, type );
				}
			} else {
				readUnknownElement();
			}
		}
	}
}

void ReadXmlTemplate::readSuperTrait( cv_Species::Species sp ) {
	while ( !atEnd() ) {
		readNext();

		if ( isEndElement() )
			break;

		if ( isStartElement() ) {
			if ( name() == "supertrait" ) {
				cv_SuperEffect superEffect;
				superEffect.species = sp;
				superEffect.fuelMax = attributes().value( "fuelMax" ).toString().toInt();
				superEffect.fuelPerTurn = attributes().value( "fuelPerTurn" ).toString().toInt();
				superEffect.traitMax = attributes().value( "traitMax" ).toString().toInt();
				superEffect.value = readElementText().toInt();

				storage->appendSuperEffect( superEffect);
			} else
				readUnknownElement();
		}
	}
}


void ReadXmlTemplate::readTraits( cv_Species::Species sp, cv_Trait::Type a ) {

	while ( !atEnd() ) {
		readNext();

		if ( isEndElement() )
			break;

		if ( isStartElement() ) {
			cv_Trait::Category category = cv_Trait::toCategory( name().toString() );
// 			QString categoryString = name().toString();
// 			cv_Trait::Category category = cv_Trait::toCategory( categoryString );
// 			qDebug() << "Kategorie " << categoryString << " gefunden.";
			readTraits( sp, a, category );
		}
	}
}

void ReadXmlTemplate::readTraits( cv_Species::Species sp, cv_Trait::Type a, cv_Trait::Category b ) {
	while ( !atEnd() ) {
		readNext();

		if ( isEndElement() )
			break;

		if ( isStartElement() ) {
			if ( name() == "trait" ) {
				cv_Trait trait = storeTraitData( sp, a, b );
// 				qDebug() << Q_FUNC_INFO << trait.name;

				// Alle Eigenschaften können 0 als Wert haben, auch wenn dies nicht in den XML-Dateien steht.

				if ( !trait.possibleValues.isEmpty() ) {
					// Wenn ich diese Debug-Ausgabe weglasse, dauert der Programmstart \emph{viel} länger.
// 					qDebug() << Q_FUNC_INFO << trait.name << trait.possibleValues;

					trait.possibleValues.append( 0 );
				}

				storage->appendTrait( trait );

// 				// Diese Funktion benötige ich, damit er zum nächsten trait-Eintrag springt.
// 				readNext();

// 				int existsAt = -1;
// 				cv_Trait tmp = readInList(sp, a, b);

// 				for ( int i = 0; i < traitList.count(); i++ ) {
// 										if ( traitList.at( i ).name == tmp.name ) {
// 											existsAt = i;
// 										}
// 				}
// 				if ( existsAt < 0 ) {
// 					traitList.append( tmp );
// 				} else {
// 					// Die Details einer Eigenschaft.
// 					for (int i = 0; i < tmp.details.count(); i++){
// 						cv_TraitDetail traitDetail;
// 						traitDetail.name = tmp.details.at(i).name;
// 						traitDetail.species = sp;
// 						traitList[existsAt].details.append(traitDetail);
// 					}
// 				}
			} else
				readUnknownElement();
		}
	}
}

cv_Trait ReadXmlTemplate::storeTraitData( cv_Species::Species sp, cv_Trait::Type a, cv_Trait::Category b ) {
	// Es besteht die Möglichkeit, daß einzelne Eigenschaften in mehreren XML-DAteien auftauchen. Beispiel: Fertigkeit mit Spezialisierungen speziell für eine Spezies.
	// Momentan löse ich das Problem nicht hier beim Einlesen, sondern bei der Ausgabe in Storage.cpp
// 	QString specialtyName;

	cv_Trait trait;
	trait.species = sp;
	trait.type = a;
	trait.category = b;
	// Keinefalls darf ich zulassen, daß dieser Wert uninitialisiert bleibt, sonst führt das zu Problemen.
	trait.value = 0;

	if ( isStartElement() ) {
		trait.name = attributes().value( "name" ).toString();
// 		qDebug() << Q_FUNC_INFO << trait.name;
		trait.era = cv_Trait::toEra( attributes().value( "era" ).toString() );
		trait.age = cv_Trait::toAge( attributes().value( "age" ).toString() );
		trait.custom = attributes().value( "custom" ).toString() == QString( "true" );

// 		if (trait.custom){
// 			qDebug() << Q_FUNC_INFO << trait.name << "ist besonders!";
// 		}

		while ( !atEnd() ) {
			readNext();

			if ( isEndElement() ) {
				break;
			}

			if ( isStartElement() ) {
				if ( name() == "specialty" ) {
					QString specialtyName = readElementText();
					cv_TraitDetail traitDetail;
					traitDetail.name = specialtyName;
					traitDetail.value = false;
// 					traitDetail.species = sp;
					trait.details.append( traitDetail );
				} else if ( name() == "value" ) {
					int value = readElementText().toInt();
					trait.possibleValues.append( value );
				} else if ( name() == "prerequisite" ) {
					QString text = readElementText();
					trait.prerequisites.append( text );
				} else {
					readUnknownElement();
				}
			}
		}
	}

	return trait;
}


