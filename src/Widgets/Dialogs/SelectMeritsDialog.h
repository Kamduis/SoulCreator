/**
 * \file
 * \author Victor von Rhein <victor@caern.de>
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

#ifndef CHOOSEMERITSDIALOG_H
#define CHOOSEMERITSDIALOG_H

#include <QGridLayout>

#include <QDialog>


namespace Ui {
class SelectMeritsDialog;
}

/**
 * @brief Dialog zur Auswahl der darzustellenden Merits.
 *
 * Alle Merits darzustellen ist wohl etwas viel. Über diesen Dialog kann der Benutzer auswählen, welche und im Falle von Merits mit Zusatztext, wieviele er angezeigt haben möchte.
 **/
class SelectMeritsDialog : public QDialog {
		Q_OBJECT

	public:
		/**
		 * Konstruktor
		 **/
		SelectMeritsDialog( QWidget *parent = 0 );
		/**
		 * Zerstört das Objekt und gibt alle zugeteilten Ressourcen wieder frei.
		 **/
		~SelectMeritsDialog();

	private:
		/**
		 * Graphische Benutzeroberfläche, erstellt mit dem Designer.
		 */
		Ui::SelectMeritsDialog* ui;

	public slots:

	private slots:

	signals:
};

#endif
