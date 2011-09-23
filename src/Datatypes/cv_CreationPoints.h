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

#ifndef CV_CREATIONPOINTS_H
#define CV_CREATIONPOINTS_H

#include <QString>

/**
 * @brief Datentyp für die freien Erschaffungspunkte.
 *
 * Diese Punkte können bei der Charaktererschaffung auf dem Charakterbogen verteilt werden.
 */
class cv_CreationPoints {
	public:
		/**
		 * Konstruktor.
		 **/
		cv_CreationPoints();

		/**
		 * Die freien Attributspunkte für die primäre Kategorie.
		 **/
		static const int creationPointsAttA;
		/**
		 * Die freien Attributspunkte für die sekundäre Kategorie.
		 **/
		static const int creationPointsAttB;
		/**
		 * Die freien Attributspunkte für die tertiäre Kategorie.
		 **/
		static const int creationPointsAttC;
		/**
		 * Die freien Fertigkeitspunkte für die primäre Kategorie.
		 **/
		static const int creationPointsSkillA;
		/**
		 * Die freien Fertigkeitspunkte für die sekundäre Kategorie.
		 **/
		static const int creationPointsSkillB;
		/**
		 * Die freien Fertigkeitspunkte für die tertiäre Kategorie.
		 **/
		static const int creationPointsSkillC;
		/**
		 * Die freien Fertigkeitsspezialisierungen
		 **/
		static const int creationPointsSkillSpecialties;
		/**
		 * Die freien Meritpunkte.
		 **/
		static const int creationPointsMerits;
		/**
		 * Die freien Meritpunkte.
		 **/
		static const int creationPointsPowersVampire;
		
		/**
		 * Primäre Kategorie der Attribute.
		 **/
		int attributesA;
		/**
		 * Sekundäre Kategorie der Attribute.
		 **/
		int attributesB;
		/**
		 * Tertiäre Kategorie der Attribute.
		 **/
		int attributesC;
		/**
		 * Primäre Kategorie der Fertigkeiten.
		 **/
		int skillsA;
		/**
		 * Sekundäre Kategorie der Fertigkeiten.
		 **/
		int skillsB;
		/**
		 * Tertiäre Kategorie der Fertigkeiten.
		 **/
		int skillsC;
		/**
		 * Anzahl der freien Spezialisierungen.
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
		 * Gibt die übrigen Meritpunkte als String aus.
		 **/
		QString meritsOut();
		/**
		 * Gibt die übrigen Punkte für übernatürliche Kräfte als String aus.
		 **/
		QString powersOut();

		bool operator==( const cv_CreationPoints &points ) const;
		bool operator!=( const cv_CreationPoints &points ) const;

	private:
		/**
		 * Gibt die negativen Werte in Warnfarbe aus.
		 **/
		QString outputPoint(int val);
};

#endif

