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
 *
 * Die hier deklarierten Berechnungsfunktionen werden zwar bei der Änderung jeder Eigenschaft aufgerufen, aber berechnen die Werte nur, wenn eine Eigenschaft verändert wurde, welche Einfluß auf das Ergebnis nimmt. Sie geben allerdings immer das Ergebnis der berechnung aus. Entweder den neuen Wert, oder den alten Wert, der in dieser Klasse gespeichert wird.
 */

class CalcAdvantages : public QObject {
		Q_OBJECT

	public:
		CalcAdvantages( QObject* parent = 0 );

	private:
		StorageCharacter* character;

		int v_size;
		int v_initiative;
		int v_speed;
		int v_defense;
		int v_health;
		int v_willpower;

	private slots:
		/**
		 * Berechnung der Größe des Charakters.
		 *
		 * \todo Bislang nur vom Merit Size abhängig. Nicht von anderen Merits oder dem Alter (Kinder haben Size = 4).
		 **/
		int calcSize( cv_Trait trait );
		/**
		 * Berechnung der Initiative des Charakters.
		 *
		 * \todo Bislang nur von Dexterity, Composure und Fast Reflexes abhängig.
		 **/
		int calcInitiative( cv_Trait trait );
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
		/**
		 * Berechnung der Gesundheit.
		 *
		 * Dieser Slot wird nur bei einer Veränderung von Stamina angesprochen. Für eine Veränderung der Größe gibt es einen extra slot (siehe calcHealth( int size )).
		 **/
		int calcHealth( cv_Trait trait );
		/**
		 * Berechnung der Willenskraft.
		 **/
		int calcWillpower( cv_Trait trait );
		/**
		 * Berechnung der Gesundheit.
		 *
		 * Dieser Slot wird nur bei einer Veränderung der Größe angesprochen. Für eine Veränderung der Stamina gibt es einen extra slot (siehe calcHealth( cv_Trait trait )).
		 **/
		int calcHealth( int size );

	signals:
		/**
		 * Size hat sich verändert.
		 **/
		void sizeChanged( int );
		/**
		 * Initiative hat sich verändert.
		 **/
		void initiativeChanged( int );
		/**
		 * Speed hat sich verändert.
		 **/
		void speedChanged( int );
		/**
		 * Defense hat sich verändert.
		 **/
		void defenseChanged( int );
		/**
		 * Health hat sich verändert.
		 **/
		void healthChanged( int );
		/**
		 * Die Willenskraft hat sich verändert.
		 **/
		void willpowerChanged( int );
};

#endif

