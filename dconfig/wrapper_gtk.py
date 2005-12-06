#
# D-Config
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


import gtk


class SettingWrapper:
    def get(self):
        pass
    def set(self, value):
        pass

class LabelledControl(gtk.HBox):
    
    def __init__(self, label):
    
        gtk.HBox.__init__(self, False, 10)
        
        lbl = gtk.Label(str(label))
        lbl.set_alignment(0, 0.5)
        self.pack_start(lbl, False, False)

class Frame(gtk.Frame):
    
    def __init__(self, title = None):
    
        if title != None:
            title = str(title)
        
        gtk.Frame.__init__(self, title)
        
        self.box = gtk.VBox(False, 3)
        self.box.set_border_width(3)
        gtk.Frame.add(self, self.box)
        
    def add(self, widget, a = True, b = True):
        self.box.pack_start(widget, a, b)
        
    def pack_start(self, widget, a = True, b = True):
        self.box.pack_start(widget, a, b)


class wrapper_text(SettingWrapper, LabelledControl):
    
    def __init__(self, description, default, tmax):
    
        LabelledControl.__init__(self, str(description+":"))
        
        self.entry = gtk.Entry(int(tmax))
        if default:
            self.entry.set_text(str(default))
        
        self.add(self.entry)
    
    def get(self):
        return self.entry.get_text()
    def set(self, value):
        self.entry.set_text(str(value))
    
class wrapper_boolean(SettingWrapper, gtk.CheckButton):
    
    def __init__(self, description, default):
        
        gtk.CheckButton.__init__(self, str(description))
        self.set_border_width(3)
        
        default = str(default)
        if default.lower() == "on":
            self.set_active(True)
        else:
            self.set_active(False)
        
    def get(self):
        return self.get_active()
    def set(self, value):
        self.set_active(bool(value))

class wrapper_number(SettingWrapper, LabelledControl):
    
    def __init__(self, description, digits, default = None, smin = None, smax = None):
        
        LabelledControl.__init__(self, description+":")
        
        step = 10**(-int(digits))
        adj = gtk.Adjustment(0, 0, 0, step)
        
        self.spin = gtk.SpinButton(adj, 1, int(digits))
        
        self.spin.set_numeric(True)
        if smin != None and smax != None:
            self.spin.set_range(float(smin), float(smax))
        if default != None:
            self.spin.set_value(float(default))
        
        self.add(self.spin)
        
    def get(self):
        return self.spin.get_value()
    def set(self, value):
        self.spin.set_value(float(value))
        
class wrapper_switch(SettingWrapper, LabelledControl):
    
    def __init__(self, description, options, default = None):
        
        LabelledControl.__init__(self, str(description+":"))
        
        self.model = gtk.ListStore(str, str)
        self.combo = gtk.ComboBox(self.model)

        cell = gtk.CellRendererText()
        self.combo.pack_start(cell, True)
        self.combo.add_attribute(cell, 'text', 1)

        self.add(self.combo)
        
        for o in options:
            self.model.append(o)
    
        if default:
            self.combo.set_active(int(default)-1)

    def get(self):
        return list(self.model[self.combo.get_active()])[0]
    def set(self, value):
        self.combo.set_active(int(value))

class wrapper_radio(SettingWrapper, Frame):
    
    def __init__(self, description, options, default):
        
        Frame.__init__(self, description)
        
        b = None
        for o in options:
            b = gtk.RadioButton(b, o)
            if default and default == o:
                b.set_active(True)
            self.add(b)
    
    def get(self):
        return 


class DConfigGuiWrapper(gtk.Notebook):
    
    
    def __init__(self):
        
        gtk.Notebook.__init__(self)
    

    def pack(self, widget, parent):
        
        parent.pack_start(widget, False, False)

    
    def new_section(self, title):
    
        page = gtk.VBox(False, 3)
        page.set_border_width(3)
        
        self.append_page(page, gtk.Label(str(title)))
        
        return page
    
        
    def new_setting_boolean(self, description, parent, default = "off"):
    
        w = wrapper_boolean(description, default)
        self.pack(w, parent)
        return w
    
    
    def new_setting_number(self, description, parent, digits, default = None, smin = None, smax = None):
    
        w = wrapper_number(description, digits, default, smin, smax)
        self.pack(w, parent)
        return w
        
    
    def new_setting_switch(self, description, parent, options, default = None):
    
        w = wrapper_switch(description, options, default)
        self.pack(w, parent)
        return w
    
    
    def new_setting_text(self, description, parent, default = None, tmax = 0):
    
        w = wrapper_text(description, default, tmax)
        self.pack(w, parent)
        return w
    
    
    def new_setting_radio(self, description, parent, options, default):
        
        w = wrapper_radio(description, options, default)
        self.pack(w, parent)
        return w
    
    
    def new_group(self, title, parent):
    
        w = Frame(title)
        self.pack(w, parent)
        return w
        
    
    
    def new_labelled_control(self, label, widget):
    
        w = LabelledControl(label)
        w.add(widget)
        return w
    
