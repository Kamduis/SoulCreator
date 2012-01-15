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

from PySide.QtCore import Qt, Signal
from PySide.QtGui import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QComboBox

from src.Config import Config
#from src import Error
#from ReadXml import ReadXml
from src.Widgets.Components.Dot import Dot
from src.Debug import Debug




class MoralityWidget(QWidget):
	"""
	@brief Dieses Widget stellt die Moral-Tabelle dar.

	Diese Tabelle zeigt die aktuelle Moralstufe an und bietet Platz für das Eintragen von Geistesstörungen.

	\todo Ich bin mit den Geistesstörungen noch nicht gänzlich zufrieden. Es besteht die Gefahr, daß einzelne Geistesstörungen immer und immer wieder zu dem Charkater hinzugefügt werden und dementsprechend das Programm und den gespeicherten Charakter aufblähen können.
	"""


	valueChanged = Signal(int)


	def __init__(self, template, character, parent=None):
		QWidget.__init__(self, parent)

		self.__character = character
		self.__storage = template

		self.__value = 0

		self.__layout = QVBoxLayout()
		self.setLayout( self.__layout )

		self.__layoutHeading = QHBoxLayout()
		self.__layout.addLayout(self.__layoutHeading)

		self.__labelHeading = QLabel("Test")
		self.__labelHeading.setAlignment(Qt.AlignHCenter)

		self.__layoutHeading.addStretch()
		self.__layoutHeading.addWidget(self.__labelHeading)
		self.__layoutHeading.addStretch()

		self.__layoutTab = QGridLayout()
		# Nur die Spalte mit den GEistesstörungen soll sich strecken dürfen.
		self.__layoutTab.setColumnStretch(1, 1)
		self.__layout.addLayout(self.__layoutTab)

		self.__dotList = {}

		for i in xrange(Config.moralityTraitMax):
			label = QLabel("{}".format(Config.moralityTraitMax - i))
			label.setAlignment(Qt.AlignRight)
			self.__layoutTab.addWidget(label, i, 0)

			dot = Dot()
			# Den Punkt zu einer Liste hinzufügen, um später zu sehen, welcher Punkt den Wert änderte.
			self.__dotList[Config.moralityTraitMax - i] = dot
			self.__layoutTab.addWidget(dot, i, 2)

			if i >= Config.moralityTraitMax - Config.derangementMoralityTraitMax:
				box = QComboBox()
				self.__layoutTab.addWidget(box, i, 1)

			dot.clicked.connect(self.__calcValue)

		self.__character.speciesChanged.connect(self.setMoralityName)
		self.__character.moralityChanged.connect(self.setValue)
		self.valueChanged.connect(self.__character.setMorality)


#MoralityWidget::MoralityWidget( QWidget *parent ) : QWidget( parent )  {
	#v_value = 0;

	#layout = new QGridLayout( this );
	#setLayout( layout );

	#labelHeader = new QLabel();
	#labelHeader->setAlignment( Qt::AlignHCenter );

	#layout->addWidget( labelHeader, 0, 0, 1, 3 );

	#int layoutLine;

	#QList< cv_Trait > list;
	#v_category = cv_AbstractTrait::getCategoryList( cv_AbstractTrait::Derangement );

	#for ( int i = Config::moralityTraitMax; i > 0; i-- ) {
		#layoutLine =  Config::moralityTraitMax - i + 1;

		#QLabel* label = new QLabel( QString::number( i ) );
		#TraitDots* traitDots = new TraitDots();
		#traitDots->setMaximum( 1 );

		#layout->addWidget( label, layoutLine, 0 );
		#layout->addWidget( traitDots, layoutLine, 2 );

		#if ( i <= Config::derangementMoralityTraitMax ) {
			#DerangementComboBox* comboBox = new DerangementComboBox();
			#comboBox->setMaximumHeight( Config::inlineWidgetHeightMax );

			#layout->addWidget( comboBox, layoutLine, 1 );

			#connect( comboBox, SIGNAL( currentIndexChanged( cv_Derangement ) ), this, SLOT( saveDerangements( cv_Derangement ) ) );
			#connect( character, SIGNAL( derangementsChanged() ), this, SLOT( updateDerangements() ) );
		#}

		#connect( traitDots, SIGNAL( valueClicked( int ) ), this, SLOT( resetValue( int ) ) );
	#}

	#connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( renameHeader( cv_Species::SpeciesFlag ) ) );

	#connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( updateDerangements( cv_Species::SpeciesFlag ) ) );
	#connect( character, SIGNAL( moralityChanged( int ) ), this, SLOT( setValue( int ) ) );
	#connect( this, SIGNAL( valueChanged( int ) ), character, SLOT( setMorality( int ) ) );
	#connect( this, SIGNAL( valueChanged( int ) ), this, SLOT( drawValue( int ) ) );
	#connect( this, SIGNAL( valueChanged( int ) ), this, SLOT( disableDerangements( int ) ) );

	#setValue( Config::moralityTraitDefaultValue );
