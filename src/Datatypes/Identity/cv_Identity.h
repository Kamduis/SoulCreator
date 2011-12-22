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

#ifndef CV_IDENTITY_H
#define CV_IDENTITY_H

// #include <QStringList>
// #include <QString>

#include "cv_Name.h"

/**
 * @brief Speichert die vollständige Identität des Charakters.
 *
 * Zusätzlich zu den Namen speichert diese Klasse auch Geschlecht ...
 */
class cv_Identity : public cv_Name {
	public:
		/**
		* Die möglichen Geschlechter.
		**/
		enum Gender {
			GenderNo,
			Male,
			Female
		};

		/**
		* Konstruktor
		**/
		cv_Identity( QString surename = "", QString firstname = "", cv_Identity::Gender gen = cv_Identity::Male );
		
		/**
		* Speichert das Geschlecht des Charakters.
		**/
		cv_Identity::Gender gender;

		/**
		 * Wandelt das Geschlecht in den in den Xml-Dateien gebräuchlichen Namen um.
		 *
		 * Diese Methode benötige ich, um die Strings in den XML-Template-Dateien zu erzeugen.
		 **/
		static QString toXmlString(cv_Identity::Gender gen);
		/**
		 * Wandelt ein Geschlecht in seinen realen Namen um.
		 *
		 * \note Diese Funktion unterscheidet sich insofern von toXmlString(), daß eine Übersetzung erfolgen kann.
		 **/
		static QString toString(cv_Identity::Gender gen);
		/**
		 * Wandelt den Namen eines Geschlechts in den entsprechenden Enumerator um.
		 **/
		static cv_Identity::Gender toGender(QString text);
};

#endif

