
#
# Foopanel MUSICCONTROL plugin
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

name = "MusicControl"
version = "0.1"
description = "Control your music player"
authors = ["Federico Pelloni <federico.pelloni@gmail.com>"]
requires = {}
copyright = "Copyright (C) 2005 - 2006, Federico Pelloni"


config_scheme = [
   # Player wrapper
    { 
      'type': 'dropdown', 
      'label': 'Music player', 
      'bind': ( 'player', 'set_player' ),
      'options': [('quodlibet', 'QuodLibet')],
      'default': 'quodlibet'
    },
    # Show cover
    {
      'type':    'boolean',
      'label':   'Show album cover (if supported)',
      'bind':    ('show_cover', 'set_show_cover'),
      'default': True
    }
]


from foopanel.lib import abstract, globals
import os.path

class Plugin(abstract.AbstractPlugin):
    
    __loaded_player = None
    __loaded_widget = None
    
    __show_cover = False
    
    def __init__(self):
        
        abstract.AbstractPlugin.__init__(self)
        
        
    
    def set_player(self, player):
        
        if self.__loaded_widget is not None:
            self.remove(self.__loaded_widget)
            self.__loaded_widget = None
        
        if self.__loaded_player is not None:
            self.__loaded_player = None
        
        if player is None or player == "None":
            return
            
        exec("from %s_wrapper import Wrapper" % player)
        self.__loaded_player = Wrapper
        w = self.__loaded_player()
        w.show_all()
        self.add(w)
        
        self.__loaded_widget = w
    
    
    def set_show_cover(self, show):
        
        self.__loaded_widget.set_show_cover(show)
            


