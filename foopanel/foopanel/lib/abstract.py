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



import gtk
from foopanel import config
from foopanel.lib import globals
import os.path



class AbstractPlugin(gtk.HBox):

    def __init__(self):
    
        gtk.HBox.__init__(self, False, 3)
        
        self.show()
            
            
    


class PopupWindow(gtk.Window):


    def __init__(self):
    
        gtk.Window.__init__(self, gtk.WINDOW_POPUP)
        
        self.set_name("FoopanelPopupWindow")
        
        self.set_border_width(3)
        
        self.opener = None
        
        self._box = gtk.VBox()
        self._box.show()
        gtk.Window.add(self, self._box)
        
    
    def add(self, widget, expand = False):
    
        self._box.pack_start(widget, expand, expand)
    
    
    
    def set_header(self, title = None, description = None, icon = None):
    
        header = gtk.HBox(False, 10)
        header.set_name("FoopanelPopupHeader")
        header.show()
        header.set_border_width(10)
        self.add(header)
    
        if icon:

            image = gtk.Image()
            image.set_from_pixbuf(icon)
            image.show()
            header.pack_start(image, False, False)
            
        
        if title or description:
        
            lbl = gtk.Label("")
            
            txt = "<big>"
            if title:
                txt += "<b>%s</b>" % title
                if description:
                    txt += "\n"
            if description:
                txt += description
            txt += "</big>"
            
            lbl.set_markup(txt)
            lbl.set_property("xalign", 0)
            lbl.show()
            header.add(lbl)

        sep = gtk.HSeparator()
        sep.show()
        self.add(sep)

    
        
    
    def run(self):
    
        self.show()
        
        
        
    def open(self, widget = 0):
    
        if globals.opened_popup:
            globals.opened_popup.close()
                           
        if type(widget) == type(1):
            x = widget
        else:
            self.opener = widget
            try:
                x = widget.allocation.x
            except:
                x = 0
                self.opener = None
    
        h = self.get_size()[1]
        
        if config.position == "top":
            y = globals.y + config.height
        else:
            y = globals.y - h
    
        self.move(x, y)
        self.show()
        
        globals.opened_popup = self
        
        
        
    def close(self):
    
        self.hide()
        
        try:
            self.opener.set_active(False)
        except:
            raise

        globals.opened_popup = None
        

        
    
    
    def toggle(self, widget = 0):
    
        if globals.opened_popup:
        
            if id(self) != id(globals.opened_popup):
            
                globals.opened_popup.close()
                self.open(widget)
                
            else:
        
                self.close()
                
        else:
        
            self.open(widget)



