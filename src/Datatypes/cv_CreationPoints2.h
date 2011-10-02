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

#ifndef CV_CREATIONPOINTS2_H
#define CV_CREATIONPOINTS2_H

#include <QList>

#include "Datatypes/cv_Species.h"

#include <QString>

/**
 * @brief Datentyp für die freien Erschaffungspunkte.
 *
 * Diese Punkte können bei der Charaktererschaffung auf dem Charakterbogen verteilt werden.
 */
class cv_CreationPoints2 {
	public:
		/**
		 * Konstruktor.
		 **/
		cv_CreationPoints2();

		/**
		 * Für welche Spezies diese Punkte zählen.
		 **/
		cv_Species::Species species;
		
		/**
		 * Punkte für die Attribute.
		 *
		 * Index 0 -> primär.
		 *
		 * Index 1 -> sekundär.
		 *
		 * Index 2 -> tertiär.
		 **/
		QList< int > attributes;
		/**
		 * Punkte für die Fertigkeiten.
		 *
		 * Index 0 -> primär.
		 *
		 * Index 1 -> sekundär.
		 *
		 * Index 2 -> tertiär.
		 **/
		QList< int > skills;
		/**
		 * Fertigkeitsspezialisierungen.
		 **/
		int skillSpecialties;
		/**
		 * Merits
		 **/
		int merits;
		/**
		 * Powers
		 **/
		int powers;

		/**
		 * Gibt die übrigen Attributspunkte als String aus.
		 **/
		QString attributesOut();
		/**
		 * Gibt die übrigen Fertigkeitspunkte als String aus.
		 **/
		QString skillsOut();
		/**
		 * Gibt die übrigen Spezialisierungen als String aus.
		 **/
		QString skillSpecialtiesOut();
		/**
		 * Gibt die übrigen Meritpunkte als String aus.
		 **/
		QString meritsOut();
		/**
		 * Gibt die übrigen Punkte für übernatürliche Kräfte als String aus.
		 **/
		QString powersOut();

		bool operator==( const cv_CreationPoints2 &points ) const;
		bool operator!=( const cv_CreationPoints2 &points ) const;

	private:
		/**
		 * Gibt die negativen Werte in Warnfarbe aus.
		 **/
		QString outputPoint(int val);
};

#endif

