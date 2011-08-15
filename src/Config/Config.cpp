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

#include "CMakeConfig.h"

#include "Config.h"

const int Config::traitCategorySpace = 10;

const int Config::traitMultipleMax = 3;

const int Config::displayTimeout = 10000;

QString Config::name() {
	return PROGRAM_NAME;
}

QString Config::version() {
	return QString::number( PROGRAM_VERSION_MAJOR ) +
		   "." +
		   QString::number( PROGRAM_VERSION_MINOR ) +
		   "." +
		   QString::number( PROGRAM_VERSION_CHANGE );
}

QString Config::importantTextColorName() {
	return "darkBlue";
}

QColor Config::importantTextColor() {
	return QColor( "importantTextColorName" );
}

QString Config::saveDir() {
	return "save";
}




Config::Config() {
}