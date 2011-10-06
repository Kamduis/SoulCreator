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

#ifndef CALCADVANTAGES_H
#define CALCADVANTAGES_H

#include "Storage/StorageCharacter.h"
// #include "Config/Config.h"
#include "Datatypes/cv_Shape.h"
#include "Datatypes/Trait.h"

#include <QObject>

/**
 * \brief Diese Klasse führt die berechnung der abgeleiteten Eigenschaften durch.
 *
 * Die hier deklarierten Berechnungsfunktionen werden zwar bei der Änderung jeder Eigenschaft aufgerufen, aber berechnen die Werte nur, wenn eine Eigenschaft verändert wurde, welche Einfluß auf das Ergebnis nimmt. Sie geben allerdings immer das Ergebnis der berechnung aus. Entweder den neuen Wert, oder den alten Wert, der in dieser Klasse gespeichert wird.
 */

class CalcAdvantages : public QObject {
		Q_OBJECT

	public:
		/**
		 * Konstruktor.
		 **/
		CalcAdvantages( QObject* parent = 0 );
		/**
		 * Konstruktor, welcher direkt Zeiger zu den relevanten Eigenschaften erfordert, um nur dann neu zu berechnen, wenn diese sich ändern.
		 *
		 * \todo Hat noch keinen Effekt.
		 *
		 * \todo Soll später den Konstruktor ersetzen.
		 **/
		CalcAdvantages( Trait* tmp /** Temporär, damit der Konstruktor überladen wird. */,
						QObject* parent = 0 );
		/**
		 * Destruktor.
		 *
		 * Gibt die verwendeten Ressourcen wieder frei.
		 **/
		~CalcAdvantages();

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
		int initiative( cv_Shape::WerewolfShape shape = cv_Shape::ShapeNo ) const;
		/**
		 * Berechnet die Geschwindigkeit des Charakters abhängig von den unterschiedlichen Gestalten.
		 *
		 * \note Es wird auf das Ergebnis der Funktion calcSpeed() zurückgegriffen, welche bei jeder Veränderung einer Eigenschaft, die Auswirkung auf diee Eigenschaft haben kann, aufgerufen wird.
		 **/
		int speed( cv_Shape::WerewolfShape shape = cv_Shape::ShapeNo ) const;
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
		static int manipulation( int man, cv_Shape::WerewolfShape shape = cv_Shape::ShapeNo );

	private:
		StorageCharacter* character;

		Trait* attrWit;
		Trait* attrRes;
		Trait* attrStr;
		Trait* attrDex;
		Trait* attrSta;
		Trait* attrCom;
		Trait* meritGiant;
		Trait* meritFastReflexes;
		Trait* meritFleetOfFoot;

		static int v_size;
		static int v_initiative;
		static int v_speed;
		static int v_defense;
		static int v_health;
		static int v_willpower;

		/**
		 * Findet anwendung in sämtlichen Konstruktoren.
		 **/
		void construct();

	private slots:
		/**
		 * Berechnung der Größe des Charakters.
		 *
		 * \todo Bislang nur vom Merit Size abhängig. Nicht von anderen Merits oder dem Alter (Kinder haben Size = 4).
		 **/
		int calcSize();
		/**
		 * Berechnung der Initiative des Charakters.
		 *
		 * \todo Bislang nur von Dexterity, Composure und Fast Reflexes abhängig.
		 **/
		int calcInitiative();
		/**
		 * Berechnung der Geschwindigkeit des Charakters.
		 *
		 * \todo Bislang nur von Strength und Dexterity abhängig.
		 **/
		int calcSpeed();
		/**
		 * Berechnung der Defense
		 *
		 * \todo Bislang nicht von der Spezies abhängig. Tiere haben stets das größere von Dex und Wits als Defense.
		 **/
		int calcDefense();
		/**
		 * Berechnung der Gesundheit.
		 **/
		int calcHealth();
		/**
		 * Berechnung der Willenskraft.
		 **/
		int calcWillpower();

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

