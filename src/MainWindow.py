# -*- coding: utf-8 -*-

"""
\file
\author Victor von Rhein <victor@caern.de>

\section License

Copyright (C) 2011 by Victor von Rhein

This file is part of SoulCreator.

SoulCreator is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SoulCreator is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with SoulCreator.  If not, see <http://www.gnu.org/licenses/>.
"""




from __future__ import division, print_function

from PySide.QtCore import Qt, QCoreApplication
from PySide.QtGui import QMainWindow, QIcon, QMessageBox

from Error import ErrFileNotOpened, ErrXmlParsing, ErrXmlVersion
from Config import Config
from IO.ReadXmlTemplate import ReadXmlTemplate
from Storage.StorageCharacter import StorageCharacter
from Widgets.Display.InfoWidget import InfoWidget

from ui.ui_MainWindow import Ui_MainWindow





class MainWindow(QMainWindow):
	"""
	@brief Das Hauptfenster der Anwendung.

	Hier werden die Widgets präsentiert und die hier laufen die Verbindungen zwischen den einzelnen Objekten zusammen.

	\todo Die Information, daß manche Merits nur bei Charaktererschaffung gewählt werden können, in das Programm einbinden.

	\todo Beim Wechseln zwischen den Spezies eie Warnung ausgeben, wenn Powers und Merits gelöscht würden.

	\todo Bei den Werwölfen müssen die Kräfte, welche je nach Vorzeichen nicht erlaubt sind, ausgegraut werden.

	\todo Sonderkräfte der Spezies fehlen. Bei Werwölfen müssen z.B. noch die Gaben/Riten berücksichtigt werden.

	\todo Nutze eine qchecksum, um die Integrität der XML-DAteien zu überprüfen. Ist nicht ganz einfach, wenn ich das Ergebnis der checksum in der selben xml-Datei stehen haben möchte, die ich überprüfe. Aber somit merkt SoulCreator, wenn die gespeicherten Charaktere korrupt sind. Es dürfte am besten sein, sie trotzdem zu laden, aber eine Warnung auszugeben.

	\todo So könnte es gehen: Erzeuge die XML-Datei mit einem leeren Feld für die Checksumme. Dann berechne die Chacksumme für diese Datei und füge sie anschließend in das leere Feld ein. Beim Laden verfahre genau andersherum! Lade die DAtei, hole die Checksumme, erzeuge eine temporäre Datei, in der alles identisch ist, bis auf die Checksumme, deren Feld nun leer ist. Berechne die Checksumme auf diese temporäre Datei und vergleiche sie mit der zuvor gelesenen Checksumme. Tadaa!

	\todo Zwischen den Kategorien (bei Attributen zumindest) Vertikale Striche als optischen Trenner einfügen. Diese können ja auch als Bilder realisiert werden und je nach Spezies unterschiedlich sein (Dornen, Krallenspuren etc.).

	\todo Charaktererschaffung in Schritten und Erfahrungspunkte einbauen.

	\todo Waffen einbauen.

	\todo Charakterbeschreibung einbauen.

	\todo Benutzer sollen ihre eigenen Spezialisierungen, Merits etc. eintragen können. Dafür sollte ich ihnen eine eigene template-DAtei bereitstellen, i welche dann all diese Eigenschaften hineingeschrieben werden. Diese Datei wird gleichberechtigt ausgelesen wie die anderen, befindet sich jedoch nicht in der Ressource, sondern liegt als externe Datei vor.

	\todo Bonus-Attributspuntke bei Vampiren und Magier bzw. Bonus-Spezialisierung bei Werwölfen und Wechselbälgern beachten.

	\todo Kräfte alphabetisch sortieren oder in Kategorien unterteilen.

	\todo Damit beim Laden einer Datei eine Eigenschaft, welche eigentlich nicht zur Verfügung steht, keine Punkte hat, sollte nach dem Laden nochmal eine Kontrolle durchgeführt werden.

	\todo Die Widgets weiter aufteilen in Main-Widgets, Tool-Widgets etc.

	\todo Damit die SVG-Grafiken unter Windows XP dargestellt werden ist auch QtXML4.dll erforderlich.

	\todo Von der Klasse Trait mehrere Unterklassen ableiten, je nach Typ der Eigenschaft. TraitAttribute hat leicht andere Eigenschaften als TraitSkill etc.? Das würde mehr objektorientiert aussehen. Und natürlich kann ich durch virtuelle Funktionen immer auch auch verschiedene Erben durch ihre Basisklasse Trait vergleichen, aussuchen usw.
	"""


	def __init__(self, parent=None):
		QMainWindow.__init__(self, parent)

		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		QCoreApplication.setOrganizationName( Config.organization )
		QCoreApplication.setApplicationName( Config.programName )
		QCoreApplication.setApplicationVersion( Config.version() )

		#QApplication::setStyle(new QGtkStyle(this));

		self.setWindowTitle( "" );
		self.setWindowIcon( QIcon( ":/icons/images/WoD.png" ) )

		self.__character = StorageCharacter()
	#storage = new StorageTemplate( this );
	#readCharacter = new ReadXmlCharacter();
	#writeCharacter = new WriteXmlCharacter();
	#specialties = new CharaSpecialties( this );

		self.ui.pushButton_next.clicked.connect(self.tabNext)
		self.ui.pushButton_previous.clicked.connect(self.tabPrevious)
		self.ui.selectWidget_select.currentRowChanged.connect(self.ui.stackedWidget_traits.setCurrentIndex)
	#connect( self.ui->stackedWidget_traits, SIGNAL( currentChanged( int ) ), this, SLOT( setTabButtonState( int ) ) );
	#connect( self.ui->stackedWidget_traits, SIGNAL( currentChanged( int ) ), this, SLOT( selectSelectorItem( int ) ) );

		self.storeTemplateData()
		self.populateUi()
	#activate();

	#connect( self.ui->stackedWidget_traits, SIGNAL( currentChanged( int ) ), this, SLOT( showCreationPoints( int ) ) );

	#connect( readCharacter, SIGNAL( oldVersion( QString, QString ) ), this, SLOT( raiseExceptionMessage( QString, QString ) ) );

	#connect( self.ui->actionSettings, SIGNAL( triggered() ), this, SLOT( showSettingsDialog() ) );
	#connect( self.ui->actionNew, SIGNAL( triggered() ), this, SLOT( newCharacter() ) );
	#connect( self.ui->actionOpen, SIGNAL( triggered() ), this, SLOT( openCharacter() ) );
	#connect( self.ui->actionSave, SIGNAL( triggered() ), this, SLOT( saveCharacter() ) );
	#connect( self.ui->actionExport, SIGNAL( triggered() ), this, SLOT( exportCharacter() ) );
	#connect( self.ui->actionPrint, SIGNAL( triggered() ), this, SLOT( printCharacter() ) );
		self.ui.actionAbout.triggered.connect(self.aboutApp)

	#connect( self.__self.__character, SIGNAL( nameChanged( QString ) ), this, SLOT( setTitle( QString ) ) );

	#// Laden der Konfiguration
	#readSettings();
