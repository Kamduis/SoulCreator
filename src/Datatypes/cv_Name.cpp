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

#include "cv_Name.h"

cv_Name::cv_Name( QString surename, QString firstname ) {
	foreNames.append( firstname );
	sureName = surename;
	honorificName = "";
	nickName = "";
	supernaturalName = "";
}


QString cv_Name::firstName() const {
	return foreNames.at( 0 );
}

QString cv_Name::birthName() const {
	if (firstName().isEmpty() || sureName.isEmpty()){
		// In diesem Fall benötige ich keinen Abstand zwischen den Namen, da je einer leer ist.
		return firstName() + sureName;
	} else {
		return firstName() + " " + sureName;
	}

}

QString cv_Name::displayNameFull( QString last, QStringList fores ) {
	QString displayFull;
	if ( !fores.isEmpty() ) {
		displayFull = fores.at(0);
		for (int i = 1; i < fores.count(); i++){
			displayFull += " " + fores.at(i);
		}
	}
	// Vor dem Nachnamen nur dann ein Leerzeichen, wenn schon etwas davor steht.
	if ( !displayFull.isEmpty() ) {
		displayFull += " ";
	}
	displayFull += last;

	return displayFull;
}
QString cv_Name::displayNameFull( QString last, QString fore ) {
	QString displayFull = last;
	if ( !fore.isEmpty() ) {
		displayFull += " " + fore;
	}
	// Vor dem Nachnamen nur dann ein Leerzeichen, wenn schon etwas davor steht.
	if ( !displayFull.isEmpty() ) {
		displayFull += " ";
	}
	displayFull += last;

	return displayFull;
}

QString cv_Name::displayNameDisplay( QString last, QString first, QString nick ) {
	QString displayDisplay = first;
	if ( !nick.isEmpty() ) {
		displayDisplay += " \"" + nick + "\"";
	}
	// Vor dem Nachnamen nur dann ein Leerzeichen, wenn schon etwas davor steht.
	if ( !displayDisplay.isEmpty() ) {
		displayDisplay += " ";
	}
	displayDisplay += last;

	return displayDisplay;
}

QString cv_Name::displayNameHonor( QString first, QString honor ) {
	QString displayHonor = first;
	if ( !honor.isEmpty() ) {
		displayHonor += " " + honor;
	}

	return displayHonor;
}

