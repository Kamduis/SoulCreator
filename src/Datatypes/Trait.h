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

#ifndef TRAIT_H
#define TRAIT_H

#include <QFlags>
#include <QString>
#include <QList>
#include <QStringList>

#include "cv_Species.h"
#include "cv_TraitDetail.h"

#include "cv_Trait.h"
#include <QObject>

/**
 * @brief Speichert alle Eigenschaften einer einzigen Charaktereigenschaft.
 *
 * Simple Eigenschaften wie Attribute haben nur Name und Wert. Bei Fertigkeiten kommen bereits die Spezialisierungen hinzu, bei  Vorzügen noch die Einschränkungen etc.
 */
class Trait : public QObject, public cv_Trait {
	Q_OBJECT
	
	public:
		/**
		 * Konstruktor.
		 **/
		Trait(QString txt = "", int val = 0, cv_Species::Species spe = cv_Species::SpeciesNo, cv_AbstractTrait::Type ty = cv_AbstractTrait::TypeNo, cv_AbstractTrait::Category ca = cv_AbstractTrait::CategoryNo, QObject* parent = 0);
		/**
		 * Konstruktor.
		 *
		 * Dieser Konstruktor erzeugt ein Objekt dieser Klasse aus einem cv_Trait-Objekt.
		 **/
		Trait( cv_Trait trait, QObject* parent = 0 );
		/**
		 * Konstruktor.
		 *
		 * Dieser Konstruktor erzeugt ein neues Objekt aus einem bereits existierenden Trait-Objekt.
		 **/
		Trait( Trait* trait, QObject* parent = 0 );

	public slots:
		/**
		 * Verändert den Wert der Eigenschaft.
		 **/
		void setValue(int val);

	signals:
		/**
		 * Der Wert der Eigenschaft hat sich verändert.
		 **/
		void valueChanged(int);
};

#endif

