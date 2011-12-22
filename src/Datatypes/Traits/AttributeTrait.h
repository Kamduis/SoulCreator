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

#ifndef ATTRIBUTETRAIT_H
#define ATTRIBUTETRAIT_H

#include "Trait.h"

/**
 * @brief Repräsentation eines einzelnen Attributs.
 */
class AttributeTrait : public Trait {
		Q_OBJECT

	public:
		/**
		 * Konstruktor.
		 **/
		AttributeTrait( QString txt = "" /** Name */,
			   int val = 0 /** Wert */,
			   cv_Species::Species spe = cv_Species::SpeciesNo /** Sämtliche Spezies, welche über diese Eigenscahft verfügen sollen. */,
			   cv_AbstractTrait::Category ca = cv_AbstractTrait::CategoryNo /** Die Kategorie, welcher diese Eigenschaft angehört. */,
			   QObject* parent = 0 );
		/**
		 * Konstruktor.
		 *
		 * Dieser Konstruktor erzeugt ein Objekt dieser Klasse aus einem cv_Trait-Objekt.
		 **/
		AttributeTrait( cv_Trait trait, QObject* parent = 0 );
		/**
		 * Konstruktor.
		 **/
		AttributeTrait( Trait* trait, QObject* parent = 0 );

		/**
		 * Gibt den Wert der Eigenschaft wieder zurück.
		 *
		 * Bei Attributen ist der zurückgegebene Wert um +1 höher als der intern gespeicherte Wert, \emph{wenn} isBonus() "true" zurückgibt.
		 *
		 * \bug Durch diese Funktion kann ich das Widget CharaTrait nichtmehr richtig verwenden, da ja immer ein Punkt mehr angezeigt wird, als ich eigentlich klicke, und ich so nicht auf 0 oder 1 kommen kann.
		 **/
		virtual int value() const;

	private:

	public slots:
		/**
		 * Legt fest, ob diese Eigenschaft eine Bonuseigenschaft ist.
		 *
		 * Dadurch kann sich die Darstellung des Eigenscahftswerts ändern (\sa value()) ändern, weswegen in diesem besonderen Fall auch valueChanged(int) aufegrufen wird.
		 **/
		virtual void setBonus(bool sw);

	private slots:

	signals:
};

#endif

