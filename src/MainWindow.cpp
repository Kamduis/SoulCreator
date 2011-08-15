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

#include <QDir>
#include <QFile>
#include <QFileDialog>
#include <QMessageBox>
#include <QTimer>
#include <QDebug>

#include "Widgets/TraitLine.h"
#include "Widgets/Dialogs/MessageBox.h"
#include "IO/ReadXmlTemplate.h"
#include "Datatypes/cv_Trait.h"
#include "Exceptions/Exception.h"
#include "Config/Config.h"
#include "Storage/StorageCharacter.h"
#include "Storage/StorageTemplate.h"
#include "CMakeConfig.h"

#include "MainWindow.h"
#include "ui_MainWindow.h"

MainWindow::MainWindow( QWidget* parent ) : QMainWindow( parent ), ui( new Ui::MainWindow ) {
	ui->setupUi( this );

	this->setWindowTitle( Config::name() + " " + Config::version() );
	this->setWindowIcon( QIcon( ":/images/images/WoD.png" ) );

	readCharacter = new ReadXmlCharacter();
	writeCharacter = new WriteXmlCharacter();
	specialties = new CharaSpecialties( this );

	// Ich muß diesen Timer verwenden, das Programm in seinen EventLoop eintritt. Nun wird das Hauptfenster im Hintergrund dargestellt und über qApp->quit() kann das Programm nun auch sauber beendet werden. DIe Zeit, welche der Timer zählt ist nicht wichtig, muß aber natürlich sehr kurz sein.
// 	QTimer::singleShot( 200, this, SLOT( initialize() ) );
	initialize();

	connect( ui->actionOpen, SIGNAL( triggered( bool ) ), this, SLOT( openCharacter() ) );
	connect( ui->actionSave, SIGNAL( triggered( bool ) ), this, SLOT( saveCharacter() ) );
}

MainWindow::~MainWindow() {
	delete specialties;
	delete advantages;
	delete merits;
	delete skills;
	delete attributes;
	delete info;
	delete writeCharacter;
	delete readCharacter;
	delete ui;
}

void MainWindow::initialize() {
	storeTemplateData();
	populateUi();
	activate();
}

void MainWindow::storeTemplateData() {
	ReadXmlTemplate reader;

	try {
		reader.read();
	} catch ( eXmlVersion &e ) {
		MessageBox::exception( this, e.message(), e.description() );
	} catch ( eXmlError &e ) {
		MessageBox::exception( this, e.message(), e.description() );
	} catch ( eFileNotOpened &e ) {
		MessageBox::exception( this, e.message(), e.description() );
	} catch ( ... ) {
		qDebug() << Q_FUNC_INFO << "Exception!";
	}
}

void MainWindow::populateUi() {
	info = new InfoWidget( this );
	// Diese beiden kann ich nicht im Konstruktor erstellen. Wahrscheinlich, weil dann die Template-Dateien noch nicht eingelesen sind und es folglich nichts auszufüllen gibt.
	attributes = new AttributeWidget( this );
	skills = new SkillWidget( this );
// 	merits = new ComboTraitWidget( this, cv_Trait::Merit );
	merits = new MeritWidget( this );
	advantages = new AdvantagesWidget(this);

	ui->layout_info->addWidget( info );
	ui->layout_attributes->addWidget( attributes );
	ui->layout_skills->addWidget( skills );
	ui->layout_merits->addWidget( merits );
	ui->layout_specialties->addWidget( specialties );
	ui->layout_advantages->addWidget( advantages );

	// Die Spazialisierungen einer Fertigkeit sollen angezeigt werden.
	connect( skills, SIGNAL( specialtiesClicked( bool, QString, QList< cv_TraitDetail > ) ), this, SLOT( showSkillSpecialties( bool, QString, QList< cv_TraitDetail > ) ) );
}

void MainWindow::showCharacterTraits() {
}

void MainWindow::showSkillSpecialties( bool sw, QString skillName, QList< cv_TraitDetail > specialtyList ) {
	qDebug() << Q_FUNC_INFO << "Zeige Spazialisierungen.";

	specialties->clear();

	if ( sw ) {
		specialties->setSkill( skillName );
		specialties->setSpecialties( specialtyList );
	}
}


void MainWindow::activate() {
}


void MainWindow::openCharacter() {
	QString appPath = QApplication::applicationDirPath();

	// Pfad zum Speicherverzeichnis
	QString savePath = appPath + "/" + Config::saveDir();

	if ( !QDir( savePath ).exists() ) {
		savePath = appPath;
	}

	QString filePath = QFileDialog::getOpenFileName( this, tr( "Select Character File" ), savePath, tr( "WoD Characters (*.chr)" ) );

	if ( !filePath.isEmpty() ) {
		QFile* file = new QFile( filePath );

		try {
			readCharacter->read( file );
		} catch ( eXmlVersion &e ) {
			MessageBox::exception( this, e.message(), e.description() );
		} catch ( eXmlError &e ) {
			MessageBox::exception( this, e.message(), e.description() );
		} catch ( eFileNotOpened &e ) {
			MessageBox::exception( this, e.message(), e.description() );
		}

		delete file;
	}
}

void MainWindow::saveCharacter() {
	QString appPath = QApplication::applicationDirPath();

	// Pfad zum Speicherverzeichnis
	QString savePath = appPath + "/" + Config::saveDir();

	// Wenn Unterverzeichnis nicht existiert, erstelle es
	QDir dir( appPath );

	try {
		if ( !dir.mkdir( savePath ) ) {
			if ( !QDir( savePath ).exists() ) {
				throw eDirNotCreated( dir.absolutePath() );
			}
		}
	} catch ( eDirNotCreated &e ) {
		MessageBox::exception( this, e.description(), e.message() );
	}

	QString filePath = QFileDialog::getSaveFileName( this, tr( "Save Character" ), savePath + "/untitled.chr", tr( "WoD Characters (*.chr)" ) );

	if ( !filePath.isEmpty() ) {
		QFile* file = new QFile( filePath );

		try {
			writeCharacter->write( file );
		} catch ( eXmlVersion &e ) {
			MessageBox::exception( this, e.message(), e.description() );
		} catch ( eXmlError &e ) {
			MessageBox::exception( this, e.message(), e.description() );
		} catch ( eFileNotOpened &e ) {
			MessageBox::exception( this, e.message(), e.description() );
		}

		delete file;
	}
}

