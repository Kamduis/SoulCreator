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

#ifndef TRAITBONUS_H
#define TRAITBONUS_H

#include "Trait.h"

/**
 * @brief Speichert eine Bonuseiegnschaft des Charakters
 *
 * Dieser Datentyp enthält die Bonuseigenschaft, welche dem Charkater zur Verfügung stehen könnte, und die Eigenschaft, von welcher dieser Umstand abhängt.
 */
class TraitBonus : public Trait {
	Q_OBJECT
	
	public:
		/**
		 * Konstruktor.
		 **/
		TraitBonus(Trait* tr1, QString breed, QObject* parent = 0);

		/**
		 * Zugriff auf die Voraussetzung für diese Bonuseigenschaft.
		 **/
		QString breedDependant() const;
	private:
		QString v_breedDependant;

	public slots:

	private slots:

	signals:

};

#endif

