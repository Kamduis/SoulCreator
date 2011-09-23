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

#include "Storage/StorageCharacter.h"
#include "Calc/CalcAdvantages.h"
#include "Datatypes/cv_Species.h"
#include "Datatypes/cv_Shape.h"

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

		/**
		 * Jetzt wird gezeichnet und gedruckt.
		 **/
		void print();

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

		/**
		 * Mit dieser Hilfsfunktion für drawMerits() werden die passenden Merits aus dem Charakter geholt.
		 *
		 * Diese globale Variable legt fest, ob bei einer Überschreitung der Eigenschaftshöchstwerte eine Ausnahme geworfen wird (false/Standardverhalten), oder die Grenzen einfach fest durchgesetzt werden.
		 **/
		QList< cv_Trait > getTraits( cv_Trait::Type type, int maxNumber, bool enforceTraitLimits = false /** Wird dieser Schalter auf true gesetzt (standardmäßig ist er false), werden die Grenzen für die maximale Anzahl durchgesetzt, auch wenn dadurch nicht alle Eigenschaften des Charakters auf Papier gebannt werden. */ );

	public slots:
		/**
		 * Legt den QPrinter fest, mit dem diese Klasse auf den Drucker zeichnen wird.
		 **/
		void setPrinter( QPrinter* printer );

	private slots:
		/**
		 * Diese Funktion Schreibt Namen, Virtue/Vice etc. in den Kopf des Charakterbogens.
		 **/
		void drawInfo( QPainter* painter,
							 qreal offsetH = 0 /** Horizontaler Abstand zwischen Bildkante und der rechten Kante des Platzes für den Namen. */,
							 qreal offsetV = 0 /** Vertikaler Abstand zwischen Bildkante und dem Platz für den Namen. */,
							 qreal distanceH = 0 /** Horizontaler Abstand zwischen den Zeilen. */,
							 qreal distanceV = 0 /** Vertikaler Abstand zwischen den Spalten. */,
				 			 qreal textWidth = 0 /** Textbreite. */
						   );
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
						 qreal offsetH = 0 /** Horizontaler Abstand zwischen Bildkante und dem ersten Punkt der ersten Eigenschaft. */,
						 qreal offsetV = 0 /** Vertikaler Abstand zwischen Bildkante und dem ersten Punkt der ersten Eigenschaft. */,
						 qreal distanceV = 0 /** Vertikaler Abstand zwischen den Fertigkeiten derselben Kategorie. */,
						 qreal distanceVCat = 0 /** Vertikaler Abstand zwischen der ersten Fertigkeit einer Kategorie und der ersten Fertigkeit der nächsten Kategorie. */,
						 qreal textWidth = 0 /** Textbreite, der für die Spezialisierungen zur Verfügung steht. */
					   );
		/**
		 * Diese Funktion malt die Fertigkeitspunkte aus und schreibt die Spezialisierungen.
		 *
		 * \warning Aufgrund der vorgefertigten Charakterbögen, können nur eine begrenzte Anzahl von Meritzs auf Papier gebannt werden.
		 *
		 * \exception
		 **/
		void drawMerits( QPainter* painter,
						 qreal offsetH = 0 /** Horizontaler Abstand zwischen Bildkante und dem ersten Punkt der ersten Eigenschaft. */,
						 qreal offsetV = 0 /** Vertikaler Abstand zwischen Bildkante und dem ersten Punkt der ersten Eigenschaft. */,
						 qreal distanceV = 0 /** Vertikaler Abstand zwischen den Fertigkeiten derselben Kategorie. */,
						 qreal textWidth = 0 /** Textbreite, der für die Benamung zur Verfügung steht. */,
						 int maxNumber = 0 /** Maximale Anzahl an Eigenschaften, die gezeichnet werden können. Wird diesem Argumetn '0' übergeben, werden alle Eigenschaften auf den Bogen gezeichnet. */
					   );
		/**
		 * Diese Funktion malt die Schwächen des Charakters
		 *
		 * \bug Die Merits halten sich nicht an die Linien im vorgefertigten Charakterbogen.
		 **/
		void drawFlaws( QPainter* painter,
						 qreal offsetH = 0 /** Horizontaler Abstand zwischen Bildkante und dem Textfeld. */,
						 qreal offsetV = 0 /** Vertikaler Abstand zwischen Bildkante und dem Textfeld. */,
						 qreal textWidth = 0 /** Textbreite, der für die Benamung zur Verfügung steht. */
					   );
		/**
		 * Zeichne die berechneten Eigenschaften.
		 *
		 * Werwölfe haben berechnete Eigenschaften für jede ihrer Gestalten, weswegen sie gesondert behanelt werden.
		 **/
		void drawAdvantages( QPainter* painter,
							 qreal offsetH = 0 /** Horizontaler Abstand zwischen Bildkante und der Beschriftungslinie. */,
							 qreal offsetV = 0 /** Vertikaler Abstand zwischen Bildkante und dem rechten Rand der Beschriftungslinie. */,
							 qreal distanceV = 0 /** Vertikaler Abstand zwischen den Eigenschaften. */,
							 qreal textWidth = 0 /** Textbreite, der zur Verfügung steht. */,
							 cv_Species::SpeciesFlag species = cv_Species::SpeciesNo /** Welcher Spezies der Charakter angehört. */,
							 qreal distanceH = 0 /** Abstand zwischen den unterschiedlichen Gestalten. */
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
						   qreal textWidth = 0 /** Textbreite, der für die Geistesstörungen zur Verfügung steht. */,
						   qreal dotSizeFactor = 1 /** Der Faktor zwischen der normalen Punktgröße und der Punktgröße für die Moral. */
						 );
		/**
		 * Zeichne die übernatürlichen Kräfte.
		 *
		 * Zeichne die übernatürlichen Kräfte für Magier und Werwölfe müssen gesondert behandelt werden. Die Arcana und Renown werden in zwei Spalten angeordnet und die zweite Spalte hat eine andere Richtung.
		 *
		 * \todo Es fehlen bei Werwölfen noch die Rites. Jetzt ist genug Platz da, also können sie auch bei den Powers eingetragen werden.
		 **/
		void drawPowers( QPainter* painter,
						 qreal offsetH = 0 /** Horizontaler Abstand zwischen Bildkante und dem ersten Punkt der ersten Eigenschaft. */,
						 qreal offsetV = 0 /** Vertikaler Abstand zwischen Bildkante und dem ersten Punkt der ersten Eigenschaft. */,
						 qreal distanceV = 0 /** Vertikaler Abstand zwischen den Kräften. */,
						 qreal textWidth = 0 /** Textbreite, der für die Benamung zur Verfügung steht. */,
						 int maxNumber = 0 /** Maximale Anzahl an Eigenschaften, die gezeichnet werden können. Wird diesem Argumetn '0' übergeben, werden alle Eigenschaften auf den Bogen gezeichnet. */,
						 cv_Species::SpeciesFlag species = cv_Species::SpeciesNo /** Welcher Spezies der Charakter angehört. */,
						 qreal distanceH = 0 /** Horizontaler Abstand zwischen den Kräften. */
					   );
		/**
		 * Zeichne die übernatürliche Eigenschaft (Wyrd, Gnosis etc.)
		 **/
		void drawSuper( QPainter* painter,
						qreal offsetH = 0 /** Horizontaler Abstand zwischen Bildkante und dem ersten Punkt. */,
						qreal offsetV = 0 /** Vertikaler Abstand zwischen Bildkante und dem ersten Punkt. */,
						qreal distanceH = 0 /** Horizontaler Abstand zwischen den Punkten. */,
						qreal dotSizeFactor = 1 /** Der Faktor zwischen der normalen Punktgröße und der hier genutzten Punktgröße. */
					  );
		/**
		 * Streiche die überzähligen Kästchen der Energie.
		 **/
		void drawFuelMax( QPainter* painter,
						  qreal offsetH = 0 /** Horizontaler Abstand zwischen Bildkante und rechter Kante des letzten Kästchens. */,
						  qreal offsetV = 0 /** Vertikaler Abstand zwischen Bildkante und Oberkante der zweiten Kästchenzeile. */,
						  qreal distanceH = 0 /** Der Abstand zwischen zwei Kästchen. */,
						  qreal widthpPerSquare = 0 /** Die Breite zwischen dem Anfang eines Kästchens zum Anfang des nächsten. */
						);
		/**
		 * Trage die maximale rate ein, mit welcher der Charakter seine Energie ausgeben kann.
		 **/
		void drawFuelPerTurn( QPainter* painter,
							  qreal offsetH = 0 /** Horizontaler Abstand zwischen Bildkante und Buchstabe. */,
							  qreal offsetV = 0 /** Vertikaler Abstand zwischen Bildkante und Buchstabe. */,
							  qreal distanceH = 0 /** Horizontzale Breite des Textes. */
							);

	signals:
		/**
		 * Dieses Signal wird ausgesandt, wann immer ein Eigenschaftstyp nicht auf die vorgegebene Charakterbogen-Matrix paßt.
		 *
		 * \warning Aktuell ist das Programm so beschaffen, daß dieses Signal ausgesandt wird der Druck aber fortgesetzt wird, wobei jedoch die überzähligen Eigenschaften ignoriert werden.
		 **/
		void enforcedTraitLimits( cv_Trait::Type type /** Dieses Argument teilt mit, bei der Bearbeitung welchen Eigenschaftstyps das Limit überschritten wurde. */ );
};

#endif

