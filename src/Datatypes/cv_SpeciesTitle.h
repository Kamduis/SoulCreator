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

#ifndef CV_SPECIESTITLES_H
#define CV_SPECIESTITLES_H

#include <QString>

#include "cv_Species.h"

/**
 * @brief Grundlegender Datentyp die unterchiedlichen Bezeichnungen von Eigenschaften bei Spezies.
 */
class cv_SpeciesTitle {
	public:
		/**
		 * Zu welchem Titel gehört dieser Bezeichner.
		 *
		 */
		enum Title {
			TitleNo,
			Breed,
			Faction
		};
		/**
		 * Konstruktor.
		 **/
		cv_SpeciesTitle( Title tit = TitleNo, QString txt = "", cv_Species::Species spe = cv_Species::SpeciesNo );
		
		/**
		 * Der Titel, um den es hier geht.
		 **/
		Title title;
		/**
		 * Der Name des Titels.
		 **/
		QString name;
		/**
		 * Für welche spezies dieser Titel gilt.
		 **/
		cv_Species::Species species;

		/**
		 * Wandelt QString in Title-Typ um.
		 **/
		static Title toTitle( QString str );

		/**
		* Vergleich zwischen zwei Instanzen dieser Klasse.
		**/
		bool operator==( const cv_SpeciesTitle &tit ) const;
};

#endif

