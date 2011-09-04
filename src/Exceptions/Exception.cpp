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

#include <QObject>
#include <QDebug>

#include "Exception.h"

Exception::Exception( QString message ) {
	setMessage( message );
}

QString Exception::message() {
	return v_message;
}

void Exception::setMessage( QString message ) {
	if ( v_message != message ) {
		v_message = message;
	}
}

QString Exception::description() {
	return v_description;
}

void Exception::setDescription( QString desc ) {
	if ( v_description != desc ) {
		v_description = desc;
	}
}


eNumber::eNumber() : Exception() {
	setMessage( QObject::tr( "Unspecified Problem with a number." ) );
	setDescription( QObject::tr( "An unspecified error occured while handling a number or what should at least be a number." ) );
}

eNotANumber::eNotANumber() : eNumber() {
	setMessage( QObject::tr( "Not a Number." ) );
	setDescription( QObject::tr( "While expecting a number, somethin other than a number was given." ) );
}


eDir::eDir( QString dirName ) : Exception() {
	setMessage( QObject::tr( "Unspecified Problem with a directory." ) );
	setDescription( QObject::tr( "An unspecified error occured while handling directory %1" ).arg( dirName ) );
}

eDirNotCreated::eDirNotCreated( QString dirName ) : eDir() {
	setMessage( QObject::tr( "Cannot create Directory." ) );
	setDescription( QObject::tr( "Directory %1 could not be created" ).arg( dirName ) );
}


eFile::eFile( QString filename ) : Exception() {
	setMessage( QObject::tr( "Unspecified Problem with a file." ) );
	setDescription( QObject::tr( "An unspecified error occured while handling file %1" ).arg( filename ) );
}

eFileNotOpened::eFileNotOpened( QString fileName, QString lastError ) : eFile() {
	setMessage( QObject::tr( "Cannot open File." ) );
	setDescription( QObject::tr( "File %1 could not be opened: %2" ).arg( fileName ).arg( lastError ) );
}

eFileNotDeleted::eFileNotDeleted( QString filename ) : eFile() {
	setMessage( QObject::tr( "Deletion not successful." ) );
	setDescription( QObject::tr( "File %1 could not be deleted." ).arg( filename ) );
}


eXml::eXml( QString error ) : Exception() {
	setMessage( QObject::tr( "XML-Problem" ) );
	setDescription( QObject::tr( "%1" ).arg( error ) );
}

eXmlError::eXmlError( QString fileName, QString error ) : eXml() {
	setMessage( QObject::tr( "XML-Parsing raised error." ) );
	setDescription( QObject::tr( "While trying to parse the XML-File, the following error was raised: \"%2\" in file \"%1\"" ).arg( fileName ).arg( error ) );
}

eXmlVersion::eXmlVersion( QString expected, QString got ) : eXml() {
	setMessage( QObject::tr( "Wrong XML-Version." ) );
	setDescription( QObject::tr( "Got %1 but expected was %2" ).arg( got ).arg( expected ) );
}


eSpecies::eSpecies() : Exception() {
	setMessage( QObject::tr( "Character Species Problem" ) );
	setDescription( QObject::tr( "There is a problem with a character species." ) );
}

eSpeciesNotExisting::eSpeciesNotExisting( cv_Species::SpeciesFlag species ) : eSpecies() {
	setMessage( QObject::tr( "Character Species Problem" ) );
	setDescription( QObject::tr( "Species %1 is missing." ).arg( species ) );
}

eSpeciesNotExisting::eSpeciesNotExisting() : eSpecies() {
	setMessage( QObject::tr( "Character Species Problem" ) );
	setDescription( QObject::tr( "Species is missing." ) );
}


eTrait::eTrait() : Exception() {
	setMessage( QObject::tr( "Character Trait Problem" ) );
	setDescription( QObject::tr( "There is a problem with a character trait." ) );
}

eTraitNotExisting::eTraitNotExisting() : eTrait() {
	setMessage( QObject::tr( "Character Trait Problem" ) );
	setDescription( QObject::tr( "Trait is missing." ) );
}

eTraitCategory::eTraitCategory( cv_Trait::Category category ) : eTrait() {
	setMessage( QObject::tr( "Category of a Trait not valid" ) );
	setDescription( QObject::tr( "The Category %1 is not valid at this point." ).arg( QString::number( category ) ) );
}

eTraitType::eTraitType( cv_Trait::Type type ) : eTrait() {
	setMessage( QObject::tr( "Type of a Trait not valid" ) );
	setDescription( QObject::tr( "The Type %1 is not valid at this point." ).arg( QString::number( type ) ) );
}


ePrint::ePrint() : Exception() {
	setMessage( QObject::tr( "Printing Problem" ) );
	setDescription( QObject::tr( "There is a problem while trying to print the character sheet." ) );
}

eTraitsExceedSheetCapacity::eTraitsExceedSheetCapacity( cv_Trait::Type type, int maxNumber ) : ePrint() {
	setMessage( QObject::tr( "Too many %1 to print on character sheet." ).arg( cv_Trait::toString( type, true ) ) );
	setDescription( QObject::tr( "Trying to print too many %1. The character sheet hat only room for %2" ).arg( cv_Trait::toString( type, true ) ).arg( maxNumber ) );
}

eValueExceedsSheetCapacity::eValueExceedsSheetCapacity( int value, QString name ) : ePrint() {
	setMessage( QObject::tr( "A value exceeds the capacity of the Charactersheet." ) );
	setDescription( QObject::tr( "The character sheet has no room for %1 %2" ).arg( QString::number( value ) ).arg( name ) );
}


eEntry::eEntry() : Exception() {
	setMessage( QObject::tr( "Entry Problem." ) );
	setDescription( QObject::tr( "There is a problem with an expected Input." ) );
}

eUserEntry::eUserEntry() : eEntry() {
	setMessage( QObject::tr( "User Entry Problem." ) );
	setDescription( QObject::tr( "There is a problem with an expected User Input." ) );
}

eMissingUserEntry::eMissingUserEntry() : eUserEntry() {
	setMessage( QObject::tr( "Missing User Entry." ) );
	setDescription( QObject::tr( "An expected User Input is missing." ) );
}


eWerewolfShape::eWerewolfShape() {
	setMessage( QObject::tr( "Problem with werewolf shape." ) );
	setDescription( QObject::tr( "A Probklem regarding a shape of the werewolf has occured." ) );
}
eWerewolfShapeNotExisting::eWerewolfShapeNotExisting( cv_Shape::WerewolfShape shape ): eWerewolfShape() {
	setMessage( QObject::tr( "Shape not existing." ) );
	setDescription( QObject::tr( "The chosen Shape %1 does not exist." ).arg(shape) );
}
eWerewolfShapeNotExisting::eWerewolfShapeNotExisting( QString shape ): eWerewolfShape() {
	setMessage( QObject::tr( "Shape not existing." ) );
	setDescription( QObject::tr( "The chosen Shape %1 does not exist." ).arg(shape) );
}
