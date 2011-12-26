# -*- coding: utf-8 -*-

"""
\file
\author Victor von Rhein <victor@caern.de>

\section License

Copyright (C) 2011 by Victor von Rhein

This file is part of SoulCreator.

SoulCreator is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SoulCreator is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with SoulCreator.  If not, see <http://www.gnu.org/licenses/>.
"""




from __future__ import division, print_function

from PySide.QtGui import QWidget, QHBoxLayout, QPushButton, QLineEdit, QLabel

from src.Config import Config
from src.Widgets.Components.TraitDots import TraitDots
from src.Debug import Debug




class TraitLine(QWidget):
	"""
	@brief Die grafische Darstellung einer einzigen Eigenschaft auf dem Charakterbogen.
 
	Die Simplen Eigenschaften (z.B. Attribute) bestehen nur aus Name und Wert. Bei kompliziertere Eigenschaften müssen noch Spezialisieren und andere Parameter beachtet werden.
	"""


	def __init__(self, name, value, parent=None):
		QWidget.__init__(self, parent)

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

		#connect( traitDots, SIGNAL( valueChanged( int ) ), SIGNAL( valueChanged( int ) ) );
		#connect( traitDots, SIGNAL( valueChanged( int ) ), self, SLOT( enableSpecialties( int ) ) );
		#connect( button, SIGNAL( clicked( bool ) ), self, SIGNAL( specialtiesClicked( bool ) ) );
		#connect( lineEdit, SIGNAL( textChanged( QString ) ), self, SIGNAL( textChanged( QString ) ) );

		self.setName( name )
		self.setValue( value )
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


	def name(self):
		return self.__labelName.text()

	def setName( self, name ):
		self.__labelName.setText( name )


#QString TraitLine::text() const {
	#return lineEdit.text();
#}

#void TraitLine::setText( QString text ) {
	#lineEdit.setText( text );
#}

#void TraitLine::setButtonText( QString txt ) {
	#button.setText( txt );
#}
#void TraitLine::setButtonText( int val ) {
	#button.setText( QString::number(val) );
#}


	def value(self):
		return self.__traitDots.value()

	def setValue( self, value ):
		self.__traitDots.setValue( value )


#void TraitLine::setPossibleValues( QList< int > valueList ) {
	#traitDots.setAllowedValues( &valueList );
#}

#int TraitLine::minimum() const {
	#return traitDots.minimum();
#}

#void TraitLine::setMinimum( int value ) {
	#traitDots.setMinimum( value );
#}

#void TraitLine::setSpecialtyButtonChecked( bool sw ) {
	#button.setChecked( sw );
#}



#void TraitLine::hideSpecialties( bool sw ) {
	#if ( sw )
		#button.hide();
	#else
		#button.show();
#}

#void TraitLine::enableSpecialties( int number ) {
	#if ( number > 0 ) {
		#button.setEnabled( true );
	#} else {
		#button.setEnabled( false );
	#}
#}

#void TraitLine::hideDescription( bool sw ) {
	#if ( sw ) {
		#lineEdit.hide();
	#} else {
		#lineEdit.show();
	#}
#}

