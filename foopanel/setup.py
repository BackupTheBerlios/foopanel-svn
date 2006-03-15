#
# Foopanel setup script
#
# Copyright (C) 2006, Federico Pelloni <federico.pelloni@gmail.com>
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


from distutils.core import setup
import string

setup(
       # Application information
       name         = "foopanel",
       version      = "0.1.0",
       description  = "A powerful themable and extensible panel for your desktop",
       author       = "Federico Pelloni",
       author_email = "federico.pelloni@gmail.com",
       url          = "http://foopanel.berlios.de/",
       
       # Application components
       packages     = [
                        # CORE
                        'foopanel',
                        'foopanel.lib',
                        'foopanel.lib.elementtree',
                        'foopanel.plugins',
                        # PLUGINS
                        'foopanel.plugins.clock',
                        'foopanel.plugins.cpuload',
                        'foopanel.plugins.flexible_space',
                        'foopanel.plugins.meminfo',
                        'foopanel.plugins.menu',
                        'foopanel.plugins.musiccontrol',
                        'foopanel.plugins.pager',
                        'foopanel.plugins.quickterminal',
                        'foopanel.plugins.separator',
                        'foopanel.plugins.volumecontrol'
                        ],
       package_data = {'foopanel': ['lib/config_ui.glade', 'config.xml.in', 'themes/*/*']},
       scripts      = ['scripts/foopanel'],
      )
