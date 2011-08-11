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

#ifndef STORAGECHARACTER_H
#define STORAGECHARACTER_H

#include "../Datatypes/cv_Trait.h"
#include "../Datatypes/cv_NameList.h"

#include <QObject>

/**
 * @brief In dieser Klasse werden sämtliche Daten des gerade geöffneten Charakters gespeichert.
 *
 * Wird ein Wert durch das Programm geändert, muß der Wert tatsächlich in dieser Klasse verändert werden. Denn der Inhalt dieser Klasse wird beim Speichern in eine Datei geschrieben und beim Laden wird diese Klasse aufgefüllt. Die Anzeige nimmt all ihre Daten aus dieser Klasse.
 *
 * Außerdem bietet diese Klasse angenehme Zugriffsfunktionen aus den Informationen, welche zum Programmstart aus den Template-Dateien geladen werden.
 *
 * \note Bei dieser Klasse handelt es sich um eine Singleton-Klasse. Es kann stets nur eine Instanz dieser Klasse existieren. Einen zeiger auf diese instanz erzeugt man mittels folgendem Code:
 * \code
 * StorageCharacter* character = StorageCharacter::getInstance();
 * \endcode
 **/

class StorageCharacter : public QObject {
		Q_OBJECT
// 		/**
// 		 * Eine Liste aller Identitäten des Charakters. Hierin werden alle seine zahlreichen Namen gespeichert.
// 		 *
// 		 * \access identities(), setIdentities()
// 		 *
// 		 * \notifier identitiesChanged()
// 		 **/
// 		Q_PROPERTY( cv_NameList identities READ identities WRITE setIdentities NOTIFY identitiesChanged )

	private:
		/*
		 * Konstruktor
		 *
		 * Von außen Keine Instanz erzeugbar.
		 **/
		StorageCharacter( QObject* parent = 0 );
		/**
		 * Zerstört das Objekt und gibt alle zugeteilten Ressourcen wieder frei.
		 **/
		~StorageCharacter();

		/**
		 * Statischer Zeiger auf diese Klasse.
		 **/
		static StorageCharacter* p_instance;

		/**
		 * Nicht kopierbar.
		 **/
		StorageCharacter( const StorageCharacter* ) {}
		/**
		 * Nicht zuweisbar.
		 **/
		StorageCharacter* operator=( const StorageCharacter* ) {}

	public:
		/**
		 * Über diese Funktion kann ein Zeiger auf diese Singleton-Klasse erzeugt werden.
		 **/
		static StorageCharacter* getInstance();
		/**
		 * Diese Funktion gibt eine Möglichkeit, die einzig existierende Instanz dieser Klasse zu zerstören.
		 **/
		static void destroy();
		
		/**
		 * Gibt die Spezies des Charakters aus.
		 **/
		cv_Species::SpeciesFlag species() const;
		/**
		 * Gibt eine Liste aller Identitäten des Charkaters aus.
		 **/
		cv_NameList identities() const;
		/**
		 * Gibt eine Liste aller Eigenscahften des Charkaters aus, welche über die Argumente spezifiziert sind.
		 **/
		QList< cv_Trait > traits( cv_Trait::Type type, cv_Trait::Category category ) const;
		/**
		 * Gibt eine Liste aller Attribute des Charkaters aus.
		 **/
		QList< cv_Trait > attributes( cv_Trait::Category category ) const;

	private:
		/**
		 * Die Spezies des Charakters.
		 *
		 * Es lohnt nicht, hier die \ref cv_Species Klasse zu verwenden.
		 **/
		static cv_Species::SpeciesFlag v_species;
		/**
		 * Eine Liste aller Identitäten des Charakters. Hierin werden alle seine zahlreichen Namen gespeichert.
		 **/
		static cv_NameList v_identities;
		/**
		 * Eine Liste sämtlicher Eigenschaften des Charakters.
		 *
		 * \todo Sollte ich nicht so machen. So werden ja alle Daten aus dem Template in den Charkater geschrieben. ich woll dort aber nur stehen haben, was auch der Charkater hat. Insbesondere bei Spezialisierungen ist das wichtig. Vielleicht einfach die Spazialisierungen wieder rauslöschen.
		 **/
		static QList< cv_Trait > v_traits;

	public slots:
		/**
		 * Legt die Spezies des Charakters fest.
		 *
		 * \bug Es wird zwar das Signal speciesChanged ausgesandt, wenn diese Funktion aufgerufen wird, aber natürlich nur an das Objekt, welches diese Klasse als Objekt erzeugt hat. Also nicht an jede Klasse mit einem Zeiger auf eine Instanz dieser Klasse. Deswegen werden die Widgets nicht verändert, wenn der Inhalt des statischen Objekts dieser Klasse über ein anderes Objekt dieser Klasse modifiziert wird. Möglicherweise ist es eine Lösung, diese Klasse als Singleton zu erzeugen.
		 **/
		void setSpecies( cv_Species::SpeciesFlag species );
		/**
		 * Fügt eine neue Identität an der angegebenen Stelle ein.
		 **/
		void insertIdentity( int index, cv_Name name );
		/**
		 * Hängt eine neue Identität an die Liste aller Identitäten des Charkaters an.
		 **/
		void addIdentity( cv_Name name );
		/**
		 * Legt den Wert der über die Argumente spezifizierten Eigenschaft fest. Unterscheidet sich der Wert vom zuvor gespeicherten, wird automatisch das Signal valueChanged() ausgesandt.
		 **/
		void setValue( int value, cv_Trait::Type type, cv_Trait::Category category, QString name );
		/**
		 * Legt die Spezialisierungen des Charakters fest.
		 *
		 * \todo Wenn die Fertigkeit nicht existiert, zu der die Spezialisierungen gehören, sollte diese Funktion eine Ausnahme werfen.
		 **/
		void setSkillSpecialties( QString name /** Name der Fertigkeit, zu welcher diese Spezialisierungen gehören. */,
								  QList< cv_TraitDetail > details /** Liste der Spezialisierungen. */
								);

	private slots:
// 		void emitSpeciesChanged( cv_Species::SpeciesFlag species );

	signals:
		/**
		* Dieses Signal wird ausgesandt, wann immer sich der Wert einer Eigenschaft ändert.
		**/
		void valueChanged( int, cv_Trait::Type, cv_Trait::Category, QString );
		/**
		* Dieses Signal wird ausgesandt, wann immer sich die Spezies des Charakters ändert.
		**/
		void speciesChanged( cv_Species::SpeciesFlag species );


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
// 		* @brief Speichert einen Trait in StorageCharacter::storedTraits.
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
// 		ReadXmlTemplate* readTemplate;
//
// //		static QList<Name> storedNames;
//
// //	public slots:
};

#endif
