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
 * \brief Mit den gespeicherten Werten vernetzte Darstellung einer einzigen Eigenschaft auf dem Charakterbogen.
 *
 * Anders als \ref TraitLine, ist dieses Widget direkt mit der korrespondierenden Eigenschaft in der Klasse \ref StorageCharacter verknüpft. Ändert sich der Wert dort, wird automatisch dieses Widget entsprechend verändert. Gleichermaßen wird \ref StorageCharacter verändert, sollte der Benutzer dieses Widget ändern.
 *
 * \todo Solange kein Text in der TExtbox einer Eigenschaft mit Zusatztext steht, sollte der Wert nicht verändert werden können.
 *
 * \todo Den Parser \ref StringBoolParser erweitern, damit übriggebliebener Text nach den Ersetzungen der Eigesncahften durch ihre Werte mit 0 gleichgesetzt wird. Aktuell mache ich das durch Stringmanipulation, aber das ist natürlich langsamer.
 **/

class CharaTrait : public TraitLine {
		Q_OBJECT

	public:
		/**
		 * Konstruktor.
		 **/
		CharaTrait( QWidget *parent, cv_Trait::Type type, cv_Trait::Category category, cv_Species::Species species, QString name, bool custom = false, int value = 0 );
		/**
		 * An diesen Konstruktor kann direkt die Eigenschaft übergeben werden, welche dieses Widget anzeigt.
		 **/
		CharaTrait( QWidget *parent, cv_Trait trait );
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
		/**
		 * Gibt die Spezies zurück, der die hier dargestellte Eigenschaft angehört.
		 **/
		cv_Species::Species species() const;
		/**
		 * Gibt zurück, ob es sich um eine Eigenschaft mit einem besonderen Text handelt.
		 **/
		bool custom() const;

	private:
		StorageCharacter *character;

		QList< cv_TraitDetail > v_specialties;
		cv_Trait::Type v_type;
		cv_Trait::Category v_category;
		cv_Species::Species v_species;
		bool v_custom;
		QString v_prerequisites;

		/**
		 * Hilfsfunktion, um bei überladenen Konstruktoren nicht alles doppelt aufrufen zu müssen.
		 **/
		void construction( cv_Trait::Type type, cv_Trait::Category category, cv_Species::Species species, QString name, bool custom, int value);

		/**
		 * Hilfsfunktion für checkTraitPrerequisites().
		 **/
		QString parsePrerequisites( QString text );

	public slots:
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
		void setCustom(bool sw);
		void addSpecialty(cv_TraitDetail specialty);

	private slots:
		void emitTraitChanged( int value );
		/**
		 * Verbirgt die Schaltfläche für Spezialisierungen für alle Eigenschaften außer den Fertigkeiten.
		 **/
		void hideSpecialtyWidget( cv_Trait::Type type );
		/**
		 * Verbirgt die Textzeile für den Beschreibungstext bei allen, außer Merits mit custom=true.
		 *
		 * \todo Muß natürlich auch bei manchen Powers vorhanden sein.
		 **/
		void hideDescriptionWidget();
		void emitSpecialtiesClicked(bool sw);
		/**
		 * Sorgt dafür, daß das Widget disabled wird, wenn die Voraussetzungen nicht erfüllt sind. Diese Funktion überprüft nur, ob sich die Voraussetzungen verändert haben, weil sich diese eine Eigenschaft verändert hat.
		 **/
		void checkTraitPrerequisites( cv_Trait trait /** Veränderte Eigenscahft, die \emph{möglicherweise} Auswirkungen auf die Verfügbarkeit der Eigenschaft hat, die durch die Instanz dieser Klasse repräsentiert wird. */);
		/**
		 * Kontrolliert, ob die Eigenschaft für die Spezies im Argument überhaupt existiert.
		 *
		 * Wenn nicht, werde sie versteckt und auf 0 gesetzt.
		 **/
		void hideTraitIfNotAvailable( cv_Species::SpeciesFlag species );

		/**
		 * Ändert alle Parameter dieses Widgets, damit es der übergebenen Eigenschaft entspricht.
		 **/
		virtual void setTrait( cv_Trait trait );

	signals:
		/**
		 * Dieses Signal wird ausgesandt, wann immer sich die Kategorie dieser Eigenschaft ändern sollte.
		 *
		 * Das wird zwar selten passieren, wenn das Widget erst einmal angelegt wurde (nie!), aber so kann ich einfach die Anzeige für die Spazialisierungen an und Ausschalten, wenn das Widget zu einer Fertigkeit gemacht wird.
		 **/
		void typeChanged( cv_Trait::Type );
// 		/**
// 		 * Dieses Signal wird ausgesandt, wann immer sich die Spezies ändert, welcher diese Kategorie zugeordnet ist.
// 		 **/
// 		void speciesChanged( cv_Species::Species );
		void customChanged( bool sw);
		/**
		 * Dieses Signal wird ausgesandt, wann immer sich die Eigenschaft des Widgets ändert.
		 **/
		void traitChanged( cv_Trait trait );
		/**
		 * Der Knopf zum Anzeigen der Spazialisierungen wurde gedrückt.
		 **/
		void specialtiesClicked( bool state /** Gibt an, welchen Zusatand (checked | unchecked) der Knopf nun hat. */,
								 QString name /** der Name der Eigenschaft. */,
								 QList< cv_TraitDetail > specialtyList /** Eine Liste der Spezialisierungen für diese Fertigkeit. Diese Liste beinhaltet zwar \emph{alle} Spezialisierungen für die spez */
							   );
};

#endif
