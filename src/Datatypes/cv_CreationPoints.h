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

#ifndef CV_CREATIONPOINTS_H
#define CV_CREATIONPOINTS_H

#include <QList>

#include "Datatypes/cv_Species.h"
#include "Datatypes/Traits/cv_AbstractTrait.h"

/**
 * @brief Datentyp für die freien Erschaffungspunkte.
 *
 * In dieser Klasse werden die freien Erschaffungspunkte eines einzigen Eigenschaftstyps gespeichert, natürlich abhängig von der Spezies.
 */
class cv_CreationPoints {
	public:
		/**
		 * Konstruktor.
		 **/
		cv_CreationPoints();

		/**
		 * Für welche Spezies diese Punkte zählen.
		 **/
		cv_Species::Species species;
		
		/**
		 * Für welchen Eigenscahftstyp diese Punkte zählen.
		 **/
		cv_AbstractTrait::Type type;

		/**
		 * Punkte.
		 *
		 * Bei Attributen und Fertigkeiten:
		 *
		 * Index 0 -> primär.
		 *
		 * Index 1 -> sekundär.
		 *
		 * Index 2 -> tertiär.
		 *
		 * Bei Fertigkeiten:
		 *
		 * Index 3 -> Spezialisierungen
		 **/
		QList< int > points;

		bool operator==( const cv_CreationPoints &points ) const;
// 		bool operator!=( const cv_CreationPoints2 &points ) const;

	private:
// 		/**
// 		 * Gibt die negativen Werte in Warnfarbe aus.
// 		 **/
// 		QString outputPoint(int val);
};

#endif

