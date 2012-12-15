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
from PyQt4.QtGui import QWidget, QHBoxLayout, QCheckBox, QLineEdit

import src.Config as Config
#from src.Tools import ListTools
from src.Datatypes.StandardTrait import StandardTrait
#import src.Debug as Debug




class CheckTrait(QWidget):
	"""
	\brief An- bzw. Abwählbare Eigenschaft.

	Diese Eigensachft ist ähnlich wie CharaTrait mit den Eigenschaften im Speicher verknpüft, allerdings besitzen sie keine Werte, sondern sind nur an- oder Abwählbar. Beispiel für eine solche Eigenscahft sind die Nachteile.
	"""

	def __init__(self, trait, parent=None):
		super(CheckTrait, self).__init__(parent)

		self.__trait = trait

		#character = StorageCharacter::getInstance();

		self.__layout = QHBoxLayout()
		self.setLayout( self.__layout )

		self.__checkBox = QCheckBox()
		self.__checkBox.setText( trait.name )
		self.__checkBox.setMaximumHeight( Config.WIDGET_INLINE_HEIGHT_MAX )

		self.__lineEdit = QLineEdit()
		#self.__lineEdit.setMinimumWidth( Config.TRAIT_CUSTOMTEXT_WIDTH_MIN )
		self.__lineEdit.setMaximumHeight(Config.WIDGET_INLINE_HEIGHT_MAX)

		self.__layout.addWidget( self.__checkBox )
		self.__layout.addStretch()
		self.__layout.addWidget( self.__lineEdit )

		self.__checkBox.stateChanged.connect(self.setTraitValue)
		self.__lineEdit.textChanged.connect(self.setTraitCustomText)
		self.__trait.valueChanged.connect(self.setValue)
		if type(self.__trait) == StandardTrait:
			self.__trait.customTextChanged.connect(self.setText)
		self.__trait.availableChanged.connect(self.setEnabled)


	def __getValue(self):
		return self.__checkBox.checkState()

	def setValue(self, value):
		if value == 0:
			checkState = Qt.Unchecked
		elif value == 1:
			checkState = Qt.PartiallyChecked
		else:
			checkState = Qt.Checked

		self.__checkBox.setCheckState(checkState)

	value = property(__getValue, setValue)


	def setTraitValue( self, value ):
		"""
		Legt den Wert der Eigenschaft im Speicher fest.
		"""
		
		if ( self.__trait.value != value ):
			self.__trait.value = value


	def setText(self, text):
		"""
		Legt den Zusatztext in diesem Widget fest.
		"""
		
		self.__lineEdit.setText(text)


	def setTraitCustomText( self, text ):
		"""
		Legt den Zusatztext der Eigenschaft im Speicher fest.
		"""
		
		if ( self.__trait.customText != text ):
			self.__trait.customText = text


	def setDescriptionHidden( self, sw ):
		"""
		Mit dieser Methode verstecke ich die Textzeile, in welcher zusätzlicher Beschreibungstext eingegeben werden kann.
		"""

		if ( sw ):
			self.__lineEdit.hide()
		else:
			self.__lineEdit.show()


	def hideOrShowTrait(self, species=None, age=None, era=None, breed=None, faction=None):
		"""
		Versteckt oder zeigt diese Eigenschaft.

		\note age und era gibt es zwar nicht bei SubPowerTrait, aber damit diese Funktion mit StorageCharacter.traitVisibleReasonChanged kompatible bleibt, werden sie als Argument übergeben.
		"""

		visible = True
		# Es können nur Eigenschaften versteckt werden, die einen age- bzw. era-Eintrag besitzen.
		if (
			(species and self.__trait.species and self.__trait.species != species) or
			#(age and self.__trait.age and self.__trait.age != age) or
			#(era and self.__trait.era and era not in self.__trait.era) or
			((breed or faction) and self.__trait.only and breed not in self.__trait.only and faction not in self.__trait.only)
		):
			visible = False

		self.setVisible(visible)


	#def hideOrShowTrait(self, species):
		#"""
		#Versteckt oder zeigt diese Eigenschaft, je nach gewählter Spezies.
		#"""

		#if (not self.__trait.species or self.__trait.species == species):
			#self.setHidden(False)
			##Debug.debug("Verstecke {}, da Alter {} bzw. Ära {}".format(self.name, age, era))
		#else:
			#self.setHidden(True)

