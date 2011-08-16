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

#ifndef STRINGBOOLPARSER_H
#define STRINGBOOLPARSER_H

#include "../Datatypes/cv_Species.h"
#include "../Datatypes/cv_Trait.h"

#include <QObject>


/**
 * @brief Bedinungen aus String lesen.
 *
 * Mit Hilfe dieser Klasse werden die Bedinungen aus einem String in auswertbare Bedinungen umgewandelt.
 */

class StringBoolParser : public QObject {
	public:
		bool validate( QString checkString );

	private:
		enum Token {
			AND,
			OR,
			EQUAL,
			GREATER,
			GREATEREQUAL,
			SMALLER,
			SMALLEREQUAL,
			LPAR,
			RPAR,
			NUMBER,
			END,
			ERROR
		};

		/**
		 * Das zuletzt erkannte Token.
		 **/
		Token actualToken;
		/**
		 * Dder Wert bei Zahlenkonstanten
		 **/
		double tokenNumberValue;
		/**
		 * Programm-Position
		 **/
		char* srcPos;

		Token nextToken();
		bool compare();
		bool paranthesis();
		bool operatorOR();
		bool operatorAND();
};

#endif
