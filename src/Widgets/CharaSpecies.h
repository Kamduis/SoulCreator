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

#ifndef CHARASPECIES_H
#define CHARASPECIES_H

#include "Storage/StorageCharacter.h"
// #include "Datatypes/cv_Trait.h"
// #include "Datatypes/cv_TraitDetail.h"

#include <QComboBox>

/**
 * @brief Mit den gespeicherten Werten vernetzte Darstellung der Spezies auf dem Charakterbogen.
 *
 * Diese Combobox ist direkt mit den im Speicher vorgehaltenen Charakterdaten verknüpft. Verändert sich das Widget, wird der Speicher aktualisiert, verändert sich der Speicher, wird das Widget aktualisiert.
 **/

class CharaSpecies : public QComboBox {
		Q_OBJECT

	public:
		/**
		 * Konstruktor.
		 **/
		CharaSpecies( QWidget *parent );
		/**
		 *Zerstört das Objekt und gibt alle zugeteilten Ressourcen wieder frei.
		 **/
		~CharaSpecies();

		/**
		 * Gibt die Spezies zurück.
		 **/
		cv_Species::SpeciesFlag species() const;

	private:
		StorageCharacter *character;

		cv_Species::SpeciesFlag v_species;

	public slots:
		/**
		 * Legt die Spezies fest. Die ComboBox wird auf den Index gelegt, der der Spezies zugeordnet ist.
		 *
		 * \exception eSpeciesNotExisting Da setSpecies aber auch über eine SLOT-Funktion aufgerufen wird, existiert in dieser Klasse keine try-Block!
		 **/
		void setSpecies( cv_Species::SpeciesFlag species );

	private slots:
		void emitSpeciesChanged( int index );
		void setStorageSpecies( cv_Species::SpeciesFlag species );

	signals:
		void speciesChanged( cv_Species::SpeciesFlag species );
};

#endif
