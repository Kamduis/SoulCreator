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

ReadXmlCharacter::ReadXmlCharacter() : ReadXml() {
	storage = new StorageTemplate();
	character = new StorageCharacter();
}

ReadXmlCharacter::~ReadXmlCharacter() {
	delete character;
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

			if ( checkXmlVersion( elementName, elementVersion ) ) {
				readSpecies();
			}
		}
	}

	if ( hasError() ) {
		qDebug() << Q_FUNC_INFO << "Error!";
		throw eXmlError( file->fileName(), errorString() );
	}

	closeFile( file );
}

void ReadXmlCharacter::readSpecies() {
	while ( !atEnd() ) {
		readNext();

		if ( isEndElement() )
			break;

		if ( isStartElement() ) {
			if ( name() == "species" ) {
				QString speciesName = readElementText();

				cv_Species species;
				for (int i = 0; i < storage->species().count(); i++ ){
					if (speciesName == storage->species().at(i).name) {
						species = storage->species().at(i);
						species.name = speciesName;
						break;
					}
				}

				character->setSpecies(species);
			} else
				readUnknownElement();
		}
	}
}

