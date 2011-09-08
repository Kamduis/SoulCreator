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

#ifndef READXMLCHARACTER_H
#define READXMLCHARACTER_H

#include <QFile>

#include "../Storage/StorageTemplate.h"
#include "../Storage/StorageCharacter.h"
#include "../Datatypes/cv_Species.h"
#include "../Datatypes/cv_Trait.h"

#include <QObject>
#include "ReadXml.h"


/**
 * @brief Liest die gespeicherten Charakterwerte in das Programm.
 *
 * Diese Klasse dient dazu, einen auf Datenträger gespeicherten Charakter wieder in das Programm zu laden.
 */

class ReadXmlCharacter : public QObject, public ReadXml {
	Q_OBJECT
	
	public:
		ReadXmlCharacter();
		/**
		 *Zerstört das Objekt und gibt alle zugeteilten Ressourcen wieder frei.
		 **/
		~ReadXmlCharacter();

		/**
		 * Diese Methode startet den Lesevorgang.
		 **/
		bool read( QFile *file );

	private:
		/**
		 * Zeiger auf den Programmspeicher, der die Template-Daten enthält.
		 *
		 * \todo Ich weiß nicht, wie gefährlich es ist, diese Zeiger bei Schließen der Kalsse wieder zu löschen. Ist dann auch die statische Variable weg, in der ich alles speichere?
		 **/
		StorageTemplate* storage;
		/**
		 * Zeiger auf den Programmspeicher, der die Charakter-Daten enthält.
		 *
		 * \todo Ich weiß nicht, wie gefährlich es ist, diese Zeiger bei Schließen der Kalsse wieder zu löschen. Ist dann auch die statische Variable weg, in der ich alles speichere?
		 **/
		StorageCharacter* character;
		
		/**
		 * In dieser Liste werden die Eigenschaften zum einfachen Zugriff gespeichert.
		 **/
		static QList< cv_Trait > traitList;
		/**
		 * Lese die Spezies aus dem gespeicherten Charakter.
		 **/
		void readSoulCreator();
		/**
		 * Lese die Eigenschaften aus dem gespeicherten Charakter.
		 **/
		void readTraits( cv_Trait::Type type );
		/**
		 * Lese die Eigenschaften aus dem gespeicherten Charakter.
		 **/
		void readTraits( cv_Trait::Type type, cv_Trait::Category category );

	signals:
		void oldVersion( QString, QString );
};

#endif
