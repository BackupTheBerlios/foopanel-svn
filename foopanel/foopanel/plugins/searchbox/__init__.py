
#
# Foopanel "SearchBox" plugin
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


name = "SearchBox"
version = "0.1"
description = """Provide a smart box to search on the internet."""
authors = ["Federico Pelloni <federico.pelloni@gmail.com>"]
copyright = "Copyright (C) 2005 - 2006, Federico Pelloni"
requires = {}


browser = "firefox %s"
query = "http://www.google.it/search?q=%s"


from foopanel.lib import abstract
import gtk, gobject
from os import system


class Plugin(abstract.AbstractPlugin):

    def __init__(self):
    
        abstract.AbstractPlugin.__init__(self)
        
        box = gtk.VBox(False, 2)
        box.show()
        self.add(box)
        
        lbl = gtk.Label("Web <b>search</b> for:")
        lbl.set_use_markup(True)
        lbl.set_alignment(0, 1)
        lbl.show()
        box.add(lbl)
        
        al = gtk.Alignment()
        al.show()
        box.add(al)
        
        entry = gtk.Entry()
        entry.x_done = False
        entry.set_width_chars(15)
        entry.connect("button-press-event", self.manage_click)
        entry.connect("activate", self.go)
        entry.show()
        al.add(entry)
       
        
    def go(self, entry):
    
        url = query % entry.get_text()
        system(browser % url)
        entry.x_done = True
    
    
    def manage_click(self, entry, event):
    
        if entry.x_done:
        
            entry.set_text("")
            entry.x_done = False
    
    
    
