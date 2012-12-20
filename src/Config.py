# -*- coding: utf-8 -*-

"""
# Copyright

Copyright (C) 2012 by Victor
victor@caern.de

# License

This file is part of SoulCreator.

SoulCreator is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

SoulCreator is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
SoulCreator.  If not, see <http://www.gnu.org/licenses/>.
"""




"""
Konfigurationsmodul des Programms.

Hier werden die Konfigurationseinstellungen gespeichert.
"""




from PyQt4.QtCore import Qt, QSize
#from PyQt4.QtGui import QColor




PATH_RESOURCE_BUILDER = "external/ResourcesPythonQt/resourcesPythonQt.py"
PATH_RESOURCE         = "res/"
PATH_UI               = "ui/"
PATH_LANGUAGES        = "lang/"
FILEXT_RESOURCE       = "qrc"
FILEXT_UI             = "ui"



# Programmdaten
PROGRAM_NAME = "SoulCreator"
PROGRAM_AUTHOR = "Victor von Rhein"
PROGRAM_AUTHOR_EMAIL = "victor@caern.de"
PROGRAM_VERSION = {
	"major": 0,
	"minor": 12,
	"change": 0,
}
PROGRAM_DESCRIPTION = "Charaktergenerator for the World of Darkness."
ORGANIZATION = "Caern"

# Debug-Level
DEBUG_LEVELS = (
	"none",
	"normal",
	"detailed",
	"extensive",
	"extreme",
	"ultimate",
)
DEBUG_LEVEL_NONE             = 0
DEBUG_LEVEL_STD              = 1
DEBUG_LEVEL_LINENUMBERS      = len( DEBUG_LEVELS ) - 1
DEBUG_LEVEL_MODIFIES_EXPORTS = 3 ## From this debug level on, debug information is even added to the exports (printing, exporting etc.).

# Konfigurationsdatei
CONFIG_FILE = "config.ini"

# Verzeichnisnamen
# Verzeichnisname für gespeicherte Charaktere
SAVE_DIR = "save"

# Verzeichnisname für Ressourcen
RESOURCE_DIR_TEMPLATES = "templates"

# Dateiendung komprimierter Dateien.
FILE_SUFFIX_COMPRESSED = "scd"
# Dateiendung der gespeicherten Charkatere
FILE_SUFFIX_SAVE = "chr"

# Zeichen, um Listeneinträge in den XML-Dateien zu trennen
XML_SEPARATION_SYMBOL = ";"

# Format von Daten bei der Umwandlung in Strings
DATE_FORMAT      = Qt.ISODate
DATE_FORMAT_TEXT = "dd.MM.yyyy"

# Einstellungen für das Auswahl-Widget
WIDGET_SELECT_ICON_SIZE = QSize(50,50)
WIDGET_SELECT_WIDTH     = 150

### Minimale Breite für textEdit-Felder, in denen mehrzeiliger Text eingegeben werden soll.
#textEditWidthMin = 200

## Das Charakterbild darf höchstens die hier festgelegte Größe annehmen.
CHARACTER_PIC_WIDTH_MAX  = 800
CHARACTER_PIC_HEIGHT_MAX = CHARACTER_PIC_WIDTH_MAX

## Das Charakterbild wird in dem hier festgelegten Format gespeichert.
CHARACTER_PIC_FORMAT     = "png"#"jpg"

# Vordefinierte Farben
##  Wichtige Textabschnitte
COLOR_TEXT_IMPORTANT = "darkBlue"

## Die Hintergrundfarbe für ernste Geistesstörungen in der Auswahlliste.
COLOR_DERANGEMENTS_SEVERE = "sandybrown"

## Warnfarbe, wenn zuviele Punkte vergeben wurden.
COLOR_POINTS_NEGATIVE = "orangered"

## Warnfarbe, wenn zuwenige Punkte vergeben wurden.
COLOR_POINTS_POSITIVE = "chartreuse"

##  Deaktivierte textabschnitte
COLOR_TEXT_DEACTIVATED = "darkgrey"

## Kennzeichnung von Bonuseigenschaften.
COLOR_BONUS = "red"

## Symbole für die verschiedenen Waffencategorien.
ICONS_WEAPONS = {}
ICONS_WEAPONS["melee"]  = ":/items/images/svg/machete.svg"
ICONS_WEAPONS["thrown"] = ":/items/images/svg/shuriken.svg"
ICONS_WEAPONS["ranged"] = ":/items/images/svg/uzi.svg"

