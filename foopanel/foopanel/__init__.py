
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

import sys, os, os.path

here = os.path.dirname(__file__)

if os.path.exists(os.path.realpath(os.path.join(here, "..", "setup.py"))) and \
   os.path.isdir(os.path.realpath(os.path.join(here, "..", "foopanel"))):
   
    globals.localrun = True
    globals.paths.plugins = [os.path.join(here, "plugins")]
    globals.paths.themes  = [os.path.join(here, "themes")]
        
else:

    globals.localrun = False
    

for p in globals.paths.plugins:
    sys.path.insert(0, os.path.realpath(os.path.join(p, "..")))

def run():
    
    if not os.path.isdir(globals.paths.user):
        try:
            os.mkdir(globals.paths.user)
        except:
            print _("Error: Unable to create personal directory (~/.foopanel)")
            sys.exit(2)
            
    personal_theme_dir = os.path.join(globals.paths.user, "themes")
    if not os.path.isdir(personal_theme_dir):
        try:
            os.mkdir(personal_theme_dir)
        except:
            pass
    
    personal_plugin_dir = os.path.join(globals.paths.user, "plugins")
    if not os.path.isdir(personal_plugin_dir):
        try:
            os.mkdir(personal_plugin_dir)
        except:
            pass
    

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