#}

#MainWindow::~MainWindow() {
	#delete specialties;
	#delete advantages;
	#delete flaws;
	#delete powers;
	#delete morality;
	#delete merits;
	#delete skills;
	#delete attributes;
	#delete info;
	#delete writeCharacter;
	#delete readCharacter;
	#delete creation;
	#delete storage;

	#// Ganz am Schluß lösche ich natürlich auch den Charakterspeicher, welcher ja als Singleton-Klasse realisiert wurde.
	#self.__self.__character->destroy();

	#delete self.ui;
#}


#void MainWindow::closeEvent( QCloseEvent *event ) {
	#if ( maybeSave() ) {
		#writeSettings();
		#event->accept();
	#} else {
		#event->ignore();
	#}
#}


	def storeTemplateData(self):
		reader = ReadXmlTemplate()

		#connect( &reader, SIGNAL( oldVersion( QString, QString ) ), this, SLOT( raiseExceptionMessage( QString, QString ) ) );

		#try:
			#reader.read()
		#except ErrXmlVersion as e:
			#MessageBox.exception( this, e.message(), e.description() )
		#except ErrXmlParsing as e:
			#MessageBox.exception( this, e.message(), e.description() )
		#except ErrFileNotOpened as e:
			#MessageBox.exception( this, e.message(), e.description() )


	def populateUi(self):
		#// Funktioniert nicht richtig.
		#// 	// Bevor wir alles in der GUI anzeigen, wollen wir ersteinmal eine alphabetische Reihefolge garantieren.
		#// 	// Ich weiß nicht, ob das bei den Attributen so gut ist.
		#// 	storage->sortTraits();

		info = InfoWidget(self)
		#// Diese beiden kann ich nicht im Konstruktor erstellen. Wahrscheinlich, weil dann die Template-Dateien noch nicht eingelesen sind und es folglich nichts auszufüllen gibt.
		#attributes = new AttributeWidget( this );
		#skills = new SkillWidget( this );
		#// Warnung: Merits müssen später erschaffen werden, da sie Voraussetzungen überprüfen und das zum Problem wird, wenn Eigenschaften in der Liste überprüft werden, die noch nicht existieren. Glaube ich zumindest.
		#merits = new MeritWidget( this );
		#flaws = new FlawWidget( this );
		#morality = new MoralityWidget( this );
		#powers = new PowerWidget( this );
		#advantages = new AdvantagesWidget( this );

		self.ui.layout_info.addWidget( info )
		#ui->layout_attributes->addWidget( attributes );
		#ui->layout_skills->addWidget( skills );
		#ui->layout_merits->addWidget( merits );
		#ui->layout_morality->addWidget( morality );
		#ui->layout_powers->addWidget( powers );
		#ui->layout_flaws->addWidget( flaws );
		#ui->layout_specialties->addWidget( specialties );
		#ui->layout_advantages->addWidget( advantages );

		#/**
		#* \todo Überprüfen, ob das wirklich eine so gute Idee ist, die Breite Händisch festzulegen.
		#**/
		#ui->frame_merits->setMinimumWidth( Config::traitListVertivalWidth );
		#ui->frame_merits->setMaximumWidth( self.ui->frame_merits->minimumWidth() );
		#ui->frame_powers->setMinimumWidth( Config::traitListVertivalWidth );
		#ui->frame_powers->setMaximumWidth( self.ui->frame_powers->minimumWidth() );
		#ui->frame_flaws->setMinimumWidth( Config::traitListVertivalWidth );
		#ui->frame_flaws->setMaximumWidth( self.ui->frame_powers->minimumWidth() );

		#// Zu Beginn soll immer das erste Tab angezeigt werden.
		#ui->stackedWidget_traits->setCurrentIndex( 1 );
		#ui->stackedWidget_traits->setCurrentIndex( 0 );

		#// Die Spazialisierungen einer Fertigkeit sollen angezeigt werden.
		#connect( skills, SIGNAL( specialtiesClicked( bool, QString, QList< cv_TraitDetail > ) ), this, SLOT( showSkillSpecialties( bool, QString, QList< cv_TraitDetail > ) ) );

		#// Menschen haben keine übernatürlichen Kräfte, also zeige ich sie auch nicht an.
		#connect( self.__self.__character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( disablePowerItem( cv_Species::SpeciesFlag ) ) );

		#connect( self.__self.__character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( showBackround( cv_Species::SpeciesFlag ) ) );
	#}


