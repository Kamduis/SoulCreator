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

#ifndef CV_SUPEREFFECT_H
#define CV_SUPEREFFECT_H

#include "cv_Species.h"

/**
 * @brief Speichert die Effekte, welche das Superattribut je nach Spezies besitzt.
 *
 * Menge der Energie und maximale Rate, mit welcher diese eingesetzt werden kann hängt ebenso vom Superattribut ab, wie die höchstwerte der Attribute.
 */
class cv_SuperEffect {
	public:
		cv_SuperEffect();

		/**
		 * Bei welchem Wert des Superattributs die gleichfalls gespeicherten Effekte auftreten.
		 **/
		int value;
		/**
		 * Bei welcher Spezies die hier gespeicherten Effekte auftreten.
		 **/
		cv_Species::Species species;
		/**
		 * Wieviel Energie en Charakter mit \ref species und einem Wert \ref value dieses Superattributs maximal in sich tragen kann.
		 **/
		int fuelMax;
		/**
		 * Wieviel Energie en Charakter mit \ref species und einem Wert \ref value dieses Superattributs pro Runde maximal ausgeben kann.
		 **/
		int fuelPerTurn;
		/**
		 * Ein Charkter mit \ref species und \ref value seines Superattributs kann Eigenschaften mit diesem Höchstwert haben.
		 **/
		int traitMax;
};

#endif

