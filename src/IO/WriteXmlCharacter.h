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

#ifndef WRITEXMLCHARACTER_H
#define WRITEXMLCHARACTER_H

#include <QFile>
#include <QObject>

#include "../Storage/StorageCharacter.h"
#include "../Datatypes/cv_Species.h"
#include "../Datatypes/cv_Trait.h"

#include <QXmlStreamWriter>


/**
 * @brief Liest die Eigenschaften aus den beigefügten xml-Dateien.
 *
 * Diese Klasse dient dazu einen möglichst simplen Zugriff auf die Eigenschaften der WoD-Charaktere zu bieten. Dazu werden die Eigenschaften und all ihre Zusatzinformationen aus den xml-Dateien gelesen und in Listen gespeichert.
 *
 * Es wird nur in die Datei geschrieben, was auch wirklich benötigt wird (Speicherplatz sparen).
 */
class WriteXmlCharacter : public QObject, public QXmlStreamWriter {
	Q_OBJECT
	
	public:
		WriteXmlCharacter();
		/**
		 *Zerstört das Objekt und gibt alle zugeteilten Ressourcen wieder frei.
		 **/
		~WriteXmlCharacter();

	private:
		StorageCharacter *character;
		
		/**
		 * Schreibt die veränderten Eigenschaften in die Datei.
		 **/
		void writeCharacterTraits();
		/**
		 * Schreibt die Geistesstörungen in die Datei.
		 **/
		void writeCharacterDerangements();

	public slots:
		/**
		 * Schreibt die veränderten Eigenschaften in die Datei.
		 *
		 * \todo Momentan nutze ich nur den Vornamen als Speicher für den gesamten Charakternamen. Ist nicht gerade vernünftig und produziert Leerzeichen am Ende. (Zumindest vermute ich, daß diese Leerzeigen daher stammen).
		 **/
		void write(QFile *file);
};

#endif
