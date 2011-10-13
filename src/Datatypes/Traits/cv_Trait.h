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

#ifndef CV_TRAIT_H
#define CV_TRAIT_H

#include <QFlags>
// #include <QString>
// #include <QList>
// #include <QStringList>

// #include "cv_Species.h"
#include "cv_TraitDetail.h"

#include "cv_AbstractTrait.h"

/**
 * @brief Speichert alle Eigenschaften einer einzigen Charaktereigenschaft.
 *
 * Simple Eigenschaften wie Attribute haben nur Name und Wert. Bei Fertigkeiten kommen bereits die Spezialisierungen hinzu, bei  Vorzügen noch die Einschränkungen etc.
 */
class cv_Trait : public cv_AbstractTrait {
	public:
		/**
		 * In welche Era findet diese Eigenschaft ihre Anwendung? In der Moderne oder in der Antike?
		 *
		 *  <table border=0px>
		 *  <tr>
		 *     <td><b>Enum</b></td>
		 *     <td><b>Value</b></td>
		 *     <td><b>Description</b></td>
		 *  </tr>
		 *  <tr>
		 *     <td>Era::EraNo</td>
		 *     <td>000</td>
		 *     <td>Gültig für keine Era. (Kann mir momentan keinen Grund für diesen Aufzählungspunkt vorstellen.)</td>
		 *  </tr>
		 *  <tr>
		 *     <td>Era::Modern</td>
		 *     <td>001</td>
		 *     <td>Gültig nur für die Moderne.</td>
		 *  </tr>
		 *  <tr>
		 *     <td>Era::Reason</td>
		 *     <td>010</td>
		 *     <td>Gültig ab dem Zeitalter der Vernunft. (Science, Ride, Firearms)</td>
		 *  </tr>
		 *  <tr>
		 *     <td>Era::Antique</td>
		 *     <td>100</td>
		 *     <td>Gültig für die Antike bis hin zum Zeitalter der Vernunft. (Religion, Ride, Archery)</td>
		 *  </tr>
		 *  <tr>
		 *     <td>Era::EraAll</td>
		 *     <td>111</td>
		 *     <td>Fertigkeiten für alle Zeitepochen.</td>
		 *  </tr>
		 *  </table>
		 */
		enum EraFlag {
			EraNo	= 0x0,
			Modern	= 0x1,
			Reason	= 0x2,
			Antique	= 0x4,
			EraAll	= 0x7	// Binäre Summe aller Flags
		};
		Q_DECLARE_FLAGS( Era, EraFlag )	// Hiermit ermögliche ich die Verwendung von xx1|xx2|xx3

		/**
		 * Welches Charakteralter wird für diese Eigenschaft vorausgesetzt? Erwachsen oder Kind.
		 *
		 *  <table border=0px>
		 *  <tr>
		 *     <td><b>Flag</b></td>
		 *     <td><b>Value</b></td>
		 *     <td><b>Description</b></td>
		 *  </tr>
		 *  <tr>
		 *     <td>Age::AgeNo</td>
		 *     <td>00</td>
		 *     <td>Gültig für kein Alter. (Kann mir momentan keinen Grund für diesen Aufzählungspunkt vorstellen.)</td>
		 *  </tr>
		 *  <tr>
		 *     <td>Age::Adult</td>
		 *     <td>01</td>
		 *     <td>Gültig nur für erwachsene Charaktere.</td>
		 *  </tr>
		 *  <tr>
		 *     <td>Age::Kid</td>
		 *     <td>10</td>
		 *     <td>Gültig nur für Kinder.</td>
		 *  </tr>
		 *  <tr>
		 *     <td>Age::AgeAll</td>
		 *     <td>11</td>
		 *     <td>Gültig nur jedes Alter.</td>
		 *  </tr>
		 *  </table>
		 */
		enum AgeFlag {
			AgeNo	= 0x0,
			Adult	= 0x1,
			Kid		= 0x2,
			AgeAll	= 0x3	// Binäre Summe aller Flags
		};
		Q_DECLARE_FLAGS( Age, AgeFlag )	// Hiermit ermögliche ich die Verwendung von xx1|xx2|xx3

		/**
		 * Konstruktor.
		 **/
		cv_Trait(QString txt = "", int val = 0, cv_Species::Species spe = cv_Species::SpeciesNo, cv_AbstractTrait::Type ty = cv_AbstractTrait::TypeNo, cv_AbstractTrait::Category ca = cv_AbstractTrait::CategoryNo);
		/**
		 * Destruktor.
		 **/
		virtual ~cv_Trait();

