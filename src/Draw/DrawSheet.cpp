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

#include <QFont>
#include <QPainter>
#include <QDebug>

#include "../Storage/StorageTemplate.h"
#include "../Exceptions/Exception.h"
#include "../Config/Config.h"

#include "DrawSheet.h"

DrawSheet::DrawSheet( QObject* parent ) : QObject( parent ) {
	construct();
}

DrawSheet::DrawSheet( QObject* parent, QPrinter* printer ) : QObject( parent ) {
	construct();
	setPrinter( printer );
}

void DrawSheet::construct() {
	// Vorsicht, ist ein Zeiger.
	v_printer = 0;

	v_dotDiameterH = 1;
	v_dotDiameterV = 1;
	v_textHeight = 0;
	v_textDotsHeightDifference = 0;
	v_colorFill = QColor( 255, 0, 0 );

	character = StorageCharacter::getInstance();
	calcAdvantages = new CalcAdvantages( this );
}



void DrawSheet::setPrinter( QPrinter* printer ) {
	if ( v_printer != printer ) {
		v_printer = printer;
	}
}


void DrawSheet::print() {
	QPainter painter;

	painter.begin( v_printer );

	painter.setBrush( v_colorFill );

	QImage image;

	if ( character->species() == cv_Species::Human ) {
		image = QImage( ":/characterSheets/images/Charactersheet-Human.jpg" );
	} else if ( character->species() == cv_Species::Changeling ) {
		image = QImage( ":/characterSheets/images/Charactersheet-Changeling-1.jpg" );
	} else if ( character->species() == cv_Species::Mage ) {
		image = QImage( ":/characterSheets/images/Charactersheet-Mage-1.jpg" );
	} else if ( character->species() == cv_Species::Vampire ) {
		image = QImage( ":/characterSheet/images/Charactersheet-Vampire-1.jpg" );
	} else if ( character->species() == cv_Species::Werewolf ) {
		image = QImage( ":/characterSheets/images/Charactersheet-Werewolf-1.jpg" );
	} else {
		throw eSpeciesNotExisting( character->species() );
	}

	QRectF source( 0.0, 0.0, static_cast<double>( image.width() ), static_cast<double>( image.height() ) );

	QRectF target( 0.0, 0.0, static_cast<double>( v_printer->width() ), static_cast<double>( v_printer->height() ) );

	v_dotDiameterH = target.width() * 0.01156;
	v_dotDiameterV = target.height() * 0.0082;

	v_textHeight = target.height() * 0.0182;
	v_textDotsHeightDifference = target.height() * 0.002;

	qreal dotSizeFactor = 1.27;

	qreal offsetHAttributes = target.width() * 0.36;
	qreal offsetVAttributes = target.height() * 0.152;
	qreal distanceHAttributes = target.width() * 0.2764;
	qreal distanceVAttributes = target.height() * 0.0158;

	qreal offsetHSkills = target.width() * 0.338;
	qreal offsetVSkills = target.height() * 0.235;
	qreal distanceVSkills = target.height() * 0.0179;
	qreal distanceVCat = target.height() * 0.1735;
	qreal textWidthSkills = target.width() * 0.23;

	int maxMerits = 17;
	qreal offsetHMerits = target.width() * 0.66;
	qreal offsetVMerits = offsetVSkills;
	qreal distanceVMerits = target.height() * 0.0178;
	qreal textWidthMerits = target.width() * 0.247;

	int maxPowers = 0;
	qreal offsetHPowers = 0;
	qreal offsetVPowers = 0;
	qreal distanceVPowers = 0;
	qreal textWidthPowers = 0;

	qreal offsetHAdvantages = target.width() * 0.9823;
	qreal offsetVAdvantages = target.height() * 0.2119;
	qreal distanceVAdvantages = target.height() * 0.022;
	qreal textWidthAdvantages = target.width() * 0.174;

	qreal offsetHHealth = target.width() * 0.766;
	qreal offsetVHealth = target.height() * 0.3532;
	qreal distanceHHealth = target.width() * 0.017;

	qreal offsetHWillpower = target.width() * 0.77503;
	qreal offsetVWillpower = target.height() * 0.4145;
	qreal distanceHWillpower = distanceHHealth;

	qreal offsetHSuper = 0;
	qreal offsetVSuper = 0;
	qreal distanceHSuper = 0;

	qreal offsetHFuel = 0;
	qreal offsetVFuel = 0;
	qreal distanceHFuel = 0;
	qreal squareSizeFuel = 0;

	qreal offsetHFuelPerTurn = 0;
	qreal offsetVFuelPerTurn = 0;
	qreal distanceHFuelPerTurn = 0;

	qreal offsetHMorality = target.width() * 0.9565;
	qreal offsetVMorality = target.height() * 0.608;
	qreal distanceVMorality = target.height() * 0.0144;

	if ( character->species() == cv_Species::Human ) {
		// Werte bleiben, wie sie zuvor definiert wurden.
	} else if ( character->species() == cv_Species::Changeling ) {
		offsetHAttributes = target.width() * 0.352;
		offsetVAttributes = target.height() * 0.177;
		distanceHAttributes = target.width() * 0.257;
		distanceVAttributes = target.height() * 0.016;

		offsetHSkills = target.width() * 0.2955;
		offsetVSkills = target.height() * 0.261;
		distanceVCat = target.height() * 0.1665;
		textWidthSkills = target.width() * 0.14;

		maxMerits = 14;
		offsetHMerits = target.width() * 0.6085;
		offsetVMerits = target.height() * 0.4255;
		textWidthMerits = target.width() * 0.237;

		offsetHAdvantages = target.width() * 0.79;
		offsetVAdvantages = target.height() * 0.237;

		offsetHHealth = target.width() * 0.686;
		offsetVHealth = target.height() * 0.3725;

		offsetHWillpower = target.width() * 0.7255;
		offsetVWillpower = target.height() * 0.4275;

		offsetHSuper = target.width() * 0.73015;
		offsetVSuper = target.height() * 0.4887;
		distanceHSuper = target.width() * 0.016;

		offsetHMorality = target.width() * 0.909;
		offsetVMorality = target.height() * 0.716;
		distanceVMorality = target.height() * 0.0143;

		offsetHFuel = target.width() * 0.861;
		offsetVFuel = target.height() * 0.544;
		distanceHFuel = target.width() * 0.0032;
		squareSizeFuel = target.width() * 0.014;

		offsetHFuelPerTurn = target.width() * 0.865;
		offsetVFuelPerTurn = target.height() * 0.527;
		distanceHFuelPerTurn = target.height() * 0.045;

		maxPowers = 8;
		offsetHPowers = offsetHMerits;
		offsetVPowers = offsetVSkills;
		distanceVPowers = distanceVMerits;
		textWidthPowers = textWidthMerits;
	} else if ( character->species() == cv_Species::Mage ) {
	} else if ( character->species() == cv_Species::Vampire ) {
	} else if ( character->species() == cv_Species::Werewolf ) {
	} else {
		throw eSpeciesNotExisting( character->species() );
	}

	QFont characterFont;

	characterFont.setPointSize( v_textHeight*Config::textSizeFactorPrintNormal );

	painter.setFont( characterFont );

// 	qDebug() << Q_FUNC_INFO << "Punktradius" << v_dotDiameterH << v_dotDiameterV;

	painter.save();

	painter.drawImage( target, image, source );

	drawAttributes( &painter, offsetHAttributes, offsetVAttributes, distanceHAttributes, distanceVAttributes );
	drawSkills( &painter, offsetHSkills, offsetVSkills, distanceVSkills, distanceVCat, textWidthSkills );
	drawMerits( &painter, offsetHMerits, offsetVMerits, distanceVMerits, textWidthMerits, maxMerits );
	drawAdvantages( &painter, offsetHAdvantages, offsetVAdvantages, distanceVAdvantages, textWidthAdvantages );
	drawHealth( &painter, offsetHHealth, offsetVHealth, distanceHHealth, dotSizeFactor );
	drawWillpower( &painter, offsetHWillpower, offsetVWillpower, distanceHWillpower, dotSizeFactor );
	drawMorality( &painter, offsetHMorality, offsetVMorality, distanceVMorality );

	if ( character->species() != cv_Species::Human ) {
		drawPowers( &painter, offsetHPowers, offsetVPowers, distanceVPowers, textWidthPowers, maxPowers );
		drawSuper( &painter, offsetHSuper, offsetVSuper, distanceHSuper, dotSizeFactor );
		drawFuelMax( &painter, offsetHFuel, offsetVFuel, distanceHFuel, squareSizeFuel );
		drawFuelPerTurn( &painter, offsetHFuelPerTurn, offsetVFuelPerTurn, distanceHFuelPerTurn );
	}

	painter.restore();

	painter.end();
	qDebug() << Q_FUNC_INFO << "Fertig";
}


