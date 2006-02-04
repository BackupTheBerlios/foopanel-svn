
#
# Foopanel MUSICCONTROL plugin - Quodlibet wrapper
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


quodlibet_version = "0.15"


class ControlsClass:

    def __init__(self, version):
        self.version = version

    _ctls = {
        '0.14': {
            'next'      : '>',
            'previous'  : '<',
            'playpause' : '-'
        },
        '0.15': {
            'next'      : 'next',
            'previous'  : 'previous',
            'playpause' : 'play-pause'
        }
    }
    
    def __getattr__(self, key):
        
        return self._ctls[self.version][key]
        
controls = ControlsClass(quodlibet_version)


from PlayerWrapper import AbstractPlayerWrapper

import os, os.path
import re

expr = re.compile("^~?#?(\w+)=(.+)$", re.M)

class Wrapper(AbstractPlayerWrapper):


    _is_running = False
    
    _control_file = os.path.expanduser("~/.quodlibet/control")
    _current_file = os.path.expanduser("~/.quodlibet/current")
    _cover_file = os.path.expanduser("~/.quodlibet/current.cover")
    _paused_file = os.path.expanduser("~/.quodlibet/paused")
    
    control = None
    
    _current_info = None
    
    _version = None
    

    def __init__(self):
    
        AbstractPlayerWrapper.__init__(self)
        
        self.register_update_function(self.try_load)
        self.register_update_function(self.check_paused)
        self.register_update_function(self.parse_song)
        
        
    
    def try_load(self):
    
        if os.path.exists(self._control_file):
            if not self._is_running:
                self._is_running = True
        else:
            if self.control:
                self._is_running = False
    
    
    
    def check_paused(self):
    
        if self._is_running:
            p = os.popen("quodlibet --status")
            if p.read().split()[0] == 'playing':
                self.set_paused(False)
            else:
                self.set_paused(True)
        
                
    
    def parse_song(self):
    
        if self._is_running:
        
            if os.path.exists(self._current_file):
            
                f = open(self._current_file)
                tinfo = f.read()
                f.close()
                
                if tinfo != self._current_info:
                
                    self._current_info = tinfo
                    
                    info = {}
                    for k,v in expr.findall(tinfo):
                        info[k] = v
                    
                    title = info.get("title", "[untitled]")
                    artist = info.get("artist", "[unknown artist]")
                    
                    self.set_title(artist, title)
                    
                    if os.path.exists(self._cover_file):
                        self.set_cover(self._cover_file)
                    else:
                        self.set_cover()
            
        else:
            
            self.set_title()
            self.set_cover()
            self.set_paused()
    
    
            
     
    def control(self, cmd, load = False):
    
        #if not self._is_running and load:
        
        #    self.start()
     
        if self._is_running:
        
            f = open(self._control_file, 'w')
            f.write(cmd)
            f.close()
                
    
    def start(self):
        #os.system("quodlibet &")
        os.spawnlp(os.P_NOWAIT, "quodlibet", "&")
    
            
    # These are the callbacks on user interaction
    
    def focus(self):
        #os.system("quodlibet &")
        os.spawnlp(os.P_NOWAIT, "quodlibet", "&")
                
        
    def next(self):
        self.control(controls.next, True)
    
    
    def previous(self):
        self.control(controls.previous)
            
            
    def play_pause(self):
        self.control(controls.playpause, True)
        self.check_paused()
    
            
            
    
