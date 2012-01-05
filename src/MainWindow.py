# -*- coding: utf-8 -*-

"""
\file
\author Victor von Rhein <victor@caern.de>

\section License

Copyright (C) Victor von Rhein, 2011, 2012

This file is part of SoulCreator.

SoulCreator is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SoulCreator is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with SoulCreator.  If not, see <http://www.gnu.org/licenses/>.
"""




from __future__ import division, print_function

import sys
import os

from PySide.QtCore import Qt, QCoreApplication, QFile, QSize, QPoint, QByteArray
from PySide.QtGui import QMainWindow, QIcon, QMessageBox, QFileDialog, QPrinter, QFont, QFontDatabase

from src.GlobalState import GlobalState
from Error import ErrFileNotOpened, ErrXmlParsing, ErrXmlVersion, ErrSpeciesNotExisting
from Config import Config
from IO.Settings import Settings
from IO.ReadXmlTemplate import ReadXmlTemplate
from IO.ReadXmlCharacter import ReadXmlCharacter
from IO.WriteXmlCharacter import WriteXmlCharacter
from Storage.StorageCharacter import StorageCharacter
from Storage.StorageTemplate import StorageTemplate
from Calc.CalcAdvantages import CalcAdvantages
from Widgets.InfoWidget import InfoWidget
from Widgets.AttributeWidget import AttributeWidget
from Widgets.SkillWidget import SkillWidget
from Widgets.Specialties import Specialties
from Widgets.MeritWidget import MeritWidget
from Widgets.MoralityWidget import MoralityWidget
from Widgets.AdvantagesWidget import AdvantagesWidget
from Widgets.Dialogs.MessageBox import MessageBox
from Draw.DrawSheet import DrawSheet
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

		if GlobalState.isDebug:
			print("{} wurde im Debug-Modus aufgerufen.".format(Config.programName))

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

		self.ui.pushButton_next.clicked.connect(self.ui.selectWidget_select.selectNext)
		self.ui.pushButton_previous.clicked.connect(self.ui.selectWidget_select.selectPrevious)
		self.ui.selectWidget_select.currentRowChanged.connect(self.ui.stackedWidget_traits.setCurrentIndex)
		self.ui.selectWidget_select.currentRowChanged.connect(self.setTabButtonState)
	#connect( self.ui.stackedWidget_traits, SIGNAL( currentChanged( int ) ), self, SLOT( selectSelectorItem( int ) ) );

		self.populateUi()
		self.activate()
		self.reset()

	#connect( self.ui.stackedWidget_traits, SIGNAL( currentChanged( int ) ), self, SLOT( showCreationPoints( int ) ) );

	#connect( readCharacter, SIGNAL( oldVersion( QString, QString ) ), self, SLOT( raiseExceptionMessage( QString, QString ) ) );

	#connect( self.ui.actionSettings, SIGNAL( triggered() ), self, SLOT( showSettingsDialog() ) );
		self.ui.actionNew.triggered.connect(self.newCharacter)
		self.ui.actionOpen.triggered.connect(self.openCharacter)
		self.ui.actionSave.triggered.connect(self.saveCharacter)
		self.ui.actionExport.triggered.connect(self.exportCharacter)
		self.ui.actionPrint.triggered.connect(self.printCharacter)
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
		"""
		In dieser Funktion werden die Template-Daten aus den XML-Dateien ausgelesen und gespeichert, um damit zu einem späteren Zeitpunkt die GUI füllen zu können.
		"""
		
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
		"""
		Die Graphische Oberfläche wird bevölkert.
		"""
		
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
		morality = MoralityWidget( self.__storage, self.__character, self )
		#powers = new PowerWidget( self );
		#flaws = new FlawWidget( self );
		self.__advantages = AdvantagesWidget( self.__storage, self.__character, self )

		self.ui.layout_info.addWidget( info )
		self.ui.layout_attributes.addWidget( attributes )
		self.ui.layout_skills.addWidget( skills )
		self.ui.layout_specialties.addWidget( specialties )
		self.ui.layout_merits.addWidget( merits )
		self.ui.layout_morality.addWidget( morality )
		#ui.layout_powers.addWidget( powers );
		#ui.layout_flaws.addWidget( flaws );
		self.ui.layout_advantages.addWidget( self.__advantages )

		## Wenn sich der Name im InfoWidget ändert, soll sich auch die Titelzeile des Programms ändern
		info.nameChanged.connect(self.setTitle)

		#/**
		#* \todo Überprüfen, ob das wirklich eine so gute Idee ist, die Breite händisch festzulegen.
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
		QFontDatabase.addApplicationFont(":fonts/fonts/ArchitectsDaughter.ttf")
		QFontDatabase.addApplicationFont(":fonts/fonts/CloisterBlack.ttf")
		QFontDatabase.addApplicationFont(":fonts/fonts/HVD_Edding.otf")
		QFontDatabase.addApplicationFont(":fonts/fonts/Note_this.ttf")
		QFontDatabase.addApplicationFont(":fonts/fonts/Tangerine_Regular.ttf")
		QFontDatabase.addApplicationFont(":fonts/fonts/Tangerine_Bold.ttf")
		QFontDatabase.addApplicationFont(":fonts/fonts/Mutlu__Ornamental.ttf")
		QFontDatabase.addApplicationFont(":fonts/fonts/Blokletters-Balpen.ttf")


	def activate(self):
		"""
		Diese Funktion "aktiviert" SoulCreator. Hier werden beispielsweise Merits mit allen anderen Eigenschaften verknüpft, die in ihren Voraussetzungen vorkommen. und bei einem ändern dieser Eigenschaft, wird neu geprüft, ob der Merit verfügbar ist, oder nicht.
		"""

		# Merits müssen mit allen Eigenschaften verknüpft werden, die in ihrer Prerequisits-Eigenschaft vorkommen.
		typ = "Merit"
		categoriesMerits = self.__storage.categories(typ)
		for category in categoriesMerits:
			for merit in self.__character.traits[typ][category].values():
				if merit.hasPrerequisites:
					meritPrerequisites = merit.prerequisitesText[0]
					for item in Config.typs:
						categories = self.__storage.categories(item)
						for subitem in categories:
							for subsubitem in self.__character.traits[item][subitem].values():
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

		# Bei der Änderung gewisser Eigenschaften müssen die Advantages neu berechnet werden. Die Verknüpfung dazu werden hier festgelegt.
		calc = CalcAdvantages( self.__character, self )
		#Debug.debug(self.__character.traits[typ]["Mental"]["Resolve"].name)
		self.__character.ageChanged.connect(calc.calcSize)
		self.__character.traits["Merit"]["Physical"]["Giant"].valueChanged.connect(calc.calcSize)
		self.__character.traits["Attribute"]["Physical"]["Dexterity"].valueChanged.connect(calc.calcInitiative)
		self.__character.traits["Attribute"]["Social"]["Composure"].valueChanged.connect(calc.calcInitiative)
		self.__character.traits["Merit"]["Physical"]["Fast Reflexes"].valueChanged.connect(calc.calcInitiative)
		self.__character.traits["Attribute"]["Physical"]["Strength"].valueChanged.connect(calc.calcSpeed)
		self.__character.traits["Attribute"]["Physical"]["Dexterity"].valueChanged.connect(calc.calcSpeed)
		self.__character.traits["Merit"]["Physical"]["Fleet of Foot"].valueChanged.connect(calc.calcSpeed)
		self.__character.traits["Attribute"]["Mental"]["Wits"].valueChanged.connect(calc.calcDefense)
		self.__character.traits["Attribute"]["Physical"]["Dexterity"].valueChanged.connect(calc.calcDefense)
		self.__character.traits["Attribute"]["Physical"]["Stamina"].valueChanged.connect(calc.calcHealth)
		self.__character.traits["Attribute"]["Mental"]["Resolve"].valueChanged.connect(calc.calcWillpower)
		self.__character.traits["Attribute"]["Social"]["Composure"].valueChanged.connect(calc.calcWillpower)
		
		calc.sizeChanged.connect(self.__advantages.setSize)
		calc.initiativeChanged.connect(self.__advantages.setInitiative)
		calc.speedChanged.connect(self.__advantages.setSpeed)
		calc.defenseChanged.connect(self.__advantages.setDefense)
		calc.healthChanged.connect(self.__advantages.setHealth)
		calc.willpowerChanged.connect(self.__advantages.setWillpower)

		#creation = new Creation( self );
		#// Schreibe die übrigen Erschaffungspunkte
		#connect( creation, SIGNAL( pointsChanged() ), self, SLOT( showCreationPoints() ) );
		#connect( creation, SIGNAL( pointsDepleted( cv_AbstractTrait.Type ) ), self, SLOT( warnCreationPointsDepleted( cv_AbstractTrait.Type ) ) );
		#connect( creation, SIGNAL( pointsNegative( cv_AbstractTrait.Type ) ), self, SLOT( warnCreationPointsNegative( cv_AbstractTrait.Type ) ) );
		#connect( creation, SIGNAL( pointsPositive( cv_AbstractTrait.Type ) ), self, SLOT( warnCreationPointsPositive( cv_AbstractTrait.Type ) ) );


	def reset(self):
		self.__character.resetCharacter()
		# Direkt nach dem Start ist der Charkater natürlich nicht modifiziert.
		self.__character.setModified(False)

		# Wir wollen zu Beginn immer die Informationen sehen.
		self.ui.selectWidget_select.setCurrentRow(0)



