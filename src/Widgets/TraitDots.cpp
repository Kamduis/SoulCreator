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

#include <QtGui>

#include "TraitDots.h"

// #include "valgrind/memcheck.h"

TraitDots::TraitDots( QWidget *parent ) : QWidget( parent ) {
	// Variablen initialisieren.
	v_minimum = 0;
	v_maximum = 5;
	v_readOnly = false;
	v_value = 0;

	// Es gibt anfangs keine verbotenen Werte, also nur eine leere Liste erstellen
	v_forbiddenValues = new QList<int>();

	// Standardwerte setzen
	setMinimum( 0 );
	setMaximum( 5 );

	// setValue() muß nach dem Füllen der MyAllowedValues-Liste aufgurefen werden, damit die List Einträge besitzt, bevort sie abgefragt wird.
	setValue( 0 );

	// Widget darf nur proportional in seiner Größe verändert werden?
	// Minimalgröße festlegen
	v_minimumSizeY = 8;
	int minimumSizeX = v_minimumSizeY * maximum();
	setMinimumSize( minimumSizeX, v_minimumSizeY );
	//setMinimumSize(50, 10);
	setSizePolicy( QSizePolicy::Minimum, QSizePolicy::Fixed );

	// Setze Standardfarbe weiß
	v_colorEmpty = QColor( 255, 255, 255 );
	v_colorFull = QColor( 0, 0, 0 );
	v_colorFrame = QColor( 0, 0, 0 );

	connect( this, SIGNAL( maximumChanged( int ) ), this, SLOT( resetMinimumSize( int ) ) );
}


TraitDots::~TraitDots() {
	delete v_forbiddenValues;
}


// Das automatisch ausgelöste paintEvent, das das Widget bei jeder Fensterveränderung neu zeichnet.
void TraitDots::paintEvent( QPaintEvent * ) {
	// Wenn das Widget disabled ist, muß ich den Alphakanal meiner Farben verändern.

	static const int frameWidth = 16;
	static const QPoint dotCenter = QPoint( 0, 0 );
	QPoint shiftCenter = dotCenter;
	// Damit der Rahmen nicht irgendwie abgeschnitten wird, muß der Kreis entsprechend kleiner sein.
	static const int dotRadius = 100;
	static QPen framePen = QPen( QBrush( Qt::OpaqueMode ), frameWidth );
	framePen.setColor( v_colorFrame );

	int dotDiameter = 2 * dotRadius + frameWidth;

	QPainter painter( this );

	double windowWidth = double( width() ) / maximum();
	double windowHeight = double( height() );
	double side = qMin( windowWidth, windowHeight );

	painter.setRenderHint( QPainter::Antialiasing );

	if ( !isEnabled() ) {
		painter.setOpacity( .5 );
	}

	painter.translate( double( side / 2 ), double( height() / 2 ) );

	painter.scale( side / double( dotDiameter ), side / double( dotDiameter ) );

	painter.setPen( framePen );
	painter.setBrush( v_colorFull );

	painter.setPen( framePen );
	painter.setBrush( v_colorFull );

	painter.save();

	for ( int i = 0; i < v_value; i++ ) {
		shiftCenter = dotCenter + QPoint( 0 + dotDiameter * i, 0 );
		painter.drawEllipse( shiftCenter, dotRadius, dotRadius );
// 		if (v_forbiddenValues->contains(i+1)){
// 			painter.drawEllipse(shiftCenter, dotRadius/2, dotRadius/2);
// 		}
	}

	painter.restore();

	painter.setBrush( v_colorEmpty );

	painter.save();

	for ( int i = v_value; i < maximum(); i++ ) {
		shiftCenter = dotCenter + QPoint( 0 + dotDiameter * i, 0 );
		painter.drawEllipse( shiftCenter, dotRadius, dotRadius );

		if ( v_forbiddenValues->contains( i + 1 ) ) {
			int dotRadiusHalf = dotRadius / 2;
			painter.drawLine( shiftCenter.x() - dotRadiusHalf, shiftCenter.y() - dotRadiusHalf, shiftCenter.x() + dotRadiusHalf, shiftCenter.y() + dotRadiusHalf );
			painter.drawLine( shiftCenter.x() - dotRadiusHalf, shiftCenter.y() + dotRadiusHalf, shiftCenter.x() + dotRadiusHalf, shiftCenter.y() - dotRadiusHalf );
		}
	}

// 	for (int i = 0; i < v_forbiddenValues->count(); i++) {
// 		shiftCenter = dotCenter + QPoint( 0 + dotDiameter * (v_forbiddenValues->at(i) - 1), 0 );
// // 		painter.drawLine(shiftCenter.x()-dotDiameter/2, shiftCenter.y()-dotDiameter/2, shiftCenter.x()+dotDiameter/2, shiftCenter.y()+dotDiameter/2);
// // 		painter.drawLine(shiftCenter.x()+dotDiameter/2, shiftCenter.y()-dotDiameter/2, shiftCenter.x()-dotDiameter/2, shiftCenter.y()+dotDiameter/2);
// 		painter.drawEllipse(shiftCenter, dotRadius/2, dotRadius/2);
// 	}

	painter.restore();
}


