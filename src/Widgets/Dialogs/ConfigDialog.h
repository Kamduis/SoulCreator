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

#ifndef CONFIGUREDIALOG_H
#define CONFIGUREDIALOG_H

#include <QDialog>


namespace Ui {
class ConfigDialog;
}

/**
 * @brief Konfigurationsdialog, in welchem die Einstellungen für das Programm geändert werden können.
 *
 * Die verschiedenen Einstellungen werden erst dann gespeichert, wenn der Dialog akzeptiert wird.
 **/
class ConfigDialog : public QDialog {
		Q_OBJECT

	public:
		/**
		 * Konstruktor
		 **/
		ConfigDialog( QWidget *parent = 0 );
		/**
		 * Zerstört das Objekt und gibt alle zugeteilten Ressourcen wieder frei.
		 **/
		~ConfigDialog();

	private:
		/**
		 * Graphische Benutzeroberfläche, erstellt mit dem Designer.
		 */
		Ui::ConfigDialog* ui;

	public slots:

	private slots:
		/**
		 * Speichert die im Dialog vorgenommen Änderungen.
		 **/
		void saveChanges();

	signals:
};

#endif
