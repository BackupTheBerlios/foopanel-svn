#
# Foopanel
# 
# Copyright (C) 2005, Federico Pelloni <federico.pelloni@gmail.com>
#
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#

#
# This code was stole from gsmile
# I had no will to write something like this, as I already did it
#

import gtk



def error(msg1, msg2, parent = None):
    """Show an error dialog"""

    return _shared (parent, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR,\
						  gtk.BUTTONS_OK, msg1, msg2 )


def warning(msg1, msg2, parent = None):
	"""Show a warning dialog"""

	return _shared (parent, gtk.DIALOG_MODAL, gtk.MESSAGE_WARNING,\
							  gtk.BUTTONS_OK, msg1, msg2 )
	

def info(msg1, msg2, parent = None):
	"""Show an information dialog"""

	return _shared (parent, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO,\
							  gtk.BUTTONS_CLOSE, msg1, msg2 )


def question(msg1, msg2, parent = None):
	"""Show a question dialog"""

	return _shared (parent, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION,\
							  gtk.BUTTONS_YES_NO, msg1, msg2 )
	

def _shared(parent, mode, type, buttons, msg1, msg2):
	"""Show a generic dialog (used by gui.dialog_* methods)"""

	dialog 	= gtk.MessageDialog (parent, 
								 mode,
								 type,
								 buttons,
								 None )
	
	dialog.set_markup("<span size=\"larger\" weight=\"bold\">%s</span>\n\n%s" %\
	                  (msg1, msg2) )
	
	result = dialog.run ()
	
	dialog.destroy ()
	
	return result

