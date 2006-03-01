
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
from lib import config, core, globals, functions


def run():

    gettext.install("foopanel")
    
    globals.config = config.FooConfig()

    theme = lib.globals.config.theme
    if theme != "None":
        functions.load_theme(theme)
        
    globals.tooltips = gtk.Tooltips()
    globals.tooltips.enable()
        
    gui = core.Gui()
    
    globals.config.gui = core.ConfDialog()

    plugin_manager = core.PluginManager()

    gui.add(plugin_manager)
    
    #gui.set_translucent() - Not yet
        
    gui.run()


