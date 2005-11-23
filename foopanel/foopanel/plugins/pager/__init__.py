
#
# Foopanel "PAGER" plugin
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


name = "Pager"
version = "0.1"
description = "Draw a pager on the panel"
authors = ["Federico Pelloni <federico.pelloni@gmail.com>"]
requires = {"gnome-python-extras": "wnck"}
expand = False


from foopanel.lib import abstract
from foopanel import config
import gtk, gtk.gdk
import wnck


class Plugin(abstract.AbstractPlugin):

    def __init__(self):
    
        abstract.AbstractPlugin.__init__(self)
        
        self.set_border_width(3)
        
        #self.set_size_request(int(config.height * 4 / 3), config.height)
        
        screen = wnck.screen_get_default()
        
        tb = wnck.Pager(screen)
        tb.show()
        
        rect = gtk.gdk.Rectangle(0, 0, 10, 25)
        tb.size_allocate(rect)
        tb.set_n_rows(int(config.height // 25))

        al = gtk.Alignment(0.5, 0.5, 0, 0)
        self.add(al)
        al.show()

        al.add(tb)
        
        
        
        
        
        
        
        
