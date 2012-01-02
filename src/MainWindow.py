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

import sys
import os

from PySide.QtCore import Qt, QCoreApplication, QFile, QSize, QPoint, QByteArray
from PySide.QtGui import QMainWindow, QIcon, QMessageBox, QFileDialog

from Error import ErrFileNotOpened, ErrXmlParsing, ErrXmlVersion
from Config import Config
from IO.Settings import Settings
from IO.ReadXmlTemplate import ReadXmlTemplate
from IO.ReadXmlCharacter import ReadXmlCharacter
from IO.WriteXmlCharacter import WriteXmlCharacter
from Storage.StorageCharacter import StorageCharacter
from Storage.StorageTemplate import StorageTemplate
from Widgets.Display.InfoWidget import InfoWidget
from Widgets.Display.AttributeWidget import AttributeWidget
from Widgets.Display.SkillWidget import SkillWidget
from Widgets.Display.MeritWidget import MeritWidget
from Widgets.Display.Specialties import Specialties
from Widgets.Dialogs.MessageBox import MessageBox
from Debug import Debug

from ui.ui_MainWindow import Ui_MainWindow




def getPath():
	"""
	Bestimmt den Pfad zu diesem Skript, unabhängig davon, wie es ausgeführt wird.
	"""

	# Bestimmt, ob diese Anwednung eine normale Python-Ausfürhung ist oder ob es sich um eine "Frozen Executable" handelt.
	if hasattr(sys,  'frozen'):
			# Es wird eine "Frozen Executable" ausgeführt.
			dir_path = os.path.dirname(sys.executable)
	elif '__file__' in locals():
			# Es wird ein normales py-Skript ausgeführt.
			dir_path = os.path.dirname(__file__)
	else:
			# Es wird von der Kommandozeile gestartet.
			dir_path = sys.path[0]
	return dir_path





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

		#QApplication.setStyle(new QGtkStyle(self));

		self.setWindowTitle( "" );
		self.setWindowIcon( QIcon( ":/icons/images/WoD.png" ) )

		self.__storage = StorageTemplate( self )
		self.storeTemplateData()
		self.__character = StorageCharacter(self.__storage)
		self.__readCharacter = ReadXmlCharacter(self.__character)
		self.__writeCharacter = WriteXmlCharacter(self.__character)

		self.ui.pushButton_next.clicked.connect(self.tabNext)
		self.ui.pushButton_previous.clicked.connect(self.tabPrevious)
		self.ui.selectWidget_select.currentRowChanged.connect(self.ui.stackedWidget_traits.setCurrentIndex)
	#connect( self.ui.stackedWidget_traits, SIGNAL( currentChanged( int ) ), self, SLOT( setTabButtonState( int ) ) );
	#connect( self.ui.stackedWidget_traits, SIGNAL( currentChanged( int ) ), self, SLOT( selectSelectorItem( int ) ) );

		self.populateUi()
		self.activate()

	#connect( self.ui.stackedWidget_traits, SIGNAL( currentChanged( int ) ), self, SLOT( showCreationPoints( int ) ) );

	#connect( readCharacter, SIGNAL( oldVersion( QString, QString ) ), self, SLOT( raiseExceptionMessage( QString, QString ) ) );

	#connect( self.ui.actionSettings, SIGNAL( triggered() ), self, SLOT( showSettingsDialog() ) );
		self.ui.actionNew.triggered.connect(self.newCharacter)
		self.ui.actionOpen.triggered.connect(self.openCharacter)
		self.ui.actionSave.triggered.connect(self.saveCharacter)
	#connect( self.ui.actionExport, SIGNAL( triggered() ), self, SLOT( exportCharacter() ) );
	#connect( self.ui.actionPrint, SIGNAL( triggered() ), self, SLOT( printCharacter() ) );
		self.ui.actionAbout.triggered.connect(self.aboutApp)

		# Laden der Konfiguration
		self.readSettings()


	def closeEvent( self, event ):
		if ( self.maybeSave() ):
			self.writeSettings()
			event.accept()
		else:
			event.ignore()


	def storeTemplateData(self):
		reader = ReadXmlTemplate(self.__storage)

		#connect( &reader, SIGNAL( oldVersion( QString, QString ) ), self, SLOT( raiseExceptionMessage( QString, QString ) ) );

		try:
			reader.read()
		except ErrXmlVersion as e:
			MessageBox.exception( self, e.message(), e.description() )
		except ErrXmlParsing as e:
			MessageBox.exception( self, e.message(), e.description() )
		except ErrFileNotOpened as e:
			MessageBox.exception( self, e.message(), e.description() )


	def populateUi(self):
		#// Funktioniert nicht richtig.
		#// 	// Bevor wir alles in der GUI anzeigen, wollen wir ersteinmal eine alphabetische Reihefolge garantieren.
		#// 	// Ich weiß nicht, ob das bei den Attributen so gut ist.
		#// 	storage.sortTraits();

		info = InfoWidget(self.__storage, self.__character, self)
		attributes = AttributeWidget( self.__storage, self.__character, self )
		skills = SkillWidget( self.__storage, self.__character, self )
		specialties = Specialties( self.__storage.traits["Skill"], self )
		#// Warnung: Merits müssen später erschaffen werden, da sie Voraussetzungen überprüfen und das zum Problem wird, wenn Eigenschaften in der Liste überprüft werden, die noch nicht existieren. Glaube ich zumindest.
		merits = MeritWidget( self.__storage, self.__character, self )
		#flaws = new FlawWidget( self );
		#morality = new MoralityWidget( self );
		#powers = new PowerWidget( self );
		#advantages = new AdvantagesWidget( self );

		self.ui.layout_info.addWidget( info )
		self.ui.layout_attributes.addWidget( attributes )
		self.ui.layout_skills.addWidget( skills )
		self.ui.layout_specialties.addWidget( specialties )
		self.ui.layout_merits.addWidget( merits )
		#ui.layout_morality.addWidget( morality );
		#ui.layout_powers.addWidget( powers );
		#ui.layout_flaws.addWidget( flaws );
		#ui.layout_advantages.addWidget( advantages );

		## Wenn sich der Name im InfoWidget ändert, soll sich auch die Titelzeile des Programms ändern
		info.nameChanged.connect(self.setTitle)

		#/**
		#* \todo Überprüfen, ob das wirklich eine so gute Idee ist, die Breite Händisch festzulegen.
		#**/
		#ui.frame_merits.setMinimumWidth( Config.traitListVertivalWidth );
		#ui.frame_merits.setMaximumWidth( self.ui.frame_merits.minimumWidth() );
		#ui.frame_powers.setMinimumWidth( Config.traitListVertivalWidth );
		#ui.frame_powers.setMaximumWidth( self.ui.frame_powers.minimumWidth() );
		#ui.frame_flaws.setMinimumWidth( Config.traitListVertivalWidth );
		#ui.frame_flaws.setMaximumWidth( self.ui.frame_powers.minimumWidth() );

		#// Zu Beginn soll immer das erste Tab angezeigt werden.
		#ui.stackedWidget_traits.setCurrentIndex( 1 );
		#ui.stackedWidget_traits.setCurrentIndex( 0 );

		# Die Spazialisierungen einer Fertigkeit sollen angezeigt werden.
		#connect( skills, SIGNAL( specialtiesClicked( bool, QString, QList< cv_TraitDetail > ) ), self, SLOT( showSkillSpecialties( bool, QString, QList< cv_TraitDetail > ) ) );
		skills.specialtiesActivated.connect(specialties.showSpecialties)

		#// Menschen haben keine übernatürlichen Kräfte, also zeige ich sie auch nicht an.
		#connect( self.__self.__character, SIGNAL( speciesChanged( cv_Species.SpeciesFlag ) ), self, SLOT( disablePowerItem( cv_Species.SpeciesFlag ) ) );

		#connect( self.__self.__character, SIGNAL( speciesChanged( cv_Species.SpeciesFlag ) ), self, SLOT( showBackround( cv_Species.SpeciesFlag ) ) );
	#}


	def activate(self):
		"""
		Diese Funktion "aktiviert" SoulCreator. Hier werden beispielsweise Merits mit allen anderen Eigenschaften verknüpft, die in ihren Voraussetzungen vorkommen. und bei einem ändern dieser Eigenschaft, wird neu geprüft, ob der Merit verfügbar ist, oder nicht.
		"""

		# Merits müssen mit allen Eigenschaften verknüpft werden, die in ihrer Prerequisits-Eigenschaft vorkommen.
		typ = "Merit"
		categoriesMerits = self.__storage.categories(typ)
		for category in categoriesMerits:
			for merit in self.__character.traits[typ][category]:
				if merit.hasPrerequisites:
					meritPrerequisites = merit.prerequisitesText[0]
					for item in Config.typs:
						categories = self.__storage.categories(item)
						for subitem in categories:
							for subsubitem in self.__character.traits[item][subitem]:
								# Überprüfen ob die Eigenschaft im Anforderungstext des Merits vorkommt.
								if subsubitem.name in meritPrerequisites:
									# Vor dem Fertigkeitsnamen darf kein anderes Wort außer "and", "or" und "(" stehen.
									idxA = meritPrerequisites.index(subsubitem.name)
									strBefore = meritPrerequisites[:idxA]
									strBefore = strBefore.rstrip()
									strBeforeList = strBefore.split(" ")
									if not strBeforeList[-1] or strBeforeList[-1] == u"and" or strBeforeList[-1] == u"or" or strBeforeList[-1] == u"(":
										# \todo Den Namen der Eigenschaft mit einem Zeiger auf diese Eigenschaft im Speicher ersetzen.
										# Die Eigenschaften in den Voraussetzungen mit dem Merit verbinden.
										#Debug.debug("Verbinde {} mit {}".format(subsubitem.name, merit.name))
										subsubitem.traitChanged.connect(merit.checkPrerequisites)
					# Es kann auch die Supereigenschaft als Voraussetzung vorkommen.
					if Config.powerstatIdentifier in meritPrerequisites:
						self.__character.powerstatChanged.connect(merit.checkPrerequisites)

		self.__character.resetCharacter()
		# Direkt nach dem Start ist der Charkater natürlich nicht modifiziert.
		self.__character.setModified(False)

		#creation = new Creation( self );
		#// Schreibe die übrigen Erschaffungspunkte
		#connect( creation, SIGNAL( pointsChanged() ), self, SLOT( showCreationPoints() ) );
		#connect( creation, SIGNAL( pointsDepleted( cv_AbstractTrait.Type ) ), self, SLOT( warnCreationPointsDepleted( cv_AbstractTrait.Type ) ) );
		#connect( creation, SIGNAL( pointsNegative( cv_AbstractTrait.Type ) ), self, SLOT( warnCreationPointsNegative( cv_AbstractTrait.Type ) ) );
		#connect( creation, SIGNAL( pointsPositive( cv_AbstractTrait.Type ) ), self, SLOT( warnCreationPointsPositive( cv_AbstractTrait.Type ) ) );

		#self.__character.setSpecies( cv_Species.Human );

		#// Um dafür zu sorgen, daß Merits ohne gültige Voraussetzungen disabled werden, muß ich einmal alle Werte ändern.
		#QList< Trait* >* list = self.__character.traits();
		#for ( int i = 0; i < list.count(); ++i ) {
			#int valueOld = self.__character.traits().at( i ).value();
			#list.at( i ).setValue( 10 );
			#list.at( i ).clearDetails();

			#// Eine Änderung der Eigenschaften sorgt dafür, daß sich die verfügbaren Erschaffungspunkte verändern.
			#if ( Creation.types().contains( list.at( i ).type() ) ) {
				#connect( list.at( i ), SIGNAL( traitChanged( Trait* ) ), creation, SLOT( calcPoints( Trait* ) ) );
			#}


			#// Löschen der Zeigerliste
			#list.at( i ).clearPrerequisitePtrs();

			#for ( int j = 0; j < list.count(); ++j ) {
				#// Erst müssen die Voraussetzungen übersetzt werden, so daß direkt die Adressen im String stehen.
				#list.at( i ).addPrerequisitePtrs( list.at( j ) );
			#}

			#// Danach verbinden wir die Signale, aber nur, wenn sie benötigt werden.
			#if ( !list.at( i ).prerequisitePtrs().isEmpty() ) {
	#// 			qDebug() << Q_FUNC_INFO << self.__character.traits2().at( i ).prerequisitPtrs();

				#for ( int j = 0; j < list.at( i ).prerequisitePtrs().count(); ++j ) {
					#connect( list.at( i ).prerequisitePtrs().at( j ), SIGNAL( traitChanged( Trait* ) ), list.at( i ), SLOT( checkPrerequisites( Trait* ) ) );
				#}
			#}

			#// Alten Wert wiederherstellen.
			#list.at( i ).setValue( valueOld );
		#}

		#// Nun wird einmal die Spezies umgestellt, damit ich nur die Merits angezeigt bekomme, die auch erlaubt sind.
		#self.__character.setSpecies( cv_Species.Human );

		#// Virtue und Vice müssen auch initial einmal festgelegt werden.
		#self.__character.setVirtue( storage.virtueNames( cv_Trait.Adult ).at( 0 ) );

		#self.__character.setVice( storage.viceNames( cv_Trait.Adult ).at( 0 ) );

		#// Das alles wurde nur getan, um die Berechnungen etc. zu initialisieren. Das stellt noch keinen Charakter dar, also muß auch nicht bedacht werden,d aß selbiger eigentlich schon geändert wurde.
		#self.__character.setModified( false );
	#}


