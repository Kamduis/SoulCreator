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

from PyQt4.QtCore import Qt, QSize
#from PyQt4.QtGui import QColor




class Config(object):
	"""
	@brief Konfigurationsklasse des Programms.

	Hier werden die Konfigurationseinstellungen gespeichert.
	"""


	# Programmdaten
	programName = "SoulCreator"
	programAuthor = "Victor von Rhein"
	programAuthorEMail = "victor@caern.de"
	programVersionMajor = 0
	programVersionMinor = 12
	programVersionChange = 0
	programDescription = "Charaktergenerator for the World of Darkness."
	organization = "Caern"

	# Konfigurationsdatei
	configFile = "config.ini"

	# Verzeichnisname für gespeicherte Charaktere
	saveDir = "save"

	# Verzeichnisname für Ressourcen
	resourceDir = "resources"
	resourceDirTemplates = "templates"

	# Verzeichnisname für Uis
	uiDir = "ui"

	# Dateiendung komprimierter Dateien.
	fileSuffixCompressed = "scd"
	# Dateiendung der gespeicherten Charkatere
	fileSuffixSave = "chr"

	compressSaves = True

	# Zeichen, um Listeneinträge in den XML-Dateien zu trennen
	sepChar = ";"

	# Format von Daten bei der Umwandlung in Strings
	dateFormat = Qt.ISODate
	textDateFormat = "dd.MM.yyyy"

	# Einstellungen für das Auswahl-Widget
	selectIconSize = QSize(50,50)
	selectWidgetWidth = 150

	### Minimale Breite für textEdit-Felder, in denen mehrzeiliger Text eingegeben werden soll.
	#textEditWidthMin = 200

	## Das Charakterbild darf höchstens die hier festgelegte Größe annehmen.
	pictureWidthMax = 800
	pictureHeightMax = 800

	## Das Charakterbild wird in dem hier festgelegten Format gespeichert.
	pictureFormat = "png"#"jpg"

	# Vordefinierte Farben
	##  Wichtige Textabschnitte
	importantTextColor = "darkBlue"

	## Die Hintergrundfarbe für ernste Geistesstörungen in der Auswahlliste.
	severeDerangementsColor = "sandybrown"

	## Warnfarbe, wenn zuviele Punkte vergeben wurden.
	pointsNegativeColor = "orangered"

	## Warnfarbe, wenn zuwenige Punkte vergeben wurden.
	pointsPositiveColor = "chartreuse"

	##  Deaktivierte textabschnitte
	deactivatedTextColor = "darkgrey"

	## Kennzeichnung von Bonuseigenschaften.
	bonusColor = "red"

	## Symbole für die verschiedenen Waffencategorien.
	weaponIcons = {}
	weaponIcons["melee"] = ":/items/images/svg/machete.svg"
	weaponIcons["thrown"] = ":/items/images/svg/shuriken.svg"
	weaponIcons["ranged"] = ":/items/images/svg/uzi.svg"

	## Symbole für die verschiedenen magischen Gegenstände.
	extraordinaryItemsIcons = {}
	extraordinaryItemsIcons["Cursed Items"] = ":/items/images/svg/curse.svg"
	extraordinaryItemsIcons["Fetishes"] = ":/items/images/svg/feather.svg"
	extraordinaryItemsIcons["Tokens"] = ":/items/images/svg/spine.svg"
	extraordinaryItemsIcons["Imbued Items"] = ":/items/images/svg/wand.svg"
	extraordinaryItemsIcons["Artifacts"] = ":/types/images/svg/pentagram.svg"

	## Symbole für die verschiedenen Fahrzeugkategorien.
	automobilesIcons = {}
	automobilesIcons["Cars"] = ":/items/images/svg/vehicle-car.svg"
	automobilesIcons["Trucks"] = ":/items/images/svg/vehicle-truck.svg"
	automobilesIcons["Motorcycles"] = ":/items/images/svg/vehicle-motorcycle.svg"
	automobilesIcons["Commercial Vehicles"] = ":/items/images/svg/vehicle-commercial.svg"

	## Normaler vertikaler Abstand. Wird für Widgets eingesetzt, die zwar untereinander erscheinen, aber nicht zusammengequetscht erscheinen sollen.
	vSpace = 5

	## Der Pixelabstand zwischen Eigenschaftsblöcken. Beispielsweise der vertikale Abstand zwischen Den Fertigkeiten der verschiedenen Kategorien.
	traitCategorySpace = 10

	companionInfluencesCount = 5

	## Die Anzahl, wie oft Eigenschaften mit Beschreibungstext mehrfach ausgewählt werden dürfen.
	traitMultipleMax = 4

	## Die Zeit, wie lange Nachrichten in der Statuszeile angezeigt werden sollen.
	displayTimeout = 10000

	## Die minimale Breite für Widgets wie Fertigkeiten, Merits, Flaws etc.
	traitLineWidthMin = 320

	## Die Minimale Breite für Textfelder für zusätzlichen Text von Eigenschaften.
	traitCustomTextWidthMin = 100

	## Die größtmögliche Höhe von Widgets, welche sich in einer Textzeile befinden.
	#
	# Diese Höhe wurde gewählt, um vertikalen Raum zu sparen.
	inlineWidgetHeightMax = 18

	## Die Breite der Armor-Spinboxes.
	spinBoxNoTextWidth = 30

	## Die Breite einer einfachen vertikalen Eigenschaftsliste.
	#const int Config::traitVerticalListWidth = 300

	## Eigenschaftshöchstwert.
	traitMax = 5

	## Bezeichnung der Moral für alle Spezies
	moralityIdentifier = "Morality"

	## Höchstwert der Moral.
	moralityTraitMax = 10

	## Höchstwert der Moral bei der ein Charakter eine Geistesstörung haben kann.
	derangementMoralityTraitMax = 7

	## Startwert der Moral.
	moralityTraitDefaultValue = 7

	## Höchstwert der Gesundheit, von Spezies zu Spezies unterschiedlich.
	healthMax = {
		"Human": 11,
		"Changeling": 11,
		"Mage": 11,
		"Vampire": 16,
		"Werewolf": 16,
	}

	## Höchstwert der Willenskraft.
	willpowerMax = 10

	## Mindestwert der besonderen übernatürlichen Eigenschaft.
	powerstatMin = 1

	## Höchstwert der besonderen übernatürlichen Eigenschaft.
	powerstatMax = 10

	## Startwert der besonderen übernatürlichen Eigenschaft.
	powerstatDefaultValue = 1

	## Bezeichnung der Übernatürlichen Grundeigenschaft für alle Spezies
	powerstatIdentifier = "Powerstat"

	## Wieviele Vinculi sollen auf dem Vampir-Charakterbogen angezeigt werden.
	vinculiCount = 5
	vinculumLevelMax = 3

	## Über wievielen Punkten die Eigenschaften 2 Erschaffungspunkte kosten.
	#
	# Alle Punkte bis einschließelich dieser Zahl kosten nur 1 Punkt pro Punkt, aber alle darüber kosten das Doppelte.
	creationTraitDouble = 4

	## Schriftgröße für den normalen Text auf dem ausdruckbaren Charakterbogen.
	#const qreal Config::textSizeFactorPrintNormal = 0.45

	## Schriftgröße für den kleinen Text auf dem ausdruckbaren Charakterbogen.
	#const qreal Config::textSizeFactorPrintSmall = 0.33

	## Die Schriftart, welche für das Programm verwendet wird.
	#QFont Config::windowFont = QFont()

	## Standardspezies eines neuen Charakters
	initialSpecies = "Human"

	## Das Standardalter eines neuen Charakters
	ageInitial = 21

	ageMin = 6

	## Das Alter ab welchem der Charakter /kein/ Kind mehr ist.
	ageAdult = 13

	heightGiant = {
		"Adult": 2.01,
		"Kid": 1.51,
	}
	heightDwarf = {
		"Adult": 1.39,
		"Kid": 0.89,
	}
	heightMax = {
		"Adult": 2.30,
		"Kid": 1.80,
	}
	heightMin = {
		"Adult": 1.10,
		"Kid": 0.70,
	}

	size = {
		"Adult": 5,
		"Kid": 4,
	}
	## Sämtliche Geschlechter einschließlich der zugehörigen Symbole
	genders = (
		("Hermaphrodite", ":/icons/images/svg/symbolHermaphrodite.svg"),
		("Male", ":/icons/images/svg/symbolMale.svg"),
		("Female", ":/icons/images/svg/symbolFemale.svg"),
	)

	## Sämtliche Eigenschaftstypen.
	typs = (
		"Attribute",
		"Skill",
		"Merit",
		"Flaw",
		"Power",
	)

	## Die Kategorien von Attributen und Fertigkeiten sollen in einer gewissen Reihenfolge dargestellt werden.
	mainCategories = (
		"Mental",
		"Physical",
		"Social",
	)

	## Die Kategorien von Merits sollen in einer gewissen Reihenfolge dargestellt werden.
	# Alle Kategorien die nicht in dieser Liste stehen, werden nach den hier aufgeführten Kategorien dargestellt.
	meritCategories = (
		"Mental",
		"Physical",
		"Social",
		"Fighting Style",
		"Debate Style",
		"Extraordinary",
		"Item",
	)

	## Die Kategorien von Flaws sollen in einer gewissen Reihenfolge dargestellt werden.
	# Alle Kategorien die nicht in dieser Liste stehen, werden nach den hier aufgeführten Kategorien dargestellt.
	flawCategories = (
		"Mental",
		"Physical",
		"Social",
		#"Extraordinary",
	)

	initialEra = "Modern"

	## Sämtliche Eras, welcher ein Charakter angehören kann und mit welchem jahr sie beginnen.
	eras = {
		"Modern": 1950,
		"Renaissance": 1500,
		"Ancient": 0,
	}

	## Sämtliche Eras, welcher ein Charakter angehören kann.
	ages = (
		"Adult",
		"Kid",
	)

	## Die Reihenfolge der Attribute ist derart wichtig, daß ich sie nicht automatisch bestimmen kann.
	attributes = (
		( "Mental", ( "Intelligence", "Wits", "Resolve", ), ),
		( "Physical", ( "Strength", "Dexterity", "Stamina", ), ),
		( "Social", ( "Presence", "Manipulation", "Composure", ), ),
	)
	attributeSorts = ( u"Power", u"Finesse", u"Resistance", )

	## Die unterschiedlichen Gestalten der Werwölfe.
	shapesWerewolf = (
		"Hishu",
		"Dalu",
		"Gauru",
		"Urshul",
		"Urhan",
	)


	## Folgende Werte können über den Einstellungsdialog verändert werden und sollten beim Beenden des Programms gespeichert und beim Starten geladen werden. Die übergebenen Werte sind die Standartwerte, wenn im Einstellungsdialog nichts verändert wird.
	# Zur Altersberechnung Kalender verwenden
	#calendarForAgeCalculation = True
	autoSelectEra = True


	@staticmethod
	def version():
		"""
		\brief Die aktuelle Version des Programms ausschließlich der Change-Nummer.

		Programme mit unterschieldicher Versionsnummer sind zueinander nicht notwendigerweise kompatibel.
		"""

		return "{}.{}".format(Config.programVersionMajor, Config.programVersionMinor)


	@staticmethod
	def versionDetail():
		"""
		\brief Die aktuelle Version des Programms einschließlich der Change-Nummer.

		Unterscheiden sich Programme in ihrer Change-Nummer, aber der Rest ihrer Versionsnummer ist gleich, sollten eigentlich keine Kompatibilitätsprobleme mit den Template-Dateien und den gespeicherten Charakteren auftreten.
		"""

		return "{}.{}.{}".format(Config.programVersionMajor, Config.programVersionMinor, Config.programVersionChange)


	@staticmethod
	def getAge(age):
		"""
		Gibt die Alterskategorie zurück.
		"""

		if age < Config.ageAdult:
			return Config.ages[1]
		else:
			return Config.ages[0]



