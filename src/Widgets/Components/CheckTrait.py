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

from PySide.QtCore import Qt
from PySide.QtGui import QWidget, QHBoxLayout, QCheckBox, QLineEdit

from src.Config import Config
#from src.Tools import ListTools
from src.Datatypes.StandardTrait import StandardTrait
from src.Debug import Debug




class CheckTrait(QWidget):
	"""
	\brief An- bzw. Abwählbare Eigenschaft.

	Diese Eigensachft ist ähnlich wie CharaTrait mit den Eigenschaften im Speicher verknpüft, allerdings besitzen sie keine Werte, sondern sind nur an- oder Abwählbar. Beispiel für eine solche Eigenscahft sind die Nachteile.
	"""

	def __init__(self, trait, parent=None):
		QWidget.__init__(self, parent)

		self.__trait = trait

		#character = StorageCharacter::getInstance();

		self.__layout = QHBoxLayout()
		self.setLayout( self.__layout )

		self.__checkBox = QCheckBox()
		self.__checkBox.setText( trait.name )
		self.__checkBox.setMaximumHeight( Config.inlineWidgetHeightMax )

		self.__lineEdit = QLineEdit()
		#self.__lineEdit.setMinimumWidth( Config.traitCustomTextWidthMin )
		self.__lineEdit.setMaximumHeight(Config.inlineWidgetHeightMax)

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


	def hideOrShowTrait_species(self, species):
		"""
		Versteckt oder zeigt diese Eigenschaft, je nach gewählter Spezies.
		"""

		if (not self.__trait.species or self.__trait.species == species):
			self.setHidden(False)
			#Debug.debug("Verstecke {}, da Alter {} bzw. Ära {}".format(self.name, age, era))
		else:
			self.setHidden(True)

