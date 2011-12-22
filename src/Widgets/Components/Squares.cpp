/**
 * \file
 * \author Victor von Rhein <victor@caern.de>
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

#include <QtGui>

#include <math.h>

#include "Squares.h"

// #include "valgrind/memcheck.h"

Squares::Squares( QWidget *parent ) : QWidget( parent ) {
	// Variablen initialisieren.
	v_minimum = 0;
	v_maximum = 5;
	v_columnMax = 10;
	v_readOnly = false;
	v_value = 0;

	// Standardwerte setzen
	setMinimum( 0 );
	setMaximum( 10 );
	setValue( 0 );

	// Widget darf nur proportional in seiner Größe verändert werden?
	// Minimalgröße festlegen
	v_minimumSizeY = 10;
	resetMinimumSize();
	//setMinimumSize(50, 10);
// 	setSizePolicy( QSizePolicy::MinimumExpanding, QSizePolicy::Preferred );

	// Setze Standardfarbe weiß
	v_colorEmpty = QColor( 255, 255, 255 );
	v_colorFrame = QColor( 0, 0, 0 );

	connect( this, SIGNAL( maximumChanged( int ) ), this, SLOT( resetMinimumSize() ) );
	connect( this, SIGNAL( columnMaxChanged( int ) ), this, SLOT( resetMinimumSize() ) );
}


Squares::~Squares() {
}


// Das automatisch ausgelöste paintEvent, das das Widget bei jeder Fensterveränderung neu zeichnet.
void Squares::paintEvent( QPaintEvent * ) {
	static const int frameWidth = 1;
	static const int separatorWidth = 1;

	// Damit der Rahmen nicht irgendwie abgeschnitten wird, muß das Quadrat entsprechend kleiner sein.
	static const int squareSideLength = 10;
	static QPen framePen = QPen( QBrush( Qt::OpaqueMode ), frameWidth );
	framePen.setColor( v_colorFrame );

	int squareSideLengthPlus = squareSideLength + 2 * frameWidth;

	QPainter painter( this );

	double windowWidth = static_cast<double>( width() ) / static_cast<double>( qMin( maximum(), columnMax() ) );
// 	qDebug() << Q_FUNC_INFO << "Witdh" << windowWidth;
	double windowHeight = ( static_cast<double>( maximum() ) / static_cast<double>( columnMax() ) );
	windowHeight = ceil( windowHeight );
	windowHeight = static_cast<double>( height() ) / windowHeight;
// 	qDebug() << Q_FUNC_INFO << "Height" << windowHeight;
	double side = qMin( windowWidth, windowHeight );

	painter.setRenderHint( QPainter::Antialiasing );

	// Wenn das Widget disabled ist, muß ich den Alphakanal meiner Farben verändern.

	if ( !isEnabled() ) {
		painter.setOpacity( .5 );
	}

// 	painter.translate( double( windowWidth ), double( windowHeight ) );

	painter.scale( side / double( squareSideLengthPlus ), side / double( squareSideLengthPlus ) );

	painter.setPen( framePen );

	painter.setBrush( v_colorEmpty );

	painter.save();

	int squareColumnIter = 0;
	int squareLineIter = 0;
	for ( int i = 0; i < maximum(); ++i ) {
		QRect square = QRect(( squareSideLength + separatorWidth ) * squareColumnIter + frameWidth * ( squareColumnIter + 1 ), ( squareSideLength + separatorWidth ) * squareLineIter + frameWidth * ( squareLineIter + 1 ), squareSideLength, squareSideLength );
// 		qDebug() << Q_FUNC_INFO << square;
		painter.drawRect( square );

		// Wir zeichnen die ausgekreuzten Quadrate
		if (value() > columnMax()*squareLineIter+ squareColumnIter){
			painter.drawLine(square.bottomLeft(), square.topRight());
			painter.drawLine(square.topLeft(), square.bottomRight());
		}

		squareColumnIter++;

		if ( squareColumnIter >= columnMax() ) {
			squareColumnIter = 0;
			squareLineIter++;
		}
	}

	painter.restore();
}


// Anklicken
void Squares::mousePressEvent( QMouseEvent *event ) {
	if ( !v_readOnly ) {
		// den ursprÜnglichen Wert speichern
		int oldValue = value();

		// Die Position des Mauszeigers beim Klicken wird errechnet. Dabei soll die Mitte der linken Seite der Position (0, 0) entsprechen.
// 		QPointF mousePoint = event->pos() - rect().bottomLeft() - QPoint( 0, rect().height() / 2 );
		QPointF mousePoint = event->pos() - rect().topLeft();

		// Größe der Quadrate
		double squareSide = static_cast<double>( width() ) / static_cast<double>( qMin( maximum(), columnMax() ) );

		// Hierdurch entspricht der neue Wert dem Punkt, auf den geklickt wurde
		int newValue = static_cast<int>( mousePoint.x() / squareSide ) + 1;
		newValue += (static_cast<int>( mousePoint.y() / squareSide )) * columnMax();

		// Dadurch kann ich aber den Wert 0 nicht erreichen.
		// Also Abfrage einbauen, damit der Wert 0 wird, wenn der Wert bereits 1 war und wieder auf 1 geklickt wird,
		if ( oldValue == 1 && newValue == 1 )
			setValue( 0 );
		else
			setValue( newValue );

		qDebug() << Q_FUNC_INFO << value();

		// Signal senden, wenn der neue Wert sich vom alten unterscheidet.
		// Dieses Signal soll nur ausgesendet werden, wenn der User den Wert ändert, nicht wenn programmtechnisch der Wert verändert wird. DafÜr existiert das signal valueChanged( int ).
		if ( value() != oldValue ) {
			emit valueClicked( value() );
		}
	}
}


bool Squares::readOnly() const {
	return v_readOnly;
}

void Squares::setReadOnly( bool sw ) {
	if ( v_readOnly != sw ) {
		v_readOnly = sw;
	}
}


void Squares::changeEvent( QEvent *event ) {
	update();
}


int Squares::value() const {
	return v_value;
}

void Squares::setValue( int valueArg ) {
	int newValue = valueArg;

	// Negative Werte werden nicht Übernommen

	if ( newValue >= 0 ) {
		// Reduziere den zu setzenden Wert solange um 1, bis er unter dem Maximum und nicht in der v_forbiddenList liegt.
		// NatÜrlich wird die Schleife abgebrochen, sollte dadurch der Wert auf 0 sinken.
		// Ich beschleunige diese Abarbeitung, falls der Wert deutlich größer als maximum() ist.
		if ( newValue > maximum() ) {
			newValue = maximum();
		} else if ( newValue < minimum() ) {
			newValue = minimum();
		}

		// Signal aussenden, wenn der Wert /verändert/ wurde
		if ( v_value != newValue ) {
			v_value = newValue;

			emit valueChanged( newValue );

			// neu zeichnen
			update();
		}

		// Signal aussenden
		emit activated( newValue );
	}
}

int Squares::maximum() const {
	return v_maximum;
}

void Squares::setMaximum( int valueArg ) {
	// Negative Werte werden nicht Übernommen
	if ( valueArg >= 0 ) {
		// Signal aussenden, wenn der Wert /verändert/ wurde
		if ( valueArg != maximum() ) {
			v_maximum = valueArg;

			emit maximumChanged( valueArg );

			// neu zeichnen
			update();
		}

		// Ist das neue Maximum kleiner als das Minimum wird letzteres verändert, um dieses mindestens so groß wie das Maximum zu behalten.
		if ( valueArg < minimum() )
			setMinimum( valueArg );

		// Ist das neue Maximum kleiner als der aktuell angezeigte Wert, muß dieser auf das Maximum gesetzt werden.
		if ( valueArg < value() ) {
			setValue( valueArg );
		}
	}
}

int Squares::minimum() const {
	return v_minimum;
}

void Squares::setMinimum( int valueArg ) {
	// Negative Werte werden nicht Übernommen
	if ( valueArg >= 0 ) {
		v_minimum = valueArg;

		// Ist das neue Minimum größer als das Maximum wird letzteres verändert, um dieses mindestens so groß wie das Minimum zu behalten.

		if ( valueArg > maximum() )
			setMaximum( valueArg );

		// Ist das neue Minimum größer als der aktuell angezeigte Wert, muß dieser auf das Minimum gesetzt werden.
		if ( valueArg > value() ) {
			setValue( valueArg );
		}
	}
}

int Squares::columnMax() const {
	return v_columnMax;
}

void Squares::setColumnMax( int value ) {
	if ( v_columnMax != value ) {
		if ( value > 1 ) {
			v_columnMax = value;
		} else {
			v_columnMax = 1;
		}

		emit columnMaxChanged( value );
	}
}


QColor Squares::colorEmpty() const {
	return v_colorEmpty;
}

void Squares::setColorEmpty( const QColor & color ) {
	v_colorEmpty = color;

	// Neu zeichnen
	update();
}

QColor Squares::colorFrame() const {
	return v_colorFrame;
}

void Squares::setColorFrame( const QColor & color ) {
	v_colorFrame
	= color;

	// Neu zeichnen
	update();
}




// Ändert sich der Maximalwert, ändert sich auch die minimale Breite, die das Widget in Anspruch nicmmt
void Squares::resetMinimumSize() {
	int countX = qMin( v_maximum, v_columnMax );
	setMinimumWidth( countX * ( v_minimumSizeY ) );

	double countYdouble = static_cast<double>( v_maximum ) / static_cast<double>( v_columnMax );
	countYdouble = ceil( countYdouble );
	int countY = static_cast<int>( countYdouble );
	setMinimumHeight( v_minimumSizeY * countY );
}


