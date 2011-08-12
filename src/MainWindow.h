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

#ifndef MAINWINDOW_H
#define MAINWINDOW_H


#include "IO/ReadXmlCharacter.h"
#include "IO/WriteXmlCharacter.h"
#include "Widgets/InfoWidget.h"
#include "Widgets/AttributeWidget.h"
#include "Widgets/SkillWidget.h"
#include "Widgets/MeritWidget.h"
#include "Widgets/CharaSpecialties.h"

#include <QMainWindow>


namespace Ui {
class MainWindow;
}

/**
 * @brief Das Hauptfenster der Anwendung.
 *
 * Hier werden die Widgets präsentiert und die hier laufen die Verbindungen zwischen den einzelnen Objekten zusammen.
 *
 * \todo Bei den Merits gibt es den effekt Custom. Den will ich aber eigentlich garnicht. Ich will den Inhalt einer Textbox speichern. Im Templete mag es dan custom=true geben, beim Speichern des Charakters aber muß es dann custom="Inhalt" sein. Außerdem gibt es dann beispielsweise den merit Language mehrfach. Muß also auch nach custom unterschieden werden.
 *
 * \todo Ich muß in StorageCharacter nichts speichern, daß den Wert 0 hat. Das kann aus dem Speicher gelöscht werden.
 */

class MainWindow : public QMainWindow {
		Q_OBJECT

	public:
		/**
		 * Konstruktor
		 **/
		MainWindow( QWidget* parent = 0 );
		/**
		 * Zerstört das Objekt und gibt alle zugeteilten Ressourcen wieder frei.
		 **/
		~MainWindow();

	private:
		/**
		 * Graphische Benutzeroberfläche, erstellt mit dem Designer.
		 */
		Ui::MainWindow* ui;

		/**
		 * In diesem Widget werden die Attribute in Spalten sortiert angezeigt.
		 **/
		InfoWidget* info;
		/**
		 * In diesem Widget werden die Informationen über den Charakter (Name, Spezies, Geschlecht ...) angezeigt.
		 **/
		AttributeWidget* attributes;
		/**
		 * In diesem Widget werden die Fertigkeiten in Spalten sortiert angezeigt.
		 **/
		SkillWidget* skills;
		/**
		 * In diesem Widget werden die Merits angezeigt.
		 *
		 * \todo Irgendwann soll die Anzahl der angezeigten Merits vom user durch klicken irgendwie erhöht werden können.
		 **/
		MeritWidget* merits;
		/**
		 * Das Widget für die Anzeige von Spezialisierungen einer Fertigkeit.
		 **/
		CharaSpecialties* specialties;
		/**
		 * Über diesen Zeiger kann die Klasse aufgerufen werden, welche für das Speichern des Charakters zuständig ist.
		 **/
		ReadXmlCharacter* readCharacter;
		/**
		 * Über diesen Zeiger kann die Klasse aufgerufen werden, welche für das Speichern des Charakters zuständig ist.
		 **/
		WriteXmlCharacter* writeCharacter;

	public slots:

	private slots:
		/**
		 * Initialisiert das Programm.
		 *
		 * Die Connections werden erzeugt und die einzelnen Teilinitialisierungen aufgerufen. Diese Funktion dient primär dazu, den Konstruktor übersichtlich zu halten.
		 */
		void initialize();
		/**
		 * In dieser Funktion werden die Template-Daten aus den XML-Dateien ausgelesen und gespeichert, um damit zu einem späteren Zeitpunkt die GUI füllen zu können.
		 **/
		void storeTemplateData();
		/**
		 * Die Graphische Oberfläche wird bevölkert.
		 **/
		void populateUi();
		/**
		 * Werte des Charakters auf der Oberfläche anzeigen.
		 **/
		void showCharacterTraits();
		/**
		 * Spezialisierungen einer Fertigkeit anzeigen.
		 **/
		void showSkillSpecialties( bool sw, QString skillName, QList< cv_TraitDetail > specialtyList );
		/**
		 * Aktiviert die Anwendung zur Benutzung.
		 *
		 * Da die Anwendung bei Anzeige des LoginDialog deaktiviert ist, muß sie erst wieder aktiviert werden, ehe der Nutzer seine Eingaben machen kann. Natürlich soll die Anwendung nur für den angemeldeten Benutzer aktiviert werden.
		 */
		void activate();
		/**
		 * Über diese Funktion wird der Dialog aufgerufen, um einen gespeicherten Charakter in das Programm laden zu können.
		 **/
		void openCharacter();
		/**
		 * Über diese Funktion wird erst der Dialog aufgerufen zum Aussuchen des Speicherortes und danach dann das Schreiben des Charakters in eine XML-Datei eingeletiet.
		 **/
		void saveCharacter();

	signals:
};

#endif
