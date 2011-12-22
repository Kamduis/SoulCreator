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


// #include "Exceptions/Exception.h"

#include "cv_SpeciesTitle.h"

cv_SpeciesTitle::cv_SpeciesTitle( Title tit, QString txt, cv_Species::Species spe ) {
	title = tit;
	name = txt;
	species = spe;
}


cv_SpeciesTitle::Title cv_SpeciesTitle::toTitle( QString str ) {
	if ( str == "Breed" )
		return cv_SpeciesTitle::Breed;
	else if ( str == "Faction" )
		return cv_SpeciesTitle::Faction;
	else if ( str == "Power" )
		return cv_SpeciesTitle::Power;
	else
		return cv_SpeciesTitle::TitleNo;
}



bool cv_SpeciesTitle::operator==( const cv_SpeciesTitle & tit ) const {
	if ( this == &tit ) {
		return true;
	}

	bool result = title == tit.title &&
				  name == tit.name &&
				  species == tit.species;

	return result;
}