#void MainWindow.showSettingsDialog() {
	"""
	Diese Funktion ruft den Konfigurationsdialog auf und sorgt dafür, daß die änderungen gespeichert oder verworfen werden.
	"""
	
	#SettingsDialog dialog;
	#if ( dialog.exec() ) {
		#// Ausführen der veränderten Einstellungen.
#// 		self.setFont(Config.windowFont);
	#}
#}

#void MainWindow.showCharacterTraits() {
	"""
	Werte des Charakters auf der Oberfläche anzeigen.
	"""
	
#}

#void MainWindow.showSkillSpecialties( bool sw, QString skillName, QList< cv_TraitDetail > specialtyList ) {
	"""
	Spezialisierungen einer Fertigkeit anzeigen.
	"""
	
#// 	qDebug() << Q_FUNC_INFO << "Zeige Spazialisierungen.";

	#specialties.clear();

	#if ( sw ) {
#// 		qDebug() << Q_FUNC_INFO << "Test Specialties";
		#specialties.setSkill( skillName );
		#specialties.setSpecialties( specialtyList );
	#}
#}

#void MainWindow.showBackround( cv_Species.SpeciesFlag spec ) {
	"""
	Für jede Spezies wird das passende Hintergrundbild angezeigt.
	"""
	
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


#void MainWindow.selectSelectorItem( int idx ) {
	"""
	Selektiert das zur aktuellen Seite der Eigenschaften zugehörige Symbol in der Auswahlleiste.
	"""
	
	#ui.selectWidget_select.setCurrentItem( self.ui.selectWidget_select.item( idx ) );