## Symbole für die verschiedenen magischen Gegenstände.
ICONS_ITEMS_EXTRAORDINARY = {}
ICONS_ITEMS_EXTRAORDINARY["Cursed Items"] = ":/items/images/svg/curse.svg"
ICONS_ITEMS_EXTRAORDINARY["Fetishes"]     = ":/items/images/svg/feather.svg"
ICONS_ITEMS_EXTRAORDINARY["Tokens"]       = ":/items/images/svg/spine.svg"
ICONS_ITEMS_EXTRAORDINARY["Imbued Items"] = ":/items/images/svg/wand.svg"
ICONS_ITEMS_EXTRAORDINARY["Artifacts"]    = ":/types/images/svg/pentagram.svg"

## Symbole für die verschiedenen Fahrzeugkategorien.
ICONS_AUTOMOBILES = {}
ICONS_AUTOMOBILES["Cars"]                = ":/items/images/svg/vehicle-car.svg"
ICONS_AUTOMOBILES["Trucks"]              = ":/items/images/svg/vehicle-truck.svg"
ICONS_AUTOMOBILES["Motorcycles"]         = ":/items/images/svg/vehicle-motorcycle.svg"
ICONS_AUTOMOBILES["Commercial Vehicles"] = ":/items/images/svg/vehicle-commercial.svg"

## Normaler vertikaler Abstand. Wird für Widgets eingesetzt, die zwar untereinander erscheinen, aber nicht zusammengequetscht erscheinen sollen.
SPACE_VERTICAL_STD = 5

## Der Pixelabstand zwischen Eigenschaftsblöcken. Beispielsweise der vertikale Abstand zwischen Den Fertigkeiten der verschiedenen Kategorien.
SPACE_TRAIT_CATEGORY = 10

## Maximale Anzahl von Influences für einen Vertrauten.
COMPANION_INFLUENCES_MAX = 5

## Die Anzahl, wie oft Eigenschaften mit Beschreibungstext mehrfach ausgewählt werden dürfen.
MULTIPLE_TRAITS_MAX = 4

## Die Zeit, wie lange Nachrichten in der Statuszeile angezeigt werden sollen.
TIMEOUT_STATUS_MESSAGE_DISPLAY = 10000

## Die minimale Breite für Widgets wie Fertigkeiten, Merits, Flaws etc.
TRAIT_WIDTH_MIN            = 320

## Die Minimale Breite für Textfelder für zusätzlichen Text von Eigenschaften.
TRAIT_CUSTOMTEXT_WIDTH_MIN = 100

## Die größtmögliche Höhe von Widgets, welche sich in einer Textzeile befinden.
#
# Diese Höhe wurde gewählt, um vertikalen Raum zu sparen.
WIDGET_INLINE_HEIGHT_MAX = 18

## Eigenschaftshöchstwert.
TRAIT_VALUE_MAX = 5

## Bezeichnung der Moral für alle Spezies
MORALITY_IDENTIFIER = "Morality"

## Höchstwert der Moral.
TRAIT_MORALITY_VALUE_MAX             = 10

## Höchstwert der Moral bei der ein Charakter eine Geistesstörung haben kann.
TRAIT_MORALITY_DERANGEMENT_VALUE_MAX = 7

## Startwert der Moral.
TRAIT_MORALITY_VALUE_DEFAULT         = 7

## Höchstwert der Gesundheit, von Spezies zu Spezies unterschiedlich.
TRAIT_HEALTH_VALUE_MAX = {
	"Human":      11,
	"Changeling": 11,
	"Mage":       11,
	"Vampire":    16,
	"Werewolf":   16,
}

## Höchstwert der Willenskraft.
TRAIT_WILLPOWER_VALUE_MAX = 10

## Werte der übernatürlichen Eigenschaft.
TRAIT_POWERSTAT_VALUE_MIN     = 1
TRAIT_POWERSTAT_VALUE_MAX     = 10
TRAIT_POWERSTAT_VALUE_DEFAULT = 1

## Bezeichnung der Übernatürlichen Grundeigenschaft für alle Spezies
POWERSTAT_IDENTIFIER = "Powerstat"

## Wieviele Vinculi sollen auf dem Vampir-Charakterbogen angezeigt werden.
VINCULI_COUNT_MAX = 5
VINCULI_LEVEL_MAX = 3

## Über wievielen Punkten die Eigenschaften 2 Erschaffungspunkte kosten.
#
# Alle Punkte bis einschließelich dieser Zahl kosten nur 1 Punkt pro Punkt, aber alle darüber kosten das Doppelte.
TRAIT_CREATION_DOUBLE_COST = 4

## Standardspezies eines neuen Charakters
SPECIES_INITIAL = "Human"

