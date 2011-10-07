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

#ifndef SELECTWIDGET_H
#define SELECTWIDGET_H

#include <QVBoxLayout>
#include <QGridLayout>
#include <QLabel>
#include <QSpinBox>

#include "Widgets/Components/TraitDots.h"
#include "Widgets/Components/Squares.h"
// #include "Storage/StorageTemplate.h"
// #include "Storage/StorageCharacter.h"
#include "Calc/CalcAdvantages.h"

#include <QListWidget>


/**
 * @brief Das Widget, in welchem sämtliche berechneten Werte angeordnet sind.
 *
 * Die Werte, welche aus den Eigenschaften des Charakters berechnet werden, kommen allesamt in dieses Widget.
 **/

class SelectWidget : public QListWidget {
		Q_OBJECT

	public:
		/**
		 * Konstruktor
		 **/
		SelectWidget( QWidget *parent = 0 );
		/**
		 * Zerstört das Objekt und gibt alle zugeteilten Ressourcen wieder frei.
		 **/
		~SelectWidget();

	private:

	public slots:

	private slots:

	signals:
};

#endif
