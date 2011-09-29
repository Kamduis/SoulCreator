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

#include "Parser/StringBoolParser.h"
#include "Exceptions/Exception.h"
#include "Dialogs/MessageBox.h"

#include "CharaTrait2.h"


CharaTrait2::CharaTrait2( QWidget* parent, Trait* trait, Trait* traitStorage ) : TraitLine( parent, trait->name(), trait->value() ) {
	// Vorsicht: Nullzeiger ist immer gefährlich!
	ptr_trait = 0;
	ptr_traitStorage = traitStorage;

	character = StorageCharacter::getInstance();

	// Falls ich mit der Maus den Wert ändere, muß er auch entsprechend verändert werden.
	connect( this, SIGNAL( valueChanged( int ) ), this, SLOT( setTraitValue( int ) ) );
	connect( this, SIGNAL( textChanged( QString ) ), this, SLOT( setCustomText( QString ) ) );
	connect( this, SIGNAL( typeChanged( cv_Trait::Type ) ), this, SLOT( hideSpecialtyWidget( cv_Trait::Type ) ) );
	connect( this, SIGNAL( typeChanged( cv_Trait::Type ) ), this, SLOT( hideDescriptionWidget() ) );
	connect( this, SIGNAL( specialtiesClicked( bool ) ), this, SLOT( emitSpecialtiesClicked( bool ) ) );

// 	connect( this, SIGNAL( traitChanged( cv_Trait* ) ), character, SIGNAL( traitChanged( cv_Trait* ) ) );
	connect( character, SIGNAL( traitChanged( Trait* ) ), this, SLOT( checkTraitPrerequisites( Trait* ) ) );
// 	connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( hideTraitIfNotAvailable( cv_Species::SpeciesFlag ) ) );

	setTraitPtr( trait );
	
	connect( traitPtr(), SIGNAL(valueChanged(int)), this, SLOT(setValue(int)) );

	if (!traitPtr()->possibleValues().isEmpty()){
		setPossibleValues(traitPtr()->possibleValues());
	}

	hideSpecialtyWidget( trait->type() );
	hideDescriptionWidget();
}


Trait* CharaTrait2::traitPtr() const {
	return ptr_trait;
}

void CharaTrait2::setTraitPtr( Trait* trait ) {
	if ( ptr_trait != trait ) {
		ptr_trait = trait;
	}
}


// int CharaTrait2::value() const {
// 	return traitPtr()->value();
// }
// void CharaTrait2::setValue( int val ) {
// 	qDebug() << Q_FUNC_INFO << name() << val << value();
// 	if ( value() != val ) {
// 		TraitLine::setValue( val );
// 	}
// }
void CharaTrait2::setTraitValue( int val ) {
	qDebug() << Q_FUNC_INFO << name() << val << value();
	if ( traitPtr()->value() != val ) {
		traitPtr()->setValue( val );
	}
}


QString CharaTrait2::customText() const {
	return traitPtr()->customText();
}
void CharaTrait2::setCustomText( QString txt ) {
	if ( traitPtr()->customText() != txt ) {
		traitPtr()->setCustomText(txt);
		
		TraitLine::setText( txt );

		emit traitChanged( traitPtr() );
	}
}


cv_Trait::Type CharaTrait2::type() const {
	return ptr_trait->type();
}

void CharaTrait2::setType( cv_Trait::Type type ) {
	if ( ptr_trait->type() != type ) {
		ptr_trait->setType(type);

		emit typeChanged( type );
		emit traitChanged( traitPtr() );
	}
}

cv_Trait::Category CharaTrait2::category() const {
	return ptr_trait->category();
}

void CharaTrait2::setCategory( cv_Trait::Category category ) {
	if ( ptr_trait->category() != category ) {
		ptr_trait->setCategory(category);

		emit traitChanged( traitPtr() );
	}
}

cv_Species::Species CharaTrait2::species() const {
	return ptr_trait->species();
}

void CharaTrait2::setSpecies( cv_Species::Species species ) {
	if ( ptr_trait->species() != species ) {
		ptr_trait->setSpecies(species);
// 		emit speciesChanged(species);

		emit traitChanged( traitPtr() );
	}
}


