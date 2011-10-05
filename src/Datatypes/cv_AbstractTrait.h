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

#ifndef CV_ABSTRACTTRAIT_H
#define CV_ABSTRACTTRAIT_H

// #include <QString>
#include <QList>

#include "cv_Species.h"

/**
 * @brief Grundlegender Datentyp für eine Charaktereigenschaft
 *
 * Dies ist die Grundlage für sämtliche Charaktereigenschaften.
 */
class cv_AbstractTrait {
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
			Breed,
			Faction,
			Attribute,
			Skill,
			Merit,
			Derangement,
			Flaw,
// 			Morale,
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
		 *     <td>Category::Extraordinary</td>
		 *     <td>Psychische Phänomene wie Psi oder Hellsicht. Auch mit Geistern in Verbindung stehende Merits.</td>
		 *  </tr>
		 *  <tr>
		 *     <td>Category::Mild</td>
		 *     <td>Milde Geistesstörungen</td>
		 *  </tr>
		 *  <tr>
		 *     <td>Category::Severe</td>
		 *     <td>Ernste Geistesstörungen.</td>
		 *  </tr>
		 *  <tr>
		 *     <td>Category::BreedPower</td>
		 *     <td>Kräfte welche hauptsächlich Angehörigen der jeweiligen Brut zugeschrieben werden.</td>
		 *  </tr>
		 *  <tr>
		 *     <td>Category::FactionPower</td>
		 *     <td>Kräfte welche hauptsächlich Angehörigen der jeweiligen Fraktion zugeschrieben werden.</td>
		 *  </tr>
		 *  <tr>
		 *     <td>Category::ClubPower</td>
		 *     <td>Kräfte welche hauptsächlich Angehörigen der jeweiligen Sonderfraktion (Blutlinie, Legat etc.) zugeschrieben werden.</td>
		 *  </tr>
		 *  </table>
		 */
		enum Category {
			CategoryNo		= 0x0000,
			Mental			= 0x0001,
			Physical		= 0x0002,
			Social			= 0x0004,
			Item			= 0x0008,
			FightingStyle	= 0x0010,
			DebateStyle		= 0x0020,
			Extraordinary	= 0x0040,
			Mild			= 0x0080,
			Severe			= 0x0100,
			BreedPower		= 0x0200,
			FactionPower	= 0x0400,
			ClubPower		= 0x0800,
			AllPower		= 0x0e00
		};
		Q_DECLARE_FLAGS( Categories, Category )	// Hiermit ermögliche ich die Verwendung von xx1|xx2|xx3

		/**
		 * Konstruktor.
		 **/
		cv_AbstractTrait( QString txt = "", cv_Species::Species spe = cv_Species::SpeciesNo, cv_AbstractTrait::Type ty = cv_AbstractTrait::TypeNo, cv_AbstractTrait::Category ca = cv_AbstractTrait::CategoryNo );
		
		/**
		 * Gibt den Namen der Eigenschaft zurück.
		 **/
		QString name() const;
		/**
		 * Legt den Namen der Eigenschaft fest
		 **/
		void setName(QString nam);
		/**
		 * Gibt aus, welche Spezies über diese Eigenschaft verfügen.
		 **/
		cv_Species::Species species() const;
		/**
		 * Legt fest, welche Spezies über diese Eigenschaft verfügen.
		 **/
		virtual void setSpecies(cv_Species::Species spe);
		/**
		 * Gibt zurück, welchem Typ diese Eigenschaft angehört.
		 **/
		Type type() const;
		/**
		 * Legt fest, welchem Typ diese Eigenschaft angehört.
		 **/
		virtual void setType(Type typ);
		/**
		 * Gibt zurpck, welcher Kategorie diese Eigenschaft angehört.
		 **/
		Category category() const;
		/**
		 * Legt fest, welcher Kategorie diese Eigenschaft angehört.
		 **/
		void setCategory(Category cat);

