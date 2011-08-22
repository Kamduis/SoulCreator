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

#ifndef CALCADVANTAGES_H
#define CALCADVANTAGES_H

#include "../Storage/StorageCharacter.h"

#include <QObject>

/**
 * \brief Diese Klasse führt die berechnung der abgeleiteten Eigenschaften durch.
 */
class CalcAdvantages : public QObject {
		Q_OBJECT

	public:
		CalcAdvantages( QObject* parent = 0 );

	private:
		StorageCharacter* character;

	public slots:
		/**
		 * Berechnung der Größe des Charakters.
		 *
		 * \todo Bislang nur vom Merit Size abhängig. Nicht von anderen Merits oder dem Alter (Kinder haben Size = 4).
		 **/
		int calcSize( cv_Trait trait );
		/**
		 * Berechnung der Geschwindigkeit des Charakters.
		 *
		 * \todo Bislang nur von Strength und Dexterity abhängig.
		 **/
		int calcSpeed( cv_Trait trait );
		/**
		 * Berechnung der Defense
		 *
		 * \todo Bislang nicht von der Spezies abhängig. Tiere haben stets das größere von Dex und Wits als Defense.
		 **/
		int calcDefense( cv_Trait trait );

	signals:
		void sizeChanged(int);
		void speedChanged(int);
		void defenseChanged(int);
};

#endif

