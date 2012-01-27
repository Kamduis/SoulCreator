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

from PySide.QtCore import Qt, QCoreApplication, QFile, QSize, QPoint, QByteArray, QDir, Signal
from PySide.QtGui import QMainWindow, QApplication, QIcon, QPixmap, QMessageBox, QFileDialog, QDialog, QPrinter, QFont, QFontDatabase, QColor, QPrintDialog

from src.GlobalState import GlobalState
from src.Tools import PathTools
from Error import ErrFileNotOpened, ErrXmlParsing, ErrXmlVersion, ErrSpeciesNotExisting
from Config import Config
from IO.Settings import Settings
from IO.ReadXmlTemplate import ReadXmlTemplate
from IO.ReadXmlCharacter import ReadXmlCharacter
from IO.WriteXmlCharacter import WriteXmlCharacter
from Storage.StorageCharacter import StorageCharacter
from Storage.StorageTemplate import StorageTemplate
from Calc.CalcAdvantages import CalcAdvantages
from Calc.Creation import Creation
from Calc.ConnectPrerequisites import ConnectPrerequisites
from Widgets.InfoWidget import InfoWidget
from Widgets.TraitWidget import AttributeWidget, SkillWidget
from Widgets.PowerWidget import PowerWidget
from Widgets.SubPowerWidget import SubPowerWidget
from Widgets.Specialties import Specialties
from Widgets.MeritWidget import MeritWidget
from Widgets.FlawWidget import FlawWidget
from Widgets.MoralityWidget import MoralityWidget
from Widgets.AdvantagesWidget import AdvantagesWidget
from Widgets.ItemWidget import ItemWidget
from Widgets.Dialogs.SettingsDialog import SettingsDialog
from Widgets.Dialogs.MessageBox import MessageBox
from Draw.DrawSheet import DrawSheet
from Debug import Debug

from ui.ui_MainWindow import Ui_MainWindow