#void MainWindow.showSettingsDialog() {
	#SettingsDialog dialog;
	#if ( dialog.exec() ) {
		#// Ausführen der veränderten Einstellungen.
#// 		self.setFont(Config.windowFont);
	#}
#}

#void MainWindow.showCharacterTraits() {
#}

#void MainWindow.showSkillSpecialties( bool sw, QString skillName, QList< cv_TraitDetail > specialtyList ) {
#// 	qDebug() << Q_FUNC_INFO << "Zeige Spazialisierungen.";

	#specialties.clear();

	#if ( sw ) {
#// 		qDebug() << Q_FUNC_INFO << "Test Specialties";
		#specialties.setSkill( skillName );
		#specialties.setSpecialties( specialtyList );
	#}
#}

#void MainWindow.showBackround( cv_Species.SpeciesFlag spec ) {
	#if ( spec == cv_Species.Changeling ) {
		#ui.widget_traits.setStyleSheet( "QWidget#widget_traits { background-image: url(:/background/images/Skull-Changeling-gray.png); background-repeat: no-repeat; background-position: center; background-attachment: fixed; }" );
	#} else if ( spec == cv_Species.Mage ) {
		#ui.widget_traits.setStyleSheet( "QWidget#widget_traits { background-image: url(:/background/images/Skull-Mage-gray.png); background-repeat: no-repeat; background-position: center; background-attachment: fixed; }" );
	#} else if ( spec == cv_Species.Vampire ) {
		#ui.widget_traits.setStyleSheet( "QWidget#widget_traits { background-image: url(:/background/images/Skull-Vampire-gray.png); background-repeat: no-repeat; background-position: center; background-attachment: fixed; }" );
	#} else if ( spec == cv_Species.Werewolf ) {
		#ui.widget_traits.setStyleSheet( "QWidget#widget_traits { background-image: url(:/background/images/Skull-Werewolf-gray.png); background-repeat: no-repeat; background-position: center; background-attachment: fixed; }" );
	#} else {
		#ui.widget_traits.setStyleSheet( "QWidget#widget_traits { background-image: url(:/background/images/Skull-Human-gray.png); background-repeat: no-repeat; background-position: center; background-attachment: fixed; }" );
	#}