## Das Standardalter eines neuen Charakters
AGE_INITIAL = 21

AGE_MIN = 6

## Das Alter ab welchem der Charakter /kein/ Kind mehr ist.
AGE_ADULT = 13

HEIGHT_GIANT_MIN = {
	"Adult": 2.01,
	"Kid": 1.51,
}
HEIGHT_DWARF_MAX = {
	"Adult": 1.39,
	"Kid": 0.89,
}
HEIGHT_MAX = {
	"Adult": 2.30,
	"Kid": 1.80,
}
HEIGHT_MIN = {
	"Adult": 1.10,
	"Kid": 0.70,
}

SIZE_DEFAULT = {
	"Adult": 5,
	"Kid": 4,
}
## Sämtliche Geschlechter einschließlich der zugehörigen Symbole
GENDERS = (
	("Hermaphrodite", ":/icons/images/svg/symbolHermaphrodite.svg"),
	("Male", ":/icons/images/svg/symbolMale.svg"),
	("Female", ":/icons/images/svg/symbolFemale.svg"),
)

### Sämtliche Eigenschaftstypen.
#TYPS = (
	#"Attribute",
	#"Skill",
	#"Merit",
	#"Flaw",
	#"Power",
#)

## Die Kategorien von Attributen und Fertigkeiten sollen in einer gewissen Reihenfolge dargestellt werden.
CATEGORIES_MAIN = (
	"Mental",
	"Physical",
	"Social",
)

## Die Kategorien von Merits sollen in einer gewissen Reihenfolge dargestellt werden.
# Alle Kategorien die nicht in dieser Liste stehen, werden nach den hier aufgeführten Kategorien dargestellt.
CATEGORIES_MERITS = (
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
CATEGORIES_FLAWS = (
	"Mental",
	"Physical",
	"Social",
	#"Extraordinary",
)

ERA_INITIAL = "Modern"

## Sämtliche Eras, welcher ein Charakter angehören kann und mit welchem jahr sie beginnen.
ERAS = {
	"Modern": 1950,
	"Renaissance": 1500,
	"Ancient": 0,
}

## Sämtliche Eras, welcher ein Charakter angehören kann.
AGES = (
	"Adult",
	"Kid",
)

## Die Reihenfolge der Attribute ist derart wichtig, daß ich sie nicht automatisch bestimmen kann.
ATTRIBUTES = (
	( "Mental", (
		"Intelligence",
		"Wits",
		"Resolve",
	), ),
	( "Physical", (
		"Strength",
		"Dexterity",
		"Stamina",
	), ),
	( "Social", (
		"Presence",
		"Manipulation",
		"Composure",
	), ),
)
ATTRIBUTE_ORDER = ( "Power", "Finesse", "Resistance", )

## Die unterschiedlichen Gestalten der Werwölfe.
SHAPES_WEREWOLF = (
	"Hishu",
	"Dalu",
	"Gauru",
	"Urshul",
	"Urhan",
)


## Folgende Werte können über den Einstellungsdialog verändert werden und sollten beim Beenden des Programms gespeichert und beim Starten geladen werden. Die übergebenen Werte sind die Standartwerte, wenn im Einstellungsdialog nichts verändert wird.

# Zur Altersberechnung Kalender verwenden
#calendarForAgeCalculation = True

# Die Era automatisch aus dem Spiel-Datum ermitteln?
era_auto_select = True

# Gespeicherte Dateien komprimieren?
compress_saves = True




def version(change=False):
	"""
	Returns the version number of the program.

	Programme mit unterschieldicher Versionsnummer sind zueinander nicht notwendigerweise kompatibel.

	Unterscheiden sich Programme in ihrer Change-Nummer, aber der Rest ihrer Versionsnummer ist gleich, sollten eigentlich keine Kompatibilitätsprobleme mit den Template-Dateien und den gespeicherten Charakteren auftreten.

	Parameters:
		change: bool
			If this parameter is set to "True", the change number of the version will be returned as well.

	Returns:
		return: string
			Version number in the format <major>.<minor>.<change>. Change is omitted by default.
	"""

	version_list = (
		str(PROGRAM_VERSION["major"]),
		str(PROGRAM_VERSION["minor"]),
		str(PROGRAM_VERSION["change"]),
	)

	if change:
		return ".".join( str(val) for val in version_list )
	else:
		return ".".join( str(val) for val in version_list[:2] )


def getAge(age):
	"""
	Gibt die Alterskategorie zurück.
	"""

	if age < AGE_ADULT:
		return AGES[1]
	else:
		return AGES[0]
