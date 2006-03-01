
#
# Foopanel "EMBEDDER" plugin
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


name = "Embedder"
version = "0.1"
description = "Embed an application into Foopanel"
authors = ["Federico Pelloni <federico.pelloni@gmail.com>"]
copyright = "Copyright (C) 2005 - 2006, Federico Pelloni"
requires = {}


from foopanel.lib import abstract
import gtk, gobject




class ContainerWindow(abstract.PopupWindow):

    def __init__(self):

        abstract.PopupWindow.__init__(self, 3, gtk.WINDOW_TOPLEVEL)

        self.set_header("Embedder", "Order to your desktop.")
        
        socket = gtk.Socket()
        socket.show()
        self.add(socket)
                
        socket.connect("plug-added", self._cb_socket, "added")
        socket.connect("plug-removed", self._cb_socket, "removed")
        
        socket.add_id(0x220000c)
        #self.show_all()
        
        #self.show_all()
        
        #box = gtk.DrawingArea()
        #self.add(box)
        #box.realize()
        
        #w = gtk.gdk.window_foreign_new(41943052)
        #print w.property_get("_NET_WM_TITLE")
        #w.reparent(box.window, 0, 0)
        
        #box.show_all()
        #w.hide()
        
    
    def _cb_socket(self, widget, action):
        
        widget.show_all()    
        print "Plug %s" % action
   


class Plugin(abstract.AbstractPlugin):

    def __init__(self):
        
        abstract.AbstractPlugin.__init__(self)
    
        self._window = ContainerWindow()
        
        btn = gtk.ToggleButton("M-bed")
        btn.set_name("EdgeButton")
        btn.connect("toggled", self._window.toggle)
        self.add(btn)
        
        self.show_all()
        
        
        
