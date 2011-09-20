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

#include <QCloseEvent>
#include <QDir>
#include <QFile>
#include <QFileDialog>
#include <QPrintDialog>
#include <QMessageBox>
#include <QPrinter>
#include <QTimer>
#include <QDebug>

#include "IO/Settings.h"
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

	QCoreApplication::setOrganizationName( Config::organization );
	QCoreApplication::setApplicationName( Config::name() );
	QCoreApplication::setApplicationVersion( Config::version() );

	this->setWindowTitle( Config::name() + " " + Config::versionDetail() );
	this->setWindowIcon( QIcon( ":/icons/images/WoD.png" ) );

	// Hübsche Symbole
	ui->actionNew->setIcon( QIcon( ":/icons/images/actions/filenew.png" ) );
	ui->actionOpen->setIcon( QIcon( ":/icons/images/actions/fileopen.png" ) );
	ui->actionSave->setIcon( QIcon( ":/icons/images/actions/filesave.png" ) );
	ui->actionExport->setIcon( QIcon( ":/icons/images/actions/fileexport.png" ) );
	ui->actionPrint->setIcon( QIcon( ":/icons/images/actions/agt_print.png" ) );

	// Hier habe ich die Standardicons genommen, aber davon gibt es nur wenige und sie sehen nicht gut aus.
// 	ui->actionNew->setIcon( style()->standardIcon( QStyle::SP_FileIcon ) );
// 	ui->actionOpen->setIcon( style()->standardIcon( QStyle::SP_DirOpenIcon ) );
// 	ui->actionSave->setIcon( style()->standardIcon( QStyle::SP_DriveFDIcon ) );
// 	ui->actionExport->setIcon( style()->standardIcon( QStyle::SP_FileIcon ) );
// 	ui->actionPrint->setIcon( style()->standardIcon( QStyle::SP_FileIcon ) );

	settingsDialog = new SettingsDialog( this );
	character = StorageCharacter::getInstance();
	storage = new StorageTemplate( this );
	readCharacter = new ReadXmlCharacter();
	writeCharacter = new WriteXmlCharacter();
	specialties = new CharaSpecialties( this );


	connect( ui->pushButton_next, SIGNAL( clicked() ), this, SLOT( tabNext() ) );
	connect( ui->pushButton_previous, SIGNAL( clicked() ), this, SLOT( tabPrevious() ) );
	connect( ui->tabWidget, SIGNAL( currentChanged( int ) ), this, SLOT( setTabButtonState( int ) ) );

	initialize();

	connect( readCharacter, SIGNAL( oldVersion( QString, QString ) ), this, SLOT( raiseExceptionMessage( QString, QString ) ) );

	connect( ui->actionSettings, SIGNAL( triggered() ), this, SLOT( showConfigDialog() ) );
	connect( ui->actionNew, SIGNAL( triggered() ), this, SLOT( newCharacter() ) );
	connect( ui->actionOpen, SIGNAL( triggered() ), this, SLOT( openCharacter() ) );
	connect( ui->actionSave, SIGNAL( triggered() ), this, SLOT( saveCharacter() ) );
	connect( ui->actionExport, SIGNAL( triggered() ), this, SLOT( exportCharacter() ) );
	connect( ui->actionPrint, SIGNAL( triggered() ), this, SLOT( printCharacter() ) );
	connect( ui->actionAbout, SIGNAL( triggered() ), this, SLOT( aboutApp() ) );

	// Laden der Konfiguration
	readSettings();
}

MainWindow::~MainWindow() {
	delete specialties;
	delete advantages;
	delete flaws;
	delete powers;
	delete morality;
	delete merits;
	delete skills;
	delete attributes;
	delete info;
	delete writeCharacter;
	delete readCharacter;
	delete storage;

	// Ganz am Schluß lösche ich natürlich auch den Charakterspeicher, welcher ja als Singleton-Klasse realisiert wurde.
	character->destroy();

	delete ui;
}


void MainWindow::closeEvent( QCloseEvent *event ) {
	if ( maybeSave() ) {
		writeSettings();
		event->accept();
	} else {
		event->ignore();
	}
}


