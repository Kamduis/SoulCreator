/**
 * \file
 * \author Victor von Rhein <victor@caern.de>
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

#ifndef READXML_H
#define READXML_H

#include <QFile>

// #include "Datatypes/cv_Species.h"
// #include "Datatypes/cv_Trait.h"

#include <QXmlStreamReader>


/**
 * @brief List aus Xml-Dateien.
 *
 * Diese Klasse bietet die grundlegendsten Funktionen für das Lesen aus Xml-Dateien.
 */

class ReadXml : public QXmlStreamReader{
	public:
		/**
		 * Öffnet die im Argument übergebe Datei.
		 *
		 * \exception eFileNotOpen Diese Ausnahme wird geworfen, wenn die XML-DaTei nicht geöffnet werden konnte.
		 **/
		void openFile(QFile *device);
		/**
		 * Schließt die im Argument übergebe Datei.
		 **/
		void closeFile(QFile *device);
		/**
		 * Diese Funktion wird immer dann aufgerufen, wenn ein Zweig mit unbekanntem Namen entsdeckt wird. Diese Funktion marschiert bis zum Ende dieses Zweiges.
		 **/
		void readUnknownElement();
		bool checkXmlVersion( QString name, QString version);
};

#endif