#void MainWindow::activate() {
	#creation = new Creation( this );
	#// Schreibe die übrigen Erschaffungspunkte
	#connect( creation, SIGNAL( pointsChanged() ), this, SLOT( showCreationPoints() ) );
	#connect( creation, SIGNAL( pointsDepleted( cv_AbstractTrait::Type ) ), this, SLOT( warnCreationPointsDepleted( cv_AbstractTrait::Type ) ) );
	#connect( creation, SIGNAL( pointsNegative( cv_AbstractTrait::Type ) ), this, SLOT( warnCreationPointsNegative( cv_AbstractTrait::Type ) ) );
	#connect( creation, SIGNAL( pointsPositive( cv_AbstractTrait::Type ) ), this, SLOT( warnCreationPointsPositive( cv_AbstractTrait::Type ) ) );

	#self.__character->setSpecies( cv_Species::Human );

	#// Um dafür zu sorgen, daß Merits ohne gültige Voraussetzungen disabled werden, muß ich einmal alle Werte ändern.
	#QList< Trait* >* list = self.__character->traits();
	#for ( int i = 0; i < list->count(); ++i ) {
		#int valueOld = self.__character->traits()->at( i )->value();
		#list->at( i )->setValue( 10 );
		#list->at( i )->clearDetails();

		#// Eine Änderung der Eigenschaften sorgt dafür, daß sich die verfügbaren Erschaffungspunkte verändern.
		#if ( Creation::types().contains( list->at( i )->type() ) ) {
			#connect( list->at( i ), SIGNAL( traitChanged( Trait* ) ), creation, SLOT( calcPoints( Trait* ) ) );
		#}


		#// Löschen der Zeigerliste
		#list->at( i )->clearPrerequisitePtrs();

		#for ( int j = 0; j < list->count(); ++j ) {
			#// Erst müssen die Voraussetzungen übersetzt werden, so daß direkt die Adressen im String stehen.
			#list->at( i )->addPrerequisitePtrs( list->at( j ) );
		#}

		#// Danach verbinden wir die Signale, aber nur, wenn sie benötigt werden.
		#if ( !list->at( i )->prerequisitePtrs().isEmpty() ) {
