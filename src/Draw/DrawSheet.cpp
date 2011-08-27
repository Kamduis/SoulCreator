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
	v_colorFill = QColor( 0, 0, 0 );

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
		image = QImage( ":/characterSheet/images/Charactersheet-Human.png" );
	} else if ( character->species() == cv_Species::Changeling ) {
		image = QImage( ":/characterSheet/images/Charactersheet-Changeling-1.png" );
	} else if ( character->species() == cv_Species::Mage ) {
		image = QImage( ":/characterSheet/images/Charactersheet-Mage-1.png" );
	} else if ( character->species() == cv_Species::Vampire ) {
		image = QImage( ":/characterSheet/images/Charactersheet-Vampire-1.png" );
	} else if ( character->species() == cv_Species::Werewolf ) {
		image = QImage( ":/characterSheet/images/Charactersheet-Werewolf-1.png" );
	} else {
		throw eSpeciesNotExisting( character->species() );
	}

	QRectF source( 0.0, 0.0, static_cast<double>( image.width() ), static_cast<double>( image.height() ) );

	QRectF target( 0.0, 0.0, static_cast<double>( v_printer->width() ), static_cast<double>( v_printer->height() ) );

	v_dotDiameterH = target.width() / 86.5;
	v_dotDiameterV = target.height() / 122;

	v_textHeight = target.height() / 55;
	v_textDotsHeightDifference = target.height() / 500;

	QFont characterFont;
	characterFont.setPointSize( v_textHeight*Config::textSizeFactorPrintNormal );

	painter.setFont( characterFont );

// 	qDebug() << Q_FUNC_INFO << "Punktradius" << v_dotDiameterH << v_dotDiameterV;

	painter.save();

	painter.drawImage( target, image, source );

	qreal offsetHAttributes = target.width() / 2.772;
	qreal offsetVAttributes = target.height() / 6.575;
	qreal distanceHAttributes = target.width() / 3.618;
	qreal distanceVAttributes = target.height() / 63.4;

	drawAttributes( &painter, offsetHAttributes, offsetVAttributes, distanceHAttributes, distanceVAttributes );

	qreal offsetHSkills = target.width() / 2.961;
	qreal offsetVSkills = target.height() / 4.25;
	qreal distanceVSkills = target.height() / 56;
	qreal distanceVCat = target.height() / 5.765;
	qreal textWidthSkills = target.width() / 4.35;

	drawSkills( &painter, offsetHSkills, offsetVSkills, distanceVSkills, distanceVCat, textWidthSkills );

	qreal offsetHMerits = target.width() / 1.516;
	qreal offsetVMerits = offsetVSkills;
	qreal distanceVMerits = target.height() / 56.2;
	qreal textWidthMerits = target.width() / 4.05;

	drawMerits( &painter, offsetHMerits, offsetVMerits, distanceVMerits, textWidthMerits );

	qreal offsetHAdvantages = target.width() / 1.018;
	qreal offsetVAdvantages = target.height() / 4.72;
	qreal distanceVAdvantages = target.height() / 45;
	qreal textWidthAdvantages = target.width() / 5.75;

	drawAdvantages( &painter, offsetHAdvantages, offsetVAdvantages, distanceVAdvantages, textWidthAdvantages );

	qreal offsetHHealth = target.width() * 0.766;
	qreal offsetVHealth = target.height() / 2.8316;
	qreal distanceHHealth = target.height() / 85.5;
	qreal dotSizeFactor = 1.27;

	drawHealth( &painter, offsetHHealth, offsetVHealth, distanceHHealth, dotSizeFactor );

	qreal offsetHWillpower = target.width() * 0.77503;
	qreal offsetVWillpower = target.height() * 0.4145;
	qreal distanceHWillpower = distanceHHealth;

	drawWillpower( &painter, offsetHWillpower, offsetVWillpower, distanceHWillpower, dotSizeFactor );

	qreal offsetHMorality = target.width() * 0.9565;
	qreal offsetVMorality = target.height() * 0.608;
	qreal distanceVMorality = target.height() * 0.0144;

	drawMorality( &painter, offsetHMorality, offsetVMorality, distanceVMorality );

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

void DrawSheet::drawMerits( QPainter* painter, qreal offsetH, qreal offsetV, qreal distanceV, qreal textWidth ) {
	QList< cv_Trait::Category > categories;
	categories.append( cv_Trait::Mental );
	categories.append( cv_Trait::Physical );
	categories.append( cv_Trait::Social );
	categories.append( cv_Trait::Item );
	categories.append( cv_Trait::FightingStyle );
	categories.append( cv_Trait::DebateStyle );
	categories.append( cv_Trait::Extraordinary );
	categories.append( cv_Trait::Species );

	QList< cv_Trait > list;
	QList< cv_Trait > listToUse;

	for ( int i = 0; i < categories.count(); i++ ) {
		list = character->merits( categories.at( i ) );

		for ( int j = 0; j < list.count(); j++ ) {
			if ( list.at( j ).value > 0 ) {
				listToUse.append( list.at( j ) );
			}
		}
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
			painter->drawText( textRect, Qt::AlignRight | Qt::AlignTop | Qt::TextWordWrap, customText );
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
		QRect dotsRect = QRect( offsetH, offsetV - distanceV*i, v_dotDiameterH * dotSizeFactor, v_dotDiameterV * dotSizeFactor );
		painter->drawEllipse( dotsRect );
	}
}
