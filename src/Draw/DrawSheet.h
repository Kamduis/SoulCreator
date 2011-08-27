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

#ifndef DRAWSHEET_H
#define DRAWSHEET_H

#include <QPrinter>
#include <QColor>

#include "../Storage/StorageCharacter.h"
#include "../Calc/CalcAdvantages.h"

#include <QObject>

/**
 * \brief Führt das Drucken des Charakters aus.
 *
 * Mit Hilfe dieser Klasse können die Charakterwerte auf Papier gebannt werden.
 **/

class DrawSheet : public QObject {
		Q_OBJECT

	public:
		/**
		 * Konstruktor
		 **/
		explicit DrawSheet( QObject* parent = 0 );
		/**
		 * Diesem Konstruktor kann sofort der Zeiger zum QPrinter übergeben werden.
		 **/
		DrawSheet( QObject* parent, QPrinter* printer );

	private:
		QPrinter* v_printer;
		StorageCharacter* character;
		CalcAdvantages* calcAdvantages;

		/**
		 * Der horizontale Radius eines Punkts auf dem Charakterbogen.
		 **/
		qreal v_dotDiameterH;
		/**
		 * Der vertikale Radius eines Punkts auf dem Charakterbogen.
		 **/
		qreal v_dotDiameterV;
		/**
		 * Die Schrifthöhe auf dem Charakterbogen.
		 **/
		qreal v_textHeight;
		/**
		 * Die Differenz in der Ausgangshöhe zwischen dem Schrifttext und den Punkten.
		 **/
		qreal v_textDotsHeightDifference;

		/**
		 * Die Farbe, mit welcher die Punkte auf dem Charakterbogen ausgefüllt werden.
		 **/
		QColor v_colorFill;

		/**
		 * Diese Funktion nutze ich, um in allen Konstruktoren dieseleben Abläufe durchzuführen.
		 **/
		void construct();

	public slots:
		/**
		 * Legt den QPrinter fest, mit dem diese Klasse auf den Drucker zeichnen wird.
		 **/
		void setPrinter( QPrinter* printer );
		/**
		 * Jetzt wird gezeichnet und gedruckt.
		 **/
		void print();

	private slots:
		/**
		 * Diese Funktion malt die Attributspunkte aus.
		 **/
		void drawAttributes( QPainter* painter,
							 qreal offsetH = 0 /** Horizontaler Abstand zwischen Bildkante und dem ersten Punkt des ersten Attributs. */,
							 qreal offsetV = 0 /** Vertikaler Abstand zwischen Bildkante und dem ersten Punkt des ersten Attributs. */,
							 qreal distanceH = 0 /** Horizontaler Abstand zwischen dem ersten Punkt einer Kategorie und dem ersten Punkt der nächsten Kategorie. */,
							 qreal distanceV = 0 /** Vertikaler Abstand zwischen den Attributen derselben Kategorie. */
						   );
		/**
		 * Diese Funktion malt die Fertigkeitspunkte aus und schreibt die Spezialisierungen.
		 **/
		void drawSkills( QPainter* painter,
							 qreal offsetH = 0 /** Horizontaler Abstand zwischen Bildkante und dem ersten Punkt des ersten Attributs. */,
							 qreal offsetV = 0 /** Vertikaler Abstand zwischen Bildkante und dem ersten Punkt des ersten Attributs. */,
							 qreal distanceV = 0 /** Vertikaler Abstand zwischen den Fertigkeiten derselben Kategorie. */,
							 qreal distanceVCat = 0 /** Vertikaler Abstand zwischen der ersten Fertigkeit einer Kategorie und der ersten Fertigkeit der nächsten Kategorie. */,
							 qreal textWidth = 0 /** Textbreite, der für die Spezialisierungen zur Verfügung steht. */
						   );
		/**
		 * Diese Funktion malt die Fertigkeitspunkte aus und schreibt die Spezialisierungen.
		 **/
		void drawMerits( QPainter* painter,
							 qreal offsetH = 0 /** Horizontaler Abstand zwischen Bildkante und dem ersten Punkt des ersten Attributs. */,
							 qreal offsetV = 0 /** Vertikaler Abstand zwischen Bildkante und dem ersten Punkt des ersten Attributs. */,
							 qreal distanceV = 0 /** Vertikaler Abstand zwischen den Fertigkeiten derselben Kategorie. */,
							 qreal textWidth = 0 /** Textbreite, der für die Benamung zur Verfügung steht. */
						   );
		/**
		 * Zeichne die berechneten Eigenschaften.
		 **/
		void drawAdvantages( QPainter* painter,
							 qreal offsetH = 0 /** Horizontaler Abstand zwischen Bildkante und der Beschriftungslinie. */,
							 qreal offsetV = 0 /** Vertikaler Abstand zwischen Bildkante und dem rechten Rand der Beschriftungslinie. */,
							 qreal distanceV = 0 /** Vertikaler Abstand zwischen den Eigenschaften. */,
							 qreal textWidth = 0 /** Textbreite, der zur Verfügung steht. */
						   );
		/**
		 * Zeichne die Willenskraft
		 **/
		void drawHealth( QPainter* painter,
							 qreal offsetH = 0 /** Horizontaler Abstand zwischen Bildkante und dem ersten Punkt. */,
							 qreal offsetV = 0 /** Vertikaler Abstand zwischen Bildkante und dem ersten Punkt. */,
							 qreal distanceH = 0 /** Horizontaler Abstand zwischen den Punkten. */,
							 qreal dotSizeFactor = 1 /** Der Faktor zwischen der normalen Punktgröße und der Punktgröße für die Gesundheit. */
						   );
		/**
		 * Zeichne die Willenskraft
		 **/
		void drawWillpower( QPainter* painter,
							 qreal offsetH = 0 /** Horizontaler Abstand zwischen Bildkante und dem ersten Punkt. */,
							 qreal offsetV = 0 /** Vertikaler Abstand zwischen Bildkante und dem ersten Punkt. */,
							 qreal distanceH = 0 /** Horizontaler Abstand zwischen den Punkten. */,
							 qreal dotSizeFactor = 1 /** Der Faktor zwischen der normalen Punktgröße und der Punktgröße für die Willenskraft. */
						   );
		/**
		 * Zeichne die Moral.
		 *
		 * \note Man bedenke, daß der \emph{erste} Punkte bei der Moral der unterste Punkt ist.
		 **/
		void drawMorality( QPainter* painter,
							 qreal offsetH = 0 /** Horizontaler Abstand zwischen Bildkante und dem ersten Punkt. */,
							 qreal offsetV = 0 /** Vertikaler Abstand zwischen Bildkante und dem ersten Punkt. */,
							 qreal distanceV = 0 /** Vertikaler Abstand zwischen den Punkten. */,
							 qreal dotSizeFactor = 1 /** Der Faktor zwischen der normalen Punktgröße und der Punktgröße für die Moral. */
						   );
};

#endif

