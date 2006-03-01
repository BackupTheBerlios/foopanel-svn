#
# Foopanel VOLUMECONTROL plugin
# 
# Copyright (C) 2006, Federico Pelloni <federico.pelloni@gmail.com>
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

name = "VolumeControl"
version = "0.1"
description = "Control audio volume"
authors = ["Federico Pelloni <federico.pelloni@gmail.com>"]
copyright = "Copyright (C) 2006, Federico Pelloni"
requires = {}

try: 
    default_term = os.environ["TERMCMD"]
except:
    try:
        default_term = os.environ["TERM"]
    except:
        default_term = "xterm"

config_scheme = [
    # Option type        Option labe                Bind    config opt  Plugin.callback
    { 
      'type': 'text', 
      'label': 'Mixer command', 
      'bind': ( 'mixer', 'set_mixer_cmd' ),
      'default': '%s -e alsamixer' % default_term
    }
]


from foopanel.lib import abstract, globals, dconfig
import gtk, gobject
import os, ossaudiodev


class Plugin(abstract.AbstractPlugin):
    
    def __init__(self):
        
        abstract.AbstractPlugin.__init__(self)
        
        box = gtk.HBox(False, 0)
        self.add(box)
        
        btn = gtk.Button()
        img = gtk.image_new_from_icon_name("stock_volume", gtk.ICON_SIZE_BUTTON)
        btn.add(img)
        btn.set_name("EdgeButton")
        btn.set_relief(gtk.RELIEF_NONE)
        box.add(btn)
        globals.tooltips.set_tip(btn, _("Open the volume control"))
        
        self._eb = gtk.EventBox()
        self.bar = gtk.ProgressBar()
        self.bar.set_orientation(gtk.PROGRESS_BOTTOM_TO_TOP)
        self.bar.set_size_request(11, 55)
        box.add(self._eb)
        self._eb.add(self.bar)
        
        btn.connect("clicked", self.__cb_mixer)
        btn.connect("scroll-event", self.__cb_scroll)
        self._eb.connect("scroll-event", self.__cb_scroll)
        
        self.mixer = ossaudiodev.openmixer()
        self.update()
        gobject.timeout_add(1000, self.update)
        
        self.show_all()
        
    
    def update(self):
        
        v = self.mixer.get(ossaudiodev.SOUND_MIXER_VOLUME)
        self.__current = float(v[0]+v[1])/200
        self.bar.set_fraction(self.__current)
        globals.tooltips.set_tip(self._eb, _("Volume: %d%%" % int(self.__current*100)))
        return True
    
    
    def __cb_scroll(self, widget, event):
        
        ratio = 0.03
        
        if event.direction == gtk.gdk.SCROLL_DOWN:
            self.__current -= ratio
        elif event.direction == gtk.gdk.SCROLL_UP:
            self.__current += ratio
        
        self.__current = max(min(self.__current, 1), 0)
        
        new = int(self.__current*100)
        self.mixer.set(ossaudiodev.SOUND_MIXER_VOLUME, (new, new))
        self.update()
      
        
    def __cb_mixer(self, widget):
        
        os.spawnlp(os.P_NOWAIT, self.mixer_cmd, "&")
        
    
    def set_mixer_cmd(self, cmd):
        
        self.mixer_cmd = cmd
        
        