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
    
        w = gtk.CheckButton(str(description))
        w.set_border_width(3)
        
        default = str(default)
        if default.lower() == "on":
            w.set_active(True)
        else:
            w.set_active(False)
        
        self.pack(w, parent)
        
        return w
    
    
    def new_setting_number(self, description, parent, digits, default = None, smin = None, smax = None):
    
        step = 10**(-int(digits))
        adj = gtk.Adjustment(0, 0, 0, step)
        w = gtk.SpinButton(adj, 1, int(digits))
        w.set_numeric(True)
        if smin != None and smax != None:
            w.set_range(float(smin), float(smax))
        if default != None:
            w.set_value(float(default))
        
        self.pack(self.new_labelled_control(str(description)+":", w), parent)
        
        return w
        
    
    def new_setting_switch(self, description, parent, options, default = None):
    
        model = gtk.ListStore(str, str)
        w = gtk.ComboBox(model)

        cell = gtk.CellRendererText()
        w.pack_start(cell, True)
        w.add_attribute(cell, 'text', 1)

        self.pack(self.new_labelled_control(str(description+":"), w), parent)
        
        for o in options:
            model.append(o)
    
        if default:
            w.set_active(int(default)-1)

        return w
    
    
    def new_setting_text(self, description, parent, default = None, tmax = 0):
    
        w = gtk.Entry(int(tmax))
        if default:
            w.set_text(str(default))
        
        self.pack(self.new_labelled_control(description+":", w), parent)
        
        return w
    
    
    def new_setting_radio(self, description, parent, options, default):
        
        frame = self.new_group(description, parent)
        
        b = None
        for o in options:
            b = gtk.RadioButton(b, o)
            if default and default == o:
                b.set_active(True)
            self.pack(b, frame)
    
        return frame
    
    
        
    def new_group(self, title, parent):
    
        if title != None:
            title = str(title)
        w = gtk.Frame(title)
        self.pack(w, parent)
        
        box = gtk.VBox(False, 3)
        box.set_border_width(3)
        w.add(box)
        
        return box
        
    
    
    def new_labelled_control(self, label, widget):
    
        box = gtk.HBox(False, 10)
        
        lbl = gtk.Label(str(label))
        lbl.set_alignment(0, 0.5)
        box.pack_start(lbl, False, False)
        
        box.pack_start(widget, True, True)
        
        return box
