
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


# Some info about the app

class app:
    name = "Foopanel"
    version = "0.1.0"
    copyright = "Copyright (C) 2005 - 2006, Federico Pelloni"
    comments = "A powerful themable and extensible panel for your desktop"
    #license = "GNU Public License version 2 or higher"
    website = "http://foopanel.berlios.de/"
    authors = [ "Federico Pelloni <federico.pelloni@gmail.com>" ]
    artists = [ "Federico Pelloni <federico.pelloni@gmail.com>" ]
    


# Some paths
from os.path import realpath, expanduser, join, dirname
class paths:
    lib = realpath(dirname(__file__))
    base = realpath(join(lib, ".."))
    user = expanduser("~/.foopanel")
    themes = [realpath(join(base, "themes")),
              expanduser("~/.foopanel/themes")]
    plugins = [realpath(join(base, "plugins")),
              expanduser("~/.foopanel/plugins")]


# Here I store some variables and constants used in various parts of Foopanel
# Just initialize them to avoid checking if they exist

localrun = None

window = None
plugins = []
plugin_manager = None

x = None
y = None
width = None
height = None

opened_popup = None


# These are the plugins registered functions

registered_functions = {
    "on_finish": [],
    "on_resize": []
}

