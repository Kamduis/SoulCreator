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

#from PySide.QtCore import QObject

#from src.Config import Config
from src.Widgets.Components.TraitLine import TraitLine
from src.Debug import Debug




class CharaTrait(TraitLine):
	"""
	\brief Mit den gespeicherten Werten vernetzte Darstellung einer einzigen Eigenschaft auf dem Charakterbogen.
 
	Anders als \ref TraitLine, ist dieses Widget direkt mit der korrespondierenden Eigenschaft in der Klasse \ref StorageCharacter verknüpft. Ändert sich der Wert dort, wird automatisch dieses Widget entsprechend verändert. Gleichermaßen wird \ref StorageCharacter verändert, sollte der Benutzer dieses Widget ändern.
 
	\todo Solange kein Text in der TExtbox einer Eigenschaft mit Zusatztext steht, sollte der Wert nicht verändert werden können.
 
	\todo Den Parser \ref StringBoolParser erweitern, damit übriggebliebener Text nach den Ersetzungen der Eigesncahften durch ihre Werte mit 0 gleichgesetzt wird. Aktuell mache ich das durch Stringmanipulation, aber das ist natürlich langsamer.
 
	\todo eine fast identische Klasse schaffen, welche Trait anstelle von cv_Trait nutzt und direkte Siganel empfangen kann.
	"""


	def __init__(self, trait, parent=None):
		TraitLine.__init__(self, trait.name, trait.value, parent)

		self.__trait = trait

		# Falls ich mit der Maus den Wert ändere, muß er auch entsprechend verändert werden.
		self.valueChanged.connect(self.setTraitValue)
		#connect( this, SIGNAL( textChanged( QString ) ), this, SLOT( setCustomText( QString ) ) );
		#connect( this, SIGNAL( typeChanged( cv_AbstractTrait::Type ) ), this, SLOT( hideSpecialtyWidget( cv_AbstractTrait::Type ) ) );
		#connect( this, SIGNAL( typeChanged( cv_AbstractTrait::Type ) ), this, SLOT( hideDescriptionWidget() ) );
		#connect( this, SIGNAL( specialtiesClicked( bool ) ), this, SLOT( emitSpecialtiesClicked( bool ) ) );
		#connect( traitPtr(), SIGNAL( detailsChanged(int)), this, SLOT( unclickButton( int ) ) );

		#connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( hideTraitIfNotAvailable( cv_Species::SpeciesFlag ) ) );
		#connect( traitPtr(), SIGNAL( valueChanged( int ) ), this, SLOT( setValue( int ) ) );
		self.__trait.valueChanged.connect(self.setValue)

		#// Die Signale hier zu verbinden funktioniert offensichtlich nicht. Vielleicht weil einige Fertigkeiten dann noch nicht existieren.
		#connect( traitPtr(), SIGNAL( availabilityChanged(bool)), this, SLOT( setEnabled(bool)) );

		#if ( !traitPtr()->possibleValues().isEmpty() ) {
			#setPossibleValues( traitPtr()->possibleValues() );
		#}

		#hideSpecialtyWidget( trait->type() );
		#hideDescriptionWidget();


#Trait* CharaTrait::traitPtr() const {
	#return ptr_trait;
#}

#void CharaTrait::setTraitPtr( Trait* trait ) {
	#if ( ptr_trait != trait ) {
		#ptr_trait = trait;
	#}
#}


#// int CharaTrait2::value() const {
#// 	return traitPtr()->value();
#// }
#// void CharaTrait2::setValue( int val ) {
#// 	qDebug() << Q_FUNC_INFO << name() << val << value();
#// 	if ( value() != val ) {
#// 		TraitLine::setValue( val );
#// 	}
#// }

	def setTraitValue( self, value ):
		#Debug.debug("Eigenschaft {} erhält den Wert {}".format(self.__trait["name"], value))
		if self.__trait.value != value:
			self.__trait.value = value
		#Debug.debug("Eigenschaft {} hat den Wert {}".format(self.__trait["name"], self.__trait["value"]))


#QString CharaTrait::customText() const {
	#return traitPtr()->customText();
#}
#void CharaTrait::setCustomText( QString txt ) {
	#if ( traitPtr()->customText() != txt ) {
		#traitPtr()->setCustomText( txt );

		#TraitLine::setText( txt );

		#emit traitChanged( traitPtr() );
	#}
#}


#cv_AbstractTrait::Type CharaTrait::type() const {
	#return ptr_trait->type();
#}

#void CharaTrait::setType( cv_AbstractTrait::Type type ) {
	#if ( ptr_trait->type() != type ) {
		#ptr_trait->setType( type );

		#emit typeChanged( type );
		#emit traitChanged( traitPtr() );
	#}
#}

#cv_AbstractTrait::Category CharaTrait::category() const {
	#return ptr_trait->category();
#}

#void CharaTrait::setCategory( cv_AbstractTrait::Category category ) {
	#if ( ptr_trait->category() != category ) {
		#ptr_trait->setCategory( category );

		#emit traitChanged( traitPtr() );
	#}
#}

#cv_Species::Species CharaTrait::species() const {
	#return ptr_trait->species();
#}

#void CharaTrait::setSpecies( cv_Species::Species species ) {
	#if ( ptr_trait->species() != species ) {
		#ptr_trait->setSpecies( species );
#// 		emit speciesChanged(species);

		#emit traitChanged( traitPtr() );
	#}
#}


#bool CharaTrait::custom() const {
	#return ptr_trait->custom();
#}

#void CharaTrait::setCustom( bool sw ) {
	#if ( ptr_trait->custom() != sw ) {
		#ptr_trait->setCustom( sw );

		#emit traitChanged( traitPtr() );
	#}
#}

#void CharaTrait::emitSpecialtiesClicked( bool sw ) {
	#if ( ptr_traitStorage != 0 ) {
		#QList< cv_TraitDetail > listStora = ptr_traitStorage->details();
		#QList< cv_TraitDetail > listChara = traitPtr()->details();

#// 		qDebug() << Q_FUNC_INFO << traitPtr()->name() << ptr_traitStorage->name() << traitPtr()->details().count() << ptr_traitStorage->details().count();

		#for ( int i = 0; i < listStora.count(); ++i ) {
			#for ( int j = 0; j < listChara.count(); ++j ) {
				#if ( listStora.at( i ).name == listChara.at( j ).name ) {
#// 					qDebug() << Q_FUNC_INFO << sw << listStora.at( i ).name << listChara.at( j ).name << listChara.at( j ).value;
					#cv_TraitDetail traitDetail = listChara.at( j );
					#listStora.replace( i, traitDetail );
				#}
			#}
		#}

		#emit specialtiesClicked( sw, name(), listStora );
	#}
#}
#void CharaTrait::unclickButton( int val )
#{
#// 	qDebug() << Q_FUNC_INFO << val;
	#if (val < 1){
		#setSpecialtyButtonChecked(false);
		#emit specialtiesClicked( false, name(), ptr_traitStorage->details());
	#}
#}



#void CharaTrait::hideTraitIfNotAvailable( cv_Species::SpeciesFlag sp ) {
	#if ( species().testFlag( sp ) ) {
		#setHidden( false );
	#} else {
		#setValue( 0 );
		#setHidden( true );
	#}
#}

