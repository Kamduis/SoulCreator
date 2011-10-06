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

#ifndef ADVANTAGESEWIDGET_H
#define ADVANTAGESEWIDGET_H

#include <QVBoxLayout>
#include <QGridLayout>
#include <QLabel>
#include <QSpinBox>

#include "TraitDots.h"
#include "Squares.h"
// #include "Storage/StorageTemplate.h"
// #include "Storage/StorageCharacter.h"
#include "Calc/CalcAdvantages.h"

#include <QWidget>


/**
 * @brief Das Widget, in welchem sämtliche berechneten Werte angeordnet sind.
 *
 * Die Werte, welche aus den Eigenschaften des Charakters berechnet werden, kommen allesamt in dieses Widget.
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

		QLabel* labelSizeValue;
		QLabel* labelInitiativeValue;
		QLabel* labelSpeedValue;
		QLabel* labelSuper;
		QLabel* labelFuel;
		TraitDots* dotsHealth;
		TraitDots* dotsSuper;
		Squares* squaresFuel;
		QLabel* fuelPerTurn;
		QSpinBox* spinBoxArmorGeneral;
		QSpinBox* spinBoxArmorFirearms;

	public slots:

	private slots:
		/**
		 * Schreibe die Größe in das Widget.
		 **/
		void writeSize( int size );
		void writeSize( cv_Species::SpeciesFlag );
		/**
		 * Schreibe die Initiative in das Widget.
		 **/
		void writeInitiative( int initiative );
		void writeInitiative( cv_Species::SpeciesFlag );
		/**
		 * Schreibe den Speed in das Widget.
		 **/
		void writeSpeed( int speed );
		void writeSpeed( cv_Species::SpeciesFlag );
		void printHealth( int value );
		void hideSuper( cv_Species::SpeciesFlag species );
		void setFuelMaximum( cv_Species::SpeciesFlag species );
		void setFuelMaximum( int value );
// 		void changeSuper(cv_Trait trait);
// 		void emitSuperChanged(int value);
		/**
		 * Schreibe die veränderte Rüstung in den Charkater.
		 **/
		void setArmor();
		/**
		 * Schreibe die veränderte Rüstung in das Widget.
		 **/
		void updateArmor(int general, int firearms);

	signals:
// 		void superChanged(cv_Trait trait);
};

#endif
