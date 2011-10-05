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

#ifndef CHARASPECIALTIES_H
#define CHARASPECIALTIES_H

// #include <QString>

#include "Storage/StorageCharacter.h"

#include "TraitSpecialties.h"



/**
 * @brief Diese Spezialisierungen werden direkt mit dem Charakter verknüpft.
 *
 * \todo Es wäre toll, wenn der Benutzer eigene Spezialisierungen eintragen könnte, zusätzlich zu denen, die schon angeboten werden.
 **/
class CharaSpecialties : public TraitSpecialties {
	Q_OBJECT

	public:
		/**
		 * Konstruktor
		 **/
		CharaSpecialties(QWidget* parent = 0);
		/**
		 * Zerstört das Objekt und gibt alle zugeteilten Ressourcen wieder frei.
		 **/
		~CharaSpecialties();

	private:
		StorageCharacter* character;

	public slots:

	private slots:
		/**
		 * Speichert die mit Haken versehenen Spezialisierungen bei den Charakterwerten im Speicher.
		 **/
		void saveSpecialties( QStringList list /** Liste der Spezialisierungen. */);
// 		/**
// 		 * Alle Fertigkeiten, die in \ref StorageCharacter und in \ref StorageTemplate aufgeführt sind, werden abgehakt.
// 		 **/
// 		void checkSpecialties( QStringList list /** Liste der abzuhakenden Spezialisierungen. */);

	signals:
};

#endif
