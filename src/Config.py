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

from PySide.QtCore import QSize
#from PySide.QtGui import QColor




class Config():
	"""
	@brief Konfigurationsklasse des Programms.

	Hier werden die Konfigurationseinstellungen gespeichert.
	"""

	# Programmdaten
	programName = "SoulCreator"
	programAuthor = "Victor"
	programVersionMajor = 0
	programVersionMinor = 7
	programVersionChange = 1
	programDescription = "Charaktergenerator für die World of Darkness."
	organization = "Caern"

	# Konfigurationsdatei
	configFile = "config.ini"

	# Verzeichnisname für gespeicherte Charaktere
	saveDir = "save"

	# Zeichen, um Listeneinträge in den XML-Dateien zu trennen
	sepChar = ";"

	# Einstellungen für das Auswahl-Widget
	selectIconSize = QSize(50,50)
	selectWidgetWidth = 150

	# Vordefinierte Farben
	##  Wichtige Textabschnitte
	importantTextColor = "darkBlue"

	## Warnfarbe, wenn zuviele Punkte vergeben wurden.
	pointsNegativeColor = "red"

	## Warnfarbe, wenn zuwenige Punkte vergeben wurden.
	pointsPositiveColor = "blue"

	## Normaler vertikaler Abstand. Wird für Widgets eingesetzt, die zwar untereinander erscheinen, aber nicht zusammengequetscht erscheinen sollen.
	vSpace = 5

	## Der Pixelabstand zwischen Eigenschaftsblöcken. Beispielsweise der vertikale Abstand zwischen Den Fertigkeiten der verschiedenen Kategorien.
	traitCategorySpace = 10

	## Die Anzahl, wie oft Eigenschaften mit Beschreibungstext mehrfach ausgewählt werden dürfen.
	traitMultipleMax = 4

	## Die Zeit, wie lange Nachrichten in der Statuszeile angezeigt werden sollen.
	#const int Config::displayTimeout = 10000

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
	#const int Config::traitMax = 5

	## Höchstwert der Moral.
	moralityTraitMax = 10

	## Höchstwert der Moral bei der ein Charakter eine Geistesstörung haben kann.
	derangementMoralityTraitMax = 7

	## Startwert der Moral.
	moralityTraitDefaultValue = 7

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

	## Über wievielen Punkten die Eigenschaften 2 Erschaffungspunkte kosten.
	#
	# Alle Punkte bis einschließelich dieser Zahl kosten nur 1 Punkt pro Punkt, aber alle darüber kosten das Doppelte.
	creationTraitDouble = 4

	## Schriftgröße für den normalen Text auf dem ausdruckbaren Charakterbogen.
	#const qreal Config::textSizeFactorPrintNormal = 0.45

	## Schriftgröße für den kleinen Text auf dem ausdruckbaren Charakterbogen.
	#const qreal Config::textSizeFactorPrintSmall = 0.33

	## Die Schriftart, welche für den exportierten Charakter verwendet wird.
	#QFont Config::exportFont = QFont()

	## Die Schriftart, welche für das Programm verwendet wird.
	#QFont Config::windowFont = QFont()

	## Standardspezies eines neuen Charakters
	initialSpecies = "Human"

	## Das Standardalter eines neuen Charakters
	initialAge = 21

	## Das Alter ab welchem der Charakter /kein/ Kind mehr ist.
	adultAge = 13


	## Sämtliche Geschlechter einschließlich der zugehörigen Symbole
	genders = (
		("Male", ":/icons/images/male.png"),
		("Female", ":/icons/images/female.png"),
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
		"Extraordinary",
	)

	## Sämtliche Eras, welcher ein Charakter angehören kann.
	eras = (
		"Modern",
		"Ancient",
	)

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

		if age < Config.adultAge:
			return Config.ages[1]
		else:
			return Config.ages[0]