void MainWindow::initialize() {
	storeTemplateData();
	populateUi();
	activate();
}

void MainWindow::storeTemplateData() {
	ReadXmlTemplate reader;

	connect( &reader, SIGNAL( oldVersion( QString, QString ) ), this, SLOT( raiseExceptionMessage( QString, QString ) ) );

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
	merits = new MeritWidget( this );
	morality = new MoralityWidget( this );
	powers = new PowerWidget( this );
	flaws = new FlawWidget( this );
	advantages = new AdvantagesWidget( this );

	ui->layout_info->addWidget( info );
	ui->layout_attributes->addWidget( attributes );
	ui->layout_skills->addWidget( skills );
	ui->layout_merits->addWidget( merits );
	ui->layout_morality->addWidget( morality );
	ui->layout_powers->addWidget( powers );
	ui->layout_flaws->addWidget( flaws );
	ui->layout_specialties->addWidget( specialties );
	ui->layout_advantages->addWidget( advantages );

	// Zu Beginn soll immer das erste Tab angezeigt werden.
	ui->tabWidget->setCurrentIndex( 1 );
	ui->tabWidget->setCurrentIndex( 0 );

	// Die Spazialisierungen einer Fertigkeit sollen angezeigt werden.
	connect( skills, SIGNAL( specialtiesClicked( bool, QString, QList< cv_TraitDetail > ) ), this, SLOT( showSkillSpecialties( bool, QString, QList< cv_TraitDetail > ) ) );

	// Menschen haben keine übernatürlichen Kräfte, also zeige ich sie auch nicht an.
	connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( hidePowers( cv_Species::SpeciesFlag ) ) );
}

void MainWindow::showCharacterTraits() {
}

void MainWindow::showSkillSpecialties( bool sw, QString skillName, QList< cv_TraitDetail > specialtyList ) {
// 	qDebug() << Q_FUNC_INFO << "Zeige Spazialisierungen.";

	specialties->clear();

	if ( sw ) {
// 		qDebug() << Q_FUNC_INFO << "Test Specialties";
		specialties->setSkill( skillName );
		specialties->setSpecialties( specialtyList );
	}
}


void MainWindow::activate() {
	// Um dafür zu sorgen, daß Merits ohne gültige Voraussetzungen disabled werden, muß ich einmal alle Werte ändern.
	for ( int k = 0; k < character->traitsAll().count(); k++ ) {
		cv_Trait trait = character->traitsAll().at( k );
// 		qDebug() << Q_FUNC_INFO << "Verändere" << trait.name << trait.value;
		// Alten Wert speichern
		int valueOld = trait.value;
		// Verändern, damit er auch wirklich \emph{verändert} wurde
		trait.value = 10;
		// In den Speicher schicken.
		character->modifyTrait( trait );
		// Wieder auf alten Wert zurücksetzen.
		trait.value = valueOld;
		character->modifyTrait( trait );
	}

	// Nun wird einmal die Spezies umgestellt, damit ich nur die Merits angezeigt bekomme, die auch erlaubt sind.
	character->setSpecies( cv_Species::Changeling );
	character->setSpecies( cv_Species::Human );

	// Virtue und Vice müssen auch initial einmal festgelegt werden.
	character->setVirtue( storage->virtueNames( cv_Trait::Adult ).at( 0 ) );
	character->setVice( storage->viceNames( cv_Trait::Adult ).at( 0 ) );

	// Das alles wurde nur getan, um die Berechnungen etc. zu initialisieren. Das stellt noch keinen Charakter dar, also muß auch nicht bedacht werden,d aß selbiger eigentlich schon geändert wurde.
	character->setModified( false );
}


void MainWindow::showConfigDialog() {
	settingsDialog->exec();
}

void MainWindow::tabPrevious() {
	if ( ui->tabWidget->currentIndex() > 0 ) {
		ui->tabWidget->setCurrentIndex( ui->tabWidget->currentIndex() - 1 );

		if ( !ui->tabWidget->widget( ui->tabWidget->currentIndex() )->isEnabled() ) {
			if ( ui->tabWidget->currentIndex() > 0 ) {
				tabPrevious();
			} else {
				tabNext();
			}
		}
	}
}

