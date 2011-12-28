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

##include <QDebug>

##include "Exceptions/Exception.h"
#// #include "Config/Config.h"

##include "ReadXml.h"



from __future__ import division, print_function

#from PySide.QtCore import Qt
from PySide.QtGui import QComboBox

#from src.Config import Config




class CharaSpecies(QComboBox):
	"""
	@brief Mit den gespeicherten Werten vernetzte Darstellung der Spezies auf dem Charakterbogen.

	Diese Combobox ist direkt mit den im Speicher vorgehaltenen Charakterdaten verknüpft. Verändert sich das Widget, wird der Speicher aktualisiert, verändert sich der Speicher, wird das Widget aktualisiert.
	"""

	def __init__(self, parent=None):
		QComboBox.__init__(self, parent)
		#v_species = cv_Species::SpeciesNo;

		#character = StorageCharacter::getInstance();
		#StorageTemplate storage;

		#for( int i = 0; i < storage.species().count(); ++i ) {
			#if( cv_Species::toSpecies( storage.species().at( i ).name ) != cv_Species::SpeciesAll ) {
				#addItem( QIcon( ":/icons/images/Skull-" + storage.species().at( i ).name + ".png" ), storage.species().at( i ).name );
			#}
		#}

		#// Wenn sich das Widget ändert, muß sich der Speicher ändern.
		#connect( this, SIGNAL( currentIndexChanged( int ) ), this, SLOT( emitSpeciesChanged( int ) ) );
		#connect( this, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( setStorageSpecies( cv_Species::SpeciesFlag ) ) );
		#// Wenn sich der Speicher ändert, muß sich die ComboBox ändern.
		#connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( setSpecies( cv_Species::SpeciesFlag ) ) );


#CharaSpecies::~CharaSpecies() {
	#// Da es sich um eine Singleton-Klasse handelt kann ich sie nicht zerstören.
#// 	delete character;
#}


#cv_Species::SpeciesFlag CharaSpecies::species() const {
	#return v_species;
#}
#void CharaSpecies::setSpecies( cv_Species::SpeciesFlag species ) {
#// 	qDebug() << Q_FUNC_INFO << "Funktion zum Ändern der Spezies wird aufgerufen!";

	#if( v_species != species ) {
		#v_species = species;

		#int speciesIndex = findText( cv_Species::toString( species ) );

		#if( speciesIndex > -1 ) {
			#setCurrentIndex( speciesIndex );
		#} else {
			#throw eSpeciesNotExisting();
		#}

		#emit speciesChanged( species );
	#}
#}


#void CharaSpecies::emitSpeciesChanged( int index ) {
	#StorageTemplate storage;

	#for( int i = 0; i < storage.species().count(); ++i ) {
		#if( itemText( index ) == storage.species().at( i ).name ) {
			#emit speciesChanged( cv_Species::toSpecies( storage.species().at( i ).name ) );
			#return;
		#}
	#}

	#throw eSpeciesNotExisting();
#}


#void CharaSpecies::setStorageSpecies( cv_Species::SpeciesFlag species ) {
	#character->setSpecies( species );
#}

