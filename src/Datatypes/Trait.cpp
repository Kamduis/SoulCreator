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

#include <QDebug>

#include "Exceptions/Exception.h"
#include "Parser/StringBoolParser.h"

#include "Trait.h"


Trait::Trait( QString txt, int val, cv_Species::Species spe, cv_AbstractTrait::Type ty, cv_AbstractTrait::Category ca, QObject* parent ) : QObject( parent ), cv_Trait( txt, val, spe, ty, ca ) {
	construct();
}

Trait::Trait( cv_Trait trait, QObject* parent ) : QObject( parent ), cv_Trait( trait.name(), trait.value(), trait.species(), trait.type(), trait.category() ) {
	construct();

	setEra( trait.era() );
	setAge( trait.age() );
	setPrerequisites( trait.prerequisites() );
	setCustom( trait.custom() );
	setCustomText( trait.customText() );
	setDetails( trait.details() );
	setPossibleValues( trait.possibleValues() );
}

Trait::Trait( Trait* trait, QObject* parent ) : QObject( parent ), cv_Trait( trait->name(), trait->value(), trait->species(), trait->type(), trait->category() ) {
	construct();

	setEra( trait->era() );
	setAge( trait->age() );
	setPrerequisites( trait->prerequisites() );
	setCustom( trait->custom() );
	setCustomText( trait->customText() );
	setDetails( trait->details() );
	setPossibleValues( trait->possibleValues() );
}

void Trait::construct() {
	// Am Anfang stehen alle Fertigkeiten zur Verfügung, aber wenn dann die Voraussetzungen geprüft werden, kann sich das ändern.
	v_available = true;

	connect( this, SIGNAL( valueChanged( int ) ), this, SLOT( emitTraitChanged() ) );
	connect( this, SIGNAL( detailsChanged( int ) ), this, SLOT( emitTraitChanged() ) );
	connect( this, SIGNAL( valueChanged( int ) ), this, SLOT( clearDetails( int ) ) );
}



void Trait::setValue( int val ) {
// 	qDebug() << Q_FUNC_INFO << name() << val << value();
	if ( value() != val ) {
		cv_Trait::setValue( val );

		emit valueChanged( val );
	}
}

void Trait::setDetails( QList< cv_TraitDetail > list ) {
	if ( details() != list ) {
		cv_Trait::setDetails( list );

		emit detailsChanged( list.count() );
	}
}
void Trait::addDetail( cv_TraitDetail det ) {
	if ( !details().contains( det ) ) {
		cv_Trait::addDetail( det );

		emit detailsChanged( details().count() );
	} else {
// 		qDebug() << Q_FUNC_INFO << "Spezialisierung" << det.name << "existiert schon";
	}
}
void Trait::clearDetails() {
// 	qDebug() << Q_FUNC_INFO << "Hallo?";
	if ( !details().isEmpty() ) {
		cv_Trait::clearDetails();

		emit detailsChanged( 0 );
	}
}
void Trait::clearDetails( int val ) {
	if ( val < 1 ) {
		this->clearDetails();
	}
}


void Trait::setType( cv_AbstractTrait::Type typ ) {
	if ( type() != typ ) {
		cv_AbstractTrait::setType( typ );

		emit typeChanged( typ );
	}
}

bool Trait::isAvailable() const {
	return v_available;
}
void Trait::setAvailability( bool sw ) {
	if ( v_available != sw ) {
		v_available = sw;

		emit availabilityChanged( sw );
	}
}



QList< Trait* > Trait::prerequisitePtrs() const {
	return v_prerequisitePtrs;
}
void Trait::clearPrerequisitePtrs() {
	v_prerequisitePtrs.clear();
}
void Trait::addPrerequisitePtrs( Trait* replacement ) {
	if ( !prerequisites().isEmpty() && ( prerequisites().contains( replacement->name() ) ) ) {
		// In die Liste einfügen.
		v_prerequisitePtrs.append( replacement );
	}
}