void MainWindow::tabNext() {
	if ( ui->tabWidget->currentIndex() < ui->tabWidget->count() - 1 ) {
		ui->tabWidget->setCurrentIndex( ui->tabWidget->currentIndex() + 1 );

		if ( !ui->tabWidget->widget( ui->tabWidget->currentIndex() )->isEnabled() ) {
			if ( ui->tabWidget->currentIndex() < ui->tabWidget->count() - 1 ) {
				tabNext();
			} else {
				tabPrevious();
			}
		}
	}
}

void MainWindow::setTabButtonState( int index ) {
	if ( index < ui->tabWidget->count() - 1 ) {
		ui->pushButton_next->setEnabled( true );
	} else {
		ui->pushButton_next->setEnabled( false );
	}

	if ( index > 0 ) {
		ui->pushButton_previous->setEnabled( true );
	} else {
		ui->pushButton_previous->setEnabled( false );
	}
}


void MainWindow::aboutApp() {
	QString aboutText = tr( "<h1>%1</h1>" ).arg( Config::name() ) +
						tr( "<h2>Version: %1</h2>" ).arg( Config::version() ) +
						tr( "<p>Copyright (C) 2011 by Victor von Rhein<br>" ) +
						tr( "EMail: goliath@caern.de</p>" ) +
						tr( "<h2>GNU General Public License</h2>" ) +
						tr( "<p>This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.</p>" ) +
						tr( "<p>This program is distributed in the hope that it will be useful, but <i>without any warranty</i>; without even the implied warranty of <i>merchantability</i> or <i>fitness for a particular purpose</i>. See the GNU General Public License for more details.</p>" ) +
						tr( "<p>You should have received a copy of the GNU General Public License along with this program. If not, see <a>http://www.gnu.org/licenses/</a>.</p>" ) +
						tr( "<h2>World of Darkness</h2>" ) +
						tr( "<p>World of Darkness, Changeling: The Lost, Mage: The Awakening, Vampire: The Requiem, Werewolf: The Forsaken, White Wolf, the White Wolf-Logo and all referring terms and symbols are copyrighted by White Wolf Inc.</p>" );

	QMessageBox::about( this, tr( "About %1" ).arg( Config::name() ), aboutText );
}


void MainWindow::newCharacter() {
	// Warnen, wenn der vorherige Charakter noch nicht gespeichert wurde!

	character->resetCharacter();
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

		// Bevor ich die Werte lade, muß ich erst alle vorhandenen Werte auf 0 setzen.
		character->resetCharacter();

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

		// Unmittelbar nach dem Laden ist der Charkter natürlich nicht mehr 'geändert'.
		character->setModified( false );
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

		// Unmittelbar nach dem Speichern ist der Charkter natürlich nicht mehr 'geändert'.
		character->setModified( false );
	}
}



void MainWindow::hidePowers( cv_Species::SpeciesFlag species ) {
	if ( species == cv_Species::Human ) {
// 		ui->groupBox_powers->setHidden( true );
		ui->tabWidget->setTabEnabled( ui->tabWidget->indexOf( ui->tabWidgetItem_Powers ), false );
	} else {
// 		ui->groupBox_powers->setHidden( false );
		ui->tabWidget->setTabEnabled( ui->tabWidget->indexOf( ui->tabWidgetItem_Powers ), true );
	}
}


void MainWindow::exportCharacter() {
// 	// Vorsicht, eine Abkürzung, die ich nur für das Testen verwenden sollte.
// 	shortcut();
// 	QString filePath = "/home/goliath/Dokumente/Programme/C++/SoulCreator/build/save/untitled.pdf";

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

	QString filePath = QFileDialog::getSaveFileName( this, tr( "Export Character" ), savePath + "/untitled.pdf", tr( "Charactersheet (*.pdf)" ) );

	QPrinter* printer = new QPrinter();
	QPrintDialog printDialog( printer, this );

	printer->setOutputFormat( QPrinter::PdfFormat );
	printer->setPaperSize( QPrinter::A4 );
	printer->setFullPage( true );
	printer->setOutputFileName( filePath );

	DrawSheet drawSheet( this, printer );

	connect( &drawSheet, SIGNAL( enforcedTraitLimits( cv_Trait::Type ) ), this, SLOT( messageEnforcedTraitLimits( cv_Trait::Type ) ) );

	try {
		drawSheet.print();
	} catch ( eSpeciesNotExisting &e ) {
		MessageBox::exception( this, e.message(), e.description() );
	}

	delete printer;
}