#// 			qDebug() << Q_FUNC_INFO << self.__character->traits2()->at( i )->prerequisitPtrs();

			#for ( int j = 0; j < list->at( i )->prerequisitePtrs().count(); ++j ) {
				#connect( list->at( i )->prerequisitePtrs().at( j ), SIGNAL( traitChanged( Trait* ) ), list->at( i ), SLOT( checkPrerequisites( Trait* ) ) );
			#}
		#}

		#// Alten Wert wiederherstellen.
		#list->at( i )->setValue( valueOld );
	#}

	#// Nun wird einmal die Spezies umgestellt, damit ich nur die Merits angezeigt bekomme, die auch erlaubt sind.
	#self.__character->setSpecies( cv_Species::Human );

	#// Virtue und Vice müssen auch initial einmal festgelegt werden.
	#self.__character->setVirtue( storage->virtueNames( cv_Trait::Adult ).at( 0 ) );

	#self.__character->setVice( storage->viceNames( cv_Trait::Adult ).at( 0 ) );

	#// Das alles wurde nur getan, um die Berechnungen etc. zu initialisieren. Das stellt noch keinen Charakter dar, also muß auch nicht bedacht werden,d aß selbiger eigentlich schon geändert wurde.
	#self.__character->setModified( false );
#}


#void MainWindow::showSettingsDialog() {
	#SettingsDialog dialog;
	#if ( dialog.exec() ) {
		#// Ausführen der veränderten Einstellungen.
#// 		this->setFont(Config::windowFont);
	#}
#}

#void MainWindow::showCharacterTraits() {
#}

#void MainWindow::showSkillSpecialties( bool sw, QString skillName, QList< cv_TraitDetail > specialtyList ) {
#// 	qDebug() << Q_FUNC_INFO << "Zeige Spazialisierungen.";

	#specialties->clear();

	#if ( sw ) {
#// 		qDebug() << Q_FUNC_INFO << "Test Specialties";
		#specialties->setSkill( skillName );
		#specialties->setSpecialties( specialtyList );
	#}
#}

#void MainWindow::showBackround( cv_Species::SpeciesFlag spec ) {
	#if ( spec == cv_Species::Changeling ) {
		#ui->widget_traits->setStyleSheet( "QWidget#widget_traits { background-image: url(:/background/images/Skull-Changeling-gray.png); background-repeat: no-repeat; background-position: center; background-attachment: fixed; }" );
	#} else if ( spec == cv_Species::Mage ) {
		#ui->widget_traits->setStyleSheet( "QWidget#widget_traits { background-image: url(:/background/images/Skull-Mage-gray.png); background-repeat: no-repeat; background-position: center; background-attachment: fixed; }" );
	#} else if ( spec == cv_Species::Vampire ) {
		#ui->widget_traits->setStyleSheet( "QWidget#widget_traits { background-image: url(:/background/images/Skull-Vampire-gray.png); background-repeat: no-repeat; background-position: center; background-attachment: fixed; }" );
	#} else if ( spec == cv_Species::Werewolf ) {
		#ui->widget_traits->setStyleSheet( "QWidget#widget_traits { background-image: url(:/background/images/Skull-Werewolf-gray.png); background-repeat: no-repeat; background-position: center; background-attachment: fixed; }" );
	#} else {
		#ui->widget_traits->setStyleSheet( "QWidget#widget_traits { background-image: url(:/background/images/Skull-Human-gray.png); background-repeat: no-repeat; background-position: center; background-attachment: fixed; }" );
	#}

