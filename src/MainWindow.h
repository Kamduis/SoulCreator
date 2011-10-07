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

#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include "Calc/Creation.h"
// #include "Datatypes/cv_CreationPoints.h"
#include "Draw/DrawSheet.h"
#include "IO/ReadXmlCharacter.h"
#include "IO/WriteXmlCharacter.h"
// #include "Storage/StorageTemplate.h"
// #include "Storage/StorageCharacter.h"
#include "Widgets/Display/InfoWidget.h"
#include "Widgets/Display/AttributeWidget.h"
#include "Widgets/Display/SkillWidget.h"
#include "Widgets/Display/MeritWidget.h"
#include "Widgets/Display/MoralityWidget.h"
#include "Widgets/Display/PowerWidget.h"
#include "Widgets/Display/FlawWidget.h"
#include "Widgets/Display/AdvantagesWidget.h"
#include "Widgets/Display/CharaSpecialties.h"

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
 * \todo Beim Wechseln zwischen den Spezies eie Warnung ausgeben, wenn Powers und Merits gelöscht würden.
 *
 * \todo Bei den Werwölfen müssen die Kräfte, welche je nach Vorzeichen nicht erlaubt sind, ausgegraut werden.
 *
 * \todo Sonderkräfte der Spezies fehlen. Bei Werwölfen müssen z.B. noch die Gaben/Riten berücksichtigt werden.
 *
 * \todo Nutze eine qchecksum, um die Integrität der XML-DAteien zu überprüfen. Ist nicht ganz einfach, wenn ich das Ergebnis der checksum in der selben xml-Datei stehen haben möchte, die ich überprüfe. Aber somit merkt SoulCreator, wenn die gespeicherten Charaktere korrupt sind. Es dürfte am besten sein, sie trotzdem zu laden, aber eine Warnung auszugeben.
 *
 * \todo So könnte es gehen: Erzeuge die XML-Datei mit einem leeren Feld für die Checksumme. Dann berechne die Chacksumme für diese Datei und füge sie anschließend in das leere Feld ein. Beim Laden verfahre genau andersherum! Lade die DAtei, hole die Checksumme, erzeuge eine temporäre Datei, in der alles identisch ist, bis auf die Checksumme, deren Feld nun leer ist. Berechne die Checksumme auf diese temporäre Datei und vergleiche sie mit der zuvor gelesenen Checksumme. Tadaa!
 *
 * \todo Zwischen den Kategorien (bei Attributen zumindest) Vertikale Striche als optischen Trenner einfügen. Diese können ja auch als Bilder realisiert werden und je nach Spezies unterschiedlich sein (Dornen, Krallenspuren etc.).
 *
 * \todo Charaktererschaffung in Schritten und Erfahrungspunkte einbauen.
 *
 * \todo Waffen einbauen.
 *
 * \todo Charakterbeschreibung einbauen.
 *
 * \todo Benutzer sollen ihre eigenen Spezialisierungen, Merits etc. eintragen können. Dafür sollte ich ihnen eine eigene template-DAtei bereitstellen, i welche dann all diese Eigenschaften hineingeschrieben werden. Diese Datei wird gleichberechtigt ausgelesen wie die anderen, befindet sich jedoch nicht in der Ressource, sondern liegt als externe Datei vor.
 *
 * \todo Bonus-Attributspuntke bei Vampiren und Magier bzw. Bonus-Spezialisierung bei Werwölfen und Wechselbälgern beachten.
 *
 * \todo Kräfte alphabetisch sortieren oder in Kategorien unterteilen.
 *
 * \todo Damit beim Laden einer Datei eine Eigenschaft, welche eigentlich nicht zur Verfügung steht, keine Punkte hat, sollte nach dem Laden nochmal eine Kontrolle durchgeführt werden.
 *
 * \todo Die Widgets weiter aufteilen in Main-Widgets, Tool-Widgets etc.
 *
 * \todo Damit die SVG-Grafiken unter Windows XP dargestellt werden ist auch QtXML4.dll erforderlich.
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
		 * Zeiger auf die Klasse, welche sämtliche Charaterwerte enthält. Eine Änderung der Werte in dieser Klasse sorgen dafür, daß sich auch die Anzeige anpaßt. Und ändert man einen Wert in der Anzeige, wird automatisch die dadurch repräsentierte Eigenschaft in dieser Klasse verändert.
		 */
		Creation* creation;

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
		 * In diesem Widget wird die Moral angezeigt.
		 **/
		MoralityWidget* morality;
		/**
		 * In diesem Widget werden die übernatürlichen Kräfte angezeigt.
		 *
		 * \todo Irgendwann soll die Anzahl der angezeigten Kräfte (mit Beschreibungstext) vom user durch klicken irgendwie erhöht werden können.
		 **/
		PowerWidget* powers;
		/**
		 * In diesem Widget werden die Nachteile angezeigt.
		 **/
		FlawWidget* flaws;
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
		 * Für jede Spezies wird das passende Hintergrundbild angezeigt.
		 **/
		void showBackround( cv_Species::SpeciesFlag spec );
		/**
		 * Zeigt die Anzahl der übrigen Punkte bei der Charaktererschaffung an.
		 *
		 * \todo Mit Wirkung versehen.
		 **/
		void showCreationPoints();
		/**
		 * Zeigt eine Warnung an, wenn nicht alle Erschafungspunkte vergeben wurden.
		 *
		 * \note Die Schrift im Auswahl-Widget, mit welchem man die verschiedenen Seiten anwählen kann wird für diese Seite blau eingefärbt.
		 **/
		void warnCreationPointsPositive(cv_AbstractTrait::Type type);
		/**
		 * Zeigt eine Warnung an, wenn zuviele Erschafungspunkte vergeben wurden.
		 *
		 * \note Die Schrift im Auswahl-Widget, mit welchem man die verschiedenen Seiten anwählen kann wird für diese Seite rot eingefärbt.
		 **/
		void warnCreationPointsNegative(cv_AbstractTrait::Type type);
		/**
		 * Zeigt eine Warnung an, wenn alle Erschafungspunkte vergeben wurden.
		 *
		 * \note Die Schrift im Auswahl-Widget, mit welchem man die verschiedenen Seiten anwählen kann wird für diese Seite wieder zur Standardfarbe verändert.
		 **/
		void warnCreationPointsDepleted(cv_AbstractTrait::Type type);
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
		 * Diese Funktion ruft den Konfigurationsdialog auf und sorgt dafür, daß die änderungen gespeichert oder verworfen werden.
		 **/
		void showSettingsDialog();
		/**
		 * Diese Funktion schaltet die Eigenschaften einen Tab zurück.
		 **/
		void tabPrevious();
		/**
		 * Diese Funktion schaltet die Eigenschaften einen Tab weiter.
		 **/
		void tabNext();
		/**
		 * Selektiert das zur aktuellen Seite der Eigenschaften zugehörige Symbol in der Auswahlleiste.
		 **/
		void selectSelectorItem( int idx );
		/**
		 * Enabled oder Disabled die Knöpfe, mit denen die Eigenschaften durchgeblättert werden können, je nachdem, ob es noch eine weitere Seite zu Blättern gibt.
		 **/
		void setTabButtonState( int index );
		/**
		 * Je nachdem, welches Tab gerade gezeigt wird, müssen die Erschaffungspunkte dargestellt oder versteckt werden.
		 **/
		void showCreationPoints( int idx );
		/**
		 * Über diese Funktion wird der Dialog aufgerufen, um einen ganz neuen Charakter zu erstellen.
		 **/
		void newCharacter();
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
		 * Fügt den Inhalt des Arguments zum Fenstertitel hinzu.
		 **/
		void setTitle( QString txt );
		/**
		 * Diese Funktion druckt den Charakter in ein PDF-Dokument.
		 **/
		void exportCharacter();
		/**
		 * Druckt den angezeigten Charakter aus.
		 **/
		void printCharacter();
		/**
		 * Zeigt eine Nachricht an, daß die Eigenschaftsanzahl das für den Charakterbogen gesetzte Limit übertrifft, und daß alle überzähligen Eigenschaften des mitgegebenen Typs ignoriert werden.
		 **/
		void messageEnforcedTraitLimits( cv_AbstractTrait::Type );
		/**
		 * Diese Funktion verbirgt die Anzeige übernatürlicher Kräfte, wenn keine zur Verfügung stehen. Dadurch bleibt mehr Platz für die Merits.
		 **/
		void disablePowerItem( cv_Species::SpeciesFlag species );

		/**
		 * Speichert die Konfiguration dieses Programms für den nächsten Aufruf.
		 **/
		void writeSettings();
		/**
		 * Lädt die Konfiguration für dieses Programm.
		 **/
		void readSettings();
		/**
		 * Fragt nach, ob die Änderungen am Charakter gespeichert werden sollen, ehe sie möglicherweise verloren gehen.
		 *
		 * Diese Frage tritt auf, wenn der dargestellte Charakter nicht gespeichert ist und ehe das Programm geschlossen werden oder einen neuen Charakter anlegen soll.
		 **/
		bool maybeSave();

		/**
		 * Ausgabe einer Fehlernachricht.
		 **/
		void raiseExceptionMessage( QString message, QString description );

	protected:
		void closeEvent( QCloseEvent *event );

	signals:
};

#endif
