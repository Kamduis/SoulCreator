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

from PySide.QtCore import QObject, Signal
#from PySide.QtGui import QDialog

from src.Config import Config
#from src.Widgets.Components.CharaSpecies import CharaSpecies
#from src.Widgets.Dialogs.NameDialog import NameDialog




class Identity(QObject):
	"""
	@brief Diese Klasse speichert die vollständige Identität eines Charakters.

	Jede Person besitzt eine Vielzahl von Namen, die über diese Klasse leicht zu verwalten sind.

	Bei Personen mit mehreren Identitäten, sollte eine Liste dieser Klasse angelegt werden, in welcher für jede Identität ein Eintrag vorgenommen wird. Auch ein Künstlername fällt unter diese Kategorie, solta also mit einem weiteren Listeneintrag realisiert werden.
	"""


	# Dieses Signal wird ausgesandt, wann immer sich ein Teil des Namens verändert hat.
	nameChanged = Signal()
	# Dieses Signal wird ausgesandt, wann immer sich das Geschlecht geändert hat.
	genderChanged = Signal(str)
	# Dieses Signal wird ausgesandt, wann immer sich ein Teil der Identität verändert hat.
	identityChanged = Signal()


	def __init__( self, surename="", firstname="", parent=None ):
		QObject.__init__(self, parent)
		
		# Liste zur Speicherung von Namen.
		#
		# {
		# 	"forenames": [Name1, Name2, Name3, ...],
		# 	"surename": Name,
		# 	"honorname": Name,
		# 	"nickame": Name,
		# 	"supername": Name,
		# }
		#
		# \sa firstName
		self.__name = {
			## Vorname.
			#
			# Dieser Name wurde dem Charakter von seinen Eltern gegeben. Es besteht die Möglichkeit, mehr als einen Vornamen zu besitzen, wesewegen diese Variable vom Typ StringList ist. Der erste Vorname in dieser Liste ist immer auch der Rufname.
			#
			# \sa self.firstName
			"forenames": [firstname],
			## Nachname
			#
			# Der Familienname der Eltern.
			"surename": surename,
			# Ein Beinahme, den der Charakter entweder durch ehrenvolle Taten, durch körperliche Besonderheiten oder durch Mißgeschick erworben hat.
			#
			# - der Starke
			# - die Schöne
			# - die Kleine
			# - der Treue
			"honorname": "",
			## Spitzname.
			#
			# Mit diesem Namen wird der Charakter meist von Freunden (Menschen) gerufen.
			"nickname": "",
			## Name unter den Übernatürlichen
			#
			# Dies ist der Name, der von den übrigen Kreaturen seiner Spezies verwendet wird.
			"supername": "",
		}
		
		## Geschlecht
		self.__gender = ""

		self.nameChanged.connect(self.identityChanged.emit)
		self.genderChanged.connect(self.identityChanged.emit)


	def __getForenames(self):
		return self.__name["forenames"]

	def __setForenames(self, names):
		"""
		\brief Legt die Formnamen fest.

		Das Argument wird nur dann übernommen, wenn wenigstens ein Vorname in der Liste nicht aus Whitespace besteht. Leer darf die Liste allerdings sein.
		"""
		
		if self.__name["forenames"] != names:
			self.__name["forenames"] = names
			self.nameChanged.emit()

	forenames = property(__getForenames, __setForenames)


	def __getFirstName(self):
		"""
		Rufname.
		
		Bei Personen mit nur einem Vornamen entspricht \ref firstName dem \ref foreName. Bei Personen mit mehreren Vornamen ist \ref firstName immer der allererste \ref foreName.
		"""
		
		return self.__name["forenames"][0]

	firstname = property(__getFirstName)


	def __getSurename(self):
		"""
		Nachname
		"""
		
		return self.__name["surename"]

	def __setSurename(self, name):
		if self.__name["surename"] != name:
			self.__name["surename"] = name
			self.nameChanged.emit()

	surename = property(__getSurename, __setSurename)


	def __getRealname(self):
		"""
		Geburtsname.
		
		Dieser Name wurde dem Charakter von seinen Eltern gegeben und besteht aus Rufname (\ref firstName) und Nachname (\ref sureName) plus Namenszusatz (\ref affixName).
		
		\note Die Kenntnis dieses Namens erleichtert Magiern sympathische Magie.
		"""
		
		if (not self.firstname or not self.surename):
			# In diesem Fall benötige ich keinen Abstand zwischen den Namen, da je einer leer ist.
			return "{}{}".format(firstname, surename)
		else:
			return "{} {}".format(firstname, surename)

	realname = property(__getRealname)

	
	def __getHonorname(self):
		return self.__name["honorname"]

	def __setHonorname(self, name):
		if self.__name["honorname"] != name:
			self.__name["honorname"] = name
			self.nameChanged.emit()

	honorname = property(__getHonorname, __setHonorname)


	def __getNickname(self):
		return self.__name["nickname"]

	def __setNickname(self, name):
		if self.__name["nickname"] != name:
			self.__name["nickname"] = name
			self.nameChanged.emit()

	nickname = property(__getNickname, __setNickname)


	def __getSupername(self):
		return self.__name["supername"]

	def __setSupername(self, name):
		if self.__name["supername"] != name:
			self.__name["supername"] = name
			self.nameChanged.emit()

	supername = property(__getSupername, __setSupername)


	def __getGender(self):
		return self.__gender

	def __setGender(self, gender):
		if self.__gender != gender:
			self.__gender = gender
			self.genderChanged.emit(gender)

	gender = property(__getGender, __setGender)


	def reset(self):
		for item in self.__name:
			if type(item) == list:
				item = []
			else:
				item = ""

		self.gender = Config.genders[0][0]
		self.nameChanged.emit()


	@staticmethod
	def displayNameFull( last, fores ):
		"""
		Voller Name.
		
		Die Summe aller Namen wird formatiert und als ein einziger String ausgegeben.
		"""

		displayFull = ""

		if ( fores ):
			if type(fores) == list:
				displayFull = fores[0]
				for item in fores[1:]:
					displayFull += u" {}".format(item)
			else:
				displayFull = fores

		# Vor dem Nachnamen nur dann ein Leerzeichen, wenn schon etwas davor steht.
		if ( displayFull ):
			displayFull += " "
		displayFull += last

		return displayFull


	@staticmethod
	def displayNameDisplay( last, first, nick ):
		"""
		Angezeigter Name.
		
		Dieser Name kann auf dem Charakterbogen angezeigt werden.
		"""
		
		displayDisplay = first
		if ( nick ):
			displayDisplay += u" \"{}\"".format(nick)

		# Vor dem Nachnamen nur dann ein Leerzeichen, wenn schon etwas davor steht.
		if ( displayDisplay ):
			displayDisplay += " "
		displayDisplay += last

		return displayDisplay


	@staticmethod
	def displayNameHonor( first, honor ):
		"""
		Ehrenname
		"""
		
		displayHonor = first
		if ( honor ):
			displayHonor += u" {}".format(honor)

		return displayHonor

