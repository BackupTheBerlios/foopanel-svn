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
    
    def __format(self, value): return value
    def __unformat(self, value): return value
    def get(self): return None
    def set(self, value): pass
    def build(self): 
        self.obj = gtk.HBox(False, 5)
        l = gtk.Label(self.option['label']+":")
        l.props.xalign = 0
        self.obj.add(l)
        w = self.widget()
        self.obj.add(w)
        return w
    
    def __init__(self): pass
    
    format = classmethod(__format)
    unformat = classmethod(__unformat)
    
    def initialize(self, plugin, option):
        self.plugin = plugin
        self.option = option
        self.w = self.build()
        try:
            self.set(self.unformat(getattr(self.plugin.settings, self.option['bind'][0])))
        except:
            try:
                self.set(self.option['default'])
            except:
                pass
        if self.signal is not None:
            self.w.connect(self.signal, self.save)
        
    def save(self, *args):
        value = self.get()
        try:
            # Set value in config
            setattr(self.plugin.settings, self.option['bind'][0], self.format(value))
            # Execute callback on widget
            getattr(self.plugin.widget, self.option['bind'][1])(self.unformat(value))
        except:
            raise
        
    def get_widget(self):
        return self.obj

### OPTI0N TYPE: LABEL
class option_label(og):
    signal = None
    def build(self):
        self.obj = gtk.Label()
        self.obj.set_markup(self.option['label'])
        return self.obj

### OPTION TYPE: BOOLEAN
class option_boolean(og):
    signal = "toggled"
    widget = gtk.CheckButton
    def get(self): return self.w.get_active()
    def set(self, value): self.w.set_active(value)
    def __format(self, value): return str(int(value))
    def __unformat(self, value): return bool(int(value))
    
### OPTION TYPE: TEXT
class option_text(og):
    signal = "changed"
    widget = gtk.Entry
    def get(self): return self.w.get_text()
    def set(self, value): self.w.set_text(value)
    def __format(self, value): return str(value) 
    def __unformat(self, value): return str(value)
        
### OPTION TYPE: DROPDOWN
class option_dropdown(og):
    signal = "changed"
    def build(self):
        self.__model = gtk.ListStore(str, str)
        for o in self.option['options']:
            self.__model.append(o)
        combo = gtk.ComboBox(self.__model)
        cr = gtk.CellRendererText()
        combo.pack_start(cr)
        combo.add_attribute(cr, 'text', 1)
        self.obj = gtk.HBox(False, 5)
        l = gtk.Label(self.option['label']+":")
        l.props.xalign = 0
        self.obj.add(l)
        self.obj.add(combo)
        return combo
    def get(self):
        try:
            return self.__model[self.w.get_active()][0]
        except:
            return None
    def set(self, value):
        for row in self.__model:
            if row[0] == value:
                self.w.set_active_iter(row.iter)
                break
    def __format(self, value): return str(value)
    def __unformat(self, value): return str(value)

### OPTION TYPE: RADIO
class option_radio(og):
    signal = "group-changed"
    def build(self):
        self.obj = gtk.HBox(False, 5)
        l = gtk.Label(self.option['label']+":")
        l.props.xalign = 0
        self.obj.add(l)
        box = gtk.HBox(True, 2)
        self.__btns = {}
        grp = None
        for o in self.option['options']:
            b = gtk.RadioButton(grp, o[1])
            if grp is None: grp = b
            self.__btns[o[0]] = b
            box.add(b)
        self.obj.add(box)
        return grp
    def get(self):
        for o, w in self.__btns.iteritems():
            if w.get_active():
                return o
                break
    def set(self, value):
        self.__btns[value].set_active(True)
    def __format(self, value): return str(value)
    def __unformat(self, value): return str(value)




class DConfig(gtk.Dialog):
    
    def __init__(self, plugin):
        
        self.plugin = plugin
        
        title = _("%s settings") % plugin.module.name
        
        gtk.Dialog.__init__(self, title, globals.config_dialog, (),\
                            (gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE))
                            
        self.set_border_width(5)
        self.vbox.set_spacing(3)
        
        lbl = gtk.Label()
        lbl.set_markup('<b><span size="larger">%s</span>\n%s</b>' % 
                        (_("%s plugin") % plugin.module.name, _("Settings"))
                      )
        lbl.props.xalign = 0
        lbl.props.ypad = 10
        self.vbox.pack_start(lbl, False)
        
        settings = plugin.module.config_scheme
        
        for s in settings:
            self.__new_setting(s)
        
        self.set_default_size(250,200)
        
        self.set_resizable(False)
        
        
        
    
    def __new_setting(self, option):

        exec("s = option_%s()" % option['type'])
        s.initialize(self.plugin, option)
        self.vbox.pack_start(s.get_widget(), False)
        
        
        

def DConfigLoad(plugin):
        
    try:
        scheme = plugin.module.config_scheme
        settings = plugin.settings
    except:
        return False
    
    for option in scheme:
        
        if not 'bind' in option:
            continue
        
        # Get the value from settings
        try:
            value = getattr(settings, option['bind'][0])
            # Unformat the value from settings file (XML) to Python value
            exec("o = option_%s" % option['type'])
            value = o.unformat(value)
        # Otherwise use default value
        except AttributeError:
            try:
                value = option['default']
            except:
                value = None
        
        # Execute the callback: plugin.widget.set_this_thing(value)
        getattr(plugin.widget, option['bind'][1])(value)
    
    
        
