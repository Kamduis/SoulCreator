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

#ifndef CV_DERANGEMENT_H
#define CV_DERANGEMENT_H

#include <QString>

#include "cv_Species.h"

#include "cv_AbstractTrait.h"

/**
 * @brief Datentyp für Geistesstörungen.
 *
 * Jede Geistesstörung kann einem Moral-Wert zugeordnet werden.
 */
class cv_Derangement : public cv_AbstractTrait {
	public:
		/**
		 * Konstruktor.
		 **/
		cv_Derangement( QString txt = "", int mor = 0, cv_Species::Species spe = cv_Species::SpeciesNo, cv_AbstractTrait::Category ca = cv_AbstractTrait::CategoryNo );
		
		/**
		 * Der Moralwert, dem diese Geistesstörung zugeordnet ist.
		 *
		 * Ist dieser Wert 0, ist die Geistesstörung keinem Moralwert zugeordnet.
		 **/
		int morality;

	private:
};

#endif

