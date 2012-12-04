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




from PyQt4.QtCore import pyqtSignal as Signal
from PyQt4.QtGui import QWidget, QHBoxLayout, QPushButton, QLineEdit, QLabel

from src.Config import Config
from src.Widgets.Components.TraitDots import TraitDots
#from src.Debug import Debug




class TraitLine(QWidget):
	"""
	@brief Die grafische Darstellung einer einzigen Eigenschaft auf dem Charakterbogen.

	Die Simplen Eigenschaften (z.B. Attribute) bestehen nur aus Name und Wert. Bei kompliziertere Eigenschaften müssen noch Spezialisieren und andere Parameter beachtet werden.
	"""


	valueChanged = Signal(int)
	bonusValueChanged = Signal(int)
	textChanged = Signal(str)
	buttonToggled = Signal(bool)


	def __init__(self, name, value, parent=None):
		super(TraitLine, self).__init__(parent)

		self.__layout = QHBoxLayout()
		#self.__layout.setMargin( 0 )
		self.setLayout( self.__layout )

		self.__labelName = QLabel( self )

		self.__button = QPushButton( self )
		self.__button.setText( "..." )
		self.__button.setMaximumHeight( Config.inlineWidgetHeightMax )
		self.__button.setCheckable( True )

		self.__lineEdit = QLineEdit( self )
		self.__lineEdit.setMinimumWidth( Config.traitCustomTextWidthMin )
		self.__lineEdit.setMaximumHeight( Config.inlineWidgetHeightMax )

		self.__traitDots = TraitDots( self )

		self.__traitDots.valueChanged.connect(self.valueChanged)
		self.__traitDots.valueChanged.connect(self.enableButton)
		self.__traitDots.bonusValueChanged.connect(self.bonusValueChanged)
		self.__button.toggled.connect(self.buttonToggled)
		self.__lineEdit.textChanged.connect(self.textChanged)

		self.name = name
		self.value = value
		#// Damit auch bei der Programminitialisierung die Spezialisierungen richtig enabled oder disabled sind.
		#enableSpecialties( value );

		self.__layout.addWidget( self.__labelName )
		self.__layout.addStretch()
		self.__layout.addWidget( self.__lineEdit )
		self.__layout.addWidget( self.__button )
		self.__layout.addWidget( self.__traitDots )



#QLabel* TraitLine::labelName() const {
	#return v_label_name;
#}


	@property
	def name(self):
		return self.__labelName.text()

	@name.setter
	def name( self, name ):
		self.__labelName.setText( name )


## Der beschreibende Text dieser Eigenschaft.
#QString TraitLine::text() const {
	#return lineEdit.text();
#}

	def setText( self, text ):
		self.__lineEdit.setText( text )


	@property
	def buttonText(self):
		"""
		Beschriftung des Knopfes.
		"""

		return self.__button.text()

	@buttonText.setter
	def buttonText( self, text ):
		self.__button.setText( str(text) )


	def __getValue(self):
		return self.__traitDots.value()

	def setValue( self, value ):
		"""
		\note Diese Funktion ist nicht privat, da ich diese Funktion als Slot benötige.
		"""

		#Debug.debug("Hurra! Setze Eigenschaft {} auf Wert {}".format(self.name(), value))
		self.__traitDots.setValue( value )

	## Der Wert, die hier dargestellten Eigenschaft.
	value = property(__getValue, setValue)


	def __getBonusValue(self):
		return self.__traitDots.bonusBonusValue()

	def setBonusValue( self, bonusBonusValue ):
		"""
		\note Diese Funktion ist nicht privat, da ich diese Funktion als Slot benötige.
		"""

		#Debug.debug("Hurra! Setze Eigenschaft {} auf Wert {}".format(self.name(), bonusBonusValue))
		self.__traitDots.setBonusValue( bonusBonusValue )

	## Der Wert, die hier dargestellten Eigenschaft.
	bonusBonusValue = property(__getBonusValue, setBonusValue)


	def setPossibleValues( self, values ):
		"""
		Legt fest, welche Werte diese Zeile annehmen darf.
		"""

		self.__traitDots.setAllowedValues( values )


#int TraitLine::minimum() const {
	#return traitDots.minimum();
#}

#void TraitLine::setMinimum( int value ) {
	#traitDots.setMinimum( value );
#}


	def __getMaximum(self):
		"""
		Der Maximalwert für die Dargestellten Punkte.
		"""

		return self.__traitDots.maximum()

	def setMaximum(self, maximum):
		self.__traitDots.setMaximum(maximum)

	maximum = property(__getMaximum, setMaximum)


	def setEnabled( self, sw=True):
		self.__labelName.setEnabled(sw)
		self.__button.setEnabled(sw)
		self.__lineEdit.setEnabled(sw)
		self.__traitDots.setEnabled(sw)


	def setSpecialtyButtonChecked( self, sw=True ):
		"""
		Aktiviere oder Deaktiviere den Spezialisierungs-Knopf.
		"""

		self.__button.setChecked( sw )


	def setSpecialtiesHidden( self, sw=True ):
		"""
		Mit dieser Methode verstecke ich die Liste der Spezialisierungen. Schließlich haben nur Fertigkeiten eine Notwendigkeit dafür.
		"""

		if ( sw ):
			self.__button.hide()
		else:
			self.__button.show()


	def setSpecialtiesEnabled( self, sw=True ):
		self.__button.setEnabled( sw )


	def setDescriptionHidden( self, sw ):
		"""
		Mit dieser Methode verstecke ich die Textzeile, in welcher zusätzlicher Beschreibungstext eingegeben werden kann.
		"""

		if ( sw ):
			self.__lineEdit.hide()
		else:
			self.__lineEdit.show()


	def enableButton( self, value):
		if value > 0:
			self.__button.setEnabled(True)
		else:
			self.__button.setChecked(False)
			self.__button.setEnabled(False)


	#def emitSpecialtiesClicked(self):
		#self.specialtiesClicked.emit(self.name)
