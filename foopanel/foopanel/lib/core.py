
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


import gtk, gtk.gdk, gobject
import os.path

import globals, functions, abstract



class PluginManager(gtk.HBox):


    def __init__(self):

        gtk.HBox.__init__(self, False, 5)

        self.set_name("PluginManager")

        globals.plugin_manager = self
        
        self.pack_start(FooMenu(), False, False)

        for p in globals.config.plugins:

                functions.load_plugin(p[0], p[1])
                continue

        self.show()


        for f in globals.registered_functions['on_finish']:

            f()
            
            



            
class Gui(abstract.FoopanelWindow):

    def __init__(self):

        abstract.FoopanelWindow.__init__(self, True)

        self.set_title("Foopanel")
        
        self.resize(int(gtk.gdk.screen_width()), int(globals.config.height))
        self.reposition()
        self.set_name("FoopanelWindow")
        
        globals.window = self
        

    def reposition(self):

        x = 0

        if globals.config.position == "top":
            y = 0
        else:
            y = gtk.gdk.screen_height() - int(globals.config.height)

        self.move(x, y)


    def run(self):

        self.show()

        globals.y = self.get_position()[1]
        globals.config.height = self.get_size()[1]
        
        gtk.main()



class AboutWindow(gtk.AboutDialog):

    def __init__(self):
    
        gtk.AboutDialog.__init__(self)
        
        for i in dir(globals.app):
            if i[0] != "_":
                eval("self.set_%s(globals.app.%s)" % (i, i))
                
                


globals.aboutwindow = AboutWindow()
globals.tooltips = gtk.Tooltips()
globals.tooltips.enable()


class FooMenu(gtk.ToggleButton):

    class FooMenuWindow(abstract.PopupWindow):
    
        class button(gtk.Button):
        
            def __init__(self, stock):
            
                gtk.Button.__init__(self, None, stock)
                self.set_relief(gtk.RELIEF_NONE)
                self.set_alignment(0, 0.5)
                
    
        def __init__(self):
        
            abstract.PopupWindow.__init__(self)
            
            #self.set_header("Foopanel", "Settings and information")
            
            box = gtk.HBox(False, 0)
            box.set_border_width(0)
            self.add(box)
            
            plugins = gtk.Button()
            plugins.set_relief(gtk.RELIEF_NONE)
            b = gtk.HBox(False, 1)
            plugins.add(b)
            b.pack_start(gtk.image_new_from_stock(gtk.STOCK_HARDDISK, gtk.ICON_SIZE_BUTTON))
            lbl = gtk.Label(_("_Plugins"))
            lbl.set_use_underline(True)
            b.add(lbl)
            box.add(plugins)
            
            settings = self.button(gtk.STOCK_PREFERENCES)
            settings.connect("clicked", lambda w: globals.config.dialog.run())
            box.add(settings)
            
            about = self.button(gtk.STOCK_ABOUT)
            about.connect("clicked", lambda w: globals.aboutwindow.run())
            box.add(about)
            
            exit = self.button(gtk.STOCK_QUIT)
            exit.connect("clicked", gtk.main_quit)
            box.add(exit)
            
            box.show_all()
        
        

    def __init__(self):
    
        gtk.ToggleButton.__init__(self)
        
        globals.tooltips.set_tip(self, _("Foopanel menu"))
        
        self.set_name("EdgeButton")
        
        if globals.config.position == "top":
            arr_dir = gtk.ARROW_DOWN
        else:
            arr_dir = gtk.ARROW_UP
        arrow = gtk.Arrow(arr_dir, gtk.SHADOW_IN)
        self.add(arrow)
        
        self.menu = self.FooMenuWindow()
        self.connect("toggled", self.menu.toggle)
        
        self.show_all()


