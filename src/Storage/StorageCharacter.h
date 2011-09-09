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
#include "../Datatypes/cv_Identity.h"
#include "../Datatypes/cv_IdentityList.h"

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
// 		Q_PROPERTY( cv_IdentityList identities READ identities WRITE setIdentities NOTIFY identitiesChanged )

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
		cv_IdentityList identities() const;
		/**
		 * Erlaubt den Zugriff auf die \emph{echte} Identität.
		 **/
		cv_Identity* realIdentity;
		/**
		 * Tugend des Charakters
		 **/
		QString virtue() const;
		/**
		 * Laster des Charakters
		 **/
		QString vice() const;
		/**
		 * Brut (Seeming, Path, Clan, Auspice) des Charakters
		 **/
		QString breed() const;
		/**
		 * Fraktion (Court, order, Covenant, Tribe) des Charakters
		 **/
		QString faction() const;
		/**
		 * Gibt eine Liste \emph{aller} Eigenschaften des Charkaters aus.
		 **/
		QList< cv_Trait > traitsAll() const;
		/**
		 * Gibt eine Liste aller Eigenscahften des Charkaters aus, welche über die Argumente spezifiziert sind.
		 *
		 * \bug Sehr zeitaufwendige Funktion, da bei jedem aufruf eine Liste mühsam gefüllt wird. Und diese Funktion wird \emph{oft} aufgerufen.
		 **/
		QList< cv_Trait > traits( cv_Trait::Type type, cv_Trait::Category category ) const;
		/**
		 * Gibt die Eigenschaft aus, auf welche mit dem Zeiger im Argument verwiesen wird.
		 **/
		cv_Trait trait( const cv_Trait* traitPtr ) const;
		/**
		 * Gibt eine Liste aller Attribute des Charkaters aus.
		 **/
		QList< cv_Trait > attributes( cv_Trait::Category category ) const;
		/**
		 * Gibt eine Liste aller Fertigkeiten des Charkaters aus.
		 **/
		QList< cv_Trait > skills( cv_Trait::Category category ) const;
		/**
		 * Gibt eine Liste aller Merits des Charkaters aus.
		 **/
		QList< cv_Trait > merits( cv_Trait::Category category ) const;
		/**
		 * Gibt den Wert des Super-Attributs aus.
		 **/
		int superTrait() const;
		/**
		 * Gibt den Wert der Moral aus.
		 **/
		int morality() const;

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
		static cv_IdentityList v_identities;
		/**
		 * Eine Liste sämtlicher Eigenschaften des Charakters.
		 *
		 * \todo Sollte ich nicht so machen. So werden ja alle Daten aus dem Template in den Charkater geschrieben. ich woll dort aber nur stehen haben, was auch der Charkater hat. Insbesondere bei Spezialisierungen ist das wichtig. Vielleicht einfach die Spazialisierungen wieder rauslöschen.
		 *
		 * \todo Anstatt alles in einer Liste zu haben, die ich dann auswerte, sollte ich vielleicht für jeden Typ und jede Kategorie eine eigene Liste haben und wenn ich dann etwas ausgebe, hänge ich die Listen zur not einfach aneinander an. Geht schneller als bei der Speziellen ausgabe inhalt für inhalt an eine neue Liste zu kleben.
		 **/
		static QString v_virtue;
		static QString v_vice;
		static QString v_breed;
		static QString v_faction;
		static QList< cv_Trait > v_traits;
		static int v_superTrait;
		static int v_morality;

	public slots:
		/**
		 * Legt die Spezies des Charakters fest.
		 **/
		void setSpecies( cv_Species::SpeciesFlag species );
		/**
		 * Fügt eine neue Identität an der angegebenen Stelle ein.
		 **/
		void insertIdentity( int index, cv_Identity id );
		/**
		 * Hängt eine neue Identität an die Liste aller Identitäten des Charkaters an.
		 **/
		void addIdentity( cv_Identity id );
		/**
		 * Legt die \emph{echte} Identität des Charakters fest. Diese Identität hat immer INdex 0 in der \ref v_identities -Liste
		 *
		 * \todo Momentan ist dies die einzige identität, die von diesem programm genutzt wird.
		 **/
		void setRealIdentity( cv_Identity id );
		/**
		 * Legt die Spezialisierungen des Charakters fest.
		 *
		 * \todo Wenn die Fertigkeit nicht existiert, zu der die Spezialisierungen gehören, sollte diese Funktion eine Ausnahme werfen.
		 **/
		void setSkillSpecialties( QString name /** Name der Fertigkeit, zu welcher diese Spezialisierungen gehören. */,
								  QList< cv_TraitDetail > details /** Liste der Spezialisierungen. */
								);
		/**
		 * Fügt dem Speicher eine neue Eigenschaft hinzu.
		 *
		 * \return Es wird ein Zeiger auf diese Eigenschaft zurückgegeben.
		 *
		 * \note Doppelte Eigenschaften werden mit dem neuen Wert überschrieben.
		 *
		 * \note Eigenschaften mit Zusatztext werden nur gespeichert, wenn dieser Text auch vorhanden ist.
		 **/
		cv_Trait* addTrait( cv_Trait trait );
		/**
		 * Ändert eine Eigenschaft im Speicher.
		 **/
		void modifyTrait( cv_Trait trait );
		/**
		 * Verändert die Tugend.
		 *
		 * \sa virtue()
		 **/
		void setVirtue( QString txt );
		/**
		 * Verändert das Laster.
		 *
		 * \sa vice()
		 **/
		void setVice( QString txt );
		/**
		 * Verändert die Brut.
		 *
		 * \sa breed()
		 **/
		void setBreed( QString txt );
		/**
		 * Verändert die Fraktion.
		 *
		 * \sa faction()
		 **/
		void setFaction( QString txt );
		/**
		 * Verändert den Wert des Super-Attributs.
		 *
		 * Bei einer Veränderung wird das Signal superTraitChanged() ausgesandt.
		 **/
		void setSuperTrait( int value );
		/**
		 * Verändert den Wert der Moral.
		 *
		 * Bei einer Veränderung wird das Signal moralityChanged() ausgesandt.
		 **/
		void setMorality( int value );
		/**
		 * Löscht alle Charakterwerte.
		 *
		 * \note Tatsächlich werden die Werte nicht gelöscht, sondern auf 0 gesetzt.
		 *
		 * \todo Kontrolle, ob das Löschen des Zusatztextes nicht ein Problem darstellt, da ich diesen Zusatext ja manchmal als Kriterium nutze.
		 **/
		void resetCharacter();

	private slots:
