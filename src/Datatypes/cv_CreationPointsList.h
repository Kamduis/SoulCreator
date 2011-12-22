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

#ifndef CV_CREATIONPOINTSLIST_H
#define CV_CREATIONPOINTSLIST_H

#include "Datatypes/cv_CreationPoints.h"

#include <QList>

/**
 * @brief Datentyp für die freien Erschaffungspunkte.
 *
 * Diese Liste Speichert die freien Erschaffungspunkte für sämtliche Eigenschaftskategorien und alle unterschiedlichen Spezies.
 */
class cv_CreationPointsList : public QList< cv_CreationPoints > {
	public:
		/**
		 * Konstruktor.
		 **/
		cv_CreationPointsList();

		/**
		 * Gibt die übrigen Erschaffungspunkte als String aus.
		 **/
		QString pointString(cv_Species::SpeciesFlag spe, cv_AbstractTrait::Type tp /** Dieses Argument bestimmt, welcher Typ bei der Ausgabe berücksichtigt wird. */);
		/**
		 * Gibt die übrigen Erschafungspunkte aus.
		 **/
		QList< int >* pointList(cv_Species::SpeciesFlag spe, cv_AbstractTrait::Type tp );
// 		/**
// 		 * Gibt die übrigen Fertigkeitspunkte als String aus.
// 		 **/
// 		QString skillsOut();
// 		/**
// 		 * Gibt die übrigen Spezialisierungen als String aus.
// 		 **/
// 		QString skillSpecialtiesOut();
// 		/**
// 		 * Gibt die übrigen Meritpunkte als String aus.
// 		 **/
// 		QString meritsOut();
// 		/**
// 		 * Gibt die übrigen Punkte für übernatürliche Kräfte als String aus.
// 		 **/
// 		QString powersOut();
// 
// 		bool operator==( const cv_CreationPointsList &points ) const;
// 		bool operator!=( const cv_CreationPointsList &points ) const;

	private:
		/**
		 * Gibt die negativen Werte in Warnfarbe aus.
		 **/
		QString outputPoint(int val);
};

#endif