bool CharaTrait2::custom() const {
	return ptr_trait->custom();
}

void CharaTrait2::setCustom( bool sw ) {
	if ( ptr_trait->custom() != sw ) {
		ptr_trait->setCustom(sw);

		emit traitChanged( traitPtr() );
	}
}

void CharaTrait2::hideSpecialtyWidget( cv_Trait::Type type ) {
	if ( type == cv_Trait::Skill ) {
		hideSpecialties( false );
	} else {
		hideSpecialties( true );
	}
}

void CharaTrait2::hideDescriptionWidget() {
	if ( custom() ) {
		hideDescription( false );
	} else {
		hideDescription( true );
	}
}

void CharaTrait2::emitSpecialtiesClicked( bool sw ) {
	if ( ptr_traitStorage != 0 ) {
		QList< cv_TraitDetail > listStora = ptr_traitStorage->details();
		QList< cv_TraitDetail > listChara = traitPtr()->details();

		qDebug() << Q_FUNC_INFO << traitPtr()->name() << ptr_traitStorage->name() << traitPtr()->details().count() << ptr_traitStorage->details().count();

		for ( int i = 0; i < listStora.count(); i++ ) {
			for ( int j = 0; j < listChara.count(); j++ ) {
				if ( listStora.at( i ).name == listChara.at( j ).name ) {
					qDebug() << Q_FUNC_INFO << sw << listStora.at( i ).name << listChara.at( j ).name << listChara.at( j ).value;
					cv_TraitDetail traitDetail = listChara.at( j );
					listStora.replace( i, traitDetail );
				}
			}
		}

		emit specialtiesClicked( sw, name(), listStora );
	}
}


void CharaTrait2::checkTraitPrerequisites( Trait* trait ) {
	if ( !ptr_traitStorage->prerequisites().isEmpty() && ptr_traitStorage->prerequisites().contains( trait->name() ) ) {
		qDebug() << Q_FUNC_INFO << "Wird für" << this->name() << "ausgeführt, weil sich Fertigkeit" << trait->name() << "geändert hat";

		QString prerequisites = parsePrerequisites( ptr_traitStorage->prerequisites() );

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


QString CharaTrait2::parsePrerequisites( QString text ) {
	QString prerequisites = text;

	// Ersetze alle Atrtribute, Fertigkeiten etc. in dem Textstring mit den entsprechenden Zahlen, damit diese später über den Parser ausgewertet werden können.
	// Nicht vorhandene Werte verbleiben natürlich in Textform und werden vom Parser wie 0en behandelt.

	if ( prerequisites.contains( QRegExp( "([a-zA-Z]+)\\s*[<>=]+" ) ) ) {
		QList< Trait* >* list = character->traits2();

		for ( int k = 0; k < list->count(); k++ ) {
			// Ersetzen der Fertigkeitsspezialisierungen von dem Format Fertigkeit.Spezialisierung mit Fertigkeitswert, wenn Spezialisierung existiert oder 0, wenn nicht.
			if ( prerequisites.contains( '.' ) && list->at( k )->type() == cv_Trait::Skill && list->at( k )->details().count() > 0 ) {
				QString testSkill = list->at( k )->name() + ".";

				if ( prerequisites.contains( testSkill ) ) {
					QString specialisation = prerequisites.right( prerequisites.indexOf( testSkill ) - testSkill.count() + 1 );
					specialisation = specialisation.left( specialisation.indexOf( ' ' ) );

					for ( int l = 0; l < list->at( k )->details().count(); l++ ) {
						// Fertigkeiten mit Spezialisierungsanforderungen werden mit dem Fertigkeitswert ersetzt, wenn Spez existiert, ansonsten mit 0.
						if ( specialisation == list->at( k )->details().at( l ).name ) {
							prerequisites.replace( testSkill + specialisation, QString::number( list->at( k )->value() ) );

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
				prerequisites.replace( list->at( k )->name(), QString::number( list->at( k )->value() ) );

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


void CharaTrait2::hideTraitIfNotAvailable( cv_Species::SpeciesFlag sp ) {
	if ( species().testFlag( sp ) ) {
		setHidden( false );
	} else {
		setValue( 0 );
		setHidden( true );
	}
}
