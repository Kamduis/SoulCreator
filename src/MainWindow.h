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

#include "Storage/StorageTemplate.h"
#include "Storage/StorageCharacter.h"
#include "IO/ReadXmlCharacter.h"
#include "IO/WriteXmlCharacter.h"
#include "Widgets/InfoWidget.h"
#include "Widgets/AttributeWidget.h"
#include "Widgets/SkillWidget.h"
#include "Widgets/MeritWidget.h"
#include "Widgets/PowerWidget.h"
#include "Widgets/AdvantagesWidget.h"
#include "Widgets/CharaSpecialties.h"
#include "Draw/DrawSheet.h"

#include <QMainWindow>


namespace Ui {
class MainWindow;
}

/**
 * @brief Das Hauptfenster der Anwendung.
 *
 * Hier werden die Widgets präsentiert und die hier laufen die Verbindungen zwischen den einzelnen Objekten zusammen.
 *
 * \todo Die Information, daß manche Merits nur bei Charaktererschaffung gewählt werden können, in das Programm einbinden.
 *
 * \bug Language mit Zusatztext wird nicht geladen. Bzw. wird schon geladen, aber nicht richtig dargestellt.
 *
 * \bug Wechselt man die Spezies, werden die alten Powers nicht restlos gelöscht. Zumindest jene nicht, welche Zusatztext besitzen.
 *
 * \todo Beim Wechseln zwischen den Spezies eie Warnung ausgeben, wenn Powers und Merits gelöscht würden.
 *
 * \todo Bei den Werwölfen müssen die Kräfte, welche je nach Vorzeichen nicht erlaubt sind, ausfgegraut werden.
 *
 * \todo Bei Werwölfen nimmt "Rites" eine Sonderstellung ein. Auch die Gaben/Riten müssen berücksichtigt werden.
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
		 * Zeiger auf die Klasse, welche sämtliche Eigenschaftsbezeichnungen enthält.
		 */
		StorageTemplate* storage;
		/**
		 * Zeiger auf die Klasse, welche sämtliche Charaterwerte enthält. Eine Änderung der Werte in dieser Klasse sorgen dafür, daß sich auch die Anzeige anpaßt. Und ändert man einen Wert in der Anzeige, wird automatisch die dadurch repräsentierte Eigenschaft in dieser Klasse verändert.
		 */
		StorageCharacter* character;

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
		 * \todo Irgendwann soll die Anzahl der angezeigten Merits (mit Beschreibungstext) vom user durch klicken irgendwie erhöht werden können.
		 **/
		MeritWidget* merits;
		/**
		 * In diesem Widget werden die übernatürlichen Kräfte angezeigt.
		 *
		 * \todo Irgendwann soll die Anzahl der angezeigten Kräfte (mit Beschreibungstext) vom user durch klicken irgendwie erhöht werden können.
		 **/
		PowerWidget* powers;
		/**
		 * Das Widget für die Anzeige von Spezialisierungen einer Fertigkeit.
		 **/
		CharaSpecialties* specialties;
		/**
		 * Das Widget für die Anzeige von Spezialisierungen einer Fertigkeit.
		 **/
		AdvantagesWidget* advantages;
		/**
		 * Über diesen Zeiger kann die Klasse aufgerufen werden, welche für das Speichern des Charakters zuständig ist.
		 **/
		ReadXmlCharacter* readCharacter;
		/**
		 * Über diesen Zeiger kann die Klasse aufgerufen werden, welche für das Speichern des Charakters zuständig ist.
		 **/
		WriteXmlCharacter* writeCharacter;

		/**
		 * Eine Simple Funktion, um alle Werte im gerade geöffneten Charater auf den selben Wert zu setzen.
		 *
		 * \warning Es wird nicht garantiert, daß dieser Wert angenommen wird. Manche Eigenschaften (MErits) können nicht beliebige Werte annehmen. Dann wird der nächstkleinere Wert angenommen.
		 **/
		void setCharacterValues( int value /** Der Wert, den alle Eigenschaften annehmen sollen */);

// 		/**
// 		 * Hier definiere ich Handgriffe, die der Benutzer eigentlich von Hand ausführen soll. Aber da ich das Programm teste, geht die beständig selbe Handlung auf den Geist.
// 		 **/
// 		void shortcut();

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
		 *
		 * \bug Ich schalte einmal zwischen zwei Spezies hin und her. ist nicht ganz ungefählrich, da es im Falle nicht vorhandener Spezies zu einer Ausnahme kommt.
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
		/**
		 * Zeigt den Informationsdialog für dieses Programm an.
		 **/
		void aboutApp();
		/**
		 * Diese Funktion druckt den Charakter in ein PDF-Dokument.
		 *
		 * \note Diese Funktion benötigt einen installierten pdf-Drucker, der automatisch in eine pdf-Datei drucken kann.
		 *
		 * \todo Überprüfen, ob das auch auf windows funktioniert, da ich ja den pdf-Drucker dafür verwende.
		 **/
		void exportCharacter();
		/**
		 * Druckt den angezeigten Charakter aus.
		 *
		 * \todo Die Abkürzung wieder entfernen, wenn ich mit dem Einrichten der Exportwerte fertig bin.
		 **/
		void printCharacter();
		/**
		 * Zeigt eine Nachricht an, daß die Eigenschaftsanzahl das für den Charakterbogen gesetzte Limit übertrifft, und daß alle überzähligen Eigenschaften des mitgegebenen Typs ignoriert werden.
		 **/
		void messageEnforcedTraitLimits( cv_Trait::Type );
		/**
		 * Diese Funktion verbirgt die Anzeige übernatürlicher Kräfte, wenn keine zur Verfügung stehen. Dadurch bleibt mehr Platz für die Merits.
		 **/
		void hidePowers(cv_Species::SpeciesFlag species);

	signals:
};

#endif
