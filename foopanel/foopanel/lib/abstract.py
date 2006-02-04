#
# Foopanel
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



import gtk
from foopanel.lib import globals
import os.path


class Plugin:
    
    name = None
    module = None
    widget = None
    settings = None
    
    def __init__(self, **kwargs):
        
        self.__dict__.update(kwargs)
        


class AbstractPlugin(gtk.HBox):

    def __init__(self):
    
        gtk.HBox.__init__(self, False, 3)
        
        self.show()
            
            



class FoopanelWindow(gtk.Window):

    def __init__(self, wtype = gtk.WINDOW_POPUP):
    
        gtk.Window.__init__(self, wtype)
        
        self.set_decorated(False)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.stick()
        
    
    
    #
    # I haven't found a way to do this
    # Just waiting for GTK to support XComposite
    #
    #def set_translucent(self):
    #
    #    iconsdir = 'foopanel/'
    #    imagename = 'bg.png'
    #
    #    path = os.path.join(iconsdir, imagename)
    #    pixbuf = gtk.gdk.pixbuf_new_from_file(path)
    #    #w, h = self.get_size()
    #    #pixbuf = pixbuf.scale_simple(w, h, gtk.gdk.INTERP_BILINEAR)
    #    pixmap, mask = pixbuf.render_pixmap_and_mask()
    #    #del pixbuf
    #    self.set_app_paintable(True)
    #    self.realize()
    #
    #    #self.shape_combine_mask(mask, 0, 0)  # make it transparent
    #    self.window.set_child_shapes()
    #    self.window.set_back_pixmap(pixmap, False)
    #    #pixbuf.render_to_drawable(self.window, x, 0,0, 0,0, -1,-1)
    #    del pixmap
    #    
    #    #self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color( 20000, 30000, 40000))
    #    
        

    


class PopupWindow(FoopanelWindow):


    def __init__(self, border = 3, wtype = gtk.WINDOW_POPUP):
    
        FoopanelWindow.__init__(self, wtype)
        
        self.set_name("FoopanelPopupWindow")
        
        self.set_border_width(border)
        
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
        
    
    def reposition(self):
        
        x = self.x + globals.window_x
        h = self.get_size()[1]
        
        if globals.config.vposition == "top":
            y = globals.window_y + globals.height
        else:
            y = globals.window_y - h
    
        self.move(x, y) 
    
        
    def open(self, widget = 0):
    
        if globals.opened_popup:
            globals.opened_popup.close()
                           
        if type(widget) == type(1):
            self.x = widget
        else:
            self.opener = widget
            try:
                self.x = widget.allocation.x
            except:
                self.x = 0
                self.opener = None
        
        self.reposition()
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