void DrawSheet::drawAttributes( QPainter* painter, qreal offsetH, qreal offsetV, qreal distanceH, qreal distanceV ) {
	QList< cv_Trait::Category > categories;
	categories.append( cv_Trait::Mental );
	categories.append( cv_Trait::Physical );
	categories.append( cv_Trait::Social );

	QList< cv_Trait > list;

	for ( int i = 0; i < categories.count(); i++ ) {
		list = character->attributes( categories.at( i ) );

		for ( int j = 0; j < list.count(); j++ ) {
			for ( int k = 0; k < list.at( j ).value; k++ ) {
				// Punkte malen.
				QRectF dotsRect( offsetH + distanceH*i + v_dotDiameterH*k, offsetV + distanceV*j, v_dotDiameterH, v_dotDiameterV );
				painter->drawEllipse( dotsRect );
			}
		}
	}
}

void DrawSheet::drawSkills( QPainter* painter, qreal offsetH, qreal offsetV, qreal distanceV, qreal distanceVCat, qreal textWidth ) {
	QList< cv_Trait::Category > categories;
	categories.append( cv_Trait::Mental );
	categories.append( cv_Trait::Physical );
	categories.append( cv_Trait::Social );

	QList< cv_Trait > list;

	for ( int i = 0; i < categories.count(); i++ ) {
		list = character->skills( categories.at( i ) );

		for ( int j = 0; j < list.count(); j++ ) {
			for ( int k = 0; k < list.at( j ).value; k++ ) {
				// Punkte malen.
				QRectF dotsRect( offsetH + v_dotDiameterH*k, offsetV + distanceV*j + distanceVCat*i, v_dotDiameterH, v_dotDiameterV );
				painter->drawEllipse( dotsRect );
			}

			if ( !list.at( j ).details.isEmpty() ) {
				QString specialities;

				for ( int k = 0; k < list.at( j ).details.count(); k++ ) {
					// Spezialisierungen hinzufügen
					specialities.append( list.at( j ).details.at( k ).name );

					if ( k < list.at( j ).details.count() - 1 ) {
						specialities.append( ", " );
					}
				}

				// Spezialisierungen schreiben.
				painter->save();

				QFont lclFont;

				lclFont.setPointSize( v_textHeight*Config::textSizeFactorPrintSmall );

				painter->setFont( lclFont );

				// Wird ein bißchen nach oben verschoben, damit der Name schön über dem Strich steht.
				QRect textRect( offsetH - textWidth, offsetV + distanceV*j + distanceVCat*i, textWidth, v_textHeight );

// 				painter->drawRect( textRect );
				painter->drawText( textRect, Qt::AlignLeft | Qt::AlignTop | Qt::TextWordWrap, specialities );

				painter->restore();
			}
		}
	}
}


