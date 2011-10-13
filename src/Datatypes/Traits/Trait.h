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

#ifndef TRAIT_H
#define TRAIT_H

// #include <QFlags>
// #include <QString>
// #include <QList>
// #include <QStringList>

// #include "cv_Species.h"
// #include "cv_TraitDetail.h"

#include "cv_Trait.h"
#include <QObject>

/**
 * @brief Speichert alle Eigenschaften einer einzigen Charaktereigenschaft.
 *
 * Simple Eigenschaften wie Attribute haben nur Name und Wert. Bei Fertigkeiten kommen bereits die Spezialisierungen hinzu, bei  Vorzügen noch die Einschränkungen etc.
 */
class Trait : public QObject, public cv_Trait {
		Q_OBJECT

	public:
		/**
		 * Konstruktor.
		 **/
		Trait( QString txt = "" /** Name */,
			   int val = 0 /** Wert */,
			   cv_Species::Species spe = cv_Species::SpeciesNo /** Sämtliche Spezies, welche über diese Eigenscahft verfügen sollen. */,
			   cv_AbstractTrait::Type ty = cv_AbstractTrait::TypeNo /** Der Typ, dem diese Eigenschaft angehört. */,
			   cv_AbstractTrait::Category ca = cv_AbstractTrait::CategoryNo /** Die Kategorie, welcher diese Eigenschaft angehört. */,
			   QObject* parent = 0 );
		/**
		 * Konstruktor.
		 *
		 * Dieser Konstruktor erzeugt ein Objekt dieser Klasse aus einem cv_Trait-Objekt.
		 **/
		Trait( cv_Trait trait, QObject* parent = 0 );
		/**
		 * Konstruktor.
		 *
		 * Dieser Konstruktor erzeugt ein neues Objekt aus einem bereits existierenden Trait-Objekt.
		 **/
		Trait( Trait* trait, QObject* parent = 0 );
		/**
		 * Destruktor.
		 **/
		virtual ~Trait();

		/**
		 * Gibt die Liste mit voraussetzungen zurück.
		 **/
		QList< Trait* > prerequisitePtrs() const;
		/**
		 * Gibt zurück, ob die Voraussetzungen der Eigenschaft erfüllt sind, ode rnicht.
		 **/
		bool isAvailable() const;

	private:
		/**
		 * Für alle Konstruktoren gleich.
		 **/
		void construct();
		/**
		 * Hilfsfunktion für checkTraitPrerequisites().
		 **/
		QString parsePrerequisites( QString text, QList< Trait* > list );

		/**
		 * Eine Liste mit Adresse von Eigenschaften, deren Änderung Auswirkungen auf diese Eigenschaft haben kann.
		 **/
		QList< Trait* > v_prerequisitePtrs;
		/**
		 * Ein Schalter, der Anzeigt, ob die Eigenschaft ihre Voraussetzungen erfüllt oder nicht. Dieser Schalter wird über checkPrerequisites() umgeschalten.
		 **/
		bool v_available;

	public slots:
		/**
		 * Verändert den Wert der Eigenschaft.
		 **/
		void setValue( int val );
		/**
		 * Legt die Zusatzeigenschaften fest.
		 **/
		void setDetails( QList< cv_TraitDetail > list );
		/**
		 * Legt die Zusatzeigenschaften fest.
		 **/
		void addDetail( cv_TraitDetail det );
		/**
		 * Löscht sämtliche Zusatzeigenschaften.
		 **/
		void clearDetails();
		/**
		 * Legt den Typ fest und sendet ein entsprechendes Signal aus.
		 **/
		void setType( cv_AbstractTrait::Type typ );
		/**
		 * Legt fest, ob diese Eigenschaft eine Bonuseigenschaft ist.
		 **/
		virtual void setBonus(bool sw);
// 		/**
// 		 * Legt fest, welche Spezies über diese Eigenschaft verfügen und sendet bei Änderung ein entsprechendes Signal aus.
// 		 **/
// 		void setSpecies(cv_Species::Species spe);
		/**
		 *Löscht die Liste mit Zeigern, welche auf Eigenschaften zeigen, welche Voraussetzungen für diese Eigenschaft sind.
		 **/
		void clearPrerequisitePtrs();
		/**
		 * Ursprünglich steht im prerequisites-String Name und Wert der Eigenscahften, von denen diese Eigenschaft abhängen kann. Dies soll durch die Adressen der jeweiligen Eigenschaften ersetzt werden.
		 *
		 * \warning Darf erst aufgerufen werden, wenn schon alle Eigenschaften im Speicher stehen, sonst können möglicherweise einige Namen nicht übersetzt werden.
		 *
		 * \todo Besser wäre natürlich, aus dem Textstring ein C++-if-Konstrukt zu erzeugen.
		 **/
		void addPrerequisitePtrs( Trait* replacement );
		/**
		 * Überprüft, ob alle Voraussetzungen für diese Eigenschaft erfüllt werden.
		 **/
		void checkPrerequisites( Trait* trait /** Veränderte Eigenschaft, die möglicherweise Auswirkungen auf die Verfügbarkeit der Eigenschaft hat, die durch die Instanz dieser Klasse repräsentiert wird. */ );

	private slots:
		/**
		 * Legt fest, ob die Eigenschaft zur Verfügung steht oder nicht.
		 *
		 * \sa checkPrerequisites()
		 **/
		void setAvailability( bool sw );
		/**
		 * Wenn der Wert einer Fertigkeit auf 0 sinkt, werden alle ihre Spezialisierungen gelöscht.
		 **/
		void clearDetails( int val );
		/**
		 * Sendet das Signal traitChanged() aus.
		 **/
		void emitTraitChanged();

	signals:
		/**
		 * Der Wert der Eigenschaft hat sich verändert.
		 **/
		void valueChanged( int );
		/**
		 * Der Typ der Eigenschaft hat sich verändert.
		 **/
		void typeChanged( cv_AbstractTrait::Type );
		/**
		 * Der Typ der Eigenschaft hat sich verändert.
		 **/
		void speciesChanged( cv_Species::SpeciesFlag );
		/**
		 * Die Details der Eigenschaft haben sich verändert.
		 **/
		void detailsChanged( int /** Dieses Argument beinhaltet die aktuelle Anzahl an Details der Eigenschaft. */ );
		/**
		 * Die Eigenschaft wurde entweder in eine Bonuseigenschaft oder von einer Bonuseigenscahft in eine normele umgewandelt.
		 **/
		void bonusChanged( bool /** true: Eigenschaft ist nun eine Bonuseigenscahft, false: Eigenschaft ist nun eine normale Eigenschaft. */ );
		/**
		 * Irgendein Aspekt der Eigenschaft hat sich verändert.
		 *
		 * \note Derzeit werden nur Veränderungen des Wertes oder der Details (Spezialisierungen) beachtet. Änderungen des Namens etc lösen kein Aussenden dieses Signals aus.
		 **/
		void traitChanged( Trait* trait );
		/**
		 * Verfügbarkeit hat sich verändert.
		 **/
		void availabilityChanged( bool sw /** Dieses Argument bestimmt, ob die Eigenscahft dem Cahrakter zur Verfügung steht (true) oder nicht (false). */ );
};

#endif