#}


	def __getValue(self):
		return self.__value

	def setValue( self, value ):
		if ( self.__value != value ):
			self.__value = value
			self.__drawValue(value)
			Debug.debug(value)
			self.valueChanged.emit( value )

	value = property(__getValue, setValue)


	def __calcValue(self, value):
		"""
		Berechnet aus dem angeklickten Punkt, welchen Wert die Moral jetzt hat.
		"""
		
		#Debug.debug(self.__dotList)
		# Ist der Wert True, suche ich nach dem höchsten wahren Punkt und mache alle kleineren auch wahr.
		# Ist der Wert False, suche ich nach dem niedrigesten False punkt, und mache die höheren alle False.
		if value:
			dotsTrue = []
			for i in xrange(1, self.__layoutTab.rowCount()+1):
				if self.__dotList[i].value:
					dotsTrue.append(i)
			maxValue = max(dotsTrue)
			#Debug.debug(dotsTrue)
			for i in xrange(1, maxValue):
				self.__dotList[i].value = True
				#Debug.debug("{}: {} (Maximalwert {})".format(i, self.__dotList[i].value, maxValue))
			self.value = maxValue
		else:
			dotsFalse = []
			for i in xrange(1, self.__layoutTab.rowCount()+1):
				if not self.__dotList[i].value:
					dotsFalse.append(i)
			minValue = min(dotsFalse)
			if minValue == self.value and minValue != 1:
				self.__dotList[minValue].value = True
			else:
				for i in xrange(minValue+1, self.__layoutTab.rowCount()+1):
					self.__dotList[i].value = False
					#Debug.debug("{}: {} (Maximalwert {})".format(i, self.__dotList[i].value, minValue))
				# Intuitiverweise will man die Moral auf den Wert setzen, auf den man klickt. Aber das gilt nicht, wenn man auf den untersten Punkt klickt.
				if minValue == 1:
					self.__dotList[minValue].value = False
					self.value = 0
				else:
					self.value = minValue



	def __drawValue( self, value ):
		"""
		Ändert sich der Wert des Widgets, wird hierüber die passende Anzahl an Punkten schwarz ausgemalt.
		"""

		if value > 0:
			for i in xrange(value, len(self.__dotList)+1):
				self.__dotList[i].value = False
			for i in xrange(1, value+1):
				self.__dotList[i].value = True
		else:
			for i in xrange(1, len(self.__dotList)+1):
				self.__dotList[i].value = False


#void MoralityWidget::resetValue( int value ) {
	#"""
	#Wird mit der Maus auf den Punkten herumgeklickt, sorgt diese Funktion dafür, daß der richtige Wert des Widgets ermittelt wird.
	#"""

	#// Verändere ich einen Punkt zu 1, wird der Gesamtwert erhöht, verändere ich einen Wert zu 0 wird der Gesamtwert reduziert.
	#bool reduceValue = true;

	#if ( value > 0 ) {
		#reduceValue = false;
	#}

	#int newValue;

	#bool changeFromHere = false;

	#if ( reduceValue ) {
		#for ( int i = layout->rowCount() - 1; i > 0; i-- ) {
			#TraitDots* traitDots = qobject_cast<TraitDots*>( layout->itemAtPosition( i, 2 )->widget() );

			#if ( traitDots->value() < 1 ) {
				#newValue = layout->rowCount() - i;

				#// Der Knopf auf den ich drücke, soll schwarz bleiben. Esseidenn natürlich, es ist der unterste, und zuvor war der Wert schon 1, dann soll er abgewählt werden.

				#if ( v_value == 1 && i == layout->rowCount() - 1 ) {
					#newValue = 0;
				#}

				#break;
			#}
		#}
	#} else {
		#for ( int i = 1; i < layout->rowCount(); ++i ) {
			#TraitDots* traitDots = qobject_cast<TraitDots*>( layout->itemAtPosition( i, 2 )->widget() );

			#if ( traitDots->value() > 0 ) {
				#newValue = layout->rowCount() - i;
				#break;
			#}
		#}
	#}

	#// Hiermit wird ein zuvor weißgeklickter Punkt (Es ist ja jeweils ein 1-Punkte Trait angenommen) wieder schwarz gesetzt.
	#drawValue( newValue );

	#if ( v_value != newValue ) {
		#v_value = newValue;
#// 		qDebug() << Q_FUNC_INFO << "Neuer Wert bei Herunterzählen:" << newValue;
		#emit valueChanged( newValue );
	#}
#}


	def setMoralityName( self, species ):
		"""
		Setzt die Überschrift dieses Widgets auf einen neuen Namen. Der name hängt von der Spezies ab.
		"""

		self.__labelHeading.setText("<b>{}</b>".format(self.__storage.moralityName(species)))


