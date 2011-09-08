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

#ifndef READXMLTEMPLATE_H
#define READXMLTEMPLATE_H

#include <QFile>

#include "../Storage/StorageTemplate.h"
#include "../Datatypes/cv_Species.h"
#include "../Datatypes/cv_Trait.h"

#include <QObject>
#include "ReadXml.h"


/**
 * @brief Liest die Eigenschaften aus den beigefügten xml-Dateien.
 *
 * Diese Klasse dient dazu einen möglichst simplen Zugriff auf die Eigenschaften der WoD-Charaktere zu bieten. Dazu werden die Eigenschaften und all ihre Zusatzinformationen aus den xml-Dateien gelesen und in Listen gespeichert.
 */

class ReadXmlTemplate : public QObject, public ReadXml {
	Q_OBJECT
	
	public:
		ReadXmlTemplate();
		/**
		 *Zerstört das Objekt und gibt alle zugeteilten Ressourcen wieder frei.
		 **/
		~ReadXmlTemplate();

// 		/**
// 		 * In dieser Liste werden die Eigenschaften zum eifanchen Zugriff gespeichert.
// 		 **/
// 		static QList<cv_Trait> traitList;
// 		/**
// 		 * In dieser Liste werden die zur Verfügung stehenden Spezies gespeichert.
// 		 **/
// 		static QList<cv_Species> speciesList;

		/**
		 * Diese Methode startet den Lesevorgang.
		 **/
		bool read();

	private:
		/**
		 * Pfad zu einer xml-Datei, in welcher Eigenschaften abgelegt sind.
		 *
		 * \todo Das Programm sollte in der Lage sein, sämtliche xml-Dateien in einem bestimmten Ordner zu prüfen, ob sie den Voraussetzungen entsprechen und dann automatisch laden.
		 **/
		static const QString templateFile_base;
		static const QString templateFile_human;
		static const QString templateFile_changeling;
		static const QString templateFile_mage;
		static const QString templateFile_vampire;
		static const QString templateFile_werewolf;

		/**
		 * Zeiger zu einer xml-Datei.
		 **/
		QFile *file_base;
		QFile *file_human;
		QFile *file_changeling;
		QFile *file_mage;
		QFile *file_vampire;
		QFile *file_werewolf;

		/**
		 * Zeiger auf den Programmspeicher, der die Template-Daten enthält.
		 **/
		StorageTemplate *storage;

		/**
		 * Arbeitet den Leseprozeß ab.
		 **/
		void process( QFile *device );
		/**
		 * Die erste Ebene in der Abarbeitung des XML-Baumes. Kontrolliert, ob es sich um eine Zuässige Template-DAtei für dieses Programm handelt und gibt dann die Leseoperation an readSoulCreator() weiter.
		 *
		 * \exception eXmlVersion Die XML-DaTei hat die falsche Version.
		 *
		 * \todo Momentan wird trotz Argument immer nur die basis-Datei abgearbeitet.
		 **/
		void readXml( QFile *device );
		/**
		 * Die zweite Ebene des XML-Baumes wird einegelesen. Es wird gespeichert, für welche Spezies dieser Zweig vorgesehen ist. Daraufhin wird die Arbeit an readTree() weitergegeben.
		 *
		 * \exception eXmlError Ist das XML_Dokument fehlerhaft, wird diese Exception mit dem passenden Fehlertext geworfen.
		 **/
		void readSoulCreator();
		/**
		 * Hier wird der cv_TRait::Type der Eigenschaftengruppe ausgelesen und danach entschieden, an welche Funktion weitergesprungen werden soll.
		 *
		 * - Virtues und Vices werden mit cv_Trait::CategoryNo bewertet (sie sind weder mental noch physisch oder sozial). Sie werden daraufhin mit der Funktion readTraits(cv_Species::Species sp, cv_Trait::Type a, cv_Trait::Categories b) weitergelesen.
		 * - Alle anderen Eigenschaften werden mit der Funktion readTraits(cv_Species::Species sp, cv_Trait::Type a) weitergelesen.
		 **/
		void readTree( cv_Species::Species sp );
		/**
		 * Diese Funktion ließt die Kategorie dieser Eigenschaft aus (mental, physisch oder sozial) und dann wird das Weiterlesen der Funktion readTraits(cv_Species::Species sp, cv_Trait::Type a, cv_Trait::Categories b) überlassen.
		 **/
		void readTraits( cv_Species::Species sp, cv_Trait::Type a );
		/**
		 * Die einzelnen Eigenschaften werden ausgelesen. Das tatsächliche Auslesen der Parameter erfolgt aber über die in readTraits(cv_Species::Species sp, cv_Trait::Type a, cv_Trait::Categories b) aufgerufene Funktion readInList(cv_Species::Species sp, cv_Trait::Type a, cv_Trait::Categories b). Diese werden dann in in die Liste traitList eingefügt.
		 **/
		void readTraits( cv_Species::Species sp, cv_Trait::Type a, cv_Trait::Category b );
		/**
		 * In dieser Funktion werden die einzelnen Parameter einer Eigenschaft im Datentyp cv_Trait gespeichert.
		 **/
		cv_Trait storeTraitData( cv_Species::Species sp, cv_Trait::Type a, cv_Trait::Category b );
// 		void readinList_prerequisites(cv_TraitPrerequisiteAnd &prerequisiteAnd);
		/**
		 * Mit dieser Funktion werden die daten über die besondere Eigenschaft der spezies ausgelsen: Eigenschaftsmaxima, Energiespeicher etc.
		 **/
		void readSuperTrait( cv_Species::Species sp );

	signals:
		void oldVersion( QString, QString );
};

#endif
