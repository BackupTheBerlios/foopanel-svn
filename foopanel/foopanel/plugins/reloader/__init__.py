
#
# Foopanel "Reloader" plugin
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

name = "Reloader"
version = "0.1"
description = "Quickly reload a plugin without restarting Foopanel"
authors = ["Federico Pelloni <federico.pelloni@gmail.com>"]
copyright = "Copyright (C) 2005 - 2006, Federico Pelloni"
requires = {}
register_functions = { 'on_finish': ['build_list', 'set_callbacks'] }


from foopanel.lib import abstract, globals, functions
import gtk
import types


class Plugin(abstract.Plugin):

    def __init__(self):
    
        abstract.Plugin.__init__(self)
        
        box = gtk.VBox(False, 2)
        box.show()
        self.add(box)
        
        self.model = gtk.ListStore(str, int)
        
        self.combo = gtk.ComboBox(self.model)
        self.combo.show()
        box.add(self.combo)
        
        cell = gtk.CellRendererText()
        self.combo.pack_start(cell, True)
        self.combo.add_attribute(cell, 'text', 0)
        
        btn = gtk.Button(None, gtk.STOCK_REFRESH)
        btn.connect("clicked", self.manage_click)
        btn.show()
        box.add(btn)
        
       
        
    
    def _cb_added_component(self, container, plugin):
    
        #pos = container.get_children().index(plugin)
        #self.model.insert(pos, (globals.plugins[-1][0], len(globals.plugins)-1))
        self.model.clear()
        self.build_list()
        
        
    def _cb_removed_component(self, container, plugin):
    
        self.model.clear()
        self.build_list()
        
        
        
    def build_list(self):
    
        x = 0
        for m in globals.plugins:
            self.model.append((m[0], x))
            x += 1
            
            
    def set_callbacks(self):
    
        globals.plugin_manager.connect('add', self._cb_added_component)
        globals.plugin_manager.connect('remove', self._cb_removed_component)
            
            
            
    def manage_click(self, button):
    
        p = self.combo.get_active()
        
        if p < 0:
            return
            
        name, index = self.model[p]
        
        if name == "Reloader":
            return
            
        functions.reload_plugin(index)
        
        

