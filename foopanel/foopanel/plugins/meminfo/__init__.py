#
# Foopanel "MemInfo" plugin
#
# Copyright (C) 2006, Sergey Fedoseev <fedoseev.sergey@gmail.com>
#                     Federico Pelloni <federico.pelloni@gmail.com>
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

from foopanel.lib import abstract, globals
import gtk, gobject

name = "MemInfo"
version = "0.1"
description = "Shows memory usage"
authors = ["Sergey Fedoseev <fedoseev.sergey@gmail.com>", "Federico Pelloni <federico.pelloni@gmail.com>"]
copyright = "Copyright (C) 2006, Sergey Fedoseev"
expand = False
requires = {}

config_scheme = [
    # Option type        Option labe                Bind    config opt  Plugin.callback
    { 'type': 'boolean', 'label': 'Vertical labels', 'bind': ( 'vlabel', 'set_label_dir' ) }
]


class Plugin(abstract.AbstractPlugin):
    def __init__(self, settings):
        abstract.AbstractPlugin.__init__(self)
        
        try:
            vlabel = bool(int(settings.vlabel))
        except:
            vlabel = False
        
        self.mem = Memory()
        self.add(self.mem)
        self.swap = Swap()
        self.add(self.swap)
        
        self.set_label_dir(vlabel)
    
    def set_label_dir(self, vertical):
        
        if vertical: angle = 90
        else: angle = 0 
        self.mem.label.set_angle(angle)
        self.swap.label.set_angle(angle)
        

class Mem(gtk.HBox):
    file = '/proc/meminfo'
    def __init__(self, vlabel = False):
        gtk.HBox.__init__(self)
        
        self.tooltip = globals.tooltips.set_tip
        
        self.eb = gtk.EventBox()
        self.bar = gtk.ProgressBar()
        self.bar.set_orientation(gtk.PROGRESS_BOTTOM_TO_TOP)
        self.bar.set_size_request(11, 55)
        
        self.label = gtk.Label(self.name)
        self.pack_start(self.label)
        self.pack_start(self.eb)
        self.eb.add(self.bar)

        self.f = open(self.file)
        gtk.quit_add(0, self.quit)
        self.update()
        gobject.timeout_add(500, self.update)

        self.show_all()

    def quit(self):
        self.f.close()

    def update(self):
        self.f.seek(0)
        meminfo = self.f.readlines()
        total = int(meminfo[self.a].split()[1])
        cached = int(meminfo[self.b].split()[1])
        free = int(meminfo[self.c].split()[1])

        free = total-cached-free

        self.tooltip(self.eb, "Used %s of %s MB" % (str(free/1024), str(total/1024)))
        self.bar.set_fraction(free/float(total))
        return True

class Memory(Mem):
    name = 'mem'

    a = 0
    b = 1
    c = 3

class Swap(Mem):
    name = 'swap'

    a = 11
    b = 4
    c = 12
