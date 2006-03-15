#
# Foopanel "CPULoad" plugin
#
# Copyright (C) 2006, Federico Pelloni <federico.pelloni@gmail.com>
# Note: part of this plugin comes from the MemInfo plugin by Sergey Fedoseev
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

from foopanel.lib import abstract, globals
import gtk, gobject

name = "CPULoad"
version = "0.1"
description = "Show CPU load"
authors = ["Federico Pelloni <federico.pelloni@gmail.com>"]
expand = False
copyright = "Copyright (C) 2006, Federico Pelloni"
requires = {}


config_scheme = [
    { 
      'type': 'boolean', 
      'label': 'Vertical label',
      'bind': ( 'vlabel', 'set_label_dir' ),
      'default': False
    }
]


class Plugin( abstract.Plugin ):
    
    name = "cpu"
    file = "/proc/stat"
    
    __oldused = 0
    __oldtotal = 0
        
    def __init__( self ):
        
        abstract.Plugin.__init__( self )
        
        self.eb = gtk.EventBox()
        self.bar = gtk.ProgressBar()
        self.bar.set_orientation( gtk.PROGRESS_BOTTOM_TO_TOP )
        self.bar.set_size_request( 11, 55 )
        
        self._label = gtk.Label( self.name )
        self.pack_start( self._label )
        self.pack_start( self.eb )
        self.eb.add( self.bar )
        
        self.tooltip = globals.tooltips.set_tip

        self.f = open( self.file )
        gtk.quit_add( 0, self.quit )
        self.update()
        gobject.timeout_add( 1000, self.update )

        self.show_all()        
        
    
    def quit( self ):
        self.f.close()

    def update( self ):
        self.f.seek( 0 )
        info = self.f.readlines()[0].split()
        used = int( info[1] ) + int( info[2] ) + int( info[3] )
        total = int( info[1] ) + int( info[2] ) + int( info[3] ) + int( info[4] )
        if total - self.__oldtotal != 0:
            load = float( used - self.__oldused ) / float( total - self.__oldtotal )
        else:
            load = 0
        self.__oldused = used
        self.__oldtotal = total
        self.tooltip( self.eb, "CPU load: %d%%" % int( load*100 ) )
        self.bar.set_fraction( load )
        return True
    
    
    def set_label_dir( self, vertical ):
        
        if vertical:
            self._label.set_angle( 90 )
        else:
            self._label.set_angle( 0 )
        
        
            