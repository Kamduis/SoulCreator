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

#include "Exceptions/Exception.h"

#include "cv_Species.h"


QString cv_Species::toString(cv_Species::SpeciesFlag sp){
	switch(sp){
		case cv_Species::SpeciesNo:
			return "SpeciesNo";
		case cv_Species::Animal:
			return "Animal";
		case cv_Species::Human:
			return "Human";
		case cv_Species::Changeling:
			return "Changeling";
		case cv_Species::Mage:
			return "Mage";
		case cv_Species::Vampire:
			return "Vampire";
		case cv_Species::Werewolf:
			return "Werewolf";
		case cv_Species::SpeciesAll:
			return "SpeciesAll";
		default:
			throw eSpeciesNotExisting(sp);
// 			return "ERROR";
	}
}

cv_Species::SpeciesFlag cv_Species::toSpecies(QString str){
	if (str == "Animal")
		return cv_Species::Animal;
	else if (str == "Human")
		return cv_Species::Human;
	else if (str == "Changeling")
		return cv_Species::Changeling;
	else if (str == "Mage")
		return cv_Species::Mage;
	else if (str == "Vampire")
		return cv_Species::Vampire;
	else if (str == "Werewolf")
		return cv_Species::Werewolf;
	else if (str == "SpeciesAll")
		return cv_Species::SpeciesAll;
	else
		return cv_Species::SpeciesNo;
}
