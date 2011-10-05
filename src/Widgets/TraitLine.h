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

#ifndef TRAITLINE_H
#define TRAITLINE_H

#include <QStringList>
#include <QHBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QLineEdit>

#include "TraitDots.h"
#include "TraitSpecialties.h"

#include <QWidget>

/**
 * @brief Die grafische Darstellung einer einzigen Eigenschaft auf dem Charakterbogen.
 *
 * Die Simplen Eigenschaften (z.B. Attribute) bestehen nur aus Name und Wert. Bei kompliziertere Eigenschaften müssen noch Spezialisieren und andere Parameter beachtet werden.
 **/
class TraitLine : public QWidget {
		Q_OBJECT
		/**
		 * Der Name, der hier dargestellten Eigenschaft.
		 *
		 * \access name(), setName()
		 **/
		Q_PROPERTY( QString name READ name WRITE setName )
		/**
		 * Der beschreibende Text dieser Eigenschaft.
		 *
		 * \access text(), setText()
		 *
		 * \notifier textChanged()
		 **/
		Q_PROPERTY( QString text READ text WRITE setText NOTIFY textChanged )
		/**
		 * Der Wert, die hier dargestellten Eigenschaft.
		 *
		 * \access value(), setValue()
		 *
		 * \notifier valueChanged()
		 **/
		Q_PROPERTY( int value READ value WRITE setValue NOTIFY valueChanged )

	public:
		/**
		 * Dieser Konstruktor übergibt sämtliche Werte.
		 **/
// 		TraitLine(QWidget *parent = 0, cv_AbstractTrait::Type type = cv_AbstractTrait::TypeNo, cv_AbstractTrait::Category category = cv_AbstractTrait::CategoryNo, QString name = "", int value = 0);
		/**
		 * Simpler Konstruktor, der einige Werte übergeben kann.
		 **/
		TraitLine(QWidget *parent = 0, QString name = "", int value = 0);
		/**
		 * Zerstört das Objekt und gibt alle zugeteilten Ressourcen wieder frei.
		 **/
		~TraitLine();

		QString name() const;
		int value() const;
		QString text() const;
		int minimum() const;
		/**
		 * Einfacher Zugriff auf das Layout, damit ich es bei den Erben verändern kann.
		 **/
		QHBoxLayout* layout() const;
		/**
		 * Einfacher Zugriff auf das Layout, damit ich es bei den Erben verändern kann.
		 **/
		QLabel* labelName() const;

	private:
		QHBoxLayout *v_layout;
		QLabel *v_label_name;
		QPushButton *button;
		QLineEdit* lineEdit;
		TraitDots *traitDots;
		TraitSpecialties *specialties;

	public slots:
		void setName(QString text);
		void setValue(int value);
		/**
		 * Gibt alle Werte zurück, welche diese Zeile annehmen darf.
		 **/
		void setPossibleValues(QList<int> valueList);
		void setText(QString text);
		/**
		 * Legt die Beschriftung des Buttons fest.
		 **/
		void setButtonText(QString txt);
		/**
		 * Legt die Beschriftung des Buttons fest.
		 *
		 * \overload setButtonText(QString txt)
		 **/
		void setButtonText( int val );
		void setMinimum(int value);
		/**
		 * Mit dieser Methode verstecke ich die Liste der Spezialisierungen. Schließlich haben nur Fertigkeiten eine Notwendigkeit dafür.
		 **/
		void hideSpecialties(bool sw = true);
		/**
		 * Aktiviere oder Deaktiviere den Spezialisierungs-Knopf.
		 **/
		void setSpecialtyButtonChecked(bool sw = true);
		/**
		 * Mit dieser Methode verstecke ich die Textzeile, in welcher zusätzlicher Beschreibungstext eingegeben werden kann.
		 **/
		void hideDescription(bool sw = true);

	private slots:
		void enableSpecialties(int number);
//		void storeTrait();

	signals:
		void textChanged(QString text);
		void valueChanged ( int value );
		/**
		 * Der Knopf zum Anzeigen der Spazialisierungen wurde gedrückt.
		 **/
		void specialtiesClicked(bool state /** Gibt an, welchen Zusatand (checked | unchecked) der Knopf nun hat. */);
};

#endif
