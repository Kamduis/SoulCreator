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
from PyQt4.QtGui import QDateEdit

#import src.Config as Config
#from src.Debug import Debug




class DateEdit(QDateEdit):
	"""
	\brief Wird Das Datum dieses DateEdit vom Nutzer verändert, wird das Signal dateEdited ausgesandt.
	"""


	dateEdited = Signal(object)


	def __init__(self, date=None, parent=None):
		super(DateEdit, self).__init__(parent)


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


