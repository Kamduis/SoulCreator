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




import ast
import gzip

from PyQt4.QtCore import pyqtSignal as Signal
from PyQt4.QtCore import QObject, QDate, QByteArray
from PyQt4.QtGui import QPixmap

from src.Config import Config
from src.Error import ErrXmlOldVersion
from src.IO.ReadXml import ReadXml
from src.Debug import Debug

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




class ReadXmlCharacter(QObject, ReadXml):
	"""
	@brief Liest die gespeicherten Charakterwerte in das Programm.

	Diese Klasse dient dazu, einen auf Datenträger gespeicherten Charakter wieder in das Programm zu laden.
	"""


	exceptionRaised = Signal(str, str, bool)


	def __init__(self, character, parent=None):
		"""
		\warning Aufgrund der multiplen Vererbung wird nicht die super()-Methode beim Aufruf der __init__()-Methoden der Elternkalssen verwendet.
		"""

		QObject.__init__(self, parent)
		ReadXml.__init__(self)

		self.__character = character


	def read( self, fileName ):
		"""
		Startet den Lesevorgang.

		\note Diese Funktion kann sowohl normale xml-Dateien als auch mittels gzip komprimierte xml-Dateien laden.
		"""

		## Mittels lxml kann diese Funktion normale XML-Dateien und offenbar auch mittels gzip komprimierte XML-Dateien laden.
		## Das normale ElementTree-Modul kann das aber nicht.
		xmlContent = None
		try:
			xmlContent = etree.parse(fileName)
		except etree.ParseError:
			## Möglicherweise eine komprimierte Datei und lxml wurde nicht verwendet?
			xmlContent = etree.parse(gzip.GzipFile(fileName))
		xmlRootElement = xmlContent.getroot()

		versionSource = xmlRootElement.attrib["version"]

		try:
			self.checkXmlVersion( xmlRootElement.tag, versionSource, fileName )
		except ErrXmlOldVersion as e:
			descriptionText = self.tr("{description} Loading of character will be continued but errors may occur.".format(message=e.message, description=e.description))
			self.exceptionRaised.emit(e.message, descriptionText, e.critical)

		## Die Daten müssen zuerst geladen werden, damit schon beim Laden die Unterschiedung zwischen Kindern und Erwachsenen erfolgen kann.
		self.readDates(xmlContent)
		self.readCharacterInfo(xmlContent)
		self.readCharacterIdentity(xmlContent)
		self.readDerangements(xmlContent)
		self.readTraits(xmlContent)
		self.readItems(xmlContent)
		self.readSpeciesSpecials(xmlContent)
		self.readPicture(xmlContent)


	def readCharacterInfo(self, tree):
		"""
		Lese die grundlegenden Charakterinformationen aus.
		"""

		self.__character.species = tree.find("species").text
		self.__character.era = tree.find("era").text
		self.__character.virtue = tree.find("virtue").text
		self.__character.vice = tree.find("vice").text
		breedElement = tree.find("breed")
		self.__character.breed = breedElement.text
		bonus = {}
		bonus["type"] = self.getElementAttribute(breedElement, "bonusType")
		bonus["name"] = self.getElementAttribute(breedElement, "bonusName")
		bonus["specialty"] = self.getElementAttribute(breedElement, "bonusSpecialty")
		if bonus["type"] or bonus["name"]:
			self.__character.bonus = bonus
		self.__character.kith = self.getElementAttribute(breedElement, "kith")
		self.__character.faction = tree.find("faction").text
		self.__character.organisation = tree.find("organisation").text
		self.__character.party = tree.find("party").text
		self.__character.height = float(tree.find("height").text)
		self.__character.weight = int(tree.find("weight").text)
		self.__character.eyes = tree.find("eyes").text
		self.__character.hair = tree.find("hair").text
		self.__character.nationality = tree.find("nationality").text
		self.__character.description = tree.find("description").text
		self.__character.powerstat = int(tree.find("powerstat").text)
		self.__character.morality = int(tree.find("morality").text)


	def readCharacterIdentity(self, tree):
		"""
		Lese die Identitäten des Charkaters aus.

		\note Derzeit gibt es nur eine. forenames="" surname="" honorname="" nickname="" supername="" gender="Male"
		"""

		identity = tree.find("identities/identity")
		if identity is not None:
			self.__character.identity.forenames = self.getElementAttribute(identity, "forenames").split(" ")
			self.__character.identity.surname = self.getElementAttribute(identity, "surname")
			self.__character.identity.honorname = self.getElementAttribute(identity, "honorname")
			self.__character.identity.nickname = self.getElementAttribute(identity, "nickname")
			self.__character.identity.supername = self.getElementAttribute(identity, "supername")
			self.__character.identity.gender = self.getElementAttribute(identity, "gender")


	def readDates(self, tree):
		"""
		Lese die Daten aus (Geburtsdatum, Verwandlungsdatum, aktuelles Datum im Spiel).
		"""

		dates = tree.find("dates")
		self.__character.dateBirth = QDate.fromString(dates.attrib["birth"], Config.DATE_FORMAT)
		self.__character.dateBecoming = QDate.fromString(dates.attrib["becoming"], Config.DATE_FORMAT)
		self.__character.dateGame = QDate.fromString(dates.attrib["game"], Config.DATE_FORMAT)


	def readDerangements(self, tree):
		"""
		Liest die Geistesstörungen des Charakters.

		\note Es ist wichtig, daß die Geistesstörungen in der richtigen Moral-Reihenfolge eingelesen werden (hoch nach tief). Dies ist der Grund, weil schwere Geistesstörungen nicht erlaubt sind, wenn ihre milde form nicht vorhanden ist.
		"""

		derangements = {}

		derangementList = tree.findall("derangements/derangement")
		for derangement in derangementList:
			moralityValue = int(derangement.attrib["morality"])
			derangementName = derangement.text
			derangements[moralityValue] = derangementName
		
		self.__character.derangements = derangements


	def readTraits(self, tree):
		"""
		Liest die Eigenschaften des Charakters aus.

		\todo ich marschiere hier durch alle Eigenschaften, um die Eigenschaft des richtigen Namens zu finden, damit ich customText abarbeiten kann. Das geht doch bestimmt auch mit Direktzugriff.
		"""

		traitRootElement = tree.find("Traits")
		for typeElement in traitRootElement.getiterator("Type"):
			typName = typeElement.attrib["name"]
			for categoryElement in typeElement.getiterator("Category"):
				categoryName = categoryElement.attrib["name"]
				for traitElement in categoryElement.getiterator("trait"):
					traitName = traitElement.attrib["name"]
					traitCustomText = ""
					if "customText" in traitElement.attrib:
						traitCustomText = traitElement.attrib["customText"]
					traitValue = int(traitElement.attrib["value"])
					## Wenn die Eigenschaft nicht im Charakter-Speicher existiert (also in den Template-Dateien nicht vorkam), wird sie ignoriert.
					for item in self.__character.traits[typName][categoryName].values():
						if item.name == traitName:
							## Wenn eine Eigenschaft mit Zusatztext bereits im Speicher existiert, muß weitergesucht werden, bis eine Eigenschaft gleichen Namens mit identischem oder ohne Zusatztext gefunden wurde.
							if item.customText and item.customText != traitCustomText:
								continue

							item.value = traitValue
							## Zusatztext
							item.customText = traitCustomText

							## Es gibt nur einen Eintrag für specialties, aber da ich den Iterator verwende, zähle ich halt bis 1.
							for specialties in traitElement.getiterator("specialties"):
								if specialties is not None:
									specialtiesText = specialties.text
									item.specialties = [n for n in specialtiesText.split(Config.XML_SEPARATION_SYMBOL)]
							break


	def readItems(self, tree):
		"""
		Liest die Gegenstände des Charakters aus.
		"""

		self.readWeapons(tree.find("Items/Weapons"))
		self.readArmor(tree.find("Items/armor"))
		self.readEquipment(tree.find("Items/Equipment"))
		self.readAutomobiles(tree.find("Items/Automobiles"))
		self.readExtraordinaryItems(tree.find("Items/ExtraordinaryItems"))


	def readWeapons(self, root):
		"""
		Liest die Waffen des Charakters aus.
		"""

		if root is not None:
			for categoryElement in root.getiterator("Category"):
				categoryName = categoryElement.attrib["name"]
				for weaponElement in categoryElement.getiterator("weapon"):
					weaponName = weaponElement.text
					self.__character.addWeapon(weaponName, categoryName)


	def readArmor(self, root):
		"""
		Liest die Rüstung des Charakters aus.
		"""

		if root is not None:
			armorDedicated = ast.literal_eval(root.attrib["dedicated"])
			armorName = root.text
			self.__character.setArmor(armorName, armorDedicated)


	def readEquipment(self, root):
		"""
		Liest die Besitztümer des Charakters.
		"""

		if root is not None:
			for equipmentElement in list(root):
				if equipmentElement.tag == "equipment":
					equipmentName = equipmentElement.text
					self.__character.addEquipment(equipmentName)
			for magicalToolElement in list(root):
				if magicalToolElement.tag == "magicalTool":
					toolName = magicalToolElement.text
					self.__character.setMagicalTool(toolName)


	def readAutomobiles(self, root):
		"""
		Liest die Fahrzeuge des Charakters aus.
		"""

		if root is not None:
			for typeElement in list(root):
				if typeElement.tag == "Type":
					typeName = typeElement.attrib["name"]
					for element in list(typeElement):
						if element.tag == "item":
							automobileName = element.text
							self.__character.addAutomobile(automobileName, typeName)


	def readExtraordinaryItems(self, root):
		"""
		Liest die magischen Gegenstände des Charakters aus.
		"""

		if root is not None:
			for typeElement in list(root):
				if typeElement.tag == "Type":
					typeName = typeElement.attrib["name"]
					for element in list(typeElement):
						if element.tag == "item":
							extraordinaryItemName = element.text
							self.__character.addExtraordinaryItem(extraordinaryItemName, typeName)


	def readSpeciesSpecials(self, tree):
		"""
		Lese die Spezialeigenschaften der Spezies aus.
		"""

		elem = tree.find("nimbus")
		if elem is not None:
			self.__character.nimbus = elem.text

		elem = tree.find("paradoxMarks")
		if elem is not None:
			self.__character.paradoxMarks = elem.text

		elem = tree.find("vinculi")
		if elem is not None:
			i = 0
			for element in list(elem):
				if element.tag == "vinculum" and i < Config.VINCULI_COUNT_MAX:
					self.__character.vinculi[i].name = element.text
					self.__character.vinculi[i].value = int(element.attrib["value"])
					i += 1

		elem = tree.find("companion")
		if elem is not None:
			self.__character.companionName = elem.attrib["name"]
			self.__character.companionPower = int(elem.attrib["power"])
			self.__character.companionFinesse = int(elem.attrib["finesse"])
			self.__character.companionResistance = int(elem.attrib["resistance"])
			self.__character.companionSize = int(elem.attrib["size"])
			self.__character.companionSpeedFactor = int(elem.attrib["speedFactor"])
			companionNumina = []
			i = 0
			for element in list(elem):
				if element.tag == "numen":
					companionNumina.append(element.text)
				if element.tag == "influence" and i < Config.COMPANION_INFLUENCES_MAX:
					self.__character.companionInfluences[i].name = element.text
					self.__character.companionInfluences[i].value = int(element.attrib["value"])
					i += 1
				if element.tag == "ban":
					self.__character.companionBan = element.text
			self.__character.companionNumina = companionNumina


	def readPicture(self, tree):
		"""
		Ließt das Charakterbild aus.
		"""

		pictureElement = tree.find("picture")
		if pictureElement is not None:
			imageData = QByteArray.fromBase64(str(pictureElement.text))
			image = QPixmap()
			image.loadFromData(imageData, Config.CHARACTER_PIC_FORMAT)
			self.__character.picture = image