// Anklicken
void TraitDots::mousePressEvent( QMouseEvent *event ) {
	if ( !v_readOnly ) {
		// den ursprÜnglichen Wert speichern
		int oldValue = value();

		// Die Position des Mauszeigers beim Klicken wird errechnet. Dabei soll die Mitte der linken Seite der Position (0, 0) entsprechen.
		QPointF mousePoint = event->pos() - rect().bottomLeft() - QPoint( 0, rect().height() / 2 );

		// Welche Breite haben die Punkte? Das bestimme ich je nachdem, ob das Fenster zu breit ist, sie alle aufzunehmen, oder zu hoch, aus Höhe bzw. Breite.
		double windowWidth = double( width() ) / maximum();
		double windowHeight = double( height() );
		double dotDiameter = qMin( windowWidth, windowHeight );

		// Hierdurch entspricht der neue Wert dem Punkt, auf den geklickt wurde
		int newValue = int( mousePoint.x() / dotDiameter ) + 1;

		// Dadurch kann ich aber den Wert 0 nicht erreichen.
		// Also Abfrage einbauen, damit der Wert 0 wird, wenn der Wert bereits 1 war und wieder auf 1 geklickt wird,

		if ( oldValue == 1 && newValue == 1 )
			setValue( 0 );
		else
			setValue( newValue );

		// Signal senden, wenn der neue Wert sich vom alten unterscheidet.
		// Dieses Signal soll nur ausgesendet werden, wenn der User den Wert ändert, nicht wenn programmtechnisch der Wert verändert wird. DafÜr existiert das signal valueChanged( int ).
		if ( value() != oldValue ) {
			emit valueClicked( value() );
		}
	}
}


bool TraitDots::readOnly() const {
	return v_readOnly;
}

void TraitDots::setReadOnly( bool sw ) {
	if ( v_readOnly != sw ) {
		v_readOnly = sw;
	}
}



// Ist anatomisch nicht sehr sinnvoll
//// Doppelklick soll den Wert entweder auf 0 setzen, wenn er vorher nicht 0 war oder ihn auf das Maximum setzen.
//void TraitDots::mouseDoubleClickEvent(QMouseEvent *event){
//	if (value() == 0)
//		setValue( maximum() );
//	else
//		setValue( 0 );
//
//	// Neu zeichnen
//	update();
//}


void TraitDots::changeEvent( QEvent *event ) {
	update();
}


int TraitDots::value() const {
	return v_value;
}

int TraitDots::maximum() const {
	return v_maximum;
}

int TraitDots::minimum() const {
	return v_minimum;
}

QColor TraitDots::colorEmpty() const {
	return v_colorEmpty;
}

QColor TraitDots::colorFull() const {
	return v_colorFull;
}

