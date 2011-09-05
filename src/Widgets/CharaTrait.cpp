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

#include <QDebug>

#include "../Parser/StringBoolParser.h"
#include "../Exceptions/Exception.h"
#include "Dialogs/MessageBox.h"

#include "CharaTrait.h"


CharaTrait::CharaTrait( QWidget* parent, cv_Trait::Type type, cv_Trait::Category category, cv_Species::Species species, QString name, bool custom, int value ) : TraitLine( parent, name, value ) {
	construction( type, category, species, name, custom, value );
}

CharaTrait::CharaTrait( QWidget* parent, cv_Trait trait ) : TraitLine( parent, trait.name, trait.value ) {
	construction( trait.type, trait.category, trait.species, trait.name, trait.custom, trait.value );

	if ( !trait.possibleValues.isEmpty() ) {
		setPossibleValues( trait.possibleValues );
// 		qDebug() << Q_FUNC_INFO << trait.name << trait.possibleValues;
	}

	v_prerequisites = trait.prerequisites;
}


void CharaTrait::construction( cv_Trait::Type type, cv_Trait::Category category, cv_Species::Species species, QString name, bool custom, int value ) {
	v_type = cv_Trait::TypeNo;
	v_category = cv_Trait::CategoryNo;
	v_species = cv_Species::SpeciesNo;
	v_custom = false;

	character = StorageCharacter::getInstance();

	connect( this, SIGNAL( valueChanged( int ) ), this, SLOT( emitTraitChanged( int ) ) );
	connect( character, SIGNAL( traitChanged( cv_Trait ) ), this, SLOT( checkTraitPrerequisites( cv_Trait ) ) );
	connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( hideTraitIfNotAvailable( cv_Species::SpeciesFlag ) ) );
	connect( this, SIGNAL( traitChanged( cv_Trait ) ), character, SLOT( addTrait( cv_Trait ) ) );
	connect( this, SIGNAL( typeChanged( cv_Trait::Type ) ), this, SLOT( hideSpecialtyWidget( cv_Trait::Type ) ) );
	connect( this, SIGNAL( typeChanged( cv_Trait::Type ) ), this, SLOT( hideDescriptionWidget() ) );
	connect( this, SIGNAL( customChanged( bool ) ), this, SLOT( hideDescriptionWidget() ) );
	connect( this, SIGNAL( specialtiesClicked( bool ) ), this, SLOT( emitSpecialtiesClicked( bool ) ) );
	// Änderungen am Charakter im Speicher müssen dieses Widget aber auch aktualisieren.
	connect( character, SIGNAL( traitChanged( cv_Trait ) ), this, SLOT( setTrait( cv_Trait ) ) );

	// Damit die Schaltfläche für die Spezialisierungen verborgen wird, wenn sie nicht nötig ist.
// 	hideSpecialtyWidget(cv_Trait::Skill);
	setType( type );
	setCategory( category );
	setSpecies( species );
	setCustom( custom );
}




cv_Trait::Type CharaTrait::type() const {
	return v_type;
}

void CharaTrait::setType( cv_Trait::Type type ) {
	if ( v_type != type ) {
		v_type = type;

		emit typeChanged( type );
	}
}

cv_Trait::Category CharaTrait::category() const {
	return v_category;
}

void CharaTrait::setCategory( cv_Trait::Category category ) {
	if ( v_category != category ) {
		v_category = category;
	}
}

cv_Species::Species CharaTrait::species() const {
	return v_species;
}

void CharaTrait::setSpecies( cv_Species::Species species ) {
	if ( v_species != species ) {
		v_species = species;
// 		emit speciesChanged(species);
	}
}


bool CharaTrait::custom() const {
	return v_custom;
}

void CharaTrait::setCustom( bool sw ) {
	if ( v_custom != sw ) {
		v_custom = sw;

		emit customChanged( sw );
	}
}


void CharaTrait::addSpecialty( cv_TraitDetail specialty ) {
	v_specialties.append( specialty );
}



void CharaTrait::hideSpecialtyWidget( cv_Trait::Type type ) {
	if ( type == cv_Trait::Skill ) {
		hideSpecialties( false );
	} else {
		hideSpecialties( true );
	}
}

void CharaTrait::hideDescriptionWidget() {
	if ( custom() ) {
		hideDescription( false );
	} else {
		hideDescription( true );
	}
}

void CharaTrait::setTrait( cv_Trait trait ) {
	if ( type() == trait.type && category() == trait.category && name() == trait.name ) {
		if ( !custom() ) {
			setValue( trait.value );
		} else if ( text() == trait.customText ){
			setValue( trait.value );
		} else if ( text() == "" ){
			setText(trait.customText);
			setValue( trait.value );
		}
	}
}






void CharaTrait::emitTraitChanged( int value ) {
	// Eigenschaften mit Beschreibungstext werden nur dann in den Speicher aktualisiert, wenn sie auch einen solchen Text besitzen.
	if ( !custom() || !text().isEmpty() ) {
		cv_Trait trait;

		// Wenn es die Eigenschaft schon im Speicher gibt, hole ich mir die Parameter natürlich von dort und ändere nur den Wert

		QList< cv_Trait > list = character->traits( type(), category() );

		for ( int i = 0; i < list.count();i++ ) {
			if ( name() == list.at( i ).name ) {
				trait = list.at( i );
				trait.value = value;
				trait.customText = text();
				emit traitChanged( trait );
				return;
			}
		}

		trait.type = type();
		trait.category = category();
		trait.name = name();
		trait.value = value;
		trait.custom = custom();
		trait.customText = text();

// 		qDebug() << Q_FUNC_INFO << "Dies ist ein Test, den ich nicht verstehe!" << name() << text();
		// Lieber nicht. Das sind nicht die ausgewählten, sondern die \emph{möglichen} Spezialisierungen.
// 		trait.details = v_specialties;

		emit traitChanged( trait );
	}
}

