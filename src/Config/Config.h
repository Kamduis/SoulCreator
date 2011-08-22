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

#ifndef CONFIG_H
#define CONFIG_H

#include <QString>
#include <QColor>

/**
 * @brief Konfigurationsklasse des Programms.
 *
 * Hier werden die Konfigurationseinstellungen gespeichert.
 */

class Config {
	public:
		/**
		 * Der Name des Programms.
		 */
		static QString name();
		/**
		 * Die aktuelle Version des Programms ausschließlich der Change-Nummer.
		 *
		 * Programme mit unterschieldicher Versionsnummer sind zueinander nicht notwendigerweise kompatibel.
		 */
		static QString version();
		/**
		 * Die aktuelle Version des Programms einschließlich der Change-Nummer.
		 *
		 * Unterscheiden sich Programme in ihrer Change-Nummer, aber der Rest ihrer Versionsnummer ist gleich, sollten eigentlich keine Kompatibilitätsprobleme mit den Template-Dateien und den gespeicherten Charakteren auftreten.
		 */
		static QString versionDetail();
		/**
		 * Der Pixelabstand zwischen Eigenschaftsblöcken. Beispielsweise der vertikale Abstand zwischen Den Fertigkeiten der verschiedenen Kategorien.
		 */
		static const int traitCategorySpace;
		/**
		 * Die Anzahl, wie oft Eigenschaften mit Beschreibungstext mehrfach ausgewählt werden dürfen.
		 */
		static const int traitMultipleMax;
		/**
		 * Die Zeit, wie lange Nachrichten in der Statuszeile angezeigt werden sollen.
		 */
		static const int displayTimeout;
		/**
		 * Wichtige Textabschnitte sollen in dieser Farbe erscheinen. Diese Funktion gibt den Farbnamen aus.
		 *
		 * \note Für die Farbe siehe auch importantTextColor().
		 **/
		static QString importantTextColorName();
		/**
		 * Wichtige Textabschnitte sollen in dieser Farbe erscheinen.
		 *
		 * \note Für den Farbnamen siehe auch importantTextColorName().
		 **/
		static QColor importantTextColor();
		/**
		 * Das Standardverzeichnis, in welchem die zu speichernden Charaktere abgelegt werden sollen.
		 **/
		static QString saveDir();
		/**
		 * Eigenschaftshöchstwert.
		 **/
		static const int traitMax;

	private:
		Config();
};

#endif