QColor TraitDots::colorFrame() const {
	return v_colorFrame;
}




// Ändert sich der Maximalwert, ändert sich auch die minimale Breite, die das Widget in Anspruch nicmmt
void TraitDots::resetMinimumSize( int sizeX ) {
	setMinimumWidth( sizeX * v_minimumSizeY );
}


void TraitDots::setValue( int valueArg ) {
	int newValue = valueArg;

	// Negative Werte werden nicht Übernommen

	if ( newValue >= 0 ) {
		// Reduziere den zu setzenden Wert solange um 1, bis er unter dem Maximum und nicht in der v_forbiddenList liegt.
		// NatÜrlich wird die Schleife abgebrochen, sollte dadurch der Wert auf 0 sinken.
		// Ich beschleunige diese Abarbeitung, falls der Wert deutlich größer als maximum() ist.
		if ( newValue > maximum() ) {
			newValue = maximum();
		}

		while ( v_forbiddenValues->contains( newValue ) && newValue > 0 ) {
			newValue--;
		}

		// sollte der reduzierte Wert irgendwie unter den Minimalwert fallen, muß er auf eben diesen gesetzt werden, selbst wenn der Minimalwert aufgrund eines Fehlers nicht erlaubt sein sollte.
		if ( newValue < minimum() ) {
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

void TraitDots::setMaximum( int valueArg ) {
	// Negative Werte werden nicht Übernommen
	if ( valueArg >= 0 ) {
		// Signal aussenden, wenn der Wert /verändert/ wurde
		if ( valueArg != maximum() ) {
			// Wert verändern
			v_maximum = valueArg;
			// Signal
			emit maximumChanged( valueArg );
			// neu zeichnen
			update();
		}

		// Ist das neue Maximum kleiner als das Minimum wird letzteres verändert, um dieses mindestens so groß wie das Maximum zu behalten.
		if ( valueArg < minimum() )
			setMinimum( valueArg );

		// Entferne das neue Maximum aus v_forbiddenList
		// Diese Liste kann (rein theoretisch) mehrere identische Werte enthalten, also das ganze Über eine while-Schleife tun.
		while ( v_forbiddenValues->contains( valueArg ) ) {
			v_forbiddenValues->removeAt( v_forbiddenValues->indexOf( valueArg ) );
		}

		// Ist das neue Maximum kleiner als der aktuell angezeigte Wert, muß dieser auf das Maximum gesetzt werden.
		if ( valueArg < value() ) {
			setValue( valueArg );
		}
	}
}

void TraitDots::setMinimum( int valueArg ) {
// 	qDebug() << Q_FUNC_INFO << "Valgrind:" << VALGRIND_CHECK_VALUE_IS_DEFINED(valueArg);
// 	qDebug() << Q_FUNC_INFO << "Valgrind:" << VALGRIND_CHECK_MEM_IS_DEFINED(valueArg, sizeof(int));

	// Negative Werte werden nicht Übernommen
	if ( valueArg >= 0 ) {
		v_minimum = valueArg;

		// Ist das neue Minimum größer als das Maximum wird letzteres verändert, um dieses mindestens so groß wie das Minimum zu behalten.

		if ( valueArg > maximum() )
			setMaximum( valueArg );

// 		qDebug() << Q_FUNC_INFO << "Valgrind:" << VALGRIND_CHECK_VALUE_IS_DEFINED(v_forbiddenValues);
		// Entferne das neue Minimum aus v_forbiddenList.
		// Diese Liste kann (rein theoretisch) mehrere identische Werte enthalten, also das agnze Über eine while-Schleife tun.
		while ( v_forbiddenValues->contains( valueArg ) ) {
			v_forbiddenValues->removeAt( v_forbiddenValues->indexOf( valueArg ) );
		}

		// Ist das neue Minimum größer als der aktuell angezeigte Wert, muß dieser auf das Minimum gesetzt werden.
		if ( valueArg > value() ) {
			setValue( valueArg );
		}
	}
}


//// Verändere die Breite des Seperators
//void TraitDots::setSeperatorWidth( int valueArg ){
//	MySeperatorWidth = valueArg;
//}
//
//
//// Verändere die Anzahl Punkte, ehe ein Seperator gesetzt wird
//void TraitDots::setSeperatorWidth( int valueArg ){
//	MySeperatorStep = valueArg;
//}


// Verändert die FÜllfarbe
void TraitDots::setColorEmpty( const QColor & color ) {
	v_colorEmpty = color;

	// Neu zeichnen
	update();
}


// Verändert die FÜllfarbe
void TraitDots::setColorFull( const QColor & color ) {
	v_colorFull = color;

	// Neu zeichnen
	update();
}


// Verändert die Randfarbe
void TraitDots::setColorFrame( const QColor & color ) {
	v_colorFrame
	= color;

	// Neu zeichnen
	update();
}


// Setzte die verbotenen Werte
// Beachtet noch nicht, daß ein aktueller Wert nach einer veränderung der verbotenen Werte erhalten bleibt, obwohl er inzsichen verboten ist.
void TraitDots::setForbiddenValues( QList<int> *values ) {
	v_forbiddenValues = values;

	// den aktuelle Minimum suchen und eventuell entfernen. Das Minimum muß immer erlaubt sein.

	while ( v_forbiddenValues->contains( minimum() ) ) {
		v_forbiddenValues->removeAt( v_forbiddenValues->indexOf( minimum() ) );
	}
}


// Das es manchmal einfacher ist, erlaubte Werte einzugeben, mÜssen diese entsprechend Übersetzt werden, ehe sie in die v_forbiddenList eingesetzt werden.
void TraitDots::setAllowedValues( QList<int> *values ) {
	// Neue List erstellen und mit den Werten aus dem Argument fÜllen. Aber da Werte kleiner 0 nie erlaubt sind, werden diese garnicht erst Übernommen
	QList<int> *tmpList = new QList<int>();

	for ( int i = 0; i < values->size(); i++ ) {
		if ( values->at( i ) >= 0 )
			tmpList->append( values->at( i ) );
	}

	// Neue Liste sortieren
	qSort( tmpList->begin(), tmpList->end() );

	// Das neue Minimum entspricht dem Wert an Index 0 der Liste
	setMinimum( tmpList->at( 0 ) );

	// Das neue Maximum bleibt unverändert, wenn es größer ist als der größte erlaubte Wert. Es werden alle maximal möglichen Punkte angezeigt, aber sie können eben nicht alle ausgefÜllt werden. Ist es allersgins kleiner wird es auf den größten erlaubten wert gesetzt.
	if ( tmpList->at( tmpList->size() - 1 ) > maximum() )
		setMaximum( tmpList->at( tmpList->size() - 1 ) );

	// Eine Schleife beginnt beim Minimalwert und reicht bis zum Maximalwert. Es werden alle Werte verboten, die nicht im Argumetn genannt werden.
	v_forbiddenValues->clear();

	for ( int i = minimum(); i <= maximum(); i++ ) {
		if ( !tmpList->contains( i ) )
			v_forbiddenValues->append( i );
	}

	delete tmpList;
}


// FÜgt einen erlaubten Wert hinzu
void TraitDots::addAllowedValue( int value ) {
	// value aus v_forbiddenList entfernen.
	if ( v_forbiddenValues->contains( value ) ) {
		v_forbiddenValues->removeAll( value );
	}
}


// FÜgt einen verbotenen Wert hinzu
void TraitDots::addForbiddenValue( int value ) {
	if ( !v_forbiddenValues->contains( value ) ) {
		v_forbiddenValues->append( value );

		// Liste wieder sortieren
		qSort( v_forbiddenValues->begin(), v_forbiddenValues->end() );
	}
}


void TraitDots::forbidAll() {
	for ( int i = minimum(); i < maximum() + 1; i++ ) {
		addForbiddenValue( i );
	}
}

void TraitDots::forbidNone() {
	v_forbiddenValues->clear();
}
