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
const int Config::traitMax = 5;
const int Config::moralityTraitMax = 10;
const int Config::derangementMoralityTraitMax = 7;
const int Config::moralityTraitDefaultValue = 7;
const int Config::willpowerMax = 10;
const int Config::superTraitMin = 1;
const int Config::superTraitMax = 10;
const int Config::superTraitDefaultValue = 1;

const qreal Config::textSizeFactorPrintNormal = 0.45;
const qreal Config::textSizeFactorPrintSmall = 0.35;


QString Config::name() {
	return PROGRAM_NAME;
}

QString Config::version() {
	return QString::number( PROGRAM_VERSION_MAJOR ) +
		   "." +
		   QString::number( PROGRAM_VERSION_MINOR );
}

QString Config::versionDetail() {
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
