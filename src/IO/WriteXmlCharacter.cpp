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

#include <QList>
#include <QDebug>

#include "Exceptions/Exception.h"
// #include "Config/Config.h"

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
	// Es wird nur die echte Identität (Index 0) berücksichtigt.
	writeStartElement( "identities" );
	writeStartElement( "identity" );
	writeAttribute( "forenames", character->identities().at( 0 ).foreNames.join( " " ) );
	writeAttribute( "surename", character->identities().at( 0 ).sureName );
	writeAttribute( "honorname", character->identities().at( 0 ).honorificName );
	writeAttribute( "nickname", character->identities().at( 0 ).nickName );
	writeAttribute( "supername", character->identities().at( 0 ).supernaturalName );
	writeAttribute( "gender", cv_Identity::toXmlString( character->identities().at( 0 ).gender ) );
	writeEndElement();
	writeEndElement();
	writeTextElement( "virtue", character->virtue() );
	writeTextElement( "vice", character->vice() );
	writeTextElement( "breed", character->breed() );
	writeTextElement( "faction", character->faction() );
	writeTextElement( "superTrait", QString::number( character->superTrait() ) );
	writeTextElement( "morality", QString::number( character->morality() ) );
	writeStartElement( "armor" );
	writeAttribute( "general", QString::number( character->armorGeneral() ) );
	writeAttribute( "firearms", QString::number( character->armorFirearms() ) );
	writeEndElement();

	writeCharacterTraits();

	writeCharacterDerangements();

	writeEndElement();
	writeEndDocument();

	file->close();
}

void WriteXmlCharacter::writeCharacterTraits() {
	QList< cv_AbstractTrait::Type > types;
	types.append( cv_AbstractTrait::Attribute );
	types.append( cv_AbstractTrait::Skill );
	types.append( cv_AbstractTrait::Merit );
	types.append( cv_AbstractTrait::Power );
	types.append( cv_AbstractTrait::Flaw );

	QList< cv_AbstractTrait::Category > category;

	QList< Trait* > list;

	for ( int i = 0; i < types.count(); i++ ) {
		try {
			writeStartElement( cv_AbstractTrait::toXmlString( types.at( i ) ) );
		} catch ( eTraitType &e ) {
			qDebug() << Q_FUNC_INFO << e.message();
		}

		// Liste der Kategorien ist je nach Typ unterschiedlich
		category = cv_AbstractTrait::getCategoryList( types.at( i ) );

		for ( int j = 0; j < category.count(); j++ ) {
			list = character->traits( types.at( i ), category.at( j ) );

// 			qDebug() << Q_FUNC_INFO << "Type" << types.at(i) << "Category" << categories.at(j) << list.count();
// 			if ( !list.isEmpty() ) {

			try {
				writeStartElement( cv_AbstractTrait::toXmlString( category.at( j ) ) );
			} catch ( eTraitCategory &e ) {
				qDebug() << Q_FUNC_INFO << e.message();
			}

			for ( int k = 0; k < list.count(); k++ ) {
				// Eigenscahften müssen nur dann gespeichert werden, wenn ihr Wert != 0 ist.
				if ( list.at( k )->value() != 0 ) {
// 					qDebug() << Q_FUNC_INFO << list.at( k )->name;
					writeStartElement( "trait" );
					writeAttribute( "name", list.at( k )->name() );
					writeAttribute( "value", QString::number( list.at( k )->value() ) );

// 					qDebug() << Q_FUNC_INFO << list.at( k ).name << list.at( k )->custom;

					if ( list.at( k )->custom() ) {
						writeAttribute( "custom", list.at( k )->customText() );
					}

// 					qDebug() << Q_FUNC_INFO << list.at( k )->details.count();
// 					if ( types.at( i ) == cv_AbstractTrait::Skill ) {
					for ( int l = 0; l < list.at( k )->details().count(); l++ ) {
// 						qDebug() << Q_FUNC_INFO << list.at( k )->details.at( l ).name;
						writeTextElement( "specialty",  list.at( k )->details().at( l ).name );
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

void WriteXmlCharacter::writeCharacterDerangements() {
	QList< cv_Derangement* > list;

	try {
		writeStartElement( cv_AbstractTrait::toXmlString( cv_AbstractTrait::Derangement ) );
	} catch ( eTraitType &e ) {
		qDebug() << Q_FUNC_INFO << e.message();
	}

	// Liste der Kategorien ist je nach Typ unterschiedlich
	QList< cv_AbstractTrait::Category > category;

	category = cv_AbstractTrait::getCategoryList( cv_AbstractTrait::Derangement );

	for ( int j = 0; j < category.count(); j++ ) {
		list = character->derangements( category.at( j ) );

		qDebug() << Q_FUNC_INFO << list.count();

		try {
			writeStartElement( cv_AbstractTrait::toXmlString( category.at( j ) ) );
		} catch ( eTraitCategory &e ) {
			qDebug() << Q_FUNC_INFO << e.message();
		}

		for ( int k = 0; k < list.count(); k++ ) {
// 					qDebug() << Q_FUNC_INFO << list.at( k )->name;
			writeStartElement( "derangement" );
			writeAttribute( "name", list.at( k )->name() );
			writeAttribute( "morality", QString::number( list.at( k )->morality() ) );

			writeEndElement();
		}

		writeEndElement();
	}

	writeEndElement();
}