		/**
		 * Wandelt einen Typ in seinen in den Xml-Dateien gebräuchlichen Namen um.
		 *
		 * Diese Methode benötige ich, um die Strings in den XML-Template-Dateien zu erzeugen.
		 **/
		static QString toXmlString( cv_AbstractTrait::Type type );
		/**
		 * Wandelt eine Kategorie in ihren in den Xml-Dateien gebräuchlichen Namen um.
		 *
		 * Diese Methode benötige ich, um die Strings in den XML-Template-Dateien zu erzeugen.
		 **/
		static QString toXmlString( cv_AbstractTrait::Category category );
		/**
		 * Wandelt einen Typ in seinen realen Namen um.
		 *
		 * \note Diese Funktion unterscheidet sich insofern von toXmlString(), daß eine Übersetzung erfolgen kann und die Ausgabe des Plural möglich ist.
		 **/
		static QString toString( cv_AbstractTrait::Type type, bool plural = false /** Ist dieses Argument true, wird die Pluralform des Typs ausgegeben. */ );
		/**
		 * Wandelt eine Kategorie in ihren realen Namen um.
		 *
		 * \note Diese Funktion unterscheidet sich insofern von toXmlString(), daß beispielsweise FightingStyle mit einem zusätzlichen Leerzeichen (Fighting Style) ausgegeben wird. Außerdem kann die Pluralform ausgegeben werden. Außerdem werden in dieser Funktion Übersetzungen berücksichtigt.
		 **/
		static QString toString( cv_AbstractTrait::Category category, bool plural = false /** Ist dieses Argument true, wird die Pluralform der Kategorie ausgegeben. */ );
		/**
		 * Wandelt den Namen eines Typs in den dazu passenden enum um.
		 *
		 * Diese Methode benötige ich, um die Strings in den XML-Template-Dateien in Flags umzuwandeln.
		 **/
		static cv_AbstractTrait::Type toType( QString str );
		/**
		 * Wandelt den Namen einer Kategorie in den dazu passenden enum um.
		 *
		 * Diese Methode benötige ich, um die Strings in den XML-Template-Dateien in Flags umzuwandeln.
		 **/
		static cv_AbstractTrait::Category toCategory( QString str );

		/**
		 * Übergibt eine Liste aller Kategorien, welche für diesen Typ angemessen sind.
		 *
		 * Diese Methode vereinfacht das bilden von Schleifen über alle Kategorien eines besonderen Typs.
		 **/
		static QList< cv_AbstractTrait::Category > getCategoryList( cv_AbstractTrait::Type type );

		/**
		* Vergleich zwischen zwei Instanzen dieser Klasse.
		*
		* \todo Die Vergleiche sind noch nicht umfassend genug. Typ und Kategorie muß nich verglichen werden. etc.
		**/
		bool operator==( const cv_AbstractTrait &trait ) const;


	private:
		/**
		 * Der Name der Eigenschaft.
		 **/
		QString v_name;
		/**
		 * Welche Spezies über diese Eigenschaft verfügen.
		 **/
		cv_Species::Species v_species;
		/**
		 * Der Typ, dem diese Eigenschaft angehört.
		 *
		 * \sa Type
		 **/
		Type v_type;
		/**
		 * Die Kategorie, der diese Eigenschaft angehört.
		 *
		 * \sa Category
		 **/
		Category v_category;

		/**
		 * Eine Liste aller Kategorien für Attribute und Fertigkeiten.
		 **/
		static const QList< cv_AbstractTrait::Category > v_categoryListGeneral;
		/**
		 * Eine Liste aller Kategorien für Nachteile.
		 **/
		static const QList< cv_AbstractTrait::Category > v_categoryListExtended;
		/**
		 * Eine Liste der Kategorien für Geistesstörungen.
		 **/
		static const QList< cv_AbstractTrait::Category > v_categoryListDerangements;
		/**
		 * Eine Liste aller Kategorien für Merits.
		 **/
		static const QList< cv_AbstractTrait::Category > v_categoryListMerits;
		/**
		 * Eine Liste aller Kategorien für Powers.
		 **/
		static const QList< cv_AbstractTrait::Category > v_categoryListPowers;
};

Q_DECLARE_OPERATORS_FOR_FLAGS( cv_AbstractTrait::Categories )

#endif