#}

	def setTabButtonState( self, index ):
		"""
		Enabled oder Disabled die Knöpfe, mit denen die Eigenschaften durchgeblättert werden können, je nachdem, ob es noch eine weitere Seite zu Blättern gibt.
		"""
		
		if ( index < self.ui.selectWidget_select.count() - 1 ):
			self.ui.pushButton_next.setEnabled( True )
		else:
			self.ui.pushButton_next.setEnabled( False )

		if ( index > 0 ):
			self.ui.pushButton_previous.setEnabled( True )
		else:
			self.ui.pushButton_previous.setEnabled( False )


#void MainWindow.showCreationPoints( int idx ) {
	"""
	Je nachdem, welches Tab gerade gezeigt wird, müssen die Erschaffungspunkte dargestellt oder versteckt werden.
	"""

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
	"""
	Zeigt die Anzahl der übrigen Punkte bei der Charaktererschaffung an.

	\todo Mit Wirkung versehen.
	"""

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
	"""
	Zeigt eine Warnung an, wenn alle Erschafungspunkte vergeben wurden.
	
	\note Die Schrift im Auswahl-Widget, mit welchem man die verschiedenen Seiten anwählen kann wird für diese Seite wieder zur Standardfarbe verändert.
	"""
	
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
	"""
	Zeigt eine Warnung an, wenn nicht alle Erschafungspunkte vergeben wurden.
	
	\note Die Schrift im Auswahl-Widget, mit welchem man die verschiedenen Seiten anwählen kann wird für diese Seite blau eingefärbt.
	"""
	
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
	"""
	Zeigt eine Warnung an, wenn zuviele Erschafungspunkte vergeben wurden.
	
	\note Die Schrift im Auswahl-Widget, mit welchem man die verschiedenen Seiten anwählen kann wird für diese Seite rot eingefärbt.
	"""
	
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
		"""
		Zeigt den Informationsdialog für dieses Programm an.
		"""
		
		aboutText = self.tr(
			"""
			<h1>{name}</h1>
			<h2>Version: {version}</h2>
			<p>Copyright (C) Victor von Rhein, 2011, 2012<br>
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
		"""
		Fügt den Inhalt des Arguments zum Fenstertitel hinzu.
		"""
		
		titleStr = u"{} {} ({})".format(Config.programName, Config.versionDetail(), name )
		if not name:
			titleStr = u"{} {}".format(Config.programName, Config.versionDetail() )
		self.setWindowTitle( titleStr )


	def newCharacter(self):
		"""
		Über diese Funktion wird der Dialog aufgerufen, um einen ganz neuen Charakter zu erstellen.
		"""
		
		# Warnen, wenn der vorherige Charakter noch nicht gespeichert wurde!
		if ( self.maybeSave() ):
			self.__character.resetCharacter()

			# Unmittelbar nach dem Laden ist der Charkter natürlich nicht mehr 'geändert'.
			self.__character.setModified( False )


	def openCharacter(self):
		"""
		Über diese Funktion wird der Dialog aufgerufen, um einen gespeicherten Charakter in das Programm laden zu können.
		"""
		
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

			if ( filePath[0] ):
				# Charakter wird erst gelöscht, wenn auch wirklich ein neuer Charkater geladen werden soll.
				self.__character.resetCharacter()

				f = QFile( filePath[0] )

				try:
					self.__readCharacter.read( f )
				except ErrXmlVersion as e:
					MessageBox.exception( self, e.message, e.description )
				except ErrXmlParsing as e:
					MessageBox.exception( self, e.message, e.description )
				except ErrFileNotOpened as e:
					MessageBox.exception( self, e.message, e.description )

				f.close()

				# Unmittelbar nach dem Laden ist der Charkter natürlich nicht mehr 'geändert'.
				self.__character.setModified( False )


	def saveCharacter(self):
		"""
		Über diese Funktion wird erst der Dialog aufgerufen zum Aussuchen des Speicherortes und danach dann das Schreiben des Charakters in eine XML-Datei eingeletiet.
		"""
		
		appPath = getPath()

		# Pfad zum Speicherverzeichnis
		savePath = "{}/{}".format(appPath, Config.saveDir)

		# Wenn Unterverzeichnis nicht existiert, erstelle es
		if not os.path.exists(savePath):
			os.makedirs(savePath)

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
	"""
	Diese Funktion verbirgt die Anzeige übernatürlicher Kräfte, wenn keine zur Verfügung stehen. Dadurch bleibt mehr Platz für die Merits.
	"""
	
	#if ( species == cv_Species.Human ) {
		#ui.selectWidget_select.item( 5 ).setFlags( Qt.NoItemFlags );;
	#} else {
		#ui.selectWidget_select.item( 5 ).setFlags( Qt.ItemIsEnabled | Qt.ItemIsSelectable );
	#}
#}


	def exportCharacter(self):
		"""
		Diese Funktion druckt den Charakter in ein PDF-Dokument.
		"""

		appPath = getPath()

		# Pfad zum Speicherverzeichnis
		savePath = "{}/{}".format(appPath, Config.saveDir)

		# Wenn Unterverzeichnis nicht existiert, erstelle es
		if not os.path.exists(savePath):
			os.makedirs(savePath)

		#filePath = QFileDialog.getSaveFileName( self, self.tr( "Export Character" ), "{}/untitled.pdf".format(savePath), self.tr( "Charactersheet (*.pdf)" ) )
		filePath = ["{}/untitled.pdf".format(savePath), ""]

		# Ohne diese Abfrage, würde der Druckauftrag auch bei einem angeblichen Abbrechen an den Drucker geschickt, aber wegen der Einstellungen als pdf etc. kommt ein seltsamer Ausruck heraus. War zumindest zu C++-Zeiten so.
		if ( filePath[0] ):
			printer = QPrinter()

			printer.setOutputFormat( QPrinter.PdfFormat )
			printer.setPaperSize( QPrinter.A4 )
			printer.setFullPage( True )
			printer.setOutputFileName( filePath[0] )

			drawSheet = DrawSheet( self.__storage, self.__character, printer, self )

			##connect( &drawSheet, SIGNAL( enforcedTraitLimits( cv_AbstractTrait.Type ) ), self, SLOT( messageEnforcedTraitLimits( cv_AbstractTrait.Type ) ) );

			try:
				drawSheet.print()
			except ErrSpeciesNotExisting as e:
				MessageBox.exception( self, e.message, e.description )


	def printCharacter(self):
		"""
		Druckt den angezeigten Charakter aus.
		"""

		Debug.debug("Jetzt würde ich drucken, wenn diese Funktion schon implementiert wäre.")
		#printer = QPrinter()
		#printDialog = QPrintDialog( printer, self )

		##// 	printer.setOutputFormat( QPrinter.PdfFormat );
		#printer.setPaperSize( QPrinter.A4 )
		##// 	printer.setOutputFileName( "print.pdf" );

		#if ( printDialog.exec_() == QDialog.Accepted ):
			#drawSheet = DrawSheet( self, printer )

			##connect( &drawSheet, SIGNAL( enforcedTraitLimits( cv_AbstractTrait.Type ) ), self, SLOT( messageEnforcedTraitLimits( cv_AbstractTrait.Type ) ) );

			##try {
				##drawSheet.print();
			##} except ( eSpeciesNotExisting &e ) {
				##MessageBox.exception( self, e.message(), e.description() );
			##}
		##}


	def writeSettings(self):
		"""
		Speichert die Konfiguration dieses Programms für den nächsten Aufruf.
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
		"""
		Fragt nach, ob die Änderungen am Charakter gespeichert werden sollen, ehe sie möglicherweise verloren gehen.
		
		Diese Frage tritt auf, wenn der dargestellte Charakter nicht gespeichert ist und ehe das Programm geschlossen werden oder einen neuen Charakter anlegen soll.
		"""
		
		
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
	"""
	Ausgabe einer Fehlernachricht.
	"""
	
	#MessageBox.warning( self, tr( "Warning" ), tr( "While opening the file the following problem arised:\n%1\n%2\nIt appears, that the self.__character will be importable, so the process will be continued." ).arg( message ).arg( description ) );
#}

#void MainWindow.messageEnforcedTraitLimits( cv_AbstractTrait.Type type ) {
	"""
	Zeigt eine Nachricht an, daß die Eigenschaftsanzahl das für den Charakterbogen gesetzte Limit übertrifft, und daß alle überzähligen Eigenschaften des mitgegebenen Typs ignoriert werden.
	"""
	
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