// 		void emitSpeciesChanged( cv_Species::SpeciesFlag species );

	signals:
		/**
		* Dieses Signal wird ausgesandt, wann immer eine Identität des Charakters verändert wird.
		**/
		void identityChanged( cv_Identity id );
		/**
		* Dieses Signal wird ausgesandt, wann immer sich der echte Name des Charakters ändert.
		**/
		void realIdentityChanged( cv_Identity id );
		/**
		* Dieses Signal wird ausgesandt, wann immer sich die Spezies des Charakters ändert.
		**/
		void speciesChanged( cv_Species::SpeciesFlag species );
		/**
		* Dieses Signal wird ausgesandt, wann immer sich eine Eigenschaft ändert.
		**/
// 		void traitChanged( cv_Trait trait );
		void traitChanged( cv_Trait* trait );
		
		/**
		* Die Tugend hat sich verändert.
		**/
		void virtueChanged( QString virtue );
		/**
		* Das Laster hat sich verändert.
		**/
		void viceChanged( QString vice );
		/**
		* Die Brut hat sich verändert.
		**/
		void breedChanged( QString breed );
		/**
		* Die Fraktion hat sich verändert.
		**/
		void factionChanged( QString faction );
		/**
		* Dieses Signal wird ausgesandt, wann immer sich der Wert des Super-Attributs verändert.
		**/
		void superTraitChanged( int value );
		/**
		* Dieses Signal wird ausgesandt, wann immer sich der Wert der Moral verändert.
		**/
		void moralityChanged( int value );
};

#endif
