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

#import sys
import os

from PySide.QtCore import QCoreApplication, QSize, QPoint, QByteArray, QDir, QTimer
from PySide.QtGui import QMainWindow, QIcon, QMessageBox, QFileDialog, QDialog, QPrinter, QFontDatabase, QColor, QPrintDialog
from PySide import QtSvg	# Damit auch unter Windows SVG-Dateien dargestellt werden.

from src.GlobalState import GlobalState
from src.Tools import PathTools
from Error import ErrFileNotOpened, ErrXmlParsing, ErrXmlVersion, ErrSpeciesNotExisting
from Config import Config
import IO.Shell
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
from Widgets.AttributeWidget import AttributeWidget
from Widgets.SkillWidget import SkillWidget
from Widgets.TemplateWidget import TemplateWidget
from Widgets.PowerWidget import PowerWidget
from Widgets.SubPowerWidget import SubPowerWidget
from Widgets.SpecialtiesWidget import SpecialtiesWidget
from Widgets.MeritWidget import MeritWidget
from Widgets.FlawWidget import FlawWidget
from Widgets.MoralityWidget import MoralityWidget
from Widgets.AdvantagesWidget import AdvantagesWidget
from Widgets.ItemWidget import ItemWidget
from Widgets.SpecialsWidget import SpecialsWidget
from Widgets.Dialogs.SettingsDialog import SettingsDialog
from Widgets.Dialogs.MessageBox import MessageBox
#from Draw.DrawSheet import DrawSheet
from Draw.RenderSheet import RenderSheet
from Debug import Debug

from ui.ui_MainWindow import Ui_MainWindow

from resources import rc_resource