class MainWindow(QMainWindow):
	"""
	@brief Das Hauptfenster der Anwendung.

	Hier werden die Widgets präsentiert und die hier laufen die Verbindungen zwischen den einzelnen Objekten zusammen.

	\todo Die Information, daß manche Merits nur bei Charaktererschaffung gewählt werden können, in das Programm einbinden.

	\todo Bei den Werwölfen müssen die Kräfte, welche je nach Vorzeichen nicht erlaubt sind, ausgegraut werden.

	\todo Speicherdateien komprimieren.

	\todo Charaktererschaffung in Schritten und Erfahrungspunkte einbauen.

	\todo Kosten von Gegenständen berücksichtigen.

	\todo Benutzer sollen ihre eigenen Spezialisierungen, Merits etc. eintragen können. Dafür sollte ich ihnen eine eigene template-Datei bereitstellen, in welche dann all diese Eigenschaften hineingeschrieben werden. Diese Datei wird gleichberechtigt ausgelesen wie die anderen, befindet sich jedoch nicht in der Ressource, sondern liegt als externe Datei vor.

	\todo Bonus-Attributspuntke bei Vampiren und Magier bzw. Bonus-Spezialisierung bei Werwölfen und Wechselbälgern beachten.

	\todo Damit beim Laden einer Datei eine Eigenschaft, welche eigentlich nicht zur Verfügung steht, keine Punkte hat, sollte nach dem Laden nochmal eine Kontrolle durchgeführt werden.

	\todo SoulCreator sollte sich Virtues und Vices "merken", wenn das Alter so niedrig gewählt wird, daß auf Asset und Fault umgestellt wird, für den Fall, daß man den Charakter wieder älter macht.

	\todo Ändert man die Körpergröße über gewisse Schwell werte, sollte der Charaktergenerator Den Flaw/Merit Tiny bzw Giant vorschlagen. Und bei einem gewissen Wert einfach mal Unter- und Obergrenze festlegen.

	\todo Benutzer kann eigene Spezialisierungen festlegen.

	\todo Erschaffungspunkte durch einen Wizard ersetzen.

	\todo Merits sollten sich der Alterskategorie anpassen.

	\todo Items sollten sich der Alterskategorie anpassen.

	\todo "Leere" Felder auf dem Charakterbogen mit Leerzeilen zum händischen Ausfüllen versehen.

	\bug Beim Zurücksetzen des Charakters bleibt der Name bestehen.

	\bug Geburtsdatum nicht vor 1752 (QDate-Limit)! Durch python-Klasse ersetzen und eigenes Widget schreiben. ;_;

	\todo Changeling: Ich vermisse das Feld für Kith und beim Aussehen die Unterscheidung zwischen Mask und Mien

	\todo Changeling: Broken Mirror
	"""


	### Wird eine neue Seite angewählt, wird dieses Signal mit der Indexnummer der neu angezeigten Seite versandt.
	#pageChanged = Signal(int)


	def __init__(self, fileName=None, parent=None):
		QMainWindow.__init__(self, parent)

		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		if GlobalState.isDebug:
			print("{} wurde im Debug-Modus aufgerufen.".format(Config.programName))

		QCoreApplication.setOrganizationName( Config.organization )
		QCoreApplication.setApplicationName( Config.programName )
		QCoreApplication.setApplicationVersion( Config.version() )

		#Debug.debug(QApplication.style())

		self.setWindowTitle( "" )
		self.setWindowIcon( QIcon( ":/icons/images/WoD.png" ) )

		self.__storage = StorageTemplate( self )
		self.storeTemplateData()
		self.__character = StorageCharacter(self.__storage)
		## Später sollte ich mich für einen entscheiden!!
		self.__readCharacter = ReadXmlCharacter(self.__character)
		self.__writeCharacter = WriteXmlCharacter(self.__character)

		self.ui.pushButton_next.clicked.connect(self.ui.selectWidget_select.selectNext)
		self.ui.pushButton_previous.clicked.connect(self.ui.selectWidget_select.selectPrevious)
		self.ui.selectWidget_select.currentRowChanged.connect(self.ui.stackedWidget_traits.setCurrentIndex)
		self.ui.selectWidget_select.currentRowChanged.connect(self.setTabButtonState)
		#self.ui.selectWidget_select.currentRowChanged.connect(self.pageChanged.emit)

		self.__readCharacter.exceptionRaised.connect(self.showExceptionMessage)

		# Laden der Konfiguration
		self.readSettings()

		self.populateUi()
		self.activate()
		self.reset()

		self.ui.selectWidget_select.currentRowChanged.connect(self.showCreationPoints)

	#connect( readCharacter, SIGNAL( oldVersion( QString, QString ) ), self, SLOT( raiseExceptionMessage( QString, QString ) ) );

		self.ui.actionSettings.triggered.connect(self.showSettingsDialog)
		self.ui.actionNew.triggered.connect(self.newCharacter)
		self.ui.actionOpen.triggered.connect(self.openCharacter)
		self.ui.actionSave.triggered.connect(self.saveCharacter)
		self.ui.actionExport.triggered.connect(self.exportCharacter)
		self.ui.actionPrint.triggered.connect(self.printCharacter)
		self.ui.actionAbout.triggered.connect(self.aboutApp)

		## Wird ein Dateiname angegeben, soll dieser sofort geladen werden.
		if fileName:
			self.openCharacter(fileName)



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

		reader.exceptionRaised.connect(self.showExceptionMessage)

		try:
			reader.read()
		except ErrXmlVersion as e:
			MessageBox.exception( self, e.message, e.description )
		except ErrXmlParsing as e:
			MessageBox.exception( self, e.message, e.description )
		except ErrFileNotOpened as e:
			MessageBox.exception( self, e.message, e.description )


	def populateUi(self):
		"""
		Die Graphische Oberfläche wird bevölkert.
		"""

		## Die Icons werden hier definiert, da der Pfad zur ressourcen-DAtei nicht stimmt, wenn pyside-uic über die ui-Datei marschiert ist.
		self.ui.pushButton_previous.setIcon(QIcon(":/icons/images/actions/1leftarrow.png"))
		self.ui.pushButton_next.setIcon(QIcon(":/icons/images/actions/1rightarrow.png"))
		self.ui.actionNew.setIcon(QIcon(":/icons/images/actions/filenew.png"))
		self.ui.actionOpen.setIcon(QIcon(":/icons/images/actions/fileopen.png"))
		self.ui.actionSave.setIcon(QIcon(":/icons/images/actions/filesave.png"))
		self.ui.actionExport.setIcon(QIcon(":/icons/images/actions/fileexport.png"))
		self.ui.actionPrint.setIcon(QIcon(":/icons/images/actions/agt_print.png"))
		self.ui.actionSettings.setIcon(QIcon(":/icons/images/actions/exec.png"))
		self.ui.actionQuit.setIcon(QIcon(":/icons/images/actions/exit.png"))

		self.info = InfoWidget(self.__storage, self.__character, self)
		self.ui.layout_info.addWidget( self.info )

		attributes = AttributeWidget( self.__storage, self.__character, self )
		self.ui.layout_attributes.addWidget( attributes )

		skills = SkillWidget( self.__storage, self.__character, self )
		self.ui.layout_skills.addWidget( skills )

		specialties = Specialties( self.__storage.traits["Skill"], self )
		self.ui.layout_specialties.addWidget( specialties )

		merits = MeritWidget( self.__storage, self.__character, self )
		self.ui.layout_merits.addWidget( merits )

		morality = MoralityWidget( self.__storage, self.__character, self )
		self.ui.layout_morality.addWidget( morality )

		if "Power" in self.__storage.traits.keys():
			powers = PowerWidget( self.__storage, self.__character, self )
			self.ui.layout_powers.addWidget( powers )

			subPowers = SubPowerWidget( self.__storage, self.__character, self )
			self.ui.layout_subPowers.addWidget( subPowers )

		flaws = FlawWidget( self.__storage, self.__character, self )
		self.ui.layout_flaws.addWidget( flaws )

		self.__advantages = AdvantagesWidget( self.__storage, self.__character, self )
		self.ui.layout_advantages.addWidget( self.__advantages )

		items = ItemWidget( self.__storage, self.__character, self )
		self.ui.layout_items.addWidget( items )

		## Wenn sich der Name im InfoWidget ändert, soll sich auch die Titelzeile des Programms ändern
		self.info.nameChanged.connect(self.setTitle)

		### Wird eine neue Seite angewählt, muß das Info-Widget den Beschreibungstext speichern.
		#self.pageChanged.connect(self.info.saveDescription)

		# Die Spezialisierungen einer Fertigkeit sollen angezeigt werden.
		skills.specialtiesActivated.connect(specialties.showSpecialties)

		# Menschen haben keine übernatürlichen Kräfte, also zeige ich sie auch nicht an.
		self.__character.speciesChanged.connect(self.disablePowerItem)

		# Hintergrundbild ändert sich je nach Spezies
		self.__character.speciesChanged.connect(self.showBackround)

		## Sämtliche Schriften in das System laden, damit ich sie auch benutzen kann.
		resourceFontDir = QDir(":/fonts/fonts")
		fontsList = resourceFontDir.entryList()
		for font in fontsList:
			QFontDatabase.addApplicationFont(resourceFontDir.filePath(font))


	def activate(self):
		"""
		Diese Funktion "aktiviert" SoulCreator. Hier werden beispielsweise Merits mit allen anderen Eigenschaften verknüpft, die in ihren Voraussetzungen vorkommen. und bei einem ändern dieser Eigenschaft, wird neu geprüft, ob der Merit verfügbar ist, oder nicht.
		"""

		## Merits und Subpowers müssen mit allen Eigenschaften verknüpft werden, die in ihrer Prerequisits-Eigenschaft vorkommen.
		ConnectPrerequisites.buildConnection(self.__storage, self.__character)

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

		self.__creation = Creation( self.__storage, self.__character, self )
		for typ in self.__creation.creationPoints[Config.initialSpecies]:
			for category in self.__storage.categories(typ):
				for trait in self.__character.traits[typ][category].values():
					trait.traitChanged.connect(self.__creation.calcPoints)

		# Schreibe die übrigen Erschaffungspunkte
		#connect( creation, SIGNAL( pointsChanged() ), self, SLOT( showCreationPoints() ) );
		self.__creation.pointsChanged.connect(self.showCreationPoints)
		self.__creation.pointsChangedZero.connect(self.warnCreationPointsDepleted)
		self.__creation.pointsChangedNegative.connect(self.warnCreationPointsNegative)
		self.__creation.pointsChangedPositive.connect(self.warnCreationPointsPositive)


	def reset(self):
		self.__character.resetCharacter()
		# Direkt nach dem Start ist der Charkater natürlich nicht modifiziert.
		self.__character.setModified(False)

		# Wir wollen zu Beginn immer die Informationen sehen.
		self.ui.selectWidget_select.setCurrentRow(0)
		# Am Anfang stehen Menschen, aber das speciesChanged-Signal wurde nicht gesendet.
		self.disablePowerItem(Config.initialSpecies)


	def showSettingsDialog(self):
		"""
		Diese Funktion ruft den Einstellungsdialog auf und sorgt dafür, daß die Änderungen gespeichert oder verworfen werden.
		"""

		dialog = SettingsDialog( self )

		#dialog.settingsChanged.connect(self.info.useCalenderForAge)

		if dialog.exec_():
			# Ausführen der veränderten Einstellungen.
			#Debug.debug("Einstellungen werden geändert")
			#// 		self.setFont(Config.windowFont);
			pass

		#dialog.settingsChanged.disconnect(self.info.useCalenderForAge)


	def showBackround( self, species ):
		"""
		Für jede Spezies wird das passende Hintergrundbild angezeigt.
		"""

		if ( species == "Changeling" ):
			self.ui.widget_traits.setStyleSheet( "BackgroundImageWidget { background-image: url(:/background/images/Skull-Changeling-gray.png); background-repeat: no-repeat; background-position: center; background-attachment: fixed; }" )
		elif ( species == "Mage" ):
			self.ui.widget_traits.setStyleSheet( "BackgroundImageWidget { background-image: url(:/background/images/Skull-Mage-gray.png); background-repeat: no-repeat; background-position: center; background-attachment: fixed; }" )
		elif ( species == "Vampire" ):
			self.ui.widget_traits.setStyleSheet( "BackgroundImageWidget { background-image: url(:/background/images/Skull-Vampire-gray.png); background-repeat: no-repeat; background-position: center; background-attachment: fixed; }" )
		elif ( species == "Werewolf" ):
			self.ui.widget_traits.setStyleSheet( "BackgroundImageWidget { background-image: url(:/background/images/Skull-Werewolf-gray.png); background-repeat: no-repeat; background-position: center; background-attachment: fixed; }" )
		else:
			self.ui.widget_traits.setStyleSheet( "BackgroundImageWidget { background-image: url(:/background/images/Skull-Human-gray.png); background-repeat: no-repeat; background-position: center; background-attachment: fixed; }" )


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


	def showCreationPoints( self ):
		"""
		Zeigt die Anzahl der übrigen Punkte bei der Charaktererschaffung an.

		Je nachdem, welches Tab gerade gezeigt wird, müssen die Erschaffungspunkte dargestellt oder versteckt werden.
		"""

		self.ui.label_pointsLeft.setHidden( True )

		pagesWithPoints = [1, 2, 3, 5]

		if self.ui.stackedWidget_traits.currentIndex() in pagesWithPoints:
			self.ui.label_pointsLeft.setHidden( False )

			if ( self.ui.stackedWidget_traits.currentIndex() == 1 ):
				typ = "Attribute"
			elif ( self.ui.stackedWidget_traits.currentIndex() == 2 ):
				typ = "Skill"
			elif ( self.ui.stackedWidget_traits.currentIndex() == 3 ):
				typ = "Merit"
			elif ( self.ui.stackedWidget_traits.currentIndex() == 5 ):
				typ = "Power"

			text = "Creation Points: "
			if typ != None:
				textList = [unicode(item) for item in self.__creation.creationPointsAvailable[self.__character.species][typ]]
				text += "/".join(textList)
				if any(x < 0 for x in self.__creation.creationPointsAvailable[self.__character.species][typ]):
					text = "<span style='color:{color}'>{text}</span>".format(color=Config.pointsNegativeColor, text=text)
			self.ui.label_pointsLeft.setText( text )


	def warnCreationPointsDepleted( self, typ ):
		"""
		Zeigt eine Warnung an, wenn alle Erschafungspunkte vergeben wurden.

		\note Die Schrift im Auswahl-Widget, mit welchem man die verschiedenen Seiten anwählen kann wird für diese Seite wieder zur Standardfarbe verändert.
		"""

		if typ == "Attribute":
			self.ui.selectWidget_select.resetItemColor( 1 )
		elif typ == "Skill":
			self.ui.selectWidget_select.resetItemColor( 2 )
		elif typ == "Merit":
			self.ui.selectWidget_select.resetItemColor( 3 )
		elif typ == "Power":
			self.ui.selectWidget_select.resetItemColor( 5 )


	def warnCreationPointsPositive( self, typ ):
		"""
		Zeigt eine Warnung an, wenn nicht alle Erschafungspunkte vergeben wurden.

		\note Die Schrift im Auswahl-Widget, mit welchem man die verschiedenen Seiten anwählen kann wird für diese Seite blau eingefärbt.
		"""

		if typ == "Attribute":
			self.ui.selectWidget_select.setItemColor( 1, QColor(Config.pointsPositiveColor))
		elif typ == "Skill":
			self.ui.selectWidget_select.setItemColor( 2, QColor(Config.pointsPositiveColor) )
		elif typ == "Merit":
			self.ui.selectWidget_select.setItemColor( 3, QColor(Config.pointsPositiveColor) )
		elif typ == "Power":
			self.ui.selectWidget_select.setItemColor( 5, QColor(Config.pointsPositiveColor) )


	def warnCreationPointsNegative( self, typ ):
		"""
		Zeigt eine Warnung an, wenn zuviele Erschafungspunkte vergeben wurden.

		\note Die Schrift im Auswahl-Widget, mit welchem man die verschiedenen Seiten anwählen kann wird für diese Seite rot eingefärbt.
		"""

		if typ == "Attribute":
			self.ui.selectWidget_select.setItemColor( 1, QColor(Config.pointsNegativeColor) )
		elif typ == "Skill":
			self.ui.selectWidget_select.setItemColor( 2, QColor(Config.pointsNegativeColor) )
		elif typ == "Merit":
			self.ui.selectWidget_select.setItemColor( 3, QColor(Config.pointsNegativeColor) )
		elif typ == "Power":
			self.ui.selectWidget_select.setItemColor( 5, QColor(Config.pointsNegativeColor) )


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


	def openCharacter(self, fileName=None):
		"""
		Über diese Funktion wird der Dialog aufgerufen, um einen gespeicherten Charakter in das Programm laden zu können.
		"""

		# Warnen, wenn der vorherige Charakter noch nicht gespeichert wurde!
		if ( self.maybeSave() ):
			#Debug.debug("Open")

			filePath = ""
			if fileName:
				filePath = fileName
			else:
				appPath = PathTools.getPath()

				# Pfad zum Speicherverzeichnis
				savePath = "{}/{}".format(appPath, Config.saveDir)

				# Wenn Unterverzeichnis nicht existiert, suche im Programmverzeichnis.
				if ( not os.path.exists( savePath ) ):
					savePath = appPath

				fileData = QFileDialog.getOpenFileName(
					self,
					self.tr( "Select Character File" ),
					savePath,
					self.tr( "WoD Characters (*.chr)" )
				)
				filePath = fileData[0]

			if ( filePath ):
				# Charakter wird erst gelöscht, wenn auch wirklich ein neuer Charkater geladen werden soll.
				self.__character.resetCharacter()

				try:
					self.__readCharacter.read(filePath)
				except ErrXmlVersion as e:
					MessageBox.exception( self, e.message, e.description )
				except ErrXmlParsing as e:
					MessageBox.exception( self, e.message, e.description )
				except ErrFileNotOpened as e:
					MessageBox.exception( self, e.message, e.description )

				# Unmittelbar nach dem Laden ist der Charkter natürlich nicht mehr 'geändert'.
				self.__character.setModified( False )


	def saveCharacter(self):
		"""
		Über diese Funktion wird erst der Dialog aufgerufen zum Aussuchen des Speicherortes und danach dann das Schreiben des Charakters in eine XML-Datei eingeletiet.
		"""

		appPath = PathTools.getPath()

		# Pfad zum Speicherverzeichnis
		savePath = "{}/{}".format(appPath, Config.saveDir)

		# Wenn Unterverzeichnis nicht existiert, erstelle es
		if not os.path.exists(savePath):
			os.makedirs(savePath)

		filePath = QFileDialog.getSaveFileName( self, self.tr( "Save Character" ), "{}/untitled.chr".format(savePath), self.tr( "WoD Characters (*.chr)" ) )

		#Debug.debug(filePath)

		# Nur Speichern, wenn ein Name eingegeben wurde.
		if filePath[0]:
			try:
				self.__writeCharacter.write( filePath[0] )
			except ErrXmlVersion as e:
				MessageBox.exception( self, e.message(), e.description() )
			except ErrXmlParsing as e:
				MessageBox.exception( self, e.message(), e.description() )
			except ErrFileNotOpened as e:
				MessageBox.exception( self, e.message(), e.description() )

			# Unmittelbar nach dem Speichern ist der Charkter natürlich nicht mehr 'geändert'.
			self.__character.setModified( False )


	def disablePowerItem( self, species ):
		"""
		Diese Funktion verbirgt die Anzeige übernatürlicher Kräfte, wenn keine zur Verfügung stehen. Dadurch bleibt mehr Platz für die Merits.
		"""

		if species == "Human":
			self.ui.selectWidget_select.setItemEnabled(5, False)
		else:
			self.ui.selectWidget_select.setItemEnabled(5, True)


	def exportCharacter(self):
		"""
		Diese Funktion druckt den Charakter in ein PDF-Dokument.
		"""

		appPath = PathTools.getPath()

		# Pfad zum Speicherverzeichnis
		savePath = "{}/{}".format(appPath, Config.saveDir)

		# Wenn Unterverzeichnis nicht existiert, erstelle es
		if not os.path.exists(savePath):
			os.makedirs(savePath)

		if GlobalState.isDevelop:
			filePath = ["{}/untitled.pdf".format(savePath), ""]
		else:
			filePath = QFileDialog.getSaveFileName( self, self.tr( "Export Character" ), "{}/untitled.pdf".format(savePath), self.tr( "Portable Document Format (*.pdf)" ) )

		# Ohne diese Abfrage, würde der Druckauftrag auch bei einem angeblichen Abbrechen an den Drucker geschickt, aber wegen der Einstellungen als pdf etc. kommt ein seltsamer Ausdruck heraus. War zumindest zu C++-Zeiten so.
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

		printer = QPrinter()
		printDialog = QPrintDialog( printer, self )

		#printer.setPaperSize( QPrinter.A4 )
		#printer.setFullPage( True )

		drawSheet = DrawSheet( self.__storage, self.__character, printer, self )

		if ( printDialog.exec_() == QDialog.Accepted ):
			drawSheet = DrawSheet( self.__storage, self.__character, printer, self )

			##connect( &drawSheet, SIGNAL( enforcedTraitLimits( cv_AbstractTrait.Type ) ), self, SLOT( messageEnforcedTraitLimits( cv_AbstractTrait.Type ) ) );

			try:
				drawSheet.print()
			except ErrSpeciesNotExisting as e:
				MessageBox.exception( self, e.message, e.description )


	def writeSettings(self):
		"""
		Speichert die Konfiguration dieses Programms für den nächsten Aufruf.
		"""

		settings = Settings( "{}/{}".format(PathTools.getPath(), Config.configFile ))

		settings.beginGroup( "MainWindow" )
		settings.setValue( "size", self.size() )
		settings.setValue( "pos", self.pos() )
		settings.setValue( "state", self.saveState() )
		settings.endGroup()

		settings.beginGroup( "Config" );
		#// 	settings.setValue( "windowFont", Config.windowFont.family() );
		settings.setValue( "calendarForAgeCalculation", Config.calendarForAgeCalculation )
		settings.endGroup();


	def readSettings(self):
		"""
		Liest die Einstellungen für das Programm aus der Konfigurationsdatei.
		"""

		appPath = PathTools.getPath()
		settings = Settings( "{}/{}".format(appPath, Config.configFile))

		settings.beginGroup( "MainWindow" );
		self.resize( settings.value( "size", QSize( 900, 600 ) ) )
		self.move( settings.value( "pos", QPoint( 200, 200 ) ) )
		self.restoreState( QByteArray(settings.value( "state" )) )
		settings.endGroup()

		settings.beginGroup( "Config" );
		#// 	Config.windowFont = QFont( settings.value( "windowFont" ).toString() );
		## bool(bla) funktioniert nicht, also sorge ich dafür, daß alles außer false (nicht case-sensitive) als Wahr gilt.
		Config.calendarForAgeCalculation = unicode(settings.value( "calendarForAgeCalculation" )).lower() != "false"
		settings.endGroup();

		#// 	// Nachdem die Einstellungen geladen wurden, müssen sie auch angewandt werden.
		#// 	setFont(Config.windowFont);


	def maybeSave(self):
		"""
		Fragt nach, ob die Änderungen am Charakter gespeichert werden sollen, ehe sie möglicherweise verloren gehen.

		Diese Frage tritt auf, wenn der dargestellte Charakter nicht gespeichert ist und ehe das Programm geschlossen werden oder einen neuen Charakter anlegen soll.
		"""


		if ( self.__character.isModifed() ):
			ret = QMessageBox.warning(
				self,
				self.tr( "Application" ),
				self.tr( "The character has been modified.\nDo you want to save your changes?" ),
				QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
			)

			if ( ret == QMessageBox.Save ):
				self.saveCharacter()
			elif ( ret == QMessageBox.Cancel ):
				return False

		return True


	def showExceptionMessage( self, message, critical=True ):
		"""
		Ausgabe einer Fehlernachricht.
		"""

		if critical:
			MessageBox.critical( self, self.tr( "Critical Error occured!" ), message )
		else:
			MessageBox.warning( self, self.tr( "Error occured!" ), message )


#void MainWindow.messageEnforcedTraitLimits( cv_AbstractTrait.Type type ) {
	"""
	Zeigt eine Nachricht an, daß die Eigenschaftsanzahl das für den Charakterbogen gesetzte Limit übertrifft, und daß alle überzähligen Eigenschaften des mitgegebenen Typs ignoriert werden.
	"""

	#MessageBox.warning( self, tr( "Too many Traits" ), tr( "There are too many %1 to fit on page.\n Printing will be done without the exceeding number of traits." ).arg( cv_AbstractTrait.toString( type, true ) ) );
#}