		/**
		 * Gibt den Wert der Eigenschaft wieder zurück.
		 *
		 * \sa setValue()
		 **/
		virtual int value() const;
		/**
		 * Ändert den Wert der Eigenschaft.
		 *
		 * \sa value()
		 **/
		virtual void setValue( int val );
		/**
		 * Liest die möglichen Werte aus, welche diese Eigenschaft annehmen kann.
		 *
		 * \sa setPossibleValues()
		 **/
		QList< int > possibleValues() const;
		/**
		 * Legt alle möglichen Werte fest, welche diese Eigenschaft annehmen kann.
		 *
		 * Fast alle Eigenschaften können Werte zwischen 0 und 10 annehmen. Allerdings gibt es beispielsweise Merits, die nur Werte zwischen 0 bis 3 oder gar nur die Werte 0, 1, 3 und 5 annehmen können.
		 *
		 * \sa possibleValues()
		 *
		 * \sa addPossibleValues()
		 **/
		void setPossibleValues( QList< int > list );
		/**
		 * Fügt eine zusätzliche mögliche Eigenschaft hinzu.
		 *
		 * \sa possibleValues()
		 **/
		void addPossibleValue( int val );
		/**
		 * Liest aus, welcher Era diese Eigenschaft angehört.
		 *
		 * \sa cv_Character::Era
		 *
		 * \sa setEra()
		 **/
		cv_Trait::Era era() const;
		/**
		 * Legt fest, welcher Era diese Eigenschaft angehört.
		 *
		 * \sa cv_Character::Era
		 *
		 * \sa era()
		 **/
		void setEra( cv_Trait::Era er );
		/**
		 * Liest aus, elches Alter des Charakters Voraussetzung für diese Eigenschaft ist.
		 *
		 * \sa cv_Character::Age
		 *
		 * \sa setAge()
		 **/
		cv_Trait::Age age() const;
		/**
		 * Legt fest, welches Alter des Charakters Voraussetzung für diese Eigenschaft ist.
		 *
		 * \sa cv_Character::Age
		 *
		 * \sa age()
		 **/
		void setAge(cv_Trait::Age ag);
		/**
		 * Gibt eine Liste aller Zusatzeigenschaften zurück.
		 **/
		QList< cv_TraitDetail > details() const;
		/**
		 * Legt die Zusatzeigenschaften fest.
		 *
		 * \sa addDetail()
		 **/
		virtual void setDetails(QList< cv_TraitDetail > list);
		/**
		 * Legt die Zusatzeigenschaften fest.
		 *
		 * \sa setDetails()
		 **/
		virtual void addDetail(cv_TraitDetail det);
		/**
		 * Löscht sämtliche Zusatzeigenschaften.
		 **/
		virtual void clearDetails();
		/**
		 * Gibt einen String mit den geforderten Voraussetzungen zurück, die notwendig sind, um diese Eigenschaft besitzen zu dürfen.
		 *
		 * \sa setPrerequisites()
		 **/
		QString prerequisites() const;
		/**
		 * Legt die Voraussetzungen fest, die notwendig sind, um diese Eigenschaft besitzen zu dürfen.
		 *
		 * \note Das Format des Strings ist: (Strength > 4 AND Brawl > 3) OR Stamina < 2
		 *
		 * \sa prerequisites()
		 **/
		virtual void setPrerequisites(QString txt);
		/**
		 * Liest aus, ob diese Eigenschaft mit einem zusätzlichen erklärenden text versehen werden kann. Wenn ja, wird diese Funktion 'true' zurückgeben.
		 *
		 * \sa setCustom()
		 **/
		bool custom() const;
		/**
		 * Legt fest, ob diese Eigenschaft mit einem zusätzlichen Text versehen werden kann. Wenn ja, muß dieser Funktion 'true' übergeben werden.
		 *
		 * \sa custom()
		 **/
		void setCustom(bool sw);
		/**
		 * Gibt den zusätzlichen erklärenden Text dieser Eigenschaft aus. Ist kein derartiger Text vorgesehen wird ein leerer String zurückgegeben.
		 *
		 * \todo Eine Exception werfen, wenn kein Zusatztext vorgesehen ist.
		 *
		 * \sa setCustomText()
		 *
		 * \sa custom()
		 **/
		QString customText() const;
		/**
		 * Mit dieser Methode kann der zusätzliche Text der Eigenschaft festgelegt werden. Wird ein derartiger Text festgelegt, ohne daß dies eigentlich vorgesehen war, wird auch custom() verändert, so daß der text nun vorgesehen ist.
		 *
		 * \sa customText()
		 **/
		void setCustomText(QString txt);
		/**
		 * Liest aus, ob diese Eigenschaft als Bonuseigenschaft zählt.
		 *
		 * \todo Wenn ich von dieser Klasse die Speziellen Eigenschaftstypen ableite (AttributeTrait, SkillTrait etc) kann ich je nach Eigenschaft genau bestimmtn, welchen Effekt es hat, wenn eine Eigenschaft als Bonus deklariert ist.
		 *
		 * \sa setBonus()
		 **/
		bool isBonus() const;
		/**
		 * Legt fest, ob diese Eigenschaft eine Bonuseigenschaft ist.
		 *
		 * \sa custom()
		 **/
		virtual void setBonus(bool sw);

