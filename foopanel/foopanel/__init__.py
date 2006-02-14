
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
import gettext
import string
import config, lib.core, lib.globals, lib.functions


def run():

    gettext.install("foopanel")
    
    lib.globals.config = config.FooConfig()

    theme = lib.globals.config.theme
    if theme != "None":
        lib.functions.load_theme(theme)
        
    lib.globals.tooltips = gtk.Tooltips()
    lib.globals.tooltips.enable()
        
    gui = lib.core.Gui()
    
    lib.globals.config.gui = lib.core.ConfDialog()

    plugin_manager = lib.core.PluginManager()

    gui.add(plugin_manager)
    
    #gui.set_translucent() - Not yet
        
    gui.run()


