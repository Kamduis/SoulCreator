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

#ifndef SQUARES_H
#define SQUARES_H

#include <QColor>
#include <QList>
#include <QEvent>

#include <QWidget>

/**
 * @brief Darstellung von ankreuzbaren Quadraten.
 *
 * Ein einfacher ganzzahliger Wert wirden in Form angekreuzter Quadrate dargestellt. Die bis zum Maximalwert übrigen Quadrate sind nicht ausgefüllt.
 *
 * Wird das Widget disabled, wird der Alphakanal genutzt, um die Quadrate teilweise durchsichtig zu machen und sie so grau erscheinen zu lassen.
 */

class Squares : public QWidget {
		Q_OBJECT
		/**
		 * Bestimmt, ob das Widget vom Benutzer direkt verändert werden kann.
		 *
		 * \access readOnly(), setReadOnly()
		 **/
		Q_PROPERTY( bool readOnly READ readOnly WRITE setReadOnly )
		/**
		 * Speichert den aktuellen Wert des Widgets.
		 *
		 * Dieser Wert stellt die Zahl der ausgefüllten Quadrate dar. Die Gesamtzahl der dargestellten Quadrate ist in \ref maximum gespeichert.
		 *
		 * Soll value auf einen Wert gesetzt werden, der über dem Maximum liegt, wird er nur auf das Maximum gesetzt, soll er unter das Minimum gesetzt werden, wird er auf Minimum gesetzt.
		 *
		 * \access value(), setValue()
		 *
		 * \notifier valueChanged()
		 **/
		Q_PROPERTY( int value READ value WRITE setValue NOTIFY valueChanged )
		/**
		 * Speichert den Maximalwert des Widgets.
		 *
		 * Der Maximalwert bestimmt, wieviele Quadrate insgesamt angezeigt werden.
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
		 * Speichert die maximale Anzahl von Quadraten, welche in enie Zeile gezeichnet werden. Alle bis zum \ref maximum überzähligen Quadrate werden in eine neue Zeile gesetzt, welche natürlich wiederum bei Füllung dieser Zahl umgebrochen wird.
		 *
		 * \access columnMax(), setColumnMax()
		 *
		 * \notifier columnMaximumChanged()
		 **/
		Q_PROPERTY( int columnMax READ columnMax WRITE setColumnMax NOTIFY columnMaxChanged )
		/**
		 * Speichert die Füllfarbe der Quadrate.
		 *
		 * \access colorEmpty(), setColorEmpty()
		 **/
		Q_PROPERTY( QColor colorEmpty READ colorEmpty WRITE setColorEmpty )
		/**
		 * Speichert die Farbe des Rahmens der Quadrate.
		 *
		 * \access colorFrame(), setColorFrame()
		 **/
		Q_PROPERTY( QColor colorFrame READ colorFrame WRITE setColorFrame )

	public:
		Squares( QWidget *parent = 0 );
		/**
		 * Zerstört das Objekt und gibt alle zugeteilten Ressourcen wieder frei.
		 **/
		~Squares();

		bool readOnly() const;
		int value() const;
		int maximum() const;
		int minimum() const;
		int columnMax() const;
		QColor colorEmpty() const;
		QColor colorFrame() const;

	private:
		int v_minimumSizeY;
		bool v_readOnly;
		int v_value;
		int v_maximum;
		int v_minimum;
		int v_columnMax;

		QColor v_colorEmpty;
		QColor v_colorFrame;

	public slots:
		void setReadOnly( bool );
		void setValue( int );
		void setMaximum( int );
		void setMinimum( int );
		void setColumnMax( int value );

		void setColorEmpty( const QColor & color );
		void setColorFrame( const QColor & color );

	private slots:
		void resetMinimumSize();

	protected:
		void paintEvent( QPaintEvent *event );
		void mousePressEvent( QMouseEvent *event );
		void changeEvent( QEvent *event );

	signals:
		// Dieses Signal wird immer ausgesandt, wenn ein Wert angegeben wird, selbst wenn dieser keine Änderung hervorruft.
		void activated( int );
		// Dieses Signal wird nur ausgesandt, wenn der Benutzer den Wert der TraitBox verändert.
		void valueClicked( int );
		void valueChanged( int );
		void maximumChanged( int );
		void minimumChanged( int );
		void columnMaxChanged( int );
};

#endif
