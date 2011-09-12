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
#include "../Config/Config.h"
#include "../Datatypes/cv_Shape.h"

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

		/**
		 * Berechnet die Größe des Charakters abhängig von den unterschiedlichen Gestalten.
		 *
		 * \note Es wird auf das Ergebnis der Funktion calcSize() zurückgegriffen, welche bei jeder Veränderung einer Eigenschaft, die Auswirkung auf die Size haben kann, aufgerufen wird.
		 **/
		int size( cv_Shape::WerewolfShape shape = cv_Shape::ShapeNo ) const;
		/**
		 * Berechnet die Initiative des Charakters abhängig von den unterschiedlichen Gestalten.
		 *
		 * \note Es wird auf das Ergebnis der Funktion calcInitiativa() zurückgegriffen, welche bei jeder Veränderung einer Eigenschaft, die Auswirkung auf die Initiative haben kann, aufgerufen wird.
		 **/
		int initiative(cv_Shape::WerewolfShape shape = cv_Shape::ShapeNo) const;
		/**
		 * Berechnet die Geschwindigkeit des Charakters abhängig von den unterschiedlichen Gestalten.
		 *
		 * \note Es wird auf das Ergebnis der Funktion calcSpeed() zurückgegriffen, welche bei jeder Veränderung einer Eigenschaft, die Auswirkung auf diee Eigenschaft haben kann, aufgerufen wird.
		 **/
		int speed(cv_Shape::WerewolfShape shape = cv_Shape::ShapeNo) const;
		/**
		 * Berechnet die Defensive des Charakters.
		 **/
		int defense() const;
		/**
		 * Berechnet die Gesundheit des Charakters.
		 **/
		int health() const;
		/**
		 * Berechnet die Willenskraft des Charakters.
		 **/
		int willpower() const;

		static int strength( int str, cv_Shape::WerewolfShape shape = cv_Shape::ShapeNo );
		static int dexterity( int dex, cv_Shape::WerewolfShape shape = cv_Shape::ShapeNo );
		static int stamina( int sta, cv_Shape::WerewolfShape shape = cv_Shape::ShapeNo );
		
	private:
		StorageCharacter* character;

		static int v_size;
		static int v_initiative;
		static int v_speed;
		static int v_defense;
		static int v_health;
		static int v_willpower;

	private slots:
		/**
		 * Berechnung der Größe des Charakters.
		 *
		 * \todo Bislang nur vom Merit Size abhängig. Nicht von anderen Merits oder dem Alter (Kinder haben Size = 4).
		 **/
		int calcSize( cv_Trait* trait );
		/**
		 * Berechnung der Initiative des Charakters.
		 *
		 * \todo Bislang nur von Dexterity, Composure und Fast Reflexes abhängig.
		 **/
		int calcInitiative( cv_Trait* trait );
		/**
		 * Berechnung der Geschwindigkeit des Charakters.
		 *
		 * \todo Bislang nur von Strength und Dexterity abhängig.
		 **/
		int calcSpeed( cv_Trait* trait );
		/**
		 * Berechnung der Defense
		 *
		 * \todo Bislang nicht von der Spezies abhängig. Tiere haben stets das größere von Dex und Wits als Defense.
		 **/
		int calcDefense( cv_Trait* trait );
		/**
		 * Berechnung der Gesundheit.
		 *
		 * Dieser Slot wird nur bei einer Veränderung von Stamina angesprochen. Für eine Veränderung der Größe gibt es einen extra slot (siehe calcHealth( int size )).
		 **/
		int calcHealth( cv_Trait* trait );
		/**
		 * Berechnung der Willenskraft.
		 **/
		int calcWillpower( cv_Trait* trait );
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

