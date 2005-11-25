
#
# Foopanel "WINDOWLIST" plugin
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


name = "WindowList"
version = "0.1"
description = "List of currently open applications"
authors = ["Federico Pelloni <federico.pelloni@gmail.com>"]
requires = {"gnome-python-extras": "wnck"}
expand = True



from foopanel.lib import abstract
from foopanel import config
import wnck
import gtk, gtk.gdk


class Plugin(abstract.AbstractPlugin):

    
    def __init__(self):
    
        abstract.AbstractPlugin.__init__(self)
        
        self.set_border_width(3)
        
        screen = wnck.screen_get_default()
        
        tb = wnck.Tasklist(screen)
        tb.show()
        
        self.add(tb)
        
        
        
        
        
        
        
        