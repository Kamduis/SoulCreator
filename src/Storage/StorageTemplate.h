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

#ifndef STORAGETEMPLATE_H
#define STORAGETEMPLATE_H

#include <QList>
#include <QStringList>

#include "Datatypes/cv_SpeciesTitle.h"
#include "Datatypes/Traits/TraitBonus.h"
// #include "Datatypes/cv_IdentityList.h"
#include "Datatypes/cv_CreationPointsList.h"
#include "Datatypes/cv_SuperEffect.h"

#include <QObject>

/**
 * @brief In dieser Klasse werden sämtliche Daten für das Programm gespeichert.
 *
 * Diese Klasse verwaltet die im Programm geladenen Daten. Zum einen gibt es eine Liste, in welcher sämtliche \emph{möglichen} Eigenschaften für die Charaktere gespeichert sind, jene welche nach Programmstart aus den Template-Dateien ausgelesen werden und zum anderen gibt es eine Liste für den aktuell angezeigten Charakter.
 *
 * Außerdem bietet diese Klasse angenehme Zugriffsfunktionen aus den Informationen, welche zum Programmstart aus den Template-Dateien geladen werden.
 **/
class StorageTemplate : public QObject {
		Q_OBJECT
// 		/**
// 		 * Eine Liste aller Identitäten des Charakters. Hierin werden alle seine zahlreichen Namen gespeichert.
// 		 *
// 		 * \access identities(), setIdentities()
// 		 *
// 		 * \notifier identitiesChanged()
// 		 **/
// 		Q_PROPERTY( cv_IdentityList identities READ identities WRITE setIdentities NOTIFY identitiesChanged )

	public:
		StorageTemplate( QObject *parent = 0 );
		/**
		 *Zerstört das Objekt und gibt alle zugeteilten Ressourcen wieder frei.
		 **/
		~StorageTemplate();

		/**
		 * Gibt eine Liste aller verfügbaren Spezies aus.
		 **/
		QList< cv_Species > species() const;
		/**
		 * Gibt eine Liste aller verfügbaren Virtues aus.
		 **/
		QStringList virtueNames( cv_Trait::AgeFlag age = cv_Trait::Adult ) const;
		/**
		 * Gibt eine Liste aller verfügbaren Vices aus.
		 **/
		QStringList viceNames( cv_Trait::AgeFlag age = cv_Trait::Adult ) const;
		/**
		 * Gibt die Bezeichnung für die Brut der jeweiligen Spezies zurück.
		 *
		 * \todo Eine Exception werfen, falls der entsprechende Titel nicht gefunden wird.
		 **/
		QString breedTitle( cv_Species::SpeciesFlag spe = cv_Species::SpeciesNo ) const;
		/**
		 * Gibt die Bezeichnung für die Fraktion der jeweiligen Spezies zurück.
		 *
		 * \todo Eine Exception werfen, falls der entsprechende Titel nicht gefunden wird.
		 **/
		QString factionTitle( cv_Species::SpeciesFlag spe = cv_Species::SpeciesNo ) const;
		/**
		 *Gibt eine Liste mit den Einzelnen Überschriften der Power-Kategorien je Spezies zurück.
		 **/
		QStringList powerHeaders( cv_Species::SpeciesFlag spe = cv_Species::SpeciesNo ) const;
		/**
		 * Gibt eine Liste aller verfügbaren Bruten aus.
		 **/
		QStringList breedNames( cv_Species::SpeciesFlag spe = cv_Species::SpeciesNo ) const;
		/**
		 * Gibt eine Liste aller verfügbaren Fraktionen aus.
		 **/
		QStringList factionNames( cv_Species::SpeciesFlag spe = cv_Species::SpeciesNo ) const;
		/**
		 * Gibt eine Liste mit Zeigern auf alle Eigenschaften zurück, die den übergebenen Parametern entsprechen.
		 *
		 * \note Wenn es keine Eigenschaft mit den übergebenen Parametern gibt, wird eine leere Liste übergeben.
		 *
		 * \todo Vielleicht kann ich die Anzahl der at()s reduzieren durch speichern des Zeigers? vor den if-Abfragen und Zuweisungen. Gilt auch für ähnliche Funktionen.
		 **/
		QList< Trait* > traits( cv_AbstractTrait::Type type, cv_AbstractTrait::Category category, cv_Trait::EraFlag era = cv_Trait::Modern, cv_Trait::AgeFlag age = cv_Trait::Adult ) const;
		/**
		 * Gibt eine Liste mit Zeigern auf alle Eigenschaften zurück, die den übergebenen Parametern entsprechen.
		 **/
		QList< Trait* > traits( cv_AbstractTrait::Type type, cv_Species::SpeciesFlag species ) const;
		/**
		 * Gibt eine Namensliste verschiedener Eigenschaften aus, spezifiziert nach Typ (\ref cv_AbstractTrait::Type), Kategorie (\ref cv_AbstractTrait::Category), Zeitalter (\ref cv_Trait::Era) und Alter (\ref cv_Character::Age).
		 **/
		QStringList traitNames( cv_AbstractTrait::Type type, cv_AbstractTrait::Category category, cv_Trait::EraFlag era = cv_Trait::EraAll, cv_Trait::AgeFlag age = cv_Trait::AgeAll ) const;
// 		/**
// 		 * Gibt die gesamte Eigenschaft zurück, welche über Typ, Kategorie und Name spezifiziert ist.
// 		 *
// 		 * \todo Sollte vielleicht eine Exception werfen, wenn keine passende Eigenschaft gefunden wurde.
// 		 *
// 		 * \todo Sollte die Funktion traits() nutzen und nicht alles nochmal selbst implementieren.
// 		 **/
// 		cv_Trait trait(cv_AbstractTrait::Type type, cv_AbstractTrait::Category category, QString name);
// 		/**
// 		 * Sortiert die Liste.
// 		 **/
// 		void sortTraits();
		/**
		 * Gibt eine Liste mit Zeigern auf alle Bonuseigenschaften zurück, die den übergebenen Parametern entsprechen.
		 **/
		QList< TraitBonus* > traitsBonus( cv_AbstractTrait::Type type, cv_Species::SpeciesFlag species ) const;