void DrawSheet::drawMerits( QPainter* painter, qreal offsetH, qreal offsetV, qreal distanceV, qreal textWidth, int maxNumber ) {
	QList< cv_Trait > listToUse;

	try {
		listToUse = getTraits( cv_Trait::Merit, maxNumber );
	} catch ( eTraitsExceedSheetCapacity &e ) {
		listToUse = getTraits( cv_Trait::Merit, maxNumber, true );
		emit enforcedTraitLimits( cv_Trait::Merit );
	}

	for ( int j = 0; j < listToUse.count(); j++ ) {
		for ( int k = 0; k < listToUse.at( j ).value; k++ ) {
			// Punkte malen.
			QRectF dotsRect( offsetH + v_dotDiameterH*k, offsetV + distanceV*j, v_dotDiameterH, v_dotDiameterV );
			painter->drawEllipse( dotsRect );
		}

		QString name = listToUse.at( j ).name;

		QString customText = listToUse.at( j ).customText;

		// Namen
		QRect textRect( offsetH - textWidth, offsetV - v_textDotsHeightDifference + distanceV*j, textWidth, v_textHeight );
		painter->drawText( textRect, Qt::AlignLeft | Qt::AlignTop | Qt::TextWordWrap, name );

		// Zusatztext

		if ( !customText.isEmpty() ) {
			painter->save();
			QFont lclFont;
			lclFont.setPointSize( v_textHeight*Config::textSizeFactorPrintSmall );
			painter->setFont( lclFont );
			painter->drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, customText + " " );
			painter->restore();
		}
	}
}