#// 	for ( int i = 0; i < self.ui.stackedWidget_traits.count(); ++i ) {
#// 		ui.stackedWidget_traits.widget( i ).setObjectName( "stackedWidget_item" + QString.number( i ) );
#// 	}
#//
#// 	if ( spec == cv_Species.Changeling ) {
#// 		for ( int i = 0; i < self.ui.stackedWidget_traits.count(); ++i ) {
#// 			ui.stackedWidget_traits.widget( i ).setStyleSheet( "QWidget#stackedWidget_item" + QString.number( i ) + "{ background-image: url(:/skulls/images/Skull-Changeling-gray.png); background-repeat: no-repeat; background-position: center }" );
#// 		}
#// 	} else if ( spec == cv_Species.Mage ) {
#// 		for ( int i = 0; i < self.ui.stackedWidget_traits.count(); ++i ) {
#// 			ui.stackedWidget_traits.widget( i ).setStyleSheet( "QWidget#stackedWidget_item" + QString.number( i ) + "{ background-image: url(:/skulls/images/Skull-Mage-gray.png); background-repeat: no-repeat; background-position: center }" );
#// 		}
#// 	} else if ( spec == cv_Species.Vampire ) {
#// 		for ( int i = 0; i < self.ui.stackedWidget_traits.count(); ++i ) {
#// 			ui.stackedWidget_traits.widget( i ).setStyleSheet( "QWidget#stackedWidget_item" + QString.number( i ) + "{ background-image: url(:/skulls/images/Skull-Vampire-gray.png); background-repeat: no-repeat; background-position: center }" );
#// 		}
#// 	} else if ( spec == cv_Species.Werewolf ) {
#// 		for ( int i = 0; i < self.ui.stackedWidget_traits.count(); ++i ) {
#// 			ui.stackedWidget_traits.widget( i ).setStyleSheet( "QWidget#stackedWidget_item" + QString.number( i ) + "{ background-image: url(:/skulls/images/Skull-Werewolf-gray.png); background-repeat: no-repeat; background-position: center }" );
#// 		}
#// 	} else {
#// 		for ( int i = 0; i < self.ui.stackedWidget_traits.count(); ++i ) {
#// 			ui.stackedWidget_traits.widget( i ).setStyleSheet( "QWidget#stackedWidget_item" + QString.number( i ) + "{ background-image: url(:/skulls/images/Skull-Mortal-gray.png); background-repeat: no-repeat; background-position: center }" );
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