#// 	for ( int i = 0; i < self.ui->stackedWidget_traits->count(); ++i ) {
#// 		ui->stackedWidget_traits->widget( i )->setObjectName( "stackedWidget_item" + QString::number( i ) );
#// 	}
#//
#// 	if ( spec == cv_Species::Changeling ) {
#// 		for ( int i = 0; i < self.ui->stackedWidget_traits->count(); ++i ) {
#// 			ui->stackedWidget_traits->widget( i )->setStyleSheet( "QWidget#stackedWidget_item" + QString::number( i ) + "{ background-image: url(:/skulls/images/Skull-Changeling-gray.png); background-repeat: no-repeat; background-position: center }" );
#// 		}
#// 	} else if ( spec == cv_Species::Mage ) {
#// 		for ( int i = 0; i < self.ui->stackedWidget_traits->count(); ++i ) {
#// 			ui->stackedWidget_traits->widget( i )->setStyleSheet( "QWidget#stackedWidget_item" + QString::number( i ) + "{ background-image: url(:/skulls/images/Skull-Mage-gray.png); background-repeat: no-repeat; background-position: center }" );
#// 		}
#// 	} else if ( spec == cv_Species::Vampire ) {
#// 		for ( int i = 0; i < self.ui->stackedWidget_traits->count(); ++i ) {
#// 			ui->stackedWidget_traits->widget( i )->setStyleSheet( "QWidget#stackedWidget_item" + QString::number( i ) + "{ background-image: url(:/skulls/images/Skull-Vampire-gray.png); background-repeat: no-repeat; background-position: center }" );
#// 		}
#// 	} else if ( spec == cv_Species::Werewolf ) {
#// 		for ( int i = 0; i < self.ui->stackedWidget_traits->count(); ++i ) {
#// 			ui->stackedWidget_traits->widget( i )->setStyleSheet( "QWidget#stackedWidget_item" + QString::number( i ) + "{ background-image: url(:/skulls/images/Skull-Werewolf-gray.png); background-repeat: no-repeat; background-position: center }" );
#// 		}
#// 	} else {
#// 		for ( int i = 0; i < self.ui->stackedWidget_traits->count(); ++i ) {
#// 			ui->stackedWidget_traits->widget( i )->setStyleSheet( "QWidget#stackedWidget_item" + QString::number( i ) + "{ background-image: url(:/skulls/images/Skull-Mortal-gray.png); background-repeat: no-repeat; background-position: center }" );
#// 		}
#// 	}
#}


	def tabPrevious(self):
		if ( self.ui.stackedWidget_traits.currentIndex() > 0 ):
			self.ui.stackedWidget_traits.setCurrentIndex( self.ui.stackedWidget_traits.currentIndex() - 1 )

			#if ( not self.ui.selectWidget_select.item( self.ui.stackedWidget_traits.currentIndex() ).flags().testFlag(Qt.ItemIsEnabled) ):
			if ( not self.ui.selectWidget_select.item( self.ui.stackedWidget_traits.currentIndex() ).flags() & Qt.ItemIsEnabled ):
				if ( self.ui.stackedWidget_traits.currentIndex() > 0 ):
					tabPrevious()
				else:
					tabNext()


	def tabNext(self):
		if ( self.ui.stackedWidget_traits.currentIndex() < self.ui.stackedWidget_traits.count() - 1 ):
			self.ui.stackedWidget_traits.setCurrentIndex( self.ui.stackedWidget_traits.currentIndex() + 1 )

			# Ist die neue Seite disabled, müssen wir noch eine Seite weiter springen.
			#if ( not self.ui.selectWidget_select.item( self.ui.stackedWidget_traits.currentIndex() ).flags().testFlag( Qt.ItemIsEnabled ) ):
			if ( not self.ui.selectWidget_select.item( self.ui.stackedWidget_traits.currentIndex() ).flags() & Qt.ItemIsEnabled ):
				if ( self.ui.stackedWidget_traits.currentIndex() < self.ui.stackedWidget_traits.count() - 1 ):
					tabNext()
				else:
					tabPrevious()


#void MainWindow::selectSelectorItem( int idx ) {
	#ui->selectWidget_select->setCurrentItem( self.ui->selectWidget_select->item( idx ) );
#}

#void MainWindow::setTabButtonState( int index ) {
	#if ( index < self.ui->stackedWidget_traits->count() - 1 ) {
		#ui->pushButton_next->setEnabled( true );
	#} else {
		#ui->pushButton_next->setEnabled( false );
	#}

	#if ( index > 0 ) {
		#ui->pushButton_previous->setEnabled( true );
	#} else {
		#ui->pushButton_previous->setEnabled( false );
	#}
#}

#void MainWindow::showCreationPoints( int idx ) {
	#ui->label_pointsLeft->setHidden( true );
#// 	ui->frame_creationPointsSpecialties->setHidden( true );

	#if ( idx == 1 || idx == 2 || idx == 3 || idx == 5 ) {
		#ui->label_pointsLeft->setHidden( false );

		#if ( idx == 1 ) {
			#ui->label_pointsLeft->setText( creation->pointsList().pointString( self.__character->species(), cv_AbstractTrait::Attribute ) );
		#} else if ( idx == 2 ) {
#// 			ui->frame_creationPointsSpecialties->setHidden( false );
			#ui->label_pointsLeft->setText( creation->pointsList().pointString( self.__character->species(), cv_AbstractTrait::Skill ) );
		#} else if ( idx == 3 ) {
			#ui->label_pointsLeft->setText( creation->pointsList().pointString( self.__character->species(), cv_AbstractTrait::Merit ) );
		#} else if ( idx == 5 ) {
			#ui->label_pointsLeft->setText( creation->pointsList().pointString( self.__character->species(), cv_AbstractTrait::Power ) );
		#}
	#}
#}

#void MainWindow::showCreationPoints() {
	#if ( self.ui->stackedWidget_traits->currentIndex() == 1 ) {
		#ui->label_pointsLeft->setText( creation->pointsList().pointString( self.__character->species(), cv_AbstractTrait::Attribute ) );
	#} else if ( self.ui->stackedWidget_traits->currentIndex() == 2 ) {
		#ui->label_pointsLeft->setText( creation->pointsList().pointString( self.__character->species(), cv_AbstractTrait::Skill ) );
	#} else if ( self.ui->stackedWidget_traits->currentIndex() == 3 ) {
		#ui->label_pointsLeft->setText( creation->pointsList().pointString( self.__character->species(), cv_AbstractTrait::Merit ) );
	#} else if ( self.ui->stackedWidget_traits->currentIndex() == 5 ) {
		#ui->label_pointsLeft->setText( creation->pointsList().pointString( self.__character->species(), cv_AbstractTrait::Power ) );
	#}