#void MoralityWidget::updateDerangements( cv_Species::SpeciesFlag species ) {
	#"""
	#Belegt die Auswahlfelder für die Geistesstörungen neu, so daß immer nur jene angeboten werden, welche ein Charakter dieser Spezies haben kann.
	#"""

	#QList< Trait* > list;
	#QList< cv_Derangement > listToUse;

	#for ( int j = 0; j < v_category.count(); ++j ) {
		#list = storage->traits( cv_AbstractTrait::Derangement, v_category.at( j ) );

		#for ( int k = 0; k < list.count(); ++k ) {
			#if ( list.at( k )->species().testFlag( species ) ) {
				#cv_Derangement lcl_derangement( list.at( k )->name(), 0, list.at( k )->species(), list.at( k )->category() );

#// 				qDebug() << Q_FUNC_INFO << lcl_derangement.name << lcl_derangement.morality;

				#listToUse.append( lcl_derangement );
			#}
		#}
	#}

	#for ( int i = 0; i < Config::derangementMoralityTraitMax; ++i ) {
		#DerangementComboBox* comboBox = qobject_cast<DerangementComboBox*>( layout->itemAtPosition( layout->rowCount() - 1 - i, 1 )->widget() );
		#comboBox->clear();

		#cv_Derangement emptyDerangement;

		#comboBox->addItem( emptyDerangement );
		#comboBox->addItems( listToUse );
	#}
#}

#void MoralityWidget::updateDerangements() {
	#"""
	#
	#"""

	#QList< cv_Derangement* > list;
	#QList< cv_AbstractTrait::Category > category = cv_AbstractTrait::getCategoryList( cv_AbstractTrait::Derangement );

	#for ( int i = 0; i < category.count(); ++i ) {
		#list.append( character->derangements( category.at( i ) ) );
	#}

	#for ( int i = 0; i < Config::derangementMoralityTraitMax; ++i ) {
		#DerangementComboBox* comboBox = qobject_cast<DerangementComboBox*>( layout->itemAtPosition( layout->rowCount() - 1 - i, 1 )->widget() );

		#// Ist die Liste leer, werden alle Geistesstörungen auf Index 0 gesetzt.
		#if ( list.count() == 0 ) {
			#comboBox->setCurrentIndex( 0 );
		#} else {
			#for ( int k = 0; k < list.count(); ++k ) {
				#if ( list.at( k )->morality() == i + 1 ) {
					#comboBox->setCurrentIndex( comboBox->findText( list.at( k )->name() ) );
					#break;
				#} else if ( k == list.count() - 1 ) {	// Taucht keine Geistesstörung bei dieser Moralstufe in der Liste auzf, wird der Index auf 0 gesetzt.
					#comboBox->setCurrentIndex( 0 );
				#}
			#}
		#}
	#}
#}



#void MoralityWidget::disableDerangements( int value ) {
	#"""
	#Die ComboBox für die Geistesstörungen wird bis zu dem Wert disabled, der im Argument angegeben wird. Mit dem Disablen werden sie auch gleichzeitig auf den (leeren) Index 0 gesetzt.
	
	#disableDerangements(7) resultiert darin, daß alle FElder für GEistesstörungen disabled werden.
	#"""

	#int lcl_value = value;

	#if ( lcl_value > Config::derangementMoralityTraitMax ) {
		#lcl_value = Config::derangementMoralityTraitMax;
	#}

	#int i = 0;

	#while ( i < lcl_value ) {
		#DerangementComboBox* comboBox = qobject_cast<DerangementComboBox*>( layout->itemAtPosition( layout->rowCount() - 1 - i, 1 )->widget() );
		#comboBox->setCurrentIndex( 0 );
		#comboBox->setEnabled( false );
		#i++;
	#}

	#while ( i < Config::derangementMoralityTraitMax ) {
		#DerangementComboBox* comboBox = qobject_cast<DerangementComboBox*>( layout->itemAtPosition( layout->rowCount() - 1 - i, 1 )->widget() );
		#comboBox->setEnabled( true );
		#i++;
	#}
#}

#void MoralityWidget::saveDerangements( cv_Derangement dera ) {
	#"""
	#Speichert die gewählte Geistesstörung im Charakter.
	
	#\todo Es muß ein neuer DAtentyp für die GEiostesstörungen entwickelt werden, damit ich weiß, bei welcher Moral sie platziert werden müssen.
	
	#\todo Wenn ich weiß bei welcher Moral die Geistesstörungen platziert werden, kann ich auch beim ändern des INdex einer Geistesstörungsbox diese direkt im Charakter ändern, ohne alle löschen und neu abarbeiten zu müssen.
	#"""

	#cv_Derangement derang;

	#for ( int i = 0; i < Config::derangementMoralityTraitMax; ++i ) {
		#DerangementComboBox* comboBox = qobject_cast<DerangementComboBox*>( layout->itemAtPosition( layout->rowCount() - 1 - i, 1 )->widget() );

		#if ( comboBox->currentItem() == dera ) {
			#derang = dera;
			#derang.setMorality(i + 1);
			#break;
		#}
	#}

	#character->addDerangement( derang );
#}


