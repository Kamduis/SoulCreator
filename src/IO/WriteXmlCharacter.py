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




from PyQt4.QtCore import QObject, QIODevice, QByteArray, QBuffer

import gzip

from src.Config import Config
#from src.Error import ErrTraitType, ErrTraitCategory
#from src.Debug import Debug

## Fallback to normal ElementTree, sollte lxml nicht installiert sein.
lxmlLoadad = False
try:
	from lxml import etree
	#Debug.debug("Running with lxml.etree")
	lxmlLoadad = True
except ImportError:
	try:
		# Python 2.5
		import xml.etree.cElementTree as etree
		#Debug.debug("running with cElementTree on Python 2.5+")
	except ImportError:
		try:
			# Python 2.5
			import xml.etree.ElementTree as etree
			#Debug.debug("running with ElementTree on Python 2.5+")
		except ImportError:
			print("Failed to import ElementTree from any known place")




class WriteXmlCharacter(QObject):
	"""
	@brief Schreibt die Charakterwerte in eine Datei.
	"""


	def __init__(self, character, parent=None):
		super(WriteXmlCharacter, self).__init__(parent)

		self.__character = character


	def write( self, fileName ):
		"""
		Startet den Schreibvorgang.
		"""

		tree = self.buildXmlTree()
		self.writeFile(tree, fileName)


	def buildXmlTree(self):
		"""
		Erzeugt den Element-Baum, der später in eine XML-Datei geschrieben werden kann.
		"""

		root = etree.Element(Config.PROGRAM_NAME, version=Config.version())

		etree.SubElement(root, "species").text = self.__character.species

		etree.SubElement(root, "era").text = self.__character.era

		## Identität
		identities = etree.SubElement(root, "identities")
		forenames = " ".join(self.__character.identity.forenames)
		etree.SubElement(identities, "identity",
			forenames=forenames,
			surname=self.__character.identity.surname,
			honorname=self.__character.identity.honorname,
			nickname=self.__character.identity.nickname,
			supername=self.__character.identity.supername,
			gender=self.__character.identity.gender,
		)

		## Daten
		etree.SubElement(root, "dates",
			birth=self.__character.dateBirth.toString(Config.DATE_FORMAT),
			becoming=self.__character.dateBecoming.toString(Config.DATE_FORMAT),
			game=self.__character.dateGame.toString(Config.DATE_FORMAT),
		)

		etree.SubElement(root, "virtue").text = self.__character.virtue

		etree.SubElement(root, "vice").text = self.__character.vice

		breedElement = etree.SubElement(root, "breed")
		breedElement.text = self.__character.breed
		if self.__character.bonus:
			breedElement.attrib["bonusType"] = self.__character.bonus["type"]
			breedElement.attrib["bonusName"] = self.__character.bonus["name"]
			if "specialty" in self.__character.bonus:
				breedElement.attrib["bonusSpecialty"] = self.__character.bonus["specialty"]
		if self.__character.species == "Changeling":
			breedElement.attrib["kith"] = self.__character.kith

		etree.SubElement(root, "faction").text = self.__character.faction

		etree.SubElement(root, "organisation").text = self.__character.organisation

		etree.SubElement(root, "party").text = self.__character.party

		etree.SubElement(root, "height").text = str(self.__character.height)

		etree.SubElement(root, "weight").text = str(self.__character.weight)

		etree.SubElement(root, "eyes").text = self.__character.eyes

		etree.SubElement(root, "hair").text = self.__character.hair

		etree.SubElement(root, "nationality").text = self.__character.nationality

		etree.SubElement(root, "description").text = self.__character.description

		etree.SubElement(root, "powerstat").text = str(self.__character.powerstat)

		etree.SubElement(root, "morality").text = str(self.__character.morality)

		## Geistesstörungen
		derangements = etree.SubElement(root, "derangements")
		for item in self.__character.derangements.items():
			if item[1]:
				etree.SubElement(derangements, "derangement", morality=str(item[0])).text = item[1]

		## Eigenschaften
		traits = etree.SubElement(root, "Traits")
		for item in self.__character.traits:
			traitTypeExists = False
			traitType = None
			for subitem in self.__character.traits[item]:
				traitCategoryExists = False
				traitCategory = None
				for subsubitem in self.__character.traits[item][subitem].values():
					## Eigenschaften müssen nur dann gespeichert werden, wenn ihr Wert != 0 ist und sie für die aktuell gewählte Spezies zur Verfügung stehen.
					if ( subsubitem.value != 0 and (not subsubitem.species or subsubitem.species == self.__character.species) ):
						if not traitTypeExists:
							traitType = etree.SubElement(traits, "Type", name=item)
							traitTypeExists = True
						if not traitCategoryExists:
							traitCategory = etree.SubElement(traitType, "Category", name=subitem)
							traitCategoryExists = True
						trait = etree.SubElement(traitCategory, "trait",
							name=subsubitem.name,
							value=str(subsubitem.value),
						)
						# Zusatztext
						if item != "Subpower" and subsubitem.custom:
							trait.attrib["customText"] =  str( subsubitem.customText )
						# Spezialisierungen
						if subsubitem.specialties:
							etree.SubElement(trait, "specialties").text = Config.XML_SEPARATION_SYMBOL.join( str(n) for n in subsubitem.specialties )

		## Gegenstände
		items = etree.SubElement(root, "Items")
		if self.__character.weapons:
			weapons = etree.SubElement(items, "Weapons")
			for category in self.__character.weapons:
				weaponCategory = etree.SubElement(weapons, "Category", name=category)
				for weapon in self.__character.weapons[category]:
					etree.SubElement(weaponCategory, "weapon").text = weapon
		if self.__character.armor:
			etree.SubElement(items, "armor", dedicated=str(self.__character.armor["dedicated"])).text = self.__character.armor["name"]
		if self.__character.equipment or self.__character.magicalTool:
			equipment = etree.SubElement(items, "Equipment")
			for item in self.__character.equipment:
				etree.SubElement(equipment, "equipment").text = item
			if self.__character.magicalTool:
				etree.SubElement(equipment, "magicalTool").text = self.__character.magicalTool
		if self.__character.automobiles:
			automobiles = etree.SubElement(items, "Automobiles")
			for typ in self.__character.automobiles:
				itemType = etree.SubElement(automobiles, "Type", name=typ)
				for automobile in self.__character.automobiles[typ]:
					etree.SubElement(itemType, "item").text = automobile
		if self.__character.extraordinaryItems:
			extraordinaries = etree.SubElement(items, "ExtraordinaryItems")
			for typ in self.__character.extraordinaryItems:
				itemType = etree.SubElement(extraordinaries, "Type", name=typ)
				for extraordinaryItem in self.__character.extraordinaryItems[typ]:
					etree.SubElement(itemType, "item").text = extraordinaryItem

		## Spezialseigenschaften der Spezies
		if self.__character.nimbus:
			etree.SubElement(root, "nimbus").text = self.__character.nimbus
		if self.__character.paradoxMarks:
			etree.SubElement(root, "paradoxMarks").text = self.__character.paradoxMarks
		if any((x.name and x.value > 0) for x in self.__character.vinculi):
			vinculi = etree.SubElement(root, "vinculi")
			for item in self.__character.vinculi:
				if item.name and item.value > 0:
					etree.SubElement(vinculi, "vinculum", value=str(item.value)).text = item.name
		companion = etree.SubElement(
			root,
			"companion",
			name = self.__character.companionName,
			power = str(self.__character.companionPower),
			finesse = str(self.__character.companionFinesse),
			resistance = str(self.__character.companionResistance),
			size = str(self.__character.companionSize),
			speedFactor = str(self.__character.companionSpeedFactor),
		)
		for item in self.__character.companionNumina:
			etree.SubElement(companion, "numen").text = item
		for item in self.__character.companionInfluences:
			if item.name and item.value > 0:
				etree.SubElement(companion, "influence", value=str(item.value)).text = item.name
		if self.__character.companionBan:
			etree.SubElement(companion, "ban").text = self.__character.companionBan
		

		if self.__character.picture:
			imageData = QByteArray()
			imageBuffer = QBuffer(imageData)
			imageBuffer.open(QIODevice.WriteOnly)
			self.__character.picture.save(imageBuffer, Config.CHARACTER_PIC_FORMAT)	# Schreibt das Bild in ein QByteArray im angegebenen Bildformat.
			imageData = imageData.toBase64().data()
			etree.SubElement(root, "picture").text = imageData.decode("UTF-8")

		return root


	def __writeTreeToFile(self, fileObject, tree):
		if lxmlLoadad:
			fileObject.write(etree.tostring(tree, pretty_print=True, encoding='UTF-8', xml_declaration=True))
		else:
			fileObject.write(etree.tostring(tree, encoding='UTF-8'))



	def writeFile(self, tree, fileName):
		"""
		Schreibt den Elementbaum in eine Datei.

		Die Charaktere werden als komprimierte Datei gespeichert.
		"""

		## In die Datei schreiben.
		if Config.COMPRESS_SAVES:
			with gzip.open(fileName, "w") as fileObject:
				self.__writeTreeToFile(fileObject, tree)
		else:
			with open(fileName, "w") as fileObject:
				self.__writeTreeToFile(fileObject, tree)
