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

#ifndef TRAITSPECIALTIES_H
#define TRAITSPECIALTIES_H

#include <QString>

#include "../Datatypes/cv_TraitDetail.h"

#include "CheckedList.h"



/**
 * @brief Die darstellung von Spezialisierungen in der GUI.
 *
 * Spezailisieren sind eine Zusatzeigenschaft von Eigenschaften (natürlich nur von Fertigkeiten), und werden in der Gui bei diesen dargestellt. Die Darstellung erfolgt über eine unter der Fertigkeit anhängende Auswahlliste.
 **/
class TraitSpecialties : public CheckedList {
		Q_OBJECT
		/**
		 * Der Name der Fertigkeit, zu welcher die Spazialisierungen, welche in dieser Klasse gespeichert sind, gehören.
		 *
		 * \access skill(), setSkill()
		 *
		 * \notifier skillChanged()
		 **/
		Q_PROPERTY( QString skill READ skill WRITE setSkill NOTIFY skillChanged )

	public:
		/**
		 * Konstruktor
		 **/
		TraitSpecialties( QWidget* parent = 0 );
		/**
		 * Zerstört das Objekt und gibt alle zugeteilten Ressourcen wieder frei.
		 **/
		~TraitSpecialties();

		QString skill() const;

	private:
		QString v_skill;

	public slots:
		void setSkill( QString skillName );
		/**
		 * Fügt eine neue Spezialisierung hinzu.
		 **/
		void addSpecialty( QString spec /** Name der Spezialisierung. */ );
		/**
		 * Fügt eine neue Spezialisierung ein.
		 **/
		void insertSpecialty( int i /** Nach dieser Indexposition für die neue Spezialisierung eingefügt. */, QString spec /** Name der Spezialisierung. */ );
		/**
		 * Legt die gesamte Liste an Spezialisierungen fest.
		 **/
		void setSpecialties( QList< cv_TraitDetail > specList /** Liste der Spezialisierungen. */ );
		/**
		 * Entfernt eine Spezialisierung.
		 *
		 * \todo Exception auswerfen, wenn das Entfernen fehlschlägt.
		 **/
		void removeSpecialty( QString spec /** Name der zu entfernenden Spezialisierung. */ );
		/**
		 * Entfernt eine Spezialisierung.
		 *
		 * \overload
		 *
		 * \todo Exception auswerfen, wenn das Entfernen fehlschlägt.
		 **/
		void removeSpecialty( int i /** Position der zu entfernenden Spezialisierung. */ );

	private slots:
		/**
		 * Diese Funktion sorgt dafür, daß das richtige Signal ausgesandt wird.
		 *
		 * \todo Momentan ist der Name der Fertigkeit noch hartcodiert und damit wenig sinnvoll.
		 **/
		void emitCheckedSpecialtiesChanged( );

	signals:
		void skillChanged( QString );
		void checkedSpecialtiesChanged( QStringList list );
};

#endif
