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

#include "../Exceptions/Exception.h"
#include "../Config/Config.h"

#include "ReadXmlCharacter.h"


QList< cv_Trait > ReadXmlCharacter::traitList;

ReadXmlCharacter::ReadXmlCharacter() : QObject(), ReadXml() {
	storage = new StorageTemplate();
	character = StorageCharacter::getInstance();
}

ReadXmlCharacter::~ReadXmlCharacter() {
	// Da es sich um eine Singleton-Klasse handelt, kann ich sie nicht zerstören.
// 	delete character;
	delete storage;
}


bool ReadXmlCharacter::read( QFile *file ) {
	openFile( file );

	setDevice( file );

	while ( !atEnd() ) {
		readNext();

		if ( isStartElement() ) {
			QString elementName = name().toString();
			QString elementVersion = attributes().value( "version" ).toString();

			cv_Identity id;

			try {
				if ( checkXmlVersion( elementName, elementVersion ) ) {
					readSoulCreator( &id );
				}
			} catch ( eXmlOldVersion &e ) {
				emit oldVersion( e.message(), e.description() );

				readSoulCreator( &id );
			}

			character->setRealIdentity( id );
		}
	}

	if ( hasError() ) {
		qDebug() << Q_FUNC_INFO << "Error!";
		throw eXmlError( file->fileName(), errorString() );
	}

	closeFile( file );
}

void ReadXmlCharacter::readSoulCreator( cv_Identity* id ) {
	while ( !atEnd() ) {
		readNext();

		if ( isEndElement() )
			break;

		if ( isStartElement() ) {
			QString elementName = name().toString();

			if ( elementName == "species" ) {
				QString speciesName = readElementText();
				character->setSpecies( cv_Species::toSpecies( speciesName ) );
			} else if ( elementName == "forenames" ) {
				QString characterNames = readElementText();
				id->foreNames = characterNames.split( " " );
			} else if ( elementName == "surename" ) {
				QString characterName = readElementText();
				id->sureName = characterName;
			} else if ( elementName == "honorname" ) {
				QString characterName = readElementText();
				id->honorificName = characterName;
			} else if ( elementName == "nickname" ) {
				QString characterName = readElementText();
				id->nickName = characterName;
			} else if ( elementName == "supername" ) {
				QString characterName = readElementText();
				id->supernaturalName = characterName;
			} else if ( elementName == "gender" ) {
				QString characterGender = readElementText();
				id->gender = cv_Identity::toGender( characterGender );
			} else if ( elementName == "virtue" ) {
				character->setVirtue( readElementText() );
			} else if ( elementName == "vice" ) {
				character->setVice( readElementText() );
			} else if ( elementName == "breed" ) {
				character->setBreed( readElementText() );
			} else if ( elementName == "faction" ) {
				character->setFaction( readElementText() );
			} else if ( elementName == "superTrait" ) {
				int superTraitValue = readElementText().toInt();
				character->setSuperTrait( superTraitValue );
			} else if ( elementName == "morality" ) {
				int moralityValue = readElementText().toInt();
				character->setMorality( moralityValue );
			} else if ( elementName == "armor" ) {
				int armorGeneral = attributes().value("general").toString().toInt();
				int armorFirearms = attributes().value("firearms").toString().toInt();
				character->setArmor( armorGeneral, armorFirearms );
				readUnknownElement();
			} else if ( elementName != cv_Trait::toXmlString( cv_Trait::TypeNo ) ) {
// 				qDebug() << Q_FUNC_INFO << elementName << "!";
				readTraits( cv_Trait::toType( elementName ) );
			} else {
				readUnknownElement();
			}
		}
	}
}

void ReadXmlCharacter::readTraits( cv_Trait::Type type ) {
	while ( !atEnd() ) {
		readNext();

		if ( isEndElement() )
			break;

		if ( isStartElement() ) {
			QString elementName = name().toString();
			readTraits( type, cv_Trait::toCategory( elementName ) );
		}
	}
}

void ReadXmlCharacter::readTraits( cv_Trait::Type type, cv_Trait::Category category ) {
	while ( !atEnd() ) {
		readNext();

		if ( isEndElement() )
			break;

		if ( isStartElement() ) {
			QString elementName = name().toString();

			if ( type == cv_Trait::Derangement && elementName == "derangement" ) {
				cv_Derangement derangement;
				derangement.name = attributes().value( "name" ).toString();
				derangement.type = type;
				derangement.category = category;
				derangement.morality = attributes().value( "morality" ).toString().toInt();

				character->addDerangement( derangement );
				
				while ( !atEnd() ) {
					readNext();

					if ( isEndElement() )
						break;

					if ( isStartElement() ) {
						readUnknownElement();
					}
				}
			} else if ( elementName == "trait" ) {
				cv_Trait trait;
				trait.name = attributes().value( "name" ).toString();
				trait.type = type;
				trait.category = category;
				trait.value = attributes().value( "value" ).toString().toInt();
				QString customText = attributes().value( "custom" ).toString();

				if ( customText.isEmpty() ) {
// 					trait.custom = false;
					trait.customText = "";
				} else {
// 					qDebug() << Q_FUNC_INFO << customText;
// 					trait.custom = true;
					trait.customText = customText;
				}

				QList< cv_TraitDetail > list;

				while ( !atEnd() ) {
					readNext();

					if ( isEndElement() )
						break;

					if ( isStartElement() ) {
						QString elementName = name().toString();

						if ( elementName == "specialty" ) {
							QString specialty = readElementText();
							cv_TraitDetail detail;
							detail.name = specialty;
							detail.value = true;
							// An Liste anfügen.
							list.append( detail );
						} else
							readUnknownElement();
					}
				}

				trait.details = list;

				character->modifyTrait( trait );
			} else
				readUnknownElement();
		}
	}
}


