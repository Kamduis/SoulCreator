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

#ifndef ADVANTAGESEWIDGET_H
#define ADVANTAGESEWIDGET_H

#include <QVBoxLayout>
#include <QGridLayout>
#include <QLabel>

#include "TraitDots.h"
#include "MoralityWidget.h"
#include "../Storage/StorageTemplate.h"
#include "../Storage/StorageCharacter.h"
#include "../Calc/CalcAdvantages.h"

#include <QWidget>


/**
 * @brief Das Widget, in welchem sämtliche berechneten Werte angeordnet sind.
 *
 * Die Werte, welche aus den Eigenschaften des Charakters berechnet werden, kommen allesamt in dieses Widget.
 *
 * \todo Armor und Superattribut müssen noch gespeichert werden, wenn der Charakter gespeichert wird.
 *
 * \todo Eine fuelWidget-Klasse muß erstellt und hier eingefügt werden, damit auch Mana, Glamour etc. angezeigt wird. Und zwar soviel, wie in den Template-DAteien festgelegt wird.
 **/
class AdvantagesWidget : public QWidget {
		Q_OBJECT

	public:
		/**
		 * Konstruktor
		 **/
		AdvantagesWidget( QWidget *parent = 0 );
		/**
		 * Zerstört das Objekt und gibt alle zugeteilten Ressourcen wieder frei.
		 **/
		~AdvantagesWidget();

	private:
		/**
		 * In diesem Layout werden die berechneten Charakterwerte angeordnet.
		 **/
		QVBoxLayout *layout;
		QGridLayout *advantagesLayout;
		StorageTemplate* storage;
		StorageCharacter* character;
		CalcAdvantages* calcAdvantages;
		MoralityWidget* moralityWidget;

		QLabel* labelSuper;
		TraitDots* dotsHealth;
		TraitDots* dotsSuper;

	public slots:

	private slots:
		void printHealth(int value);
		void hideSuper(cv_Species::SpeciesFlag species);
// 		void changeSuper(cv_Trait trait);
// 		void emitSuperChanged(int value);

	signals:
// 		void superChanged(cv_Trait trait);
};

#endif
