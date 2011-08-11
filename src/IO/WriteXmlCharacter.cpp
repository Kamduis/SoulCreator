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

#include <QList>
#include <QDebug>

#include "../Exceptions/Exception.h"
#include "../Config/Config.h"

#include "WriteXmlCharacter.h"


WriteXmlCharacter::WriteXmlCharacter() : QXmlStreamWriter() {
	character = StorageCharacter::getInstance();

	setAutoFormatting( true );
}

WriteXmlCharacter::~WriteXmlCharacter() {
	// Da es sich um eine Singleton-Klasse handelt, kann ich sie nicht zerstören.
// 	delete character;
}

void WriteXmlCharacter::write( QFile *file ) {
// 	qDebug() << Q_FUNC_INFO << "Speicherversuch";

	file->open( QIODevice::WriteOnly );
	setDevice( file );

	writeStartDocument();
	writeStartElement( Config::name() );
	writeAttribute( "version", Config::version() );
	writeTextElement( "species", cv_Species::toString(character->species() ));

	writeCharacterTraits();

	writeEndElement();
	writeEndDocument();

	file->close();
}

void WriteXmlCharacter::writeCharacterTraits() {
	QList< cv_Trait::Type > types;
	types.append( cv_Trait::Attribute );
	types.append( cv_Trait::Skill );
	types.append( cv_Trait::Merit );

	QList< cv_Trait::Category > categories;
	categories.append( cv_Trait::Mental );
	categories.append( cv_Trait::Physical );
	categories.append( cv_Trait::Social );

	for ( int i = 0; i < types.count(); i++ ) {
		try {
			writeStartElement( cv_Trait::toString( types.at( i ) ) );
		} catch ( eTraitType &e ) {
			qDebug() << Q_FUNC_INFO << e.message();
		}

		for ( int j = 0; j < categories.count(); j++ ) {
			try {
				writeStartElement( cv_Trait::toString( categories.at( j ) ) );
			} catch ( eTraitCategory &e ) {
				qDebug() << Q_FUNC_INFO << e.message();
			}

			for ( int k = 0; k < character->traits( types.at( i ), categories.at( j ) ).count(); k++ ) {
// 				qDebug() << Q_FUNC_INFO << character->traits( types.at( i ), categories.at( j ) ).at( k ).name;
				writeStartElement( "trait" );
				writeAttribute( "name", character->traits( types.at( i ), categories.at( j ) ).at( k ).name );
				writeAttribute( "value", QString::number( character->traits( types.at( i ), categories.at( j ) ).at( k ).value ) );

// 				qDebug() << Q_FUNC_INFO << character->traits( types.at( i ), categories.at( j ) ).at( k ).details.count();
// 				if ( types.at( i ) == cv_Trait::Skill ) {
					for ( int l = 0; l < character->traits( types.at( i ), categories.at( j ) ).at( k ).details.count(); l++ ) {
// 						qDebug() << Q_FUNC_INFO << character->traits( types.at( i ), categories.at( j ) ).at( k ).details.at( l ).name;
						writeTextElement( "specialty",  character->traits( types.at( i ), categories.at( j ) ).at( k ).details.at( l ).name);
					}
// 				}

				writeEndElement();
			}

			writeEndElement();
		}

		writeEndElement();
	}
}

