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

#ifndef MERITWIDGET_H
#define MERITWIDGET_H

#include <QVBoxLayout>
#include <QScrollArea>
#include <QPushButton>

#include "../Datatypes/cv_TraitDetail.h"
#include "Dialogs/SelectMeritsDialog.h"

#include <QWidget>


/**
 * @brief Das Widget, in welchem sämtliche Merits angeordnet sind.
 *
 * \todo Einen Knopf erstellen, über den der benutzer angeben kann, welche Merits er denn wirklich alle angezeigt haben will.
 *
 * \todo Bei Merits mit Zusatztext (Language) in diesem men+ ein Zahlenfle dangeben, bei welchem der benutzer einstellen kann, wieviele verschiedene dieser scheinbar identischen merits er angezeigt haben will.
 *
 * \todo Eigenscahften mit Zusatztext benötigen mehr vertikalen Raum als die anderen. Sieht nicht gut aus.
 **/
class MeritWidget : public QWidget {
		Q_OBJECT

	public:
		MeritWidget( QWidget *parent = 0 );
		/**
		 * Zerstört das Objekt und gibt alle zugeteilten Ressourcen wieder frei.
		 **/
		~MeritWidget();

	private:
		QScrollArea* scrollArea;
// 		QPushButton* button;
// 		SelectMeritsDialog* dialog;

	public slots:

	private slots:

	signals:
};

#endif