		/**
		 * Gibt den Maximalwert der Eigenschaften aus. Dieser Maximalwert hängt von der Spezies und der Höhe des Superattributs ab.
		 **/
		int traitMax( cv_Species::Species species, int value );
		/**
		 * Gibt den Maximalwert der Energieeigenscahft aus. Dieser Maximalwert hängt von der Spezies und der Höhe des Superattributs ab.
		 **/
		int fuelMax( cv_Species::Species species, int value );
		/**
		 * Gibt aus, wieviel Energie pro Runde maximal ausgegeben werden kann. Dieser Maximalwert hängt von der Spezies und der Höhe des Superattributs ab.
		 **/
		int fuelPerTurn( cv_Species::Species species, int value );

		/**
		 * Gibt die für einen Eigenschaftstyp zur Verfügung stehenden Erschaffungspunkte zurück.
		 **/
		cv_CreationPointsList* creationPoints();

	private:
		/**
		 * Eine Liste sämtlicher verfügbaren Spezies.
		 **/
		static QList< cv_Species > v_species;
		/**
		 * Eine Liste sämtlicher Titel der eizelnen Spezies.
		 **/
		static QList< cv_SpeciesTitle > v_titles;
		/**
		 * Eine Liste sämtlicher verfügbaren Eigenschaften.
		 **/
		static QList< Trait* > v_traits;
		/**
		 * Eine Liste sämtlicher Bonuseigenschaften.
		 **/
		static QList< TraitBonus* > v_traitsBonus;
		/**
		 * Eine Liste über die Effekte der Supereigenschaft.
		 **/
		static QList< cv_SuperEffect > v_superEffects;

		/**
		 * Eine Liste der Erschaffungspunkte. Jeder Listeneintrag steht für eine andere Spezies.
		 **/
		static cv_CreationPointsList v_creationPointsList;

	public slots:
// 		/**
// 		 * Speichert sämtliche verfügbaren Eigenschaften.
// 		 **/
// 		void setTraits( QList<cv_Trait> traits );
		/**
		 * Fügt eine Spezies hinzu.
		 **/
		void appendSpecies( cv_Species species );
		/**
		 * Fügt einen Titel hinzu.
		 **/
		void appendTitle( cv_SpeciesTitle title );
		/**
		 * Fügt eine Eigenschaft hinzu.
		 *
		 * \note Je nach Typ der Eigenschaft werden sie in eine dazu passende Klasse gesteckt, damit die ganzen typspezifischen Aktionen in virtuellen Funktionen so ablaufen, wie es für diesen ganz beosnderen Typ eben typisch ist. Beispiel: Die Auswirkung, falls diese Eigenschaft als Bonuseigenschaft ausgezeichnet ist.
		 *
		 * \warning Es werden nur Eigenschaften hinzugefügt, die nicht schon existieren.
		 **/
		void appendTrait( cv_Trait trait );
		/**
		 * Fügt eine Bonuseigenschaft zu der entsprechenden Liste hinzu.
		 **/
		void appendTraitBonus( Trait* tr1, QString breed /** Dies ist die Brut, von der abhängt, ob dem Charkater die Bonuseigenschaft zur Verfügung steht. */ );
		/**
		 * Fügt einen Effekt eines Superattributs hinzu.
		 **/
		void appendSuperEffect( cv_SuperEffect effect );
		/**
		 * Fügt einen neuen Satz Erschaffungspunkte zu der entsprechende Liste hinzu.
		 *
		 * \sa v_creationPoints
		 **/
		void appendCreationPoints( cv_CreationPoints points );
};

#endif
