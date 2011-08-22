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

#ifndef CV_TRAIT_H
#define CV_TRAIT_H

#include <QFlags>
#include <QString>
#include <QList>
#include <QStringList>

#include "cv_Species.h"
#include "cv_TraitDetail.h"
// #include "cv_TraitPrerequisiteAnd.h"

/**
 * @brief Speichert alle Eigenschaften einer einzigen Charaktereigenschaft.
 *
 * Simple Eigenschaften wie Attribute haben nur Name und Wert. Bei Fertigkeiten kommen bereits die Spezialisierungen hinzu, bei  Vorzügen noch die Einschränkungen etc.
 */
class cv_Trait {
	public:
		/**
		 * Zu welchem Typus gehört die Eigenschaft? Attribut, Fertigkeit, Vorzug etc.
		 *
		 *  <table border=0px>
		 *  <tr>
		 *     <td><b>Flag</b></td>
		 *     <td><b>Description</b></td>
		 *  </tr>
		 *  <tr>
		 *     <td>Type::TypeNo</td>
		 *     <td>Gehört keinem der genannten Typen an.</td>
		 *  </tr>
		 *  <tr>
		 *     <td>Type::Virtue</td>
		 *     <td>Ist eine Tugend.</td>
		 *  </tr>
		 *  <tr>
		 *     <td>Type::Vice</td>
		 *     <td>Ist eie Fertigkeit.</td>
		 *  </tr>
		 *  <tr>
		 *     <td>Type::Attribute</td>
		 *     <td>Ist ein Attribut.</td>
		 *  </tr>
		 *  <tr>
		 *     <td>Type::Skill</td>
		 *     <td>Ist eine Fertigkeit.</td>
		 *  </tr>
		 *  <tr>
		 *     <td>Type::Merit</td>
		 *     <td>Ist ein Vorzug.</td>
		 *  </tr>
		 *  <tr>
		 *     <td>Type::Morale</td>
		 *     <td>Ist die Moraleigenschaft.</td>
		 *  </tr>
		 *  <tr>
		 *     <td>Type::Super</td>
		 *     <td>Ist das Superattribut (Gnosis, Primal Urge, Blood Potency).</td>
		 *  </tr>
		 *  <tr>
		 *     <td>Type::Power</td>
		 *     <td>Ist eine übernatürliche Kraft (Discipline, Arcanum, Renown...).</td>
		 *  </tr>
		 *  </table>
		 */
		enum Type {
			TypeNo,
			Virtue,
			Vice,
			Attribute,
			Skill,
			Merit,
			Morale,
			Super,
			Power
		};
		/**
		 * Welcher Kategorie (mental, physisch, sozial) gehört die Eigenschaft an?
		 *
		 *  <table border=0px>
		 *  <tr>
		 *     <td><b>Flag</b></td>
		 *     <td><b>Description</b></td>
		 *  </tr>
		 *  <tr>
		 *     <td>Category::CategoryNo</td>
		 *     <td>Gehört keiner Kategorie an.</td>
		 *  </tr>
		 *  <tr>
		 *     <td>Category::Mental</td>
		 *     <td>Gehört der mentalen Kategorie an.</td>
		 *  </tr>
		 *  <tr>
		 *     <td>Category::Physical</td>
		 *     <td>Gehört der physischen Kategorie an.</td>
		 *  </tr>
		 *  <tr>
		 *     <td>Category::Social</td>
		 *     <td>Gehört der sozialen Kategorie an.</td>
		 *  </tr>
		 *  <tr>
		 *     <td>Category::Item</td>
		 *     <td>Gegenstände.</td>
		 *  </tr>
		 *  <tr>
		 *     <td>Category::FightingStyle</td>
		 *     <td>Kampfstile.</td>
		 *  </tr>
		 *  <tr>
		 *     <td>Category::DebateStyle</td>
		 *     <td>Debattierstile.</td>
		 *  </tr>
		 *  <tr>
		 *     <td>Category::PsychicPhenomena</td>
		 *     <td>Psychische Phänomene wie Psi oder Hellsicht.</td>
		 *  </tr>
		 *  <tr>
		 *     <td>Category::Species</td>
		 *     <td>Eigenschaften, welche ein Ausdruck der besonderen Spezies des Charakters sind.</td>
		 *  </tr>
		 *  </table>
		 */
		enum Category {
			CategoryNo,
			Mental,
			Physical,
			Social,
			Item,
			FightingStyle,
			DebateStyle,
			ShadowRealm,
			PsychicPhenomena,
			Species
		};
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
		 * Der Name der Eigenschaft.
		 **/
		QString name;
		/**
		 * Der Wert der Eigenschaft.
		 **/
		int value;
		/**
		 * Der möglichen Werte, welche diese Eigenschaft annehmen kann.
		 *
		 * Fast alle Eigenschaften können Werte zwischen 0 und 10 annehmen. Allerdings gibt es beispielsweise Merits, die nur Werte zwischen 0 bis 3 oder gar nur die Werte 0, 1, 3 und 5 annehmen können.
		 **/
		QList< int > possibleValues;
		/**
		 * Der Typ, dem diese Eigenschaft angehört.
		 *
		 * \sa Type
		 **/
		Type type;
		/**
		 * Die Kategorie, der diese Eigenschaft angehört.
		 *
		 * \sa Category
		 **/
		Category category;
		/**
		 * Welche Spezies über diese Eigenschaft verfügen.
		 **/
		cv_Species::Species species;
		/**
		 * Welcher Era diese Eigenschaft angehört.
		 *
		 * \sa cv_Character::Era
		 **/
		cv_Trait::Era era;
		/**
		 * Welches Alter des Charakters Voraussetzung für diese Eigenschaft ist.
		 *
		 * \sa cv_Character::Age
		 **/
		cv_Trait::Age age;
		/**
		 * Eine Liste der Zusatzeigenschaften.
		 **/
		QList< cv_TraitDetail > details;
		/**
		 * Ein String mit den geforderten Voraussetzungen, um diese Eigenscahft besitzen zu dürfen.
		 *
		 * \note Das Format des Strings ist: (Strength > 4 AND Brawl > 3) OR Stamina < 2
		 **/
		QString prerequisites;
		/**
		 * Manche Eigenschaften (beispielsweise der Merit Language) müssen mit einem zusätzlichen erklärenden Text versehen werden können. Wenn das der Fall ist, wird diese Variable auf 'true' gesetzt.
		 **/
		bool custom;
		/**
		 * Jene Eigenschaften, die einen zusätzlichen erklärenden Text haben können (siehe \ref custom), können eben diese Text hier speichern.
		 **/
		QString customText;
// 	QList<cv_TraitPrerequisiteAnd> prerequisites;	///< Eine Liste der Voraussetzungen. Die einzelnen Einträge dieser Liste sind ODER-verknüpft.

