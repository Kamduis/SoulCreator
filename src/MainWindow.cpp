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

	this->setWindowTitle( Config::name() + " " + Config::versionDetail() );
	this->setWindowIcon( QIcon( ":/images/images/WoD.png" ) );

	character = StorageCharacter::getInstance();
	storage = new StorageTemplate(this);
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
	delete storage;
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
	
	// Funktioniert nicht richtig.
// 	// Bevor wir alles in der GUI anzeigen, wollen wir ersteinmal eine alphabetische Reihefolge garantieren.
// 	// Ich weiß nicht, ob das bei den Attributen so gut ist.
// 	storage->sortTraits();
	
	info = new InfoWidget( this );
	// Diese beiden kann ich nicht im Konstruktor erstellen. Wahrscheinlich, weil dann die Template-Dateien noch nicht eingelesen sind und es folglich nichts auszufüllen gibt.
	attributes = new AttributeWidget( this );
	skills = new SkillWidget( this );
// 	merits = new ComboTraitWidget( this, cv_Trait::Merit );
	merits = new MeritWidget( this );
	advantages = new AdvantagesWidget( this );

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
	// Um dafür zu sorgen, daß Merits ohne gültige Voraussetzungen disabled werden, muß ich einmal alle Werte ändern.
	QList< cv_Trait::Type > types;
	types.append( cv_Trait::Attribute );
	types.append( cv_Trait::Skill );
	types.append( cv_Trait::Merit );

	QList< cv_Trait::Category > categoriesGeneral;
	categoriesGeneral.append( cv_Trait::Mental );
	categoriesGeneral.append( cv_Trait::Physical );
	categoriesGeneral.append( cv_Trait::Social );

	QList< cv_Trait::Category > categoriesMerits = categoriesGeneral;
	categoriesMerits.append( cv_Trait::Item );
	categoriesMerits.append( cv_Trait::FightingStyle );
	categoriesMerits.append( cv_Trait::DebateStyle );
	categoriesMerits.append( cv_Trait::ShadowRealm );
	categoriesMerits.append( cv_Trait::PsychicPhenomena );
	categoriesMerits.append( cv_Trait::Species );


	QList< cv_Trait::Category > categories;

	for ( int i = 0; i < types.count();i++ ) {

		// Merits haben zusätzliche Kategorien.
		if ( types.at( i ) == cv_Trait::Merit ) {
			categories = categoriesMerits;
		} else {
			categories = categoriesGeneral;
		}

		for ( int j = 0; j < categories.count(); j++ ) {
			for ( int k = 0; k < character->traits( types.at( i ), categories.at( j ) ).count(); k++ ) {
				cv_Trait trait = character->traits( types.at( i ), categories.at( j ) ).at( k );
				qDebug() << Q_FUNC_INFO << trait.name << trait.value;
				// Alten Wert speichern
				int valueOld = trait.value;
				// Verändern, damit er auch wirklich \emph{verändert} wurde
				trait.value = valueOld+1;
				// In den Speicher schicken.
				character->addTrait( trait );
				// Wieder auf alten Wert zurücksetzen.
				trait.value = valueOld;
				character->addTrait( trait );
			}
		}
	}

	// Nun wird einmal die Spezies umgestellt, damit ich nur die Merits angezeigt bekomme, die auch erlaubt sind.
	character->setSpecies(cv_Species::Changeling);
	character->setSpecies(cv_Species::Human);
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