#void MainWindow.selectSelectorItem( int idx ) {
	#ui.selectWidget_select.setCurrentItem( self.ui.selectWidget_select.item( idx ) );
#}

#void MainWindow.setTabButtonState( int index ) {
	#if ( index < self.ui.stackedWidget_traits.count() - 1 ) {
		#ui.pushButton_next.setEnabled( true );
	#} else {
		#ui.pushButton_next.setEnabled( false );
	#}

	#if ( index > 0 ) {
		#ui.pushButton_previous.setEnabled( true );
	#} else {
		#ui.pushButton_previous.setEnabled( false );
	#}
#}

#void MainWindow.showCreationPoints( int idx ) {
	#ui.label_pointsLeft.setHidden( true );
#// 	ui.frame_creationPointsSpecialties.setHidden( true );

	#if ( idx == 1 || idx == 2 || idx == 3 || idx == 5 ) {
		#ui.label_pointsLeft.setHidden( false );

		#if ( idx == 1 ) {
			#ui.label_pointsLeft.setText( creation.pointsList().pointString( self.__character.species(), cv_AbstractTrait.Attribute ) );
		#} else if ( idx == 2 ) {
#// 			ui.frame_creationPointsSpecialties.setHidden( false );
			#ui.label_pointsLeft.setText( creation.pointsList().pointString( self.__character.species(), cv_AbstractTrait.Skill ) );
		#} else if ( idx == 3 ) {
			#ui.label_pointsLeft.setText( creation.pointsList().pointString( self.__character.species(), cv_AbstractTrait.Merit ) );
		#} else if ( idx == 5 ) {
			#ui.label_pointsLeft.setText( creation.pointsList().pointString( self.__character.species(), cv_AbstractTrait.Power ) );
		#}
	#}
