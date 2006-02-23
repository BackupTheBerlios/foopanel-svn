
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


from foopanel.lib import abstract, globals
import os.path

class Plugin(abstract.AbstractPlugin):
    
    def __init__(self, settings):
        
        abstract.AbstractPlugin.__init__(self)
        
        self.__settings = settings
        
        try:
            player = str(self.__settings.player)
        except:
            player = "quodlibet"
        
        exec("from %s_wrapper import Wrapper" % player)
        w = Wrapper()
        w.show_all()
        
        self.add(w)
        


