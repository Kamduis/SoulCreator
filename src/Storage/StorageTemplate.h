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

#ifndef STORAGETEMPLATE_H
#define STORAGETEMPLATE_H

#include <QList>
#include <QStringList>

#include "../Datatypes/cv_Trait.h"
#include "../Datatypes/cv_NameList.h"
// #include "../IO/ReadXmlTemplate.h"

#include <QObject>

/**
 * @brief In dieser Klasse werden sämtliche Daten für das Programm gespeichert.
 *
 * Diese Klasse verwaltet die im Programm geladenen Daten. Zum einen gibt es eine Liste, in welcher sämtliche \emph{möglichen} Eigenschaften für die Charaktere gespeichert sind, jene welche nach Programmstart aus den Template-Dateien ausgelesen werden und zum anderen gibt es eine Liste für den aktuell angezeigten Charakter.
 *
 * Außerdem bietet diese Klasse angenehme Zugriffsfunktionen aus den Informationen, welche zum Programmstart aus den Template-Dateien geladen werden.
 **/
class StorageTemplate : public QObject {
		Q_OBJECT
// 		/**
// 		 * Eine Liste aller Identitäten des Charakters. Hierin werden alle seine zahlreichen Namen gespeichert.
// 		 *
// 		 * \access identities(), setIdentities()
// 		 *
// 		 * \notifier identitiesChanged()
// 		 **/
// 		Q_PROPERTY( cv_NameList identities READ identities WRITE setIdentities NOTIFY identitiesChanged )

	public:
		StorageTemplate( QObject *parent = 0 );
		/**
		 *Zerstört das Objekt und gibt alle zugeteilten Ressourcen wieder frei.
		 **/
		~StorageTemplate();

		/**
		 * Gibt eine Liste aller verfügbaren Spezies aus.
		 **/
		QList< cv_Species > species() const;
		/**
		 * Gibt eine Liste aller verfügbaren Virtues aus.
		 **/
		QStringList virtues( cv_Trait::AgeFlag age = cv_Trait::Adult ) const;
		/**
		 * Gibt eine Liste aller verfügbaren Vices aus.
		 **/
		QStringList vices( cv_Trait::AgeFlag age = cv_Trait::Adult ) const;
		/**
		 * Gibt eine Liste aller verfügbaren Vices aus.
		 **/
		QStringList attributes( cv_Trait::Category category ) const;
		/**
		 * Gibt eine Liste aller verfügbaren Vices aus.
		 **/
		QStringList skills( cv_Trait::Category category, cv_Trait::EraFlag era = cv_Trait::Modern, cv_Trait::AgeFlag age = cv_Trait::Adult ) const;
		/**
		 * Gibt eine Liste aller Spezialisierungen der angegebenen Fertigkeit aus.
		 **/
		QList< cv_TraitDetail > skillSpecialties( QString skillName ) const;
		/**
		 * Gibt eine Liste aller verfügbaren Merits aus.
		 **/
		QStringList merits( cv_Trait::Category category ) const;
		/**
		 * Gibt eine Liste aller möglichen Werte aus, welche der Merit annehmen kann.
		 **/
		QList< int > meritValues( QString meritName ) const;
		/**
		 * Gibt ein Logische Verkettung von Voraussetzungen aus, die zu erfüllen ist, um den Merit wählen zu können.
		 **/
		QString meritPrerequisites( QString meritName ) const;
		/**
		 * Gibt die gesamte Eigenschaft zurück, welche über Typ, Kategorie und Name spezifiziert ist.
		 **/
		cv_Trait trait(cv_Trait::Type type, cv_Trait::Category category, QString name);

	private:
		/**
		 * Eine Liste sämtlicher verfügbaren Eigenschaften.
		 **/
		static QList< cv_Trait > v_traits;
		/**
		 * Eine Liste sämtlicher verfügbaren Spezies.
		 **/
		static QList< cv_Species > v_species;

		/**
		 * Gibt eine Namensliste verschiedener Eigenschaften aus, spezifiziert nach Typ (\ref cv_Trait::Type), Kategorie (\ref cv_Trait::Category), Zeitalter (\ref cv_Trait::Era) und Alter (\ref cv_Character::Age).
		 *
		 * \todo Momentan arbeite ich nicht wirklich richtig mit den Flags in dieser Funktion. Ich muß momentan auf jedes einzelne existierende Flag prüfen. Das kann aber nicht der wahre Weg sein.
		 **/
		QStringList traitNames( cv_Trait::Type type, cv_Trait::Category category, cv_Trait::EraFlag era, cv_Trait::AgeFlag age ) const;

	public slots:
// 		/**
// 		 * Speichert sämtliche verfügbaren Eigenschaften.
// 		 **/
// 		void setTraits( QList<cv_Trait> traits );
		/**
		 * Fügt eine Spezies hinzu.
		 **/
		void appendSpecies( cv_Species species );
		/**
		 * Fügt eine Eigenschaft hinzu.
		 **/
		void appendTrait( cv_Trait trait );




// 		/**
// 		 * Jeder Charakter kann mehrere Namen haben. Allerdings kann jeder Charkater nur einen Namen pro Kategorie haben. Diese Variable enthält die verschiedenen Namen des Charakters.
// 		 **/
// 		cv_Name charaName;
//
// 		static QList<cv_Trait> storedTraits;
//
// 		QStringList speciesNames();
// 		QStringList virtueNames( cv_Character::Age age );
// 		QStringList viceNames( cv_Character::Age age );
// 		QStringList attributeNames( cv_Trait::Categories categories = cv_Trait::CategoryNo );
// 		QList<cv_Trait> attributes( cv_Trait::Categories categories = cv_Trait::CategoryNo );
// 		QStringList skillNames( cv_Trait::Categories categories = cv_Trait::CategoryNo );
// 		QStringList skillNames( cv_Trait::Categories categories, cv_Character::Era era, cv_Character::Age age );
// 		QStringList skillSpecialties( QString skillName, cv_Species::Species species = cv_Species::SpeciesNo );
// //		QStringList meritNames(cv_Character::Species species = cv_Character::SpeciesAll);
//
// //		static QString showName(Name::Category category);
// //		static void storeName(QString name, Name::Category category);	///< Speichert den QString name in storedNames. Existiert bereits ein Name der selben Kategorie, wird er überschrieben.
// 		/**
// 		* @brief Speichert einen Trait in StorageTemplate::storedTraits.
// 		*
// 		* Ist der Schalter replace wahr, wird kein neuer Trait angehängt, sondern automatisch der bereits vorhandene gleichen Namens ersetzt. Bei Attributen, Fertigkeiten, Merits sollte das nicht geschehen, bei Virtue und Vice dagegen schon. Jeder Charakter hat schließlich nur eines davon, auch wenn sie unterschiedliche Namen haben.
// 		*
// 		* @param trait
// 		* @param replace
// 		*/
// 		static void storeTrait( cv_Trait trait, bool replace = false );

// 	private:
// 		QList<cv_Trait> *traits;
//
// 		ReadXmlTemplate *readTemplate;
//
// //		static QList<Name> storedNames;
//
// //	public slots:
};

#endif