void DrawSheet::drawAdvantages( QPainter* painter, qreal offsetH, qreal offsetV, qreal distanceV, qreal textWidth ) {
	// Size
	QRect textRect = QRect( offsetH - textWidth, offsetV + distanceV * 0, textWidth, v_textHeight );
	painter->drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( calcAdvantages->size() ) );

	// Initiative
	textRect = QRect( offsetH - textWidth, offsetV + distanceV * 1, textWidth, v_textHeight );
	painter->drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( calcAdvantages->initiative() ) );

	// Speed
	textRect = QRect( offsetH - textWidth, offsetV + distanceV * 2, textWidth, v_textHeight );
	painter->drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( calcAdvantages->speed() ) );

	// Defense
	textRect = QRect( offsetH - textWidth, offsetV + distanceV * 3, textWidth, v_textHeight );
	painter->drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, QString::number( calcAdvantages->defense() ) );

	// Armor
}

void DrawSheet::drawHealth( QPainter* painter, qreal offsetH, qreal offsetV, qreal distanceH, qreal dotSizeFactor ) {
	int health = calcAdvantages->health();

	for ( int i = 0; i < health; i++ ) {
		QRect dotsRect = QRect( offsetH + distanceH * i, offsetV, v_dotDiameterH * dotSizeFactor, v_dotDiameterV * dotSizeFactor );
		painter->drawEllipse( dotsRect );
	}
}

void DrawSheet::drawWillpower( QPainter* painter, qreal offsetH, qreal offsetV, qreal distanceH, qreal dotSizeFactor ) {
	int willpower = calcAdvantages->willpower();

	for ( int i = 0; i < willpower; i++ ) {
		QRect dotsRect = QRect( offsetH + distanceH * i, offsetV, v_dotDiameterH * dotSizeFactor, v_dotDiameterV * dotSizeFactor );
		painter->drawEllipse( dotsRect );
	}
}

void DrawSheet::drawMorality( QPainter* painter, qreal offsetH, qreal offsetV, qreal distanceV, qreal dotSizeFactor ) {
	int value = character->morality();

	for ( int i = 0; i < value; i++ ) {
		QRect dotsRect = QRect( offsetH, offsetV - distanceV * i, v_dotDiameterH * dotSizeFactor, v_dotDiameterV * dotSizeFactor );
		painter->drawEllipse( dotsRect );
	}
}

void DrawSheet::drawPowers( QPainter* painter, qreal offsetH, qreal offsetV, qreal distanceV, qreal textWidth, int maxNumber ) {
	QList< cv_Trait > listToUse;

	try {
		listToUse = getTraits( cv_Trait::Power, maxNumber );
	} catch ( eTraitsExceedSheetCapacity &e ) {
		listToUse = getTraits( cv_Trait::Power, maxNumber, true );
		emit enforcedTraitLimits( cv_Trait::Power );
	}

	for ( int j = 0; j < listToUse.count(); j++ ) {
		for ( int k = 0; k < listToUse.at( j ).value; k++ ) {
			// Punkte malen.
			QRectF dotsRect( offsetH + v_dotDiameterH*k, offsetV + distanceV*j, v_dotDiameterH, v_dotDiameterV );
			painter->drawEllipse( dotsRect );
		}

		QString name = listToUse.at( j ).name;

		QString customText = listToUse.at( j ).customText;

		// Namen
		QRect textRect( offsetH - textWidth, offsetV - v_textDotsHeightDifference + distanceV*j, textWidth, v_textHeight );
		painter->drawText( textRect, Qt::AlignLeft | Qt::AlignTop | Qt::TextWordWrap, name );

		// Zusatztext

		if ( !customText.isEmpty() ) {
			painter->save();
			QFont lclFont;
			lclFont.setPointSize( v_textHeight*Config::textSizeFactorPrintSmall );
			painter->setFont( lclFont );
			painter->drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, customText + " " );
			painter->restore();
		}
	}
}