#}

#void MainWindow::warnCreationPointsDepleted( cv_AbstractTrait::Type type ) {
	#if ( type == cv_AbstractTrait::Attribute ) {
		#ui->selectWidget_select->item( 1 )->setForeground( QColor() );
	#} else if ( type == cv_AbstractTrait::Skill ) {
		#ui->selectWidget_select->item( 2 )->setForeground( QColor() );
	#} else if ( type == cv_AbstractTrait::Merit ) {
		#ui->selectWidget_select->item( 3 )->setForeground( QColor() );
	#} else if ( type == cv_AbstractTrait::Power ) {
		#ui->selectWidget_select->item( 5 )->setForeground( QColor() );
	#}
#}
#void MainWindow::warnCreationPointsPositive( cv_AbstractTrait::Type type ) {
	#if ( type == cv_AbstractTrait::Attribute ) {
		#ui->selectWidget_select->item( 1 )->setForeground( Config::pointsPositive );
	#} else if ( type == cv_AbstractTrait::Skill ) {
		#ui->selectWidget_select->item( 2 )->setForeground( Config::pointsPositive );
	#} else if ( type == cv_AbstractTrait::Merit ) {
		#ui->selectWidget_select->item( 3 )->setForeground( Config::pointsPositive );
	#} else if ( type == cv_AbstractTrait::Power ) {
		#ui->selectWidget_select->item( 5 )->setForeground( Config::pointsPositive );
	#}
#}
#void MainWindow::warnCreationPointsNegative( cv_AbstractTrait::Type type ) {
	#if ( type == cv_AbstractTrait::Attribute ) {
		#ui->selectWidget_select->item( 1 )->setForeground( Config::pointsNegative );
	#} else if ( type == cv_AbstractTrait::Skill ) {
		#ui->selectWidget_select->item( 2 )->setForeground( Config::pointsNegative );
	#} else if ( type == cv_AbstractTrait::Merit ) {
		#ui->selectWidget_select->item( 3 )->setForeground( Config::pointsNegative );
	#} else if ( type == cv_AbstractTrait::Power ) {
		#ui->selectWidget_select->item( 5 )->setForeground( Config::pointsNegative );
	#}
#}


	def aboutApp(self):
		aboutText = self.tr(
			"""
			<h1>{name}</h1>
			<h2>Version: {version}</h2>
			<p>Copyright (C) 2011 by Victor von Rhein<br>
			EMail: victor@caern.de</p>
			<h2>GNU General Public License</h2>
			<p>This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.</p>
			<p>This program is distributed in the hope that it will be useful, but <i>without any warranty</i>; without even the implied warranty of <i>merchantability</i> or <i>fitness for a particular purpose</i>. See the GNU General Public License for more details.</p>
			<p>You should have received a copy of the GNU General Public License along with this program. If not, see <a>http://www.gnu.org/licenses/</a>.</p>
			<h2>World of Darkness</h2>
			<p>World of Darkness, Changeling: The Lost, Mage: The Awakening, Vampire: The Requiem, Werewolf: The Forsaken, White Wolf, the White Wolf-Logo and all referring terms and symbols are copyrighted by White Wolf Inc.</p>
			""".format(
				name=Config.programName,
				version=Config.version()
			)
		)

		QMessageBox.about(self, self.tr("About {}".format(Config.programName)), aboutText)

#void MainWindow::setTitle( QString txt ) {
	#if ( txt.isEmpty() ) {
		#this->setWindowTitle( Config::name() + " " + Config::versionDetail() );
	#} else {
		#this->setWindowTitle( Config::name() + " " + Config::versionDetail() + " (" + txt + ") " );
	#}
#}



#void MainWindow::newCharacter() {
	#// Warnen, wenn der vorherige Charakter noch nicht gespeichert wurde!
	#if ( maybeSave() ) {
		#self.__character->resetCharacter();

		#// Unmittelbar nach dem Laden ist der Charkter natürlich nicht mehr 'geändert'.
		#self.__character->setModified( false );
	#}
#}

