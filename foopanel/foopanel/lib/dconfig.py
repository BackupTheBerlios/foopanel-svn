#
# Foopanel "DConfig" module
#
# Copyright (C) 2006, Federico Pelloni <federico.pelloni@gmail.com>
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

import gtk

import globals


### ABSTRACT OPTION
class og:
    
    def format(self, value): return value
    def unformat(self, vlaue): return value
    def get(self): return None
    def set(self, value): pass
    def build(self): 
        self.obj = gtk.HBox(False, 5)
        self.obj.add(gtk.Label(self.setting['label']))
        w = self.widget()
        self.obj.add(w)
        return w
    
    def __init__(self, plugin, setting):
        self.plugin = plugin
        self.setting = setting
        self.w = self.build()
        self.set(self.unformat(getattr(self.plugin.settings, self.setting['bind'][0])))
        self.w.connect(self.signal, self.save)
        
    def save(self, *args):
        value = self.get()
        setattr(self.plugin.settings, self.setting['bind'][0], self.format(value))
        getattr(self.plugin.widget, self.setting['bind'][1])(self.unformat(value))
        
    def get_widget(self):
        return self.obj

### OPTION TYPE: BOOLEAN
class option_boolean(og):
    signal = "toggled"
    widget = gtk.CheckButton
    def get(self): return self.w.get_active()
    def set(self, value): self.w.set_active(value)
    def format(self, value): return str(int(value))
    def unformat(self, value): return bool(int(value))
    
### OPTION TYPE: TEXT
class option_text(og):
    signal = "changed"
    widget = gtk.Entry
    def get(self): return self.w.get_text()
    def set(self, value): self.w.set_text(value)
    def format(self, value): return str(value)
    def unformat(self, value): return str(value)
        
    



class DConfig(gtk.Dialog):
    
    def __init__(self, plugin):
        
        self.plugin = plugin
        
        title = _("%s settings") % plugin.module.name
        
        gtk.Dialog.__init__(self, title, globals.config_dialog, (),\
                            (gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE))
                            
        self.vbox.set_border_width(5)
        
        lbl = gtk.Label()
        lbl.set_markup('<b><span size="larger">%s</span>\n%s</b>' % 
                        (_("%s plugin") % plugin.module.name, _("Settings"))
                      )
        self.vbox.pack_start(lbl, False)
        
        settings = plugin.module.config_scheme
        
        for s in settings:
            self.__new_setting(s)
        
        
    
    def __new_setting(self, setting):

        exec("s = option_%s(self.plugin, setting)" % setting['type'])
        self.vbox.add(s.get_widget())
        

