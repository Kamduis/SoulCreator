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

#ifndef BASEEXCEPTION_H
#define BASEEXCEPTION_H

#include <QString>

#include "Datatypes/cv_Trait.h"
#include "Datatypes/cv_Shape.h"
#include "Datatypes/cv_Identity.h"
#include "Config/Config.h"


/**
 * @brief Basisklasse für die Ausnahmebehandlung
 *
 * Diese Klasse liegt allen Ausnahmebehandlungen zugrunde.
 */

class Exception {
	public:
		/**
		 * Dem Konstruktor kann die Standardnachricht für die Ausnahme übergeben werden.
		 */
		Exception( QString message = "" );
		/**
		 * Erlaubt das Auslesen der Standardnachricht.
		 */
		QString message();
		/**
		 * Setzt die Kurznachricht über die Ausnahme.
		 */
		void setMessage( QString message );
		/**
		 * Erlaubt das Auslesen einer ausfühlrichen Beschreibung der ausgelösten Ausnahme.
		 */
		QString description();
		/**
		 * Setzt die ausfühlriche Beschreibung der Ausnahme.
		 */
		void setDescription( QString desc );

	protected:
		/**
		 * Kurze Nachricht über den Typ der Ausnahme.
		 */
		QString v_message;
		/**
		 * Ausfühlriche Beschreibung der Ausnahme.
		 */
		QString v_description;
};


/**
 * @brief Ausnahme bei Zahlen.
 *
 * Allgemeine Fehler im Umgang mit Zahlen.
 */
class eNumber : public Exception {
	public:
		/**
		 * Ausnahme: Probleme mit einer Zahl.
		 */
		eNumber();
};

/**
 * @brief Ausnahme beim Fehlen einer Zahl.
 *
 * Es wird eine Zahl erwartet, abe rkeine Zahl übergeben.
 */
class eNotANumber : public eNumber {
	public:
		/**
		 * Ausnahme: keine Zahl verfügbar.
		 */
		eNotANumber();
};


/**
 * @brief Ausnahme bei Listen oder Vektoren.
 */
class eList : public Exception {
	public:
		eList();
};

/**
 * @brief Index überschreitet Listengröße
 *
 * Es wird eine Zahl erwartet, abe rkeine Zahl übergeben.
 */
class eIndexExceedsRange : public eList {
	public:
		eIndexExceedsRange( int idx, int range );
};


/**
 * @brief Ausnahme im Verzeichnis-Management.
 *
 * Allgemeine Fehler im Umgang mit Verzeichnissen werfen diese Ausnahme.
 */
class eDir : public Exception {
	public:
		eDir( QString dirName = "unknown" );
};

/**
 * @brief Verzeichnis kann nicht angelegt werden.
 *
 * Das Programm kann das spezifizierte Verzeichnis nicht anlegen.
 */
class eDirNotCreated : public eDir {
	public:
		eDirNotCreated( QString dirName = "unknown" );
};


/**
 * @brief Ausnahme im Datei-Management.
 *
 * Allgemeine Fehler im Umgang mit Dateien werfen diese Ausnahme.
 */
class eFile : public Exception {
	public:
		/**
		 * Ausnahme: Probleme mit einer Datei.
		 */
		eFile( QString filename = "unknown" );
};

/**
 * @brief Datei kann nicht geöffnet werden.
 *
 * Das Programm kann die spezifizierte Datei nicht öffnen.
 */
class eFileNotOpened : public eFile {
	public:
		eFileNotOpened( QString fileName = "unknown", QString lastError = "unknown" );
};

/**
 * @brief Datei kann nicht gelöscht werden.
 *
 * Das Programm kann die spezifizierte Datei nicht löschen.
 */

class eFileNotDeleted : public eFile {
	public:
		/**
		 * Ausnahme: Kann Datei nicht löschen.
		 */
		eFileNotDeleted( QString filename = "unknown" );
};


/**
 * @brief Ausnahme beim Lesen der XML-Datei
 *
 * Treten Fehler beim Lesen der XML-Datei auf, wird diese Ausnahme geworfen.
 */

class eXml : public Exception {
	public:
		eXml( QString error = "unknown" );
};

/**
 * @brief Beim Parsen der XML-Datei trat ein Fehler auf.
 *
 * Während das Programm versucht, eine XML-Datei zu parsen, tritt der im Argument spezifizierte Fehler auf.
 */
class eXmlError : public eXml {
	public:
		eXmlError( QString fileName = "unknown", QString error = "unknown" );
};

/**
 * @brief Die XML-Datei weist die falsche Version auf.
 */
class eXmlVersion : public eXml {
	public:
		eXmlVersion( QString expected = "unknown", QString got = "unknown" );
};

/**
 * @brief Die Version der XML-Datei paßt zwar zu diesem programm, ist aber zu alt.
 */
class eXmlOldVersion : public eXmlVersion {
	public:
		eXmlOldVersion( QString expected = Config::version(), QString got = "unknown" );
};

/**
 * @brief Die Version der XML-Datei paßt zwar zu diesem Programm, ist aber viel zu alt.
 *
 * Die Version ist so alt, daß eine Verwendung dieser Ressource nicht empfehlenswert ist.
 */