#void MainWindow::openCharacter() {
	#// Warnen, wenn der vorherige Charakter noch nicht gespeichert wurde!
	#if ( maybeSave() ) {
		#QString appPath = QApplication::applicationDirPath();

		#// Pfad zum Speicherverzeichnis
		#QString savePath = appPath + "/" + Config::saveDir();

		#if ( !QDir( savePath ).exists() ) {
			#savePath = appPath;
		#}

		#QString filePath = QFileDialog::getOpenFileName( this, tr( "Select Character File" ), savePath, tr( "WoD Characters (*.chr)" ) );

		#if ( !filePath.isEmpty() ) {
			#// Charakter wird erst gelöscht, wenn auch wirklich ein neuer Charkater geladen werden soll.
			#self.__character->resetCharacter();

			#QFile* file = new QFile( filePath );

			#// Bevor ich die Werte lade, muß ich erst alle vorhandenen Werte auf 0 setzen.
			#self.__character->resetCharacter();

			#try {
				#readCharacter->read( file );
			#} catch ( eXmlVersion &e ) {
				#MessageBox::exception( this, e.message(), e.description() );
			#} catch ( eXmlError &e ) {
				#MessageBox::exception( this, e.message(), e.description() );
			#} catch ( eFileNotOpened &e ) {
				#MessageBox::exception( this, e.message(), e.description() );
			#}

			#delete file;

			#// Unmittelbar nach dem Laden ist der Charkter natürlich nicht mehr 'geändert'.
			#self.__character->setModified( false );
		#}
	#}
#}

#void MainWindow::saveCharacter() {
	#QString appPath = QApplication::applicationDirPath();

	#// Pfad zum Speicherverzeichnis
	#QString savePath = appPath + "/" + Config::saveDir();

	#// Wenn Unterverzeichnis nicht existiert, erstelle es
	#QDir dir( appPath );

	#try {
		#if ( !dir.mkdir( savePath ) ) {
			#if ( !QDir( savePath ).exists() ) {
				#throw eDirNotCreated( dir.absolutePath() );
			#}
		#}
	#} catch ( eDirNotCreated &e ) {
		#MessageBox::exception( this, e.description(), e.message() );
	#}

	#QString filePath = QFileDialog::getSaveFileName( this, tr( "Save Character" ), savePath + "/untitled.chr", tr( "WoD Characters (*.chr)" ) );

	#if ( !filePath.isEmpty() ) {
		#QFile* file = new QFile( filePath );

		#try {
			#writeCharacter->write( file );
		#} catch ( eXmlVersion &e ) {
			#MessageBox::exception( this, e.message(), e.description() );
		#} catch ( eXmlError &e ) {
			#MessageBox::exception( this, e.message(), e.description() );
		#} catch ( eFileNotOpened &e ) {
			#MessageBox::exception( this, e.message(), e.description() );
		#}

		#delete file;

		#// Unmittelbar nach dem Speichern ist der Charkter natürlich nicht mehr 'geändert'.
		#self.__character->setModified( false );
	#}
#}



#void MainWindow::disablePowerItem( cv_Species::SpeciesFlag species ) {
	#if ( species == cv_Species::Human ) {
		#ui->selectWidget_select->item( 5 )->setFlags( Qt::NoItemFlags );;
	#} else {
		#ui->selectWidget_select->item( 5 )->setFlags( Qt::ItemIsEnabled | Qt::ItemIsSelectable );
	#}
#}


#void MainWindow::exportCharacter() {
#// 	// Vorsicht, eine Abkürzung, die ich nur für das Testen verwenden sollte.
#// 	shortcut();
#// 	QString filePath = "/home/goliath/Dokumente/Programme/C++/SoulCreator/build/save/untitled.pdf";

	#QString appPath = QApplication::applicationDirPath();

	#// Pfad zum Speicherverzeichnis
	#QString savePath = appPath + "/" + Config::saveDir();

	#// Wenn Unterverzeichnis nicht existiert, erstelle es
	#QDir dir( appPath );

	#try {
		#if ( !dir.mkdir( savePath ) ) {
			#if ( !QDir( savePath ).exists() ) {
				#throw eDirNotCreated( dir.absolutePath() );
			#}
		#}
	#} catch ( eDirNotCreated &e ) {
		#MessageBox::exception( this, e.description(), e.message() );
	#}

	#QString filePath = QFileDialog::getSaveFileName( this, tr( "Export Character" ), savePath + "/untitled.pdf", tr( "Charactersheet (*.pdf)" ) );

	#qDebug() << Q_FUNC_INFO << filePath;

	#// Ohne diese Abfrage, würde der Druckauftrag auch bei einem angeblichen Abbrechen an den Drucker geschickt, aber wegen der Einstellungen als pdf etc. kommt ein seltsamer Ausruck heraus.
	#if ( !filePath.isEmpty() ) {
		#QPrinter* 	printer = new QPrinter();

		#printer->setOutputFormat( QPrinter::PdfFormat );
		#printer->setPaperSize( QPrinter::A4 );
		#printer->setFullPage( true );
		#printer->setOutputFileName( filePath );

		#DrawSheet drawSheet( this, printer );

		#connect( &drawSheet, SIGNAL( enforcedTraitLimits( cv_AbstractTrait::Type ) ), this, SLOT( messageEnforcedTraitLimits( cv_AbstractTrait::Type ) ) );

		#try {
			#drawSheet.print();
		#} catch ( eSpeciesNotExisting &e ) {
			#MessageBox::exception( this, e.message(), e.description() );
		#}

		#delete printer;
	#}
