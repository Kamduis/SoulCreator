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

from PySide.QtCore import Signal
from PySide.QtGui import QDateEdit

#from src.Config import Config
#from src.Debug import Debug




class DateEdit(QDateEdit):
	"""
	\brief Wird Das Datum dieses DateEdit vom Nutzer verändert, wird das Signal dateEdited ausgesandt.
	"""


	dateEdited = Signal(object)


	def __init__(self, date=None, parent=None):
		QDateEdit.__init__(self, date, parent)


	#def mousePressEvent(self, event):
		#QDateEdit.mousePressEvent(self, event)
		##Debug.debug(self.date())
		#self.dateEdited.emit(self.date())


	def mouseReleaseEvent(self, event):
		QDateEdit.mouseReleaseEvent(self, event)
		#Debug.debug(self.date())
		self.dateEdited.emit(self.date())


	def wheelEvent(self, event):
		QDateEdit.wheelEvent(self, event)
		#Debug.debug(self.date())
		self.dateEdited.emit(self.date())


	def keyPressEvent(self, event):
		QDateEdit.keyPressEvent(self, event)
		#Debug.debug(self.date())
		self.dateEdited.emit(self.date())