class eXmlTooOldVersion : public eXmlOldVersion {
	public:
		eXmlTooOldVersion( QString expected = Config::version(), QString got = "unknown" );
};


/**
 * @brief Ausnahme, falls Fehler bei den Spezies auftritt.
 *
 * Ein unspezifizierter Fehler in Zusammenhang mit den Spezies führt zu dieser Ausnahme.
 */
class eSpecies : public Exception {
	public:
		eSpecies();
};

/**
 * @brief Ausnahme, falls eine spezifizierte Spezies nicht existiert.
 *
 * Die erwartete Spezies wurde nicht gefunden.
 */
class eSpeciesNotExisting : public eSpecies {
	public:
		eSpeciesNotExisting( cv_Species::SpeciesFlag species );
		eSpeciesNotExisting();
};


/**
 * @brief Ausnahme, falls Fehler bei den Geschlechtern auftritt.
 */
class eGender : public Exception {
	public:
		eGender();
};

/**
 * @brief Ausnahme, falls das spezifizierte Geschlecht nicht existiert.
 */
class eGenderNotExisting : public eGender {
	public:
		eGenderNotExisting( cv_Identity::Gender gen );
};


/**
 * @brief Ausnahme, falls Fehler bei den Eigenschaften auftritt.
 *
 * Ein unspezifizierter Fehler in Zusammenhang mit Charaktereigenschaften führt zu dieser Ausnahme.
 */
class eTrait : public Exception {
	public:
		eTrait();
};

/**
 * @brief Ausnahme, falls eine spezifizierte Eigenscahft nicht existiert.
 *
 * Die erwartete Charaktereigenschaft wurde nicht gefunden.
 */
class eTraitNotExisting : public eTrait {
	public:
		eTraitNotExisting();
};

/**
 * @brief Ausnahme, falls eine falsche Kategorie genutzt wird.
 *
 * Die Kategorie exitiert nicht oder hat an dieser Stelle keine Gültigkeit.
 */
class eTraitCategory : public eTrait {
	public:
		eTraitCategory( cv_Trait::Category category );
};

/**
 * @brief Ausnahme, falls ein falscher Typ genutzt wird.
 *
 * Der Typ exitiert nicht oder hat an dieser Stelle keine Gültigkeit.
 */
class eTraitType : public eTrait {
	public:
		eTraitType( cv_Trait::Type type );
};


/**
 * @brief Ausnahme, falls beim Audrucken ein Fehler entsteht.
 *
 * Ein unspezifizierter Fehler beim Ausdruck ist aufgetreten.
 */
class ePrint : public Exception {
	public:
		ePrint();
};

/**
 * @brief Ausnahme, falls zu viele Eigenschaften gedruckt werden sollen.
 *
 * Aufgrund vorgefertigter Charakterbögen können je nach Typ nur eine gewissen Anzahl der entsprechenden Eigenschaften darauf aufgebracht werden. Stehen im Generator mehr dieser Eigenschaften, als gedruckt werden können, tritt diese Ausnahme auf.
 */
class eTraitsExceedSheetCapacity : public ePrint {
	public:
		eTraitsExceedSheetCapacity( cv_Trait::Type type, int maxNumber );
};

/**
 * @brief Ausnahme, falls ein zu großer Wert auf den Charakterbogen gedruckt werden soll.
 *
 * Aufgrund vorgefertigter Charakterbögen können gewisse Teiel des charkaters nicht in beliebiger Höhe dargestellt werden.
 */
class eValueExceedsSheetCapacity : public ePrint {
	public:
		eValueExceedsSheetCapacity( int value, QString name );
};


/**
 * @brief Ausnahme, falls Fehler bei einer Eingabe auftreten.
 *
 * Falsche oder Fehlende Eingabe führt zu dieser Ausnahme.
 */

class eEntry : public Exception {
	public:
		/**
		 * Ausnahme: Eingabe fehlt oder falsch.
		 */
		eEntry();
};

/**
 * @brief Ausnahme, falls Fehler bei einer Benutzereingabe auftreten.
 *
 * Falsche oder fehlende Benutzereingabe führt zu dieser Ausnahme.
 */

class eUserEntry : public eEntry {
	public:
		/**
		 * Ausnahme: Benutzereingabe fehlt oder falsch.
		 */
		eUserEntry();
};

/**
 * @brief Ausnahme, falls Fehler bei einer Benutzereingabe auftreten.
 *
 * Fehlende Benutzereingabe führt zu dieser Ausnahme.
 */

class eMissingUserEntry : public eUserEntry {
	public:
		/**
		 * Ausnahme: Benutzereingabe fehlt.
		 */
		eMissingUserEntry();
};


/**
 * @brief Ausnahme, falls Fehler Bei den Gestalten der Werwölfe auftritt.
 */
class eWerewolfShape : public Exception {
	public:
		eWerewolfShape();
};

/**
 * @brief Ausnahme, falls eine ungültige Werwolf-Gestalt gewählt wird.
 */
class eWerewolfShapeNotExisting : public eWerewolfShape {
	public:
		eWerewolfShapeNotExisting( cv_Shape::WerewolfShape shape );
		eWerewolfShapeNotExisting( QString shape );
};

#endif
