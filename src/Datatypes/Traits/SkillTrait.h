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

#ifndef SKILLTRAIT_H
#define SKILLTRAIT_H

#include "Trait.h"

/**
 * @brief Repräsentation einer einzelnen Fertigkeit.
 */
class SkillTrait : public Trait {
		Q_OBJECT

	public:
		/**
		 * Konstruktor.
		 **/
		SkillTrait( QString txt = "" /** Name */,
			   int val = 0 /** Wert */,
			   cv_Species::Species spe = cv_Species::SpeciesNo /** Sämtliche Spezies, welche über diese Eigenscahft verfügen sollen. */,
			   cv_AbstractTrait::Category ca = cv_AbstractTrait::CategoryNo /** Die Kategorie, welcher diese Eigenschaft angehört. */,
			   QObject* parent = 0 );
		/**
		 * Konstruktor.
		 *
		 * Dieser Konstruktor erzeugt ein Objekt dieser Klasse aus einem cv_Trait-Objekt.
		 **/
		SkillTrait( cv_Trait trait, QObject* parent = 0 );
		/**
		 * Konstruktor.
		 **/
		SkillTrait( Trait* trait, QObject* parent = 0 );
};

#endif

