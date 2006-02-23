
#
# Foopanel "PAGER" plugin
# 
# Copyright (C) 2005 - 2006, Federico Pelloni <federico.pelloni@gmail.com>
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
version = "0.2"
description = "Draw a pager on the panel"
authors = ["Federico Pelloni <federico.pelloni@gmail.com>"]
copyright = "Copyright (C) 2005 - 2006, Federico Pelloni"
requires = {"gnome-python-extras": "wnck"}
expand = False
register_functions = { 'on_resize': ['resize'] }



from foopanel.lib import abstract, globals
import gtk, gtk.gdk
import wnck

border = 3
row_height = 25

class Plugin(abstract.AbstractPlugin):

    def __init__(self, settings):
    
        abstract.AbstractPlugin.__init__(self)
        
        self.set_border_width(border)
        
        self.screen = wnck.screen_get_default()
        self.screen.connect("workspace-created", lambda s,w: self.resize())
        self.screen.connect("workspace-destroyed", lambda s,w: self.resize())
        
        self.pager = wnck.Pager(self.screen)
        
        #rect = gtk.gdk.Rectangle(0, 0, 10, 25)
        #pager.size_allocate(rect)
        
        al = gtk.Alignment(0.5, 0.5, 0, 0)
        al.show()

        self.add(al)
        al.add(self.pager)

        self.show_all()
    
    
    def resize(self):
        
        ws = self.screen.get_workspace_count()
        
        rows = min(max(int(int(globals.requested_size[1] - 2*border) / row_height), 1), ws)
        if ws % 2 != 0: ws += 1
        cols = ws / rows
        
        if rows * cols < ws:
            cols += 1
            rows = ws/cols
            
        width =  cols * row_height*4/3
        height = row_height * rows
        
        self.pager.set_size_request(width, height)
        self.pager.set_n_rows(rows)
        
        
        
        
