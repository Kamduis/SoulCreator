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
	writeTextElement( "species", cv_Species::toString( character->species() ) );
	writeTextElement( "name", character->realIdentity->birthName() );
	writeTextElement( "virtue", character->virtue() );
	writeTextElement( "vice", character->vice() );
	writeTextElement( "breed", character->breed() );
	writeTextElement( "faction", character->faction() );
	writeTextElement( "superTrait", QString::number( character->superTrait() ) );
	writeTextElement( "morality", QString::number( character->morality() ) );

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
	types.append( cv_Trait::Power );

	QList< cv_Trait::Category > categories;

	QList< cv_Trait > list;

	for ( int i = 0; i < types.count(); i++ ) {
		try {
			writeStartElement( cv_Trait::toXmlString( types.at( i ) ) );
		} catch ( eTraitType &e ) {
			qDebug() << Q_FUNC_INFO << e.message();
		}

		// Liste der Kategorien ist je nach Typ unterschiedlich
		categories = cv_Trait::getCategoryList( types.at(i) );

		for ( int j = 0; j < categories.count(); j++ ) {
			list = character->traits( types.at( i ), categories.at( j ) );

// 			qDebug() << Q_FUNC_INFO << "Type" << types.at(i) << "Category" << categories.at(j) << list.count();
// 			if ( !list.isEmpty() ) {
			try {
				writeStartElement( cv_Trait::toXmlString( categories.at( j ) ) );
			} catch ( eTraitCategory &e ) {
				qDebug() << Q_FUNC_INFO << e.message();
			}

			for ( int k = 0; k < list.count(); k++ ) {
				// Eigenscahften müssen nur dann gespeichert werden, wenn ihr Wert != 0 ist.
				if ( list.at( k ).value != 0 ) {
// 					qDebug() << Q_FUNC_INFO << list.at( k ).name;
					writeStartElement( "trait" );
					writeAttribute( "name", list.at( k ).name );
					writeAttribute( "value", QString::number( list.at( k ).value ) );

					qDebug() << Q_FUNC_INFO << list.at( k ).name << list.at( k ).custom;
					if ( list.at( k ).custom ) {
						writeAttribute( "custom", list.at( k ).customText );
					}

// 					qDebug() << Q_FUNC_INFO << list.at( k ).details.count();
// 					if ( types.at( i ) == cv_Trait::Skill ) {
					for ( int l = 0; l < list.at( k ).details.count(); l++ ) {
// 						qDebug() << Q_FUNC_INFO << list.at( k ).details.at( l ).name;
						writeTextElement( "specialty",  list.at( k ).details.at( l ).name );
					}
// 					}t

					writeEndElement();
				}
			}
// 			}

			writeEndElement();
		}

		writeEndElement();
	}
}