		/**
		 * Wandelt einen Typ in seinen in den Xml-Dateien gebräuchlichen Namen um.
		 *
		 * Diese Methode benötige ich, um die Strings in den XML-Template-Dateien zu erzeugen.
		 **/
		static QString toXmlString( cv_Trait::Type type );
		/**
		 * Wandelt eine Kategorie in ihren in den Xml-Dateien gebräuchlichen Namen um.
		 *
		 * Diese Methode benötige ich, um die Strings in den XML-Template-Dateien zu erzeugen.
		 **/
		static QString toXmlString( cv_Trait::Category category );
		/**
		 * Wandelt eine Kategorie in ihren realen Namen um.
		 *
		 * \note Diese Funktion unterscheidet sich insofern von toXmlString(), daß beispielsweise FightingStyle mit einem zusätzlichen Leerzeichen (Fighting Style) ausgegeben wird. Außerdem kann die Pluralform ausgegeben werden. Außerdem werden in dieser Funktion übersetzungen berücksichtigt.
		 **/
		static QString toString( cv_Trait::Category category, bool plural = false /** Ist dieses Argument true, wird die Pluralform der Kategorie ausgegeben. */ );
		/**
		 * Wandelt den Namen einer Kategorie in den dazu passenden enum um.
		 *
		 * Diese Methode benötige ich, um die Strings in den XML-Template-Dateien in Flags umzuwandeln.
		 **/
		static cv_Trait::Category toCategory( QString str );
		/**
		 * Wandelt den Namen eines Typs in den dazu passenden enum um.
		 *
		 * Diese Methode benötige ich, um die Strings in den XML-Template-Dateien in Flags umzuwandeln.
		 **/
		static cv_Trait::Type toType( QString str );
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
		* Vergleich zwischen zwei Instanzen dieser Klasse nach Reihenfolge. Wird für den qSort-Algorythmus benötigt.
		**/
		bool operator<( const cv_Trait &trait ) const;
};

Q_DECLARE_OPERATORS_FOR_FLAGS( cv_Trait::Age )
Q_DECLARE_OPERATORS_FOR_FLAGS( cv_Trait::Era )

#endif

