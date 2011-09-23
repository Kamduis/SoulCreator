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

#ifndef MESSAGEBOX_H
#define MESSAGEBOX_H

#include <QString>
#include <QSqlError>

#include "Exceptions/Exception.h"

#include <QMessageBox>


/**
 * @brief Diese Klasse stellt verschiedene Standardnachrichtenfenster für das Programm dar.
 *
 * Über das Standardnachrichtenfenster können die Nachrichten über Ausnahmen bequem an den Nutzer weitergegeben werden. Unter anderem existiert auch eine Nachrichtenbox für die Ausnahmebehandlung.
 */

class MessageBox : public QMessageBox {
	public:
		/**
		 * Standardisierte Dialogbox für die Mitteilung einer Ausnahme an den Benutzer. Dient bislang Debug-Zwecken und sind noch keine normierten Fehlermeldungen.
		 *
		 * \todo Den Dialog so umwandeln, der er auch als Fehlermeldung einem Benutzer präsentiert werden kann und nicht nur als Debug-Hilfe dienen kann. Dies wird auch Änderungen in der \ref Exception -Klasse erfordern.
		 **/
		static StandardButton exception ( QWidget *parent /** Elternfenster dieses modalen Dialogs. */,
										  QString message /** Die kurze und informative Benachrichtigung an den Benutzer. */,
										  QString description /** Die ausführliche und optisch weniger eindrucksvoll dargestellte beschreibung des Fehlers. */ );
		/**
		 * Standardisierte Dialogbox für die Mitteilung einer Ausnahme an den Benutzer. Dient bislang Debug-Zwecken und sind noch keine normierten Fehlermeldungen.
		 *
		 * Dies ist eine überladene Methode der Funktion \ref MessageBox::exception( QWidget *parent, QString message, QString description ).
		 **/
		static StandardButton exception ( QWidget *parent /** Elternfenster dieses modalen Dialogs. */,
										  Exception error /** Die Excpetionklasse. */ );
		/**
		 * Standardisierte Dialogbox für die Mitteilung einer Ausnahme an den Benutzer. Dient bislang Debug-Zwecken und sind noch keine normierten Fehlermeldungen.
		 *
		 * Dies ist eine überladene Methode der Funktion \ref MessageBox::exception( QWidget *parent, QString message, QString description ).
		 **/
		static StandardButton exception ( QWidget *parent );

	private:
		/**
		 * Formatiert Nachricht und Beschreibung für den Dialog.
		 **/
		static QString formatText ( QString message, QString description );
		/**
		 * Formatiert die wichtigen Nachrichten für den Dialog.
		 **/
		static QString formatMessage ( QString message );
		/**
		 * Formatiert die ausfürhlichere Beschreibung für den Dialog.
		 **/
		static QString formatDescription ( QString description );
};

#endif