class MainWindow(QMainWindow):
	"""
	@brief Das Hauptfenster der Anwendung.

	Hier werden die Widgets präsentiert und die hier laufen die Verbindungen zwischen den einzelnen Objekten zusammen.

	\todo Die Information, daß manche Merits nur bei Charaktererschaffung gewählt werden können, in das Programm einbinden.

	\todo Charaktererschaffung in Schritten und Erfahrungspunkte einbauen.

	\todo Kosten von Gegenständen berücksichtigen.

	\todo Benutzer sollen ihre eigenen Merits etc. eintragen können. Dafür sollte ich ihnen eine eigene template-Datei bereitstellen, in welche dann all diese Eigenschaften hineingeschrieben werden. Diese Datei wird gleichberechtigt ausgelesen wie die anderen, befindet sich jedoch nicht in der Ressource, sondern liegt als externe Datei vor.

	\todo Damit beim Laden einer Datei eine Eigenschaft, welche eigentlich nicht zur Verfügung steht, keine Punkte hat, sollte nach dem Laden nochmal eine Kontrolle durchgeführt werden.

	\todo Erschaffungspunkte durch einen Wizard ersetzen.

	\todo "Leere" Felder auf dem Charakterbogen mit Leerzeilen zum händischen Ausfüllen versehen.

	\todo Changeling: Ich vermisse beim Aussehen die Unterscheidung zwischen Mask und Mien

	\todo Attribute der Werewolf-Gestalten anzeigen

	\todo Hausregeln per Option ein-/ausschlatbar machen.

	\todo Werwolf-Gaben vervollständigen.

	\todo Gaben in ene ScrollArea packen, denn es sind viel zu viele, um die Übersicht zu bewahren. Oder ich verwende ein TreeView...

	\todo Erschaffungspunkte für Fertigkeiten bei Kindern vom Alter abhängig machen.

	\todo Beim Laden die Ganzen Hinweisfenster für das Verteilen von Giant/Tiny etc. nicht anzeigen.
	"""


	### Wird eine neue Seite angewählt, wird dieses Signal mit der Indexnummer der neu angezeigten Seite versandt.
	#pageChanged = Signal(int)


	def __init__(self, fileName=None, exportPath=None, parent=None):
		#dbgStart = Debug.timehook()
		QMainWindow.__init__(self, parent)

		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

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
		self.__character.speciesChanged.connect(self.ui.selectWidget_select.changeIcons)

		self.__readCharacter.exceptionRaised.connect(self.showExceptionMessage)

		# Laden der Konfiguration
		self.readSettings()

		self.populateUi()
		self.activate()

		self.ui.selectWidget_select.currentRowChanged.connect(self.showCreationPoints)

		self.ui.actionSettings.triggered.connect(self.showSettingsDialog)
		self.ui.actionNew.triggered.connect(self.newCharacter)
		self.ui.actionOpen.triggered.connect(self.openCharacter)
		self.ui.actionSave.triggered.connect(self.saveCharacter)
		self.ui.actionExport.triggered.connect(self.exportCharacter)
		self.ui.actionPrint.triggered.connect(self.printCharacter)
		self.ui.actionAbout.triggered.connect(self.aboutApp)

		self.reset()
		#Debug.timesince(dbgStart)

		## Wird ein Dateiname angegeben, soll dieser sofort geladen werden.
		if fileName:
			if os.path.exists(fileName):
				if GlobalState.isVerbose:
					print("Opening file {}.".format(fileName))
				self.openCharacter(fileName)
			elif fileName.lower() in [ species.lower() for species in self.__storage.species.keys() ]:
				if GlobalState.isVerbose:
					print("Empty Charactersheet of species {} will be created.".format(fileName.lower()))
				self.__character.species = fileName[0].upper() + fileName[1:].lower()
				self.__character.setModified(False)
			else:
				IO.Shell.printError("Warning! A file named {} does not exist.".format(fileName))

		#Debug.timesince(dbgStart)

		if exportPath:
			if GlobalState.isVerbose:
				print("Creating PDF {}".format(exportPath[0]))
			# exportPath ist eine Liste mit einem einzigen Element als Inhalt (argparse)
			self.__createPdf(exportPath[0])
			# Damit das Programm ordentlich geschlossen werden kann, muß auf das Starten der Event-Loop gewartet werden. dies geht am einfachsten mit einem QTimer.
			QTimer.singleShot(0, self.close)



	def closeEvent( self, event ):
		if ( self.maybeSave() ):
			self.writeSettings()
			if GlobalState.isVerbose:
				print("Closing now.")
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

		#specialties = Specialties( self.__storage.traits["Skill"], self )
		specialties = SpecialtiesWidget( self.__storage.traits["Skill"], self )
		self.ui.layout_specialties.addWidget( specialties )

		merits = MeritWidget( self.__storage, self.__character, self )
		self.ui.layout_merits.addWidget( merits )

		morality = MoralityWidget( self.__storage, self.__character, self )
		self.ui.layout_morality.addWidget( morality )

		self.template = TemplateWidget(self.__storage, self.__character, self)
		self.ui.layout_template.addWidget( self.template )

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

		speciesSpecials = SpecialsWidget(self.__storage, self.__character, self)
		self.ui.layout_specials.addWidget( speciesSpecials )

		## Wenn sich der Name im InfoWidget ändert, soll sich auch die Titelzeile des Programms ändern
		self.info.nameChanged.connect(self.setTitle)

		### Wird eine neue Seite angewählt, muß das Info-Widget den Beschreibungstext speichern.
		#self.pageChanged.connect(self.info.saveDescription)

		# Die Spezialisierungen einer Fertigkeit sollen angezeigt werden.
		skills.specialtiesActivated.connect(specialties.showSpecialties)

		# Menschen haben keine übernatürlichen Kräfte, also zeige ich sie auch nicht an.
		self.__character.speciesChanged.connect(self.ui.selectWidget_select.disableItems)

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
		self.__character.traits["Merit"]["Physical"]["Giant"].totalvalueChanged.connect(calc.calcSize)
		self.__character.traits["Merit"]["Physical"]["GiantKid"].totalvalueChanged.connect(calc.calcSize)
		self.__character.traits["Merit"]["Physical"]["Tiny"].totalvalueChanged.connect(calc.calcSize)
		self.__character.traits["Flaw"]["Physical"]["Dwarf"].totalvalueChanged.connect(calc.calcSize)
		self.__character.traits["Attribute"]["Physical"]["Dexterity"].totalvalueChanged.connect(calc.calcInitiative)
		self.__character.traits["Attribute"]["Social"]["Composure"].totalvalueChanged.connect(calc.calcInitiative)
		self.__character.traits["Merit"]["Physical"]["Fast Reflexes"].totalvalueChanged.connect(calc.calcInitiative)
		self.__character.traits["Attribute"]["Physical"]["Strength"].totalvalueChanged.connect(calc.calcSpeed)
		self.__character.traits["Attribute"]["Physical"]["Dexterity"].totalvalueChanged.connect(calc.calcSpeed)
		self.__character.traits["Merit"]["Physical"]["Fleet of Foot"].totalvalueChanged.connect(calc.calcSpeed)
		self.__character.traits["Attribute"]["Mental"]["Wits"].totalvalueChanged.connect(calc.calcDefense)
		self.__character.traits["Attribute"]["Physical"]["Dexterity"].totalvalueChanged.connect(calc.calcDefense)
		self.__character.traits["Attribute"]["Physical"]["Stamina"].totalvalueChanged.connect(calc.calcHealth)
		self.__character.traits["Attribute"]["Mental"]["Resolve"].totalvalueChanged.connect(calc.calcWillpower)
		self.__character.traits["Attribute"]["Social"]["Composure"].totalvalueChanged.connect(calc.calcWillpower)

		calc.sizeChanged.connect(self.__advantages.setSize)
		calc.initiativeChanged.connect(self.__advantages.setInitiative)
		calc.speedChanged.connect(self.__advantages.setSpeed)
		calc.defenseChanged.connect(self.__advantages.setDefense)
		calc.healthChanged.connect(self.__advantages.setHealth)
		calc.willpowerChanged.connect(self.__advantages.setWillpower)

		self.info.notificationSent.connect(self.showStatusBarMessage)

		self.__creation = Creation( self.__storage, self.__character, self )
		for typ in self.__creation.creationPoints[Config.initialSpecies]:
			for category in self.__storage.categories(typ):
				for trait in self.__character.traits[typ][category].values():
					trait.traitChanged.connect(self.__creation.calcPoints)

		# Schreibe die übrigen Erschaffungspunkte
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
		## Am Anfang stehen Menschen, aber das speciesChanged-Signal wurde nicht gesendet.
		#self.ui.selectWidget_select.disableItems(Config.initialSpecies)


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

		self.ui.widget_traits.setStyleSheet( "BackgroundImageWidget {{ background-image: url(:/background/images/species/{}/Skull-gray.png); background-repeat: no-repeat; background-position: center; background-attachment: fixed; }}".format(species) )



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

		typ = None

		if ( self.ui.selectWidget_select.currentPage() == "Attributes" ):
			typ = "Attribute"
		elif ( self.ui.selectWidget_select.currentPage() == "Skills" ):
			typ = "Skill"
		elif ( self.ui.selectWidget_select.currentPage() == "Merits" ):
			typ = "Merit"
		elif ( self.ui.selectWidget_select.currentPage() == "Powers" ):
			typ = "Power"

		if typ:
			self.ui.label_pointsLeft.setHidden( False )
			textList = [unicode(item) for item in self.__creation.creationPointsAvailable[self.__character.species][typ]]
			text = "Creation Points: "
			if typ == "Skill":
				text += "/".join(textList[1:])
				text += " Specialties: {}".format(textList[0])
			else:
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
			self.ui.selectWidget_select.resetItemColor( "Attributes" )
		elif typ == "Skill":
			self.ui.selectWidget_select.resetItemColor( "Skills" )
		elif typ == "Merit":
			self.ui.selectWidget_select.resetItemColor( "Merits" )
		elif typ == "Power":
			self.ui.selectWidget_select.resetItemColor( "Powers" )


	def warnCreationPointsPositive( self, typ ):
		"""
		Zeigt eine Warnung an, wenn nicht alle Erschafungspunkte vergeben wurden.

		\note Die Schrift im Auswahl-Widget, mit welchem man die verschiedenen Seiten anwählen kann wird für diese Seite blau eingefärbt.
		"""

		if typ == "Attribute":
			self.ui.selectWidget_select.setItemColor( "Attributes", QColor(Config.pointsPositiveColor))
		elif typ == "Skill":
			self.ui.selectWidget_select.setItemColor( "Skills", QColor(Config.pointsPositiveColor) )
		elif typ == "Merit":
			self.ui.selectWidget_select.setItemColor( "Merits", QColor(Config.pointsPositiveColor) )
		elif typ == "Power":
			self.ui.selectWidget_select.setItemColor( "Powers", QColor(Config.pointsPositiveColor) )


	def warnCreationPointsNegative( self, typ ):
		"""
		Zeigt eine Warnung an, wenn zuviele Erschafungspunkte vergeben wurden.

		\note Die Schrift im Auswahl-Widget, mit welchem man die verschiedenen Seiten anwählen kann wird für diese Seite rot eingefärbt.
		"""

		if typ == "Attribute":
			self.ui.selectWidget_select.setItemColor( "Attributes", QColor(Config.pointsNegativeColor) )
		elif typ == "Skill":
			self.ui.selectWidget_select.setItemColor( "Skills", QColor(Config.pointsNegativeColor) )
		elif typ == "Merit":
			self.ui.selectWidget_select.setItemColor( "Merits", QColor(Config.pointsNegativeColor) )
		elif typ == "Power":
			self.ui.selectWidget_select.setItemColor( "Powers", QColor(Config.pointsNegativeColor) )


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
			self.reset()


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
					self.tr( "WoD Characters (*.{})".format(Config.fileSuffixSave) )
				)
				filePath = fileData[0]

			if ( filePath ):
				# Charakter wird erst gelöscht, wenn auch wirklich ein neuer Charkater geladen werden soll.
				self.__character.resetCharacter()

				self.__character.isLoading = True
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
				self.__character.isLoading = False


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

		filePath = QFileDialog.getSaveFileName( self, self.tr( "Save Character" ), "{}/untitled.{}".format(savePath, Config.fileSuffixSave), self.tr( "WoD Characters (*.{})".format(Config.fileSuffixSave) ) )

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


	def __createPdf(self, savePath):
		"""
		Diese Funktion druckt den Charakter in ein PDF-Dokument.
		"""

		# Wenn Unterverzeichnis nicht existiert, erstelle es
		dirname = os.path.dirname(savePath)
		if not os.path.exists(dirname):
			os.makedirs(dirname)

		printer = QPrinter(QPrinter.PrinterResolution)
		#printer = QPrinter()

		printer.setOutputFormat( QPrinter.PdfFormat )
		printer.setPaperSize( QPrinter.A4 )
		printer.setFullPage( True )
		printer.setOutputFileName( savePath )

		drawSheet = RenderSheet( self.__storage, self.__character, printer, self )

		try:
			drawSheet.createSheets()
		except ErrSpeciesNotExisting as e:
			MessageBox.exception( self, e.message, e.description )


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
			self.__createPdf(filePath[0])


	def printCharacter(self):
		"""
		Druckt den angezeigten Charakter aus.
		"""

		printer = QPrinter(QPrinter.PrinterResolution)
		printDialog = QPrintDialog( printer, self )

		if ( printDialog.exec_() == QDialog.Accepted ):
			drawSheet = RenderSheet( self.__storage, self.__character, printer, self )

			try:
				drawSheet.createSheets()
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

		settings.beginGroup( "Config" )
		settings.setValue( "autoSelectEra", Config.autoSelectEra )
		settings.endGroup()


	def readSettings(self):
		"""
		Liest die Einstellungen für das Programm aus der Konfigurationsdatei.
		"""

		appPath = PathTools.getPath()
		settings = Settings( "{}/{}".format(appPath, Config.configFile))

		settings.beginGroup( "MainWindow" )
		self.resize( settings.value( "size", QSize( 900, 600 ) ) )
		self.move( settings.value( "pos", QPoint( 200, 200 ) ) )
		self.restoreState( QByteArray(settings.value( "state" )) )
		settings.endGroup()

		settings.beginGroup( "Config" )
		Config.autoSelectEra = unicode(settings.value( "autoSelectEra" )).lower() != "false"
		settings.endGroup()

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


	def showStatusBarMessage( self, message, timeout=Config.displayTimeout ):
		"""
		Zeigt eien Nachricht auf der Statusleiste an.
		"""

		#if timeout is None:
			#timeout = Config.displayTimeout
		self.statusBar().showMessage(message, timeout)


	def showExceptionMessage( self, message, description, critical=True ):
		"""
		Ausgabe einer Fehlernachricht.
		"""

		if critical:
			MessageBox.critical( self, message, description )
		else:
			MessageBox.warning( self, message, description )


#void MainWindow.messageEnforcedTraitLimits( cv_AbstractTrait.Type type ) {
	"""
	Zeigt eine Nachricht an, daß die Eigenschaftsanzahl das für den Charakterbogen gesetzte Limit übertrifft, und daß alle überzähligen Eigenschaften des mitgegebenen Typs ignoriert werden.
	"""

	#MessageBox.warning( self, tr( "Too many Traits" ), tr( "There are too many %1 to fit on page.\n Printing will be done without the exceeding number of traits." ).arg( cv_AbstractTrait.toString( type, true ) ) );
#}