void CharaTrait::emitSpecialtiesClicked( bool sw ) {
	QList< cv_TraitDetail > list = v_specialties;
	QList< cv_Trait > traitList = character->traits( type(), category() );

	for ( int i = 0; i < list.count(); i++ ) {
		for ( int j = 0; j < traitList.count(); j++ ) {
			for ( int k = 0; k < traitList.at( j ).details.count(); k++ ) {
				if ( list.at( i ).name == traitList.at( j ).details.at( k ).name ) {
					cv_TraitDetail detail = list.at( i );
					detail.value = true;
					list.replace( i, detail );
				}
			}
		}

// 		qDebug() << Q_FUNC_INFO << list.at( i ).name << list.at( i ).value;
	}

	emit specialtiesClicked( sw, name(), list );
}


void CharaTrait::checkTraitPrerequisites( cv_Trait trait ) {
// 	qDebug() << Q_FUNC_INFO << name() << v_prerequisites;
	if ( !v_prerequisites.isEmpty() && v_prerequisites.contains( trait.name ) ) {
		QString prerequisites = parsePrerequisites( v_prerequisites );

		// Alles was an Wörtern übriggeblieben ist durch 0 ersetzen.
		// Wäre schön, wenn das der Parser könnte, da kriege ich das aber nicht hin.
		QString replacementText;
		QRegExp rx( "([a-zA-Z]+)\\s*[<>=]+" );

		while ( prerequisites.contains( rx ) ) {
// 			qDebug() << Q_FUNC_INFO << name() << prerequisites;
			prerequisites.replace( "AND", "999" );
			prerequisites.replace( "OR", "88" );
			prerequisites.replace( QRegExp( "([a-zA-Z]+)" ), "0" );
			prerequisites.replace( ".0", "0" );
// 			prerequisites.replace(QRegExp("(0 0)"), '0');
			prerequisites.replace( "999", "AND" );
			prerequisites.replace( "88", "OR" );
		}

		StringBoolParser parser;

		try {
			if ( parser.validate( prerequisites ) ) {
				this->setEnabled( true );
			} else {
				setValue( 0 );
				this->setEnabled( false );
			}
		} catch ( Exception &e ) {
			qDebug() << Q_FUNC_INFO << name() << prerequisites << e.description() << e.message();
			MessageBox::exception( this, e.message(), e.description() );
		}
	}
}


QString CharaTrait::parsePrerequisites( QString text ) {
	QString prerequisites = text;

	// Ersetze alle Atrtribute, Fertigkeiten etc. in dem Textstring mit den entsprechenden Zahlen, damit diese später über den Parser ausgewertet werden können.
	// Nicht vorhandene Werte verbleiben natürlich in Textform und werden vom Parser wie 0en behandelt.

	if ( prerequisites.contains( QRegExp( "([a-zA-Z]+)\\s*[<>=]+" ) ) ) {
		QList< cv_Trait > list = character->traitsAll();

		for ( int k = 0; k < list.count(); k++ ) {
			// Ersetzen der Fertigkeitsspezialisierungen von dem Format Fertigkeit.Spezialisierung mit Fertigkeitswert, wenn Spezialisierung existiert oder 0, wenn nicht.
			if ( prerequisites.contains( '.' ) && list.at( k ).type == cv_Trait::Skill && list.at( k ).details.count() > 0 ) {
				QString testSkill = list.at( k ).name + ".";

				if ( prerequisites.contains( testSkill ) ) {
					QString specialisation = prerequisites.right( prerequisites.indexOf( testSkill ) - testSkill.count() + 1 );
					specialisation = specialisation.left( specialisation.indexOf( ' ' ) );

					for ( int l = 0; l < list.at( k ).details.count(); l++ ) {
						// Fertigkeiten mit Spezialisierungsanforderungen werden mit dem Fertigkeitswert ersetzt, wenn Spez existiert, ansonsten mit 0.
						if ( specialisation == list.at( k ).details.at( l ).name ) {
							prerequisites.replace( testSkill + specialisation, QString::number( list.at( k ).value ) );

							// Wenn alle Worte ersetzt wurden, kann ich aus den Schleifen raus.

							if ( !prerequisites.contains( QRegExp( "([a-zA-Z]+)\\s*[<>=]+" ) ) ) {
								return prerequisites;
							}
						} else {
							prerequisites.replace( testSkill + specialisation, "0" );

							// Wenn alle Worte ersetzt wurden, kann ich aus den Schleifen raus.

							if ( !prerequisites.contains( QRegExp( "([a-zA-Z]+)\\s*[<>=]+" ) ) ) {
								return prerequisites;
							}
						}
					}
				}
			} else {
				// Ersetzen von Eigenschaftsnamen mit ihren Werten.
				prerequisites.replace( list.at( k ).name, QString::number( list.at( k ).value ) );

				// Wenn alle Worte ersetzt wurden, kann ich aus den Schleifen raus.

				if ( !prerequisites.contains( QRegExp( "([a-zA-Z]+)\\s*[<>=]+" ) ) ) {
					return prerequisites;
				}
			}
		}
	} else {
		qDebug() << Q_FUNC_INFO << "Nicht durch die Schleifen." << name();
	}
}


void CharaTrait::hideTraitIfNotAvailable( cv_Species::SpeciesFlag sp ) {
	if ( species().testFlag( sp ) ) {
		setHidden( false );
	} else {
		setValue(0);
		setHidden( true );
	}
}