#}

#void MainWindow.showCreationPoints() {
	#if ( self.ui.stackedWidget_traits.currentIndex() == 1 ) {
		#ui.label_pointsLeft.setText( creation.pointsList().pointString( self.__character.species(), cv_AbstractTrait.Attribute ) );
	#} else if ( self.ui.stackedWidget_traits.currentIndex() == 2 ) {
		#ui.label_pointsLeft.setText( creation.pointsList().pointString( self.__character.species(), cv_AbstractTrait.Skill ) );
	#} else if ( self.ui.stackedWidget_traits.currentIndex() == 3 ) {
		#ui.label_pointsLeft.setText( creation.pointsList().pointString( self.__character.species(), cv_AbstractTrait.Merit ) );
	#} else if ( self.ui.stackedWidget_traits.currentIndex() == 5 ) {
		#ui.label_pointsLeft.setText( creation.pointsList().pointString( self.__character.species(), cv_AbstractTrait.Power ) );
	#}
#}

#void MainWindow.warnCreationPointsDepleted( cv_AbstractTrait.Type type ) {
	#if ( type == cv_AbstractTrait.Attribute ) {
		#ui.selectWidget_select.item( 1 ).setForeground( QColor() );
	#} else if ( type == cv_AbstractTrait.Skill ) {
		#ui.selectWidget_select.item( 2 ).setForeground( QColor() );
	#} else if ( type == cv_AbstractTrait.Merit ) {
		#ui.selectWidget_select.item( 3 ).setForeground( QColor() );
	#} else if ( type == cv_AbstractTrait.Power ) {
		#ui.selectWidget_select.item( 5 ).setForeground( QColor() );
	#}
