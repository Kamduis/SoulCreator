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

#include "Exceptions/Exception.h"
#include "Config/Config.h"

#include "ReadXml.h"



void ReadXml::openFile( QFile *file ) {
	if ( !file->open( QIODevice::ReadOnly | QIODevice::Text ) ) {
		throw eFileNotOpened( file->fileName(), file->errorString() );
	}
}

void ReadXml::closeFile( QFile *device ) {
	device->close();
}

void ReadXml::readUnknownElement() {
	while ( !atEnd() ) {
		readNext();

		if ( isEndElement() )
			break;

		if ( isStartElement() ) {
			qDebug() << Q_FUNC_INFO << "unbekanntes Element: " << name();
			readUnknownElement();
		}
	}
}

bool ReadXml::checkXmlVersion( QString name, QString version ) {
	if ( name == Config::name() ) {
		if ( version == Config::version() ) {
			return true;
		} else {
			// Unterschiede in der Minor-Version sind ignorierbar, unterschiede in der Major-Version allerdings nicht.
			int major = version.left( version.indexOf( "." ) ).toInt();
			int minor = version.right( version.indexOf( "." ) ).toInt();

			if ( major == Config::versionMajor ){
				throw eXmlOldVersion( Config::version(), version );
			} else {
				throw eXmlTooOldVersion( Config::version(), version );
			}
		}
	} else {
		throw eXmlVersion( Config::name() + Config::version(), name + version );
	}

	return false;
}

