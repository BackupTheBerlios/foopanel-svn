
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
import gettext
import string
import config, lib.globals, lib.functions
import os.path

class PluginManager(gtk.HBox):


    def __init__(self):

        gtk.HBox.__init__(self, False, 5)

        self.set_name("PluginManager")

        lib.globals.plugin_manager = self

        for p in config.plugins:

                lib.functions.load_plugin(p)
                continue

        self.show()


        for f in lib.globals.registered_functions['on_finish']:

            f()






class Gui(gtk.Window):

    def __init__(self):

        gtk.Window.__init__(self)

        self.set_title("Foopanel")
        self.set_decorated(False)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.stick()
        self.resize(gtk.gdk.screen_width(), config.height)
        self.reposition()
        self.set_name("FoopanelWindow")
        self.set_keep_above(config.ontop)
        
        lib.globals.window = self
        
        


    def reposition(self):

        x = 0

        if config.position == "top":
            y = 0
        else:
            y = gtk.gdk.screen_height() - config.height

        self.move(x, y)


    def run(self):

        self.show()

        lib.globals.y = self.get_position()[1]
        config.height = self.get_size()[1]
        
        gtk.main()




def run():

    gettext.install("foopanel")

    if config.theme:
        if config.debug:
            print _("Using theme %s") % config.theme
        try:
            gtk.rc_parse("foopanel/themes/%s/gtkrc" % config.theme)
        except:
            print _("Warning: unable to load theme, using default")

    gui = Gui()

    plugin_manager = PluginManager()

    gui.add(plugin_manager)

    gui.run()