void DrawSheet::drawSuper( QPainter* painter, qreal offsetH, qreal offsetV, qreal distanceH, qreal dotSizeFactor ) {
	int value = character->superTrait();

	for ( int i = 0; i < value; i++ ) {
		QRect dotsRect = QRect( offsetH + distanceH * i, offsetV, v_dotDiameterH * dotSizeFactor, v_dotDiameterV * dotSizeFactor );
		painter->drawEllipse( dotsRect );
	}
}

void DrawSheet::drawFuelMax( QPainter* painter, qreal offsetH, qreal offsetV, qreal distanceH, qreal widthPerSquare ) {
	StorageTemplate storage;
	int value = storage.fuelMax( character->species(), character->superTrait() );

	if ( value > 20 ) {
		QString fuel;

		for ( int i = 0; i < storage.species().count(); i++ ) {
			if ( cv_Species::toSpecies( storage.species().at( i ).name ) == character->species() ) {
				fuel = storage.species().at( i ).fuel;
				break;
			}
		}

		throw eValueExceedsSheetCapacity( value, fuel );
	}

	painter->save();

	painter->setOpacity(0.5);

	for ( int i = 0; i < 20 - value; i++ ) {
		QRect fuelRect = QRect( offsetH - (widthPerSquare + distanceH) * i, offsetV, -widthPerSquare, widthPerSquare );
// 		painter->drawLine( fuelRect.bottomLeft(), fuelRect.topRight() );
// 		painter->drawLine( fuelRect.topLeft(), fuelRect.bottomRight() );
		painter->drawRect(fuelRect);
	}

	painter->restore();
}

void DrawSheet::drawFuelPerTurn( QPainter* painter, qreal offsetH, qreal offsetV, qreal distanceH )
{
	StorageTemplate storage;
	int value = storage.fuelPerTurn( character->species(), character->superTrait() );

	QRect textRect = QRect(offsetH, offsetV, distanceH, v_textHeight );
	painter->drawText(textRect, Qt::AlignHCenter | Qt::AlignBottom, QString::number(value) );
// 	painter->drawRect(textRect);
}






QList< cv_Trait > DrawSheet::getTraits( cv_Trait::Type type, int maxNumber, bool enforceTraitLimits ) {
	QList< cv_Trait::Category > categories;
	categories.append( cv_Trait::CategoryNo );

	if ( type == cv_Trait::Merit ) {
		categories.append( cv_Trait::Mental );
		categories.append( cv_Trait::Physical );
		categories.append( cv_Trait::Social );
		categories.append( cv_Trait::Item );
		categories.append( cv_Trait::FightingStyle );
		categories.append( cv_Trait::DebateStyle );
		categories.append( cv_Trait::Extraordinary );
		categories.append( cv_Trait::Species );
	}

	QList< cv_Trait > list;

	QList< cv_Trait > listToUse;

	int iter = 0;

	for ( int i = 0; i < categories.count(); i++ ) {
		list = character->traits( type, categories.at( i ) );

		for ( int j = 0; j < list.count(); j++ ) {
			if ( list.at( j ).value > 0 ) {
				iter++;
				listToUse.append( list.at( j ) );
			}

			// Sobald keine Eigenschaften mehr auf den Charakterbogen passen, hören wir auf, weitere hinzuzuschreiben. Das gilt natürlich nur, wenn maxNumber größer als 0 ist.
			if ( maxNumber > 0 && iter >= maxNumber ) {
				if ( enforceTraitLimits ) {
					break;
				} else {
					throw eTraitsExceedSheetCapacity( type, maxNumber );
				}
			}
		}
	}

	return listToUse;
}