#}
#void MainWindow.warnCreationPointsPositive( cv_AbstractTrait.Type type ) {
	#if ( type == cv_AbstractTrait.Attribute ) {
		#ui.selectWidget_select.item( 1 ).setForeground( Config.pointsPositive );
	#} else if ( type == cv_AbstractTrait.Skill ) {
		#ui.selectWidget_select.item( 2 ).setForeground( Config.pointsPositive );
	#} else if ( type == cv_AbstractTrait.Merit ) {
		#ui.selectWidget_select.item( 3 ).setForeground( Config.pointsPositive );
	#} else if ( type == cv_AbstractTrait.Power ) {
		#ui.selectWidget_select.item( 5 ).setForeground( Config.pointsPositive );
	#}
#}
#void MainWindow.warnCreationPointsNegative( cv_AbstractTrait.Type type ) {
	#if ( type == cv_AbstractTrait.Attribute ) {
		#ui.selectWidget_select.item( 1 ).setForeground( Config.pointsNegative );
	#} else if ( type == cv_AbstractTrait.Skill ) {
		#ui.selectWidget_select.item( 2 ).setForeground( Config.pointsNegative );
	#} else if ( type == cv_AbstractTrait.Merit ) {
		#ui.selectWidget_select.item( 3 ).setForeground( Config.pointsNegative );
	#} else if ( type == cv_AbstractTrait.Power ) {
		#ui.selectWidget_select.item( 5 ).setForeground( Config.pointsNegative );
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
			<p>You should have received a copy of the GNU General Public License along with self program. If not, see <a>http://www.gnu.org/licenses/</a>.</p>
			<h2>World of Darkness</h2>
			<p>World of Darkness, Changeling: The Lost, Mage: The Awakening, Vampire: The Requiem, Werewolf: The Forsaken, White Wolf, the White Wolf-Logo and all referring terms and symbols are copyrighted by White Wolf Inc.</p>
			""".format(
				name=Config.programName,
				version=Config.version()
			)
		)

		QMessageBox.about(self, self.tr("About {}".format(Config.programName)), aboutText)


	def setTitle( self, name ):
		titleStr = u"{} {} ({})".format(Config.programName, Config.versionDetail(), name )
		if not name:
			titleStr = u"{} {}".format(Config.programName, Config.versionDetail() )
		self.setWindowTitle( titleStr )


	def newCharacter(self):
		# Warnen, wenn der vorherige Charakter noch nicht gespeichert wurde!
		if ( self.maybeSave() ):
			self.__character.resetCharacter()

			# Unmittelbar nach dem Laden ist der Charkter natürlich nicht mehr 'geändert'.
			self.__character.setModified( False )


	def openCharacter(self):
		# Warnen, wenn der vorherige Charakter noch nicht gespeichert wurde!
		if ( self.maybeSave() ):
			#Debug.debug("Open")
			
			appPath = getPath()

			# Pfad zum Speicherverzeichnis
			savePath = "{}/{}".format(appPath, Config.saveDir)

			# Wenn Unterverzeichnis nicht existiert, suche im Programmverzeichnis.
			if ( not os.path.exists( savePath ) ):
				savePath = appPath

			filePath = QFileDialog.getOpenFileName(
				self,
				self.tr( "Select Character File" ),
				savePath,
				self.tr( "WoD Characters (*.chr)" )
			)

			if ( filePath ):
				# Charakter wird erst gelöscht, wenn auch wirklich ein neuer Charkater geladen werden soll.
				self.__character.resetCharacter()

				f = QFile( filePath[0] )

				try:
					self.__readCharacter.read( f )
				except ErrXmlVersion as e:
					MessageBox.exception( self, e.message(), e.description() )
				except ErrXmlParsing as e:
					MessageBox.exception( self, e.message(), e.description() )
				except ErrFileNotOpened as e:
					MessageBox.exception( self, e.message(), e.description() )

				f.close()

				# Unmittelbar nach dem Laden ist der Charkter natürlich nicht mehr 'geändert'.
				self.__character.setModified( False )


	def saveCharacter(self):
		appPath = getPath()

		# Pfad zum Speicherverzeichnis
		savePath = "{}/{}".format(appPath, Config.saveDir)

		# Wenn Unterverzeichnis nicht existiert, erstelle es
		if not os.path.exists(savePath):
			os.makedirs(savePath)

		#try {
			#if ( !dir.mkdir( savePath ) ) {
				#if ( !QDir( savePath ).exists() ) {
					#throw eDirNotCreated( dir.absolutePath() );
				#}
			#}
		#} except ( eDirNotCreated &e ) {
			#MessageBox.exception( self, e.description(), e.message() );
		#}

		filePath = QFileDialog.getSaveFileName( self, self.tr( "Save Character" ), "{}/untitled.chr".format(savePath), self.tr( "WoD Characters (*.chr)" ) )

		#Debug.debug(filePath)

		# Nur Speichern, wenn ein Name eingegeben wurde.
		if filePath:
			f = QFile( filePath[0] )

			try:
				self.__writeCharacter.write( f )
			except ErrXmlVersion as e:
				MessageBox.exception( self, e.message(), e.description() )
			except ErrXmlParsing as e:
				MessageBox.exception( self, e.message(), e.description() )
			except ErrFileNotOpened as e:
				MessageBox.exception( self, e.message(), e.description() )

			f.close()

			# Unmittelbar nach dem Speichern ist der Charkter natürlich nicht mehr 'geändert'.
			self.__character.setModified( False )


#void MainWindow.disablePowerItem( cv_Species.SpeciesFlag species ) {
	#if ( species == cv_Species.Human ) {
		#ui.selectWidget_select.item( 5 ).setFlags( Qt.NoItemFlags );;
	#} else {
		#ui.selectWidget_select.item( 5 ).setFlags( Qt.ItemIsEnabled | Qt.ItemIsSelectable );
	#}
#}


#void MainWindow.exportCharacter() {
#// 	// Vorsicht, eine Abkürzung, die ich nur für das Testen verwenden sollte.
#// 	shortcut();
#// 	QString filePath = "/home/goliath/Dokumente/Programme/C++/SoulCreator/build/save/untitled.pdf";

	#QString appPath = QApplication.applicationDirPath();

	#// Pfad zum Speicherverzeichnis
	#QString savePath = appPath + "/" + Config.saveDir();

	#// Wenn Unterverzeichnis nicht existiert, erstelle es
	#QDir dir( appPath );

	#try {
		#if ( !dir.mkdir( savePath ) ) {
			#if ( !QDir( savePath ).exists() ) {
				#throw eDirNotCreated( dir.absolutePath() );
			#}
		#}
	#} except ( eDirNotCreated &e ) {
		#MessageBox.exception( self, e.description(), e.message() );
	#}

	#QString filePath = QFileDialog.getSaveFileName( self, tr( "Export Character" ), savePath + "/untitled.pdf", tr( "Charactersheet (*.pdf)" ) );

	#qDebug() << Q_FUNC_INFO << filePath;

	#// Ohne diese Abfrage, würde der Druckauftrag auch bei einem angeblichen Abbrechen an den Drucker geschickt, aber wegen der Einstellungen als pdf etc. kommt ein seltsamer Ausruck heraus.
	#if ( !filePath.isEmpty() ) {
		#QPrinter* 	printer = new QPrinter();

		#printer.setOutputFormat( QPrinter.PdfFormat );
		#printer.setPaperSize( QPrinter.A4 );
		#printer.setFullPage( true );
		#printer.setOutputFileName( filePath );

		#DrawSheet drawSheet( self, printer );

		#connect( &drawSheet, SIGNAL( enforcedTraitLimits( cv_AbstractTrait.Type ) ), self, SLOT( messageEnforcedTraitLimits( cv_AbstractTrait.Type ) ) );

		#try {
			#drawSheet.print();
		#} except ( eSpeciesNotExisting &e ) {
			#MessageBox.exception( self, e.message(), e.description() );
		#}

		#delete printer;
	#}
#}

#void MainWindow.printCharacter() {
	#QPrinter* printer = new QPrinter();
	#QPrintDialog printDialog( printer, self );

#// 	printer.setOutputFormat( QPrinter.PdfFormat );
	#printer.setPaperSize( QPrinter.A4 );
#// 	printer.setOutputFileName( "print.pdf" );

	#if ( printDialog.exec() == QDialog.Accepted ) {
		#DrawSheet drawSheet( self, printer );

		#connect( &drawSheet, SIGNAL( enforcedTraitLimits( cv_AbstractTrait.Type ) ), self, SLOT( messageEnforcedTraitLimits( cv_AbstractTrait.Type ) ) );

		#try {
			#drawSheet.print();
		#} except ( eSpeciesNotExisting &e ) {
			#MessageBox.exception( self, e.message(), e.description() );
		#}
	#}

	#delete printer;
#}


	def writeSettings(self):
		"""
		Speichert Größe und Position des Fensters in der Konfigurationsdatei.
		"""

		settings = Settings( "{}/{}".format(getPath(), Config.configFile ))

		settings.beginGroup( "MainWindow" )
		settings.setValue( "size", self.size() )
		settings.setValue( "pos", self.pos() )
		settings.setValue( "state", self.saveState() )
		settings.endGroup()

		#settings.beginGroup( "Config" );
		#// 	settings.setValue( "windowFont", Config.windowFont.family() );
		#settings.setValue( "exportFont", Config.exportFont.family() );
		#settings.endGroup();


	def readSettings(self):
		"""
		Liest die Einstellungen für das Programm aus der Konfigurationsdatei.
		"""

		appPath = getPath()
		settings = Settings( "{}/{}".format(appPath, Config.configFile))

		settings.beginGroup( "MainWindow" );
		self.resize( settings.value( "size", QSize( 900, 600 ) ) )
		self.move( settings.value( "pos", QPoint( 200, 200 ) ) )
		self.restoreState( QByteArray(settings.value( "state" )) )
		settings.endGroup()

		#settings.beginGroup( "Config" );
		#// 	Config.windowFont = QFont( settings.value( "windowFont" ).toString() );
		#Config.exportFont = QFont( settings.value( "exportFont" ).toString() );
		#settings.endGroup();

		#// 	// Nachdem die Einstellungen geladen wurden, müssen sie auch angewandt werden.
		#// 	setFont(Config.windowFont);


	def maybeSave(self):
		if ( self.__character.isModifed() ):
			ret = QMessageBox.warning(
				self, self.tr( "Application" ),
				self.tr( "The character has been modified.\nDo you want to save your changes?" ),
				QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel )

			if ( ret == QMessageBox.Save ):
				self.saveCharacter()
			elif ( ret == QMessageBox.Cancel ):
				return False

		return True


#void MainWindow.raiseExceptionMessage( QString message, QString description ) {
	#MessageBox.warning( self, tr( "Warning" ), tr( "While opening the file the following problem arised:\n%1\n%2\nIt appears, that the self.__character will be importable, so the process will be continued." ).arg( message ).arg( description ) );
#}

#void MainWindow.messageEnforcedTraitLimits( cv_AbstractTrait.Type type ) {
	#MessageBox.warning( self, tr( "Too many Traits" ), tr( "There are too many %1 to fit on page.\n Printing will be done without the exceeding number of traits." ).arg( cv_AbstractTrait.toString( type, true ) ) );
#}




#// void MainWindow.shortcut() {
#// 	QString filePath = "/home/goliath/Dokumente/Programme/C++/SoulCreator/build/save/untitled1.chr";
#//
#// 	if ( !filePath.isEmpty() ) {
#// 		QFile* file = new QFile( filePath );
#//
#// 		// Bevor ich die Werte lade, muß ich erst alle vorhandenen Werte auf 0 setzen.
#// 		setCharacterValues( 0 );
#//
#// 		try {
#// 			readCharacter.read( file );
#// 		} except ( eXmlVersion &e ) {
#// 			MessageBox.exception( self, e.message(), e.description() );
#// 		} except ( eXmlError &e ) {
#// 			MessageBox.exception( self, e.message(), e.description() );
#// 		} except ( eFileNotOpened &e ) {
#// 			MessageBox.exception( self, e.message(), e.description() );
#// 		}
#//
#// 		delete file;
#// 	}
#// }
