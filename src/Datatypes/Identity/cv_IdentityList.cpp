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

#include "cv_IdentityList.h"

cv_IdentityList::cv_IdentityList( QString sureName, QString firstName ): QList< cv_Identity >() {
	cv_Identity nameSet( sureName, firstName );
	this->append( nameSet );
}


QString cv_IdentityList::realName() const {
	QString name = this->at( 0 ).birthName();
	return name;
}


void cv_IdentityList::reset() {
	this->clear();
	cv_Identity nameSet;
	this->append( nameSet );
}