void Trait::checkPrerequisites( Trait* trait ) {
	if ( !prerequisitePtrs().isEmpty() ) {
// 		qDebug() << Q_FUNC_INFO << "Wird für" << this->name() << "ausgeführt, weil sich Fertigkeit" << trait->name() << "geändert hat";

		QString lcl_prerequisites = parsePrerequisites( prerequisites(), prerequisitePtrs() );

		// Alles was an Wörtern übriggeblieben ist durch 0 ersetzen.
		// Wäre schön, wenn das der Parser könnte, da kriege ich das aber nicht hin.
		QString replacementText;
		QRegExp rx( "([a-zA-Z]+)\\s*[<>=]+" );

		while ( lcl_prerequisites.contains( rx ) ) {
// 			qDebug() << Q_FUNC_INFO << name() << prerequisites;
			lcl_prerequisites.replace( "AND", "999" );
			lcl_prerequisites.replace( "OR", "88" );
			lcl_prerequisites.replace( QRegExp( "([a-zA-Z]+)" ), "0" );
			lcl_prerequisites.replace( ".0", "0" );
// 			prerequisites.replace(QRegExp("(0 0)"), '0');
			lcl_prerequisites.replace( "999", "AND" );
			lcl_prerequisites.replace( "88", "OR" );
		}

// 		qDebug() << Q_FUNC_INFO << "Voraussetzungen für" << this->name() << "sind" << lcl_prerequisites;

		StringBoolParser parser;

		try {
			if ( parser.validate( lcl_prerequisites ) ) {
				setAvailability( true );
			} else {
				setAvailability( false );
			}
		} catch ( Exception &e ) {
			qDebug() << Q_FUNC_INFO << name() << lcl_prerequisites << e.description() << e.message();
		}

// 		qDebug() << Q_FUNC_INFO << "Wurde für" << this->name() << "ausgeführt, weil sich Fertigkeit" << trait->name() << "geändert hat. Ergebnis ist:" << isAvailable();
	}
}


QString Trait::parsePrerequisites( QString text, QList< Trait* > list ) {
	QString prerequisites = text;

	// Ersetze alle Atrtribute, Fertigkeiten etc. in dem Textstring mit den entsprechenden Zahlen, damit diese später über den Parser ausgewertet werden können.
	// Nicht vorhandene Werte verbleiben natürlich in Textform und werden vom Parser wie 0en behandelt.

	if ( prerequisites.contains( QRegExp( "([a-zA-Z]+)\\s*[<>=]+" ) ) ) {
		for ( int k = 0; k < list.count(); ++k ) {
			// Ersetzen der Fertigkeitsspezialisierungen von dem Format Fertigkeit.Spezialisierung mit Fertigkeitswert, wenn Spezialisierung existiert oder 0, wenn nicht.
			if ( prerequisites.contains( '.' ) && list.at( k )->type() == cv_AbstractTrait::Skill && list.at( k )->details().count() > 0 ) {
				QString testSkill = list.at( k )->name() + ".";

				if ( prerequisites.contains( testSkill ) ) {
					QString specialisation = prerequisites.right( prerequisites.indexOf( testSkill ) - testSkill.count() + 1 );
					specialisation = specialisation.left( specialisation.indexOf( ' ' ) );

					for ( int l = 0; l < list.at( k )->details().count(); l++ ) {
						// Fertigkeiten mit Spezialisierungsanforderungen werden mit dem Fertigkeitswert ersetzt, wenn Spez existiert, ansonsten mit 0.
						if ( specialisation == list.at( k )->details().at( l ).name ) {
							prerequisites.replace( testSkill + specialisation, QString::number( list.at( k )->value() ) );

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
				prerequisites.replace( list.at( k )->name(), QString::number( list.at( k )->value() ) );

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


void Trait::emitTraitChanged() {
	emit traitChanged( this );
}