#}

#void MainWindow::printCharacter() {
	#QPrinter* printer = new QPrinter();
	#QPrintDialog printDialog( printer, this );

#// 	printer->setOutputFormat( QPrinter::PdfFormat );
	#printer->setPaperSize( QPrinter::A4 );
#// 	printer->setOutputFileName( "print.pdf" );

	#if ( printDialog.exec() == QDialog::Accepted ) {
		#DrawSheet drawSheet( this, printer );

		#connect( &drawSheet, SIGNAL( enforcedTraitLimits( cv_AbstractTrait::Type ) ), this, SLOT( messageEnforcedTraitLimits( cv_AbstractTrait::Type ) ) );

		#try {
			#drawSheet.print();
		#} catch ( eSpeciesNotExisting &e ) {
			#MessageBox::exception( this, e.message(), e.description() );
		#}
	#}

	#delete printer;
#}


#void MainWindow::writeSettings() {
	#Settings settings( QApplication::applicationDirPath() + "/" + Config::configFile );

	#settings.beginGroup( "MainWindow" );
	#settings.setValue( "size", size() );
	#settings.setValue( "pos", pos() );
	#settings.setValue( "state", saveState() );
	#settings.endGroup();

	#settings.beginGroup( "Config" );
#// 	settings.setValue( "windowFont", Config::windowFont.family() );
	#settings.setValue( "exportFont", Config::exportFont.family() );
	#settings.endGroup();
#}

#void MainWindow::readSettings() {
	#Settings settings( QApplication::applicationDirPath() + "/" + Config::configFile );

	#settings.beginGroup( "MainWindow" );
	#resize( settings.value( "size", QSize( 900, 600 ) ).toSize() );
	#move( settings.value( "pos", QPoint( 200, 200 ) ).toPoint() );
	#restoreState( settings.value( "state" ).toByteArray() );
	#settings.endGroup();

	#settings.beginGroup( "Config" );
#// 	Config::windowFont = QFont( settings.value( "windowFont" ).toString() );
	#Config::exportFont = QFont( settings.value( "exportFont" ).toString() );
	#settings.endGroup();

#// 	// Nachdem die Einstellungen geladen wurden, müssen sie auch angewandt werden.
#// 	setFont(Config::windowFont);
#}


#bool MainWindow::maybeSave() {
	#if ( self.__character->isModifed() ) {
		#QMessageBox::StandardButton ret;
		#ret = QMessageBox::warning( this, tr( "Application" ),
									#tr( "The self.__character has been modified.\n"
										#"Do you want to save your changes?" ),
									#QMessageBox::Save | QMessageBox::Discard | QMessageBox::Cancel );

		#if ( ret == QMessageBox::Save ) {
			#saveCharacter();
		#} else if ( ret == QMessageBox::Cancel ) {
			#return false;
		#}
	#}

	#return true;
#}


#void MainWindow::raiseExceptionMessage( QString message, QString description ) {
	#MessageBox::warning( this, tr( "Warning" ), tr( "While opening the file the following problem arised:\n%1\n%2\nIt appears, that the self.__character will be importable, so the process will be continued." ).arg( message ).arg( description ) );
#}

#void MainWindow::messageEnforcedTraitLimits( cv_AbstractTrait::Type type ) {
	#MessageBox::warning( this, tr( "Too many Traits" ), tr( "There are too many %1 to fit on page.\n Printing will be done without the exceeding number of traits." ).arg( cv_AbstractTrait::toString( type, true ) ) );
#}




#// void MainWindow::shortcut() {
#// 	QString filePath = "/home/goliath/Dokumente/Programme/C++/SoulCreator/build/save/untitled1.chr";
#//
#// 	if ( !filePath.isEmpty() ) {
#// 		QFile* file = new QFile( filePath );
#//
#// 		// Bevor ich die Werte lade, muß ich erst alle vorhandenen Werte auf 0 setzen.
#// 		setCharacterValues( 0 );
#//
#// 		try {
#// 			readCharacter->read( file );
#// 		} catch ( eXmlVersion &e ) {
#// 			MessageBox::exception( this, e.message(), e.description() );
#// 		} catch ( eXmlError &e ) {
#// 			MessageBox::exception( this, e.message(), e.description() );
#// 		} catch ( eFileNotOpened &e ) {
#// 			MessageBox::exception( this, e.message(), e.description() );
#// 		}
#//
#// 		delete file;
#// 	}
#// }
