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

#ifndef CHARATRAIT_H
#define CHARATRAIT_H

#include "../Storage/StorageCharacter.h"
#include "../Datatypes/cv_Trait.h"
#include "../Datatypes/cv_TraitDetail.h"

#include "TraitLine.h"

/**
 * @brief Mit den gespeicherten Werten vernetzte Darstellung einer einzigen Eigenschaft auf dem Charakterbogen.
 *
 * Anders als \ref TraitLine, ist dieses Widget direkt mit der korrespondierenden Eigenschaft in der Klasse \ref StorageCharacter verknüpft. Ändert sich der Wert dort, wird automatisch dieses Widget entsprechend verändert. Gleichermaßen wird \ref StorageCharacter verändert, sollte der Benutzer dieses Widget ändern.
 *
 * \todo Bei einem Klick auf die Fertigkeit, sollen in einem Zusatz-Widget die Spezialisierungen angezeigt werden.
 **/

class CharaTrait : public TraitLine {
		Q_OBJECT

	public:
		/**
		 * Konstruktor.
		 **/
		CharaTrait( QWidget *parent, cv_Trait::Type type, cv_Trait::Category category, QString name, int value = 0 );
// 		/**
// 		 * Konstruktor.
// 		 **/
// 		CharaTrait( QWidget *parent = 0, QString name = "", int value = 0 );

		/**
		 * Gibt den Typ zurück, dem die hier dargestellte Eigenschaft angehört.
		 **/
		cv_Trait::Type type() const;
		/**
		 * Gibt die Kategorie zurück, der die hier dargestellte Eigenschaft angehört.
		 **/
		cv_Trait::Category category() const;

	private:
		StorageCharacter *character;

		QList< cv_TraitDetail > v_specialties;
		cv_Trait::Type v_type;
		cv_Trait::Category v_category;

	public slots:
		/**
		 * Legt den Typ der hier dargestellten Eigenschaft fest.
		 **/
		void setType( cv_Trait::Type type );
		/**
		 * Legt die Kategorie der hier dargestellten Eigenschaft fest.
		 **/
		void setCategory( cv_Trait::Category category );
		void addSpecialty(cv_TraitDetail specialty);
// 		void removeSpecialty(QString text);
		/**
		 * Diese Methode füllt die Liste der angezeigten Spazialisierungen mit dem Inahlt der übergebenen Liste.
		 *
		 * \bug Momentan macht diese Funktion ... NICHTS!
		 **/
		void setSpecialties(QList< cv_TraitDetail > specialtyList);

	private slots:
		void emitValueChanged( int value );
		/**
		 * Verbirgt die Schaltfläche für Spezialisierungen für alle Eigenschaften außer den Fertigkeiten.
		 **/
		void hideSpecialtyWidget( cv_Trait::Type type );
		void emitSpecialtiesClicked(bool sw);

	signals:
		/**
		 * Dieses Signal wird ausgesandt, wann immer sich der Wert des Widgets ändert. Die zusätzlichen Argumente teilen \ref StorageCharacter mit, um welche Eigenschaft es sich handelt.
		 **/
		void valueChanged( int, cv_Trait::Type, cv_Trait::Category, QString );
		/**
		 * Dieses Signal wird ausgesandt, wann immer sich die Kategorie dieser Eigenschaft ändern sollte.
		 *
		 * Das wird zwar selten passieren, wenn das Widget erst einmal angelegt wurde (nie!), aber so kann ich einfach die Anzeige für die Spazialisierungen an und Ausschalten, wenn das Widget zu einer Fertigkeit gemacht wird.
		 **/
		void typeChanged( cv_Trait::Type );
		/**
		 * Der Knopf zum Anzeigen der Spazialisierungen wurde gedrückt.
		 **/
		void specialtiesClicked( bool state /** Gibt an, welchen Zusatand (checked | unchecked) der Knopf nun hat. */,
								 QString name /** der Name der Eigenschaft. */,
								 QList< cv_TraitDetail > specialtyList /** Eine Liste der Spezialisierungen für diese Fertigkeit. Diese Liste beinhaltet zwar \emph{alle} Spezialisierungen für die spez */
							   );
};

#endif
