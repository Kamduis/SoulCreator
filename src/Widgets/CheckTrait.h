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

#ifndef CHECKTRAIT_H
#define CHECKTRAIT_H

#include <QHBoxLayout>
#include <QLineEdit>
#include <QCheckBox>

#include "../Storage/StorageCharacter.h"
#include "../Datatypes/cv_Trait.h"

#include <QWidget>

/**
 * \brief An- bzw. Abwählbare Eigenschaft.
 *
 * Diese Eigensachft ist ähnlich wie CharaTrait mit den Eigenschaften im Speicher verknpüft, allerdings besitzen sie keine Werte, sondern sind nur an- oder Abwählbar. Beispiel für eine solche Eigenscahft sind die Nachteile.
 **/

class CheckTrait : public QWidget {
		Q_OBJECT

	public:
		/**
		 * An diesen Konstruktor kann direkt die Eigenschaft übergeben werden, welche dieses Widget anzeigt.
		 **/
		CheckTrait( QWidget *parent, cv_Trait* trait, cv_Trait* traitStorage = 0 );
		virtual ~CheckTrait();

		/**
		 * Gibt den Wert zurück, der hier angezeigt wird bzw. werden soll.
		 **/
		int value() const;
		/**
		 * Gibt den Text zurück, der als zusätzliche Beschreibung angezeigt werden soll.
		 **/
		QString customText() const;
		/**
		 * Gibt den Typ zurück, dem die hier dargestellte Eigenschaft angehört.
		 **/
		cv_Trait::Type type() const;
		/**
		 * Gibt die Kategorie zurück, der die hier dargestellte Eigenschaft angehört.
		 **/
		cv_Trait::Category category() const;
		/**
		 * Gibt die Spezies zurück, der die hier dargestellte Eigenschaft angehört.
		 **/
		cv_Species::Species species() const;
		/**
		 * Gibt zurück, ob es sich um eine Eigenschaft mit einem besonderen Text handelt.
		 **/
		bool custom() const;

		/**
		 * Gibt den Zeiger zurück, welcher auf die Eigenschaft im Speicher verweist, welche durch dieses jeweilige Widget repräsentiert wird.
		 **/
		cv_Trait* traitPtr() const;

	private:
		StorageCharacter *character;

		cv_Trait* ptr_trait;
		cv_Trait* ptr_traitStorage;

		QHBoxLayout* layout;
		QLineEdit* lineEdit;
		QCheckBox* checkBox;

		/**
		 * Hilfsfunktion für checkTraitPrerequisites().
		 **/
		QString parsePrerequisites( QString text );

	public slots:
		/**
		 * Legt den Wert der Eigenschaft fest.
		 *
		 * Dabei wird automatisch der Wert im Speicher aktualisiert und natürlich auch die Anzeige des Widget.
		 **/
		void setValue( int val );
		/**
		 * Legt den Zusatztext fest.
		 *
		 * Dabei wird automatisch der Wert im Speicher aktualisiert und natürlich auch die Anzeige des Widget.
		 **/
		void setCustomText( QString txt );
		/**
		 * Legt den Typ der hier dargestellten Eigenschaft fest.
		 **/
		void setType( cv_Trait::Type type );
		/**
		 * Legt die Kategorie der hier dargestellten Eigenschaft fest.
		 **/
		void setCategory( cv_Trait::Category category );
		/**
		 * Legt fest, welche Spezies alles über diese Eigenschaft verfügen können.
		 **/
		void setSpecies( cv_Species::Species species );
		/**
		 * Legt fest, ob es sich um eine Eigenschaft mit einem erklärenden Text handelt.
		 **/
		void setCustom( bool sw );
		
		/**
		 * Verbirgt die Textzeile für den Beschreibungstext bei allen, außer Merits mit custom=true.
		 **/
		void hideDescriptionWidget();

		/**
		 * Kontrolliert, ob die Eigenschaft für die Spezies im Argument überhaupt existiert.
		 *
		 * Wenn nicht, werde sie versteckt und auf 0 gesetzt.
		 **/
		void hideTraitIfNotAvailable( cv_Species::SpeciesFlag species );

		/**
		 * Richtet den Zeiger auf die Eigenschaft im Speicher, welche von diesem Widget repräsentiert wird.
		 **/
		void setTraitPtr( cv_Trait* trait );
		/**
		 * Sorgt dafür daß das Widget aktualisiert wird und die Werte anzeigt, auf welche es zeigt.
		 *
		 * \warning Wenn der Wert des Widget != 0 ist, wird es als gewählt markiert, andernfalls als ungewählt.
		 **/
		void updateWidget(cv_Trait* trait);

	signals:
		/**
		 * Der Status der Eigenscahft wurde verändert.
		 **/
		void stateChanged(int);
		void typeChanged( cv_Trait::Type type );
		/**
		 * Der Knopf zum Anzeigen der Spazialisierungen wurde gedrückt.
		 **/
		void traitChanged(cv_Trait* trait);
		/**
		 * Der Knopf zum Anzeigen der Spazialisierungen wurde gedrückt.
		 **/
		void specialtiesClicked( bool state /** Gibt an, welchen Zusatand (checked | unchecked) der Knopf nun hat. */,
								 QString name /** der Name der Eigenschaft. */,
								 QList< cv_TraitDetail > specialtyList /** Eine Liste der Spezialisierungen für diese Fertigkeit. Diese Liste beinhaltet zwar \emph{alle} Spezialisierungen für die spez */
							   );
};

#endif
