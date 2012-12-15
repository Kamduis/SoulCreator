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




from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget

#import src.Config as Config
#from src import Error
#from src.Debug import Debug

from ui.ui_SpecialtiesWidget import Ui_SpecialtiesWidget




class SpecialtiesWidget(QWidget):
	"""
	@brief Widget für die Wahl der Spezialisierungen.

	\todo Es wäre toll, wenn der Benutzer eigene Spezialisierungen eintragen könnte, zusätzlich zu denen, die schon angeboten werden.
	"""


	def __init__(self, template, parent=None):
		super(SpecialtiesWidget, self).__init__(parent)

		#self.__character = character
		self.__storage = template

		self.__trait = None

		self.ui = Ui_SpecialtiesWidget()
		self.ui.setupUi(self)

		self.ui.lineEdit_newSpecialty.textChanged.connect(self.__enableOrDisableButtonAdd)
		self.ui.pushButton_add.clicked.connect(self.addSpecialty)
		self.ui.listWidget_specialties.itemStateChanged.connect(self.modifyTrait)

		## Zu Beginn ist es nicht Möglich, irgendetwas zu tun.
		self.setEnabled(False)
		self.ui.pushButton_add.setEnabled(False)


	def setSpecialties( self, specialties ):
		for item in specialties:
			state = Qt.Unchecked
			isBonus = False
			if ( item in self.__trait.totalspecialties ):
				state = Qt.Checked
				if ( item in self.__trait.bonusSpecialties ):
					isBonus = True

			self.ui.listWidget_specialties.addCheckableItem( item, state, isBonus )
		self.setEnabled(True)
		## Auch wenn Spezialisierungen vorhanden sind, heißt das nicht, daß wir den Hinzufügen-Knopf auch erlauben dürfen.
		#self.ui.pushButton_add.setEnabled(False)


	def addSpecialty(self):
		"""
		Fügt den Spezialisierungen den Inhalt des LineEdits hinzu.
		"""

		newSpecialty = self.ui.lineEdit_newSpecialty.text()
		self.ui.listWidget_specialties.addCheckableItem( newSpecialty, Qt.Checked )
		## Neue Spezialisierungen nicht nur der Liste, sondern auch der Eigenschaft hinzufügen.
		if newSpecialty not in self.__trait.totalspecialties:
			self.__trait.appendSpecialty(newSpecialty)
		#Debug.debug(self.__trait.totalspecialties)
		## Ist die neue Spezialisierung hinzugefügt, wird die Zeile wieder geleert.
		self.ui.lineEdit_newSpecialty.setText("")


	def showSpecialties(self, sw, trait):
		self.ui.listWidget_specialties.clear()
		if sw:
			#Debug.debug("Zeige Spezialisierungen von {}".format(trait.name))
			if self.__trait != trait:
				# Vorherige Verbindung lösen.
				if self.__trait:
					self.__trait.totalspecialtiesChanged.disconnect(self.reshowSpecialties)
				self.__trait = trait
				# Neue Verbindung aufbauen, damit beim Laden des Charakters die angezeigten Spezialisierungen automatisch richtig abgehakt werden.
				self.__trait.totalspecialtiesChanged.connect(self.reshowSpecialties)
			#Debug.debug(self.__trait)
			for item in self.__storage:
				for subitem in self.__storage[item].items():
					#Debug.debug(subitem)
					if subitem[0] == trait.name:
						self.setSpecialties(subitem[1]["specialties"])
						## Jetzt müssen noch alle Spezialisierungen angezeigt werden, die zwar im Charkater stehen, aber nicht teil der Standard-Spezialisierungen sind.
						for charaSpecialty in self.__trait.totalspecialties:
							if charaSpecialty not in subitem[1]["specialties"]:
								self.ui.listWidget_specialties.addCheckableItem( charaSpecialty, Qt.Checked )
						return
		else:
			#Gibt es nichts zum Anzeigen, wird das ganze Widget disabled.
			self.setEnabled(False)


	def reshowSpecialties(self):
		self.ui.listWidget_specialties.clear()
		for item in self.__storage:
			for subitem in self.__storage[item].items():
				if subitem[0] == self.__trait.name:
					#Debug.debug(subitem[1]["specialties"])
					self.setSpecialties(subitem[1]["specialties"])
					## Jetzt müssen noch alle Spezialisierungen angezeigt werden, die zwar im Charkater stehen, aber nicht teil der Standard-Spezialisierungen sind.
					for charaSpecialty in self.__trait.totalspecialties:
						#Debug.debug(charaSpecialty)
						if charaSpecialty not in subitem[1]["specialties"]:
							self.ui.listWidget_specialties.addCheckableItem( charaSpecialty, Qt.Checked )
					return



	def modifyTrait(self, name, state):
		#Debug.debug("Test")
		if state == Qt.Checked:
			if name not in self.__trait.totalspecialties:
				self.__trait.appendSpecialty(name)
		elif name in self.__trait.specialties:
			self.__trait.removeSpecialty(name)


	def __enableOrDisableButtonAdd(self, text):
		"""
		Der Hinzufügen-Knopf darf nur enabled sein, wenn es einen \emph{neuen} Text zum Hinzufügen gibt.
		"""

		if text:
			textIsUnique = True
			for i in range(self.ui.listWidget_specialties.count()):
				if self.ui.listWidget_specialties.item(i).text() == text:
					textIsUnique = False
					break

			if textIsUnique:
				self.ui.pushButton_add.setEnabled(True)
			else:
				self.ui.pushButton_add.setEnabled(False)
		else:
			self.ui.pushButton_add.setEnabled(False)