		/**
		 * Wandelt den Namen einer Era in den dazu passenden enum um.
		 *
		 * Diese Methode benötige ich, um die Strings in den XML-Template-Dateien in Flags umzuwandeln.
		 **/
		static cv_Trait::Era toEra( QString str );
		/**
		 * Wandelt den Namen eines Alters in den dazu passenden enum um.
		 *
		 * Diese Methode benötige ich, um die Strings in den XML-Template-Dateien in Flags umzuwandeln.
		 **/
		static cv_Trait::Age toAge( QString str );

		/**
		* Vergleich zwischen zwei Instanzen dieser Klasse.
		*
		* \todo Die Vergleiche sind noch nicht umfassend genug. Typ und Kategorie muß nich verglichen werden. etc.
		**/
		bool operator==( const cv_Trait &trait ) const;
		/**
		* Vergleich zwischen zwei Instanzen dieser Klasse nach ihrem Wert.
		**/
		bool operator<( const cv_Trait &trait ) const;

	private:
		/**
		 * Der Wert der Eigenschaft.
		 *
		 * \todo War vorher public und jetzt wird viel nicht funktionieren, da es nun private ist.
		 **/
		int v_value;
		/**
		 * Eine Liste aller möglichen Werte, welche diese Eigenschaft annehmen kann.
		 **/
		QList< int > v_possibleValues;
		/**
		 * Enthält, welcher Era diese Eigenschaft angehört.
		 *
		 * \sa cv_Character::Era
		 **/
		cv_Trait::Era v_era;
		/**
		 * Welches Alter des Charakters Voraussetzung für diese Eigenschaft ist.
		 *
		 * \sa cv_Character::Age
		 **/
		cv_Trait::Age v_age;
		/**
		 * Eine Liste der Zusatzeigenschaften.
		 **/
		QList< cv_TraitDetail > v_details;
		/**
		 * Ein String mit den geforderten Voraussetzungen, um diese Eigenscahft besitzen zu dürfen.
		 **/
		QString v_prerequisites;
		/**
		 * Manche Eigenschaften (beispielsweise der Merit Language) müssen mit einem zusätzlichen erklärenden Text versehen werden können. Wenn das der Fall ist, wird diese Variable auf 'true' gesetzt.
		 **/
		bool v_custom;
		/**
		 * Jene Eigenschaften, die einen zusätzlichen erklärenden Text haben können (siehe \ref custom), können eben diese Text hier speichern.
		 **/
		QString v_customText;
		/**
		 * Manche Eigenschaften werden als Bonuseigenschaft deklariert. Es müssen keine Punkte (Erschaffungs- oder Erfahrungspunkte) ausgegeben werden, um sie zu erhlaten, sondern sie kommen automatisch, wenn gewisse Voraussetzungen erfüllt sind.
		 *
		 * Ist diese Variable "true", ist diese Eigenschaft eine solche Bonuseigenschaft. Welche Auswirkungen das hat, hängt von der tatsächlichen Eigenschaft ab.
		 **/
		bool v_bonus;
};

Q_DECLARE_OPERATORS_FOR_FLAGS( cv_Trait::Age )
Q_DECLARE_OPERATORS_FOR_FLAGS( cv_Trait::Era )

#endif

