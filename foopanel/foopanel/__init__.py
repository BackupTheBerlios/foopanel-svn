
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
import gettext
import string
import config, lib.core, lib.globals


def run():

    gettext.install("foopanel")
    
    lib.globals.config = config.FooConfig()

    try:
        if lib.globals.config.theme and lib.globals.config.theme != "None":
            if lib.globals.config.debug:
                print _("Using theme %s") % lib.globals.config.theme
            gtk.rc_parse("foopanel/themes/%s/gtkrc" % lib.globals.config.theme)
    except:
        print _("Warning: unable to load theme, using default")

    gui = lib.core.Gui()

    plugin_manager = lib.core.PluginManager()

    gui.add(plugin_manager)
    
    #gui.set_translucent() - Not yet
        
    gui.run()