void MainWindow::printCharacter() {
	QPrinter* printer = new QPrinter();
	QPrintDialog printDialog( printer, this );

// 	printer->setOutputFormat( QPrinter::PdfFormat );
	printer->setPaperSize( QPrinter::A4 );
// 	printer->setOutputFileName( "print.pdf" );

	if ( printDialog.exec() == QDialog::Accepted ) {
		DrawSheet drawSheet( this, printer );

		connect( &drawSheet, SIGNAL( enforcedTraitLimits( cv_Trait::Type ) ), this, SLOT( messageEnforcedTraitLimits( cv_Trait::Type ) ) );

		try {
			drawSheet.print();
		} catch ( eSpeciesNotExisting &e ) {
			MessageBox::exception( this, e.message(), e.description() );
		}
	}

	delete printer;
}


void MainWindow::writeSettings() {
	Settings settings( QApplication::applicationDirPath() + "/" + Config::configFile );

	settings.beginGroup( "MainWindow" );
	settings.setValue( "size", size() );
	settings.setValue( "pos", pos() );
	settings.endGroup();
	
	settings.beginGroup( "Config" );
	settings.setValue( "exportFont", Config::exportFont.family() );
	settings.endGroup();
}

void MainWindow::readSettings() {
	Settings settings( QApplication::applicationDirPath() + "/" + Config::configFile );

	settings.beginGroup( "MainWindow" );
	resize( settings.value( "size", QSize( 400, 400 ) ).toSize() );
	move( settings.value( "pos", QPoint( 200, 200 ) ).toPoint() );
	settings.endGroup();
	
	settings.beginGroup( "Config" );
	Config::exportFont = QFont( settings.value("exportFont").toString());
	settings.endGroup();
}


bool MainWindow::maybeSave() {
	if ( character->isModifed() ) {
		QMessageBox::StandardButton ret;
		ret = QMessageBox::warning( this, tr( "Application" ),
									tr( "The character has been modified.\n"
										"Do you want to save your changes?" ),
									QMessageBox::Save | QMessageBox::Discard | QMessageBox::Cancel );

		if ( ret == QMessageBox::Save ) {
			saveCharacter();
		} else if ( ret == QMessageBox::Cancel ) {
			return false;
		}
	}

	return true;
}


void MainWindow::raiseExceptionMessage( QString message, QString description ) {
	MessageBox::warning( this, tr( "Warning" ), tr( "While opening the file the following problem arised:\n%1\n%2\nIt appears, that the character will be importable, so the process will be continued." ).arg( message ).arg( description ) );
}

void MainWindow::messageEnforcedTraitLimits( cv_Trait::Type type ) {
	MessageBox::warning( this, tr( "Too many Traits" ), tr( "There are too many %1 to fit on page.\n Printing will be done without the exceeding number of traits." ).arg( cv_Trait::toString( type, true ) ) );
}




// void MainWindow::shortcut() {
// 	QString filePath = "/home/goliath/Dokumente/Programme/C++/SoulCreator/build/save/untitled1.chr";
//
// 	if ( !filePath.isEmpty() ) {
// 		QFile* file = new QFile( filePath );
//
// 		// Bevor ich die Werte lade, muß ich erst alle vorhandenen Werte auf 0 setzen.
// 		setCharacterValues( 0 );
//
// 		try {
// 			readCharacter->read( file );
// 		} catch ( eXmlVersion &e ) {
// 			MessageBox::exception( this, e.message(), e.description() );
// 		} catch ( eXmlError &e ) {
// 			MessageBox::exception( this, e.message(), e.description() );
// 		} catch ( eFileNotOpened &e ) {
// 			MessageBox::exception( this, e.message(), e.description() );
// 		}
//
// 		delete file;
// 	}
// }
