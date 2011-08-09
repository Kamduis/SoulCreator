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

#ifndef TRAITDOTS_H
#define TRAITDOTS_H

#include <QWidget>
#include <QColor>
#include <QList>


/**
 * @brief Eine Darstellung von Werten in Form ausgefüllter Punkte.
 *
 * Ein einfacher ganzzahliger Wert wirden in Form ausgefüllter Punkte dargestellt. Die bis zum Maximalwert übrigen Punkte sind nicht ausgefüllt.
 *
 * Es besteht die Möglichkeit aus der Menge an Werten zwischen \ref minimum und \ref maximum einige zu verbieten.
 */

class TraitDots : public QWidget {
		Q_OBJECT
		/**
		 * Speichert den aktuellen Wert des Widgets.
		 *
		 * Dieser Wert stellt die Zahl der ausgefüllten Punkte dar. Die Gesamtzahl der dargestellten Punkte ist in \ref maximum gespeichert.
		 *
		 * Soll value auf einen Wert gesetzt werden, der über dem Maximum liegt, wird er nur auf das Maximum gesetzt, soll er unter das Minimum gesetzt werden, wird er auf Minimum gesetzt.
		 * 
		 * Soll value auf einen verbotenen Wert gesetzt werden, wird er auf den nächstkleineren, erlaubten Wert gesetzt.
		 *
		 * \access value(), setValue()
		 *
		 * \notifier valueChanged()
		 **/
		Q_PROPERTY( int value READ value WRITE setValue NOTIFY valueChanged )
		/**
		 * Speichert den Maximalwert des Widgets.
		 *
		 * Der Maximalwert bestimmt, wieviele Punkte insgesamt angezeigt werden.
		 *
		 * \access maximum(), setMaximum()
		 *
		 * \notifier maximumChanged()
		 **/
		Q_PROPERTY( int maximum READ maximum WRITE setMaximum NOTIFY maximumChanged )
		/**
		 * Speichert den Minimalwert des Widgets.
		 *
		 * \access minimum(), setMinimum()
		 *
		 * \notifier minimumChanged()
		 **/
		Q_PROPERTY( int minimum READ minimum WRITE setMinimum NOTIFY minimumChanged )
		/**
		 * Speichert die Farbe der als 'leer' klassifizierten Punkte.
		 *
		 * \access colorEmpty(), setColorEmpty()
		 **/
		Q_PROPERTY( QColor colorEmpty READ colorEmpty WRITE setColorEmpty )
		/**
		 * Speichert die Farbe der als 'gefüllt' klassifizierten Punkte.
		 *
		 * \access colorFull(), setColorFull()
		 **/
		Q_PROPERTY( QColor colorFull READ colorFull WRITE setColorFull )
		/**
		 * Speichert die Farbe des Rahmens der Punkte.
		 *
		 * \access colorFrame(), setColorFrame()
		 **/
		Q_PROPERTY( QColor colorFrame READ colorFrame WRITE setColorFrame )

	public:
		TraitDots( QWidget *parent = 0 );
		/**
		 * Zerstört das Objekt und gibt alle zugeteilten Ressourcen wieder frei.
		 **/
		~TraitDots();

		int value() const;
		int maximum() const;
		int minimum() const;
		QColor colorEmpty() const;
		QColor colorFull() const;
		QColor colorFrame() const;

	private:
		int v_minimumSizeY;
		int v_value;
		int v_maximum;
		int v_minimum;
		int v_seperatorWidth;
		int v_seperatorStep;

		QColor v_colorEmpty;
		QColor v_colorFull;
		QColor v_colorFrame;

		QList<int> *v_forbiddenValues;

	public slots:
		void setValue( int );
		void setMaximum( int );
		void setMinimum( int );
		//void setSeperatorWidth( int )
		//void setSeperatorStep( int )

		void setColorEmpty( const QColor & color );
		void setColorFull( const QColor & color );
		void setColorFrame( const QColor & color );

		/**
		 * Über diese Funktion wird eine Liste der erlaubten Werte gesetzt.
		 **/
		void setAllowedValues( QList<int> * );
		/**
		 * Über diese Funktion wird eine Liste der verbotenen Werte gesetzt.
		 **/
		void setForbiddenValues( QList<int> * );
		/**
		 * Es wird ein zusätzlicher Wert erlaubt.
		 **/
		void addAllowedValue( int value );
		/**
		 * Es wird ein zusätzlicher Wert verboten.
		 **/
		void addForbiddenValue( int value );

	private slots:
		void resetMinimumSize( int );

	protected:
		void paintEvent( QPaintEvent *event );
		void mousePressEvent( QMouseEvent *event );
		//void mouseDoubleClickEvent(QMouseEvent *event);

	signals:
		// Dieses ignal wird immer ausgesandt, wenn ein Wert angegeben wird, selbst wenn dieser keine Änderung hervorruft.
		void activated( int );
		// Dieses Signal wird nur ausgesandt, wenn der Benutzer den Wert der TraitBox verändert.
		void valueClicked( int );
		void valueChanged( int );
		void maximumChanged( int );
		void minimumChanged( int );
};

#endif
