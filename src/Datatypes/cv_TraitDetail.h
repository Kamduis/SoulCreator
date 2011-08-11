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

#ifndef CV_TRAITDETAIL_H
#define CV_TRAITDETAIL_H

#include <QString>
#include <QList>
#include <QStringList>

#include "cv_Species.h"

/**
 * @brief Speichert die zusätzlichen Parameter einer Eigenschaft.
 *
 * Bei Fertigkeiten sind diese zusätzlichen Parameter die Spezialisierungen, bei Merits die zusätzlichen Informationen.
 *
 * \todo Z. B. der Vorzug "Contacts" gibt 1 Kontakt für jeden Punkt. Diese einzelnen Kontakte werden dann in diesem struct abgelegt.
 */
struct cv_TraitDetail {
	/**
	 * Der Name der Zusatzeigenschaft.
	 **/
	QString name;
	/**
	 * Ist die Zusatzeigenschaft aktiv. (Besitzt der Charakter diese Spezialisierung?)
	 **/
	bool value;
// 	/**
// 	 * Welche Spezies über diese Zusatzeigenschaft verfügen.
// 	 **/
// 	cv_Species::Species species;

	/**
	 * Vergleich zwischen zwei Instanzen dieser Klasse.
	 **/
	bool operator==(const cv_TraitDetail &detail) const;
};

#endif
