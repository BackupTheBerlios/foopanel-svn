
#
# Foopanel MUSICCONTROL plugin - Quodlibet DBus wrapper
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


from PlayerWrapper import AbstractPlayerWrapper

import os, os.path
import dbus, dbus.glib


class Wrapper(AbstractPlayerWrapper):
	
	def __init__(self):
		    
		AbstractPlayerWrapper.__init__(self)
        
		self.bus = dbus.SessionBus()
		self.set_paused(True)
		
		try:
			self.setup_dbus()
		except:
			self.bus.add_signal_receiver(self.setup_dbus, 'Hello', 'net.sacredchao.QuodLibet')
			
	
	def setup_dbus(self):
		self.proxy = self.bus.get_object('net.sacredchao.QuodLibet', 
											 '/net/sacredchao/QuodLibet')
		self.control = dbus.Interface(self.proxy, 'net.sacredchao.QuodLibet')
		self.link_dbus()

			
	
	def link_dbus(self):
		
		self.control.connect_to_signal('Paused', lambda: self.set_paused(True))
		self.control.connect_to_signal('Unpaused', lambda: self.set_paused(False))
		self.control.connect_to_signal('SongStarted', self.__cb_song_start)
		self.control.connect_to_signal('SongEnded', self.__cb_song_end)
		
		paused = self.control.GetPaused()
		self.set_paused(paused)
		song = self.control.GetSong()
		self.__parse_song(song)
		
	
	def __cb_song_end(self, skipped):
		self.set_title()
	
	def __cb_song_start(self, song):
		self.__parse_song(song)
	
	
	def __parse_song(self, song):
		if song is None:
			self.set_title()
			self.set_cover()
		self.set_title(song['artist'] or '[unknown artist]', song['title'] or '[unknown]')
		if song['cover'] != '' and os.path.exists(song['cover']):
			self.set_cover(song['cover'])
		else:
			self.set_cover()
	
	

	# These are the callbacks on user interaction

	def focus(self):
		os.spawnlp(os.P_NOWAIT, "quodlibet", "&")
	            
	def next(self):
		self.control.Next()

	def previous(self):
		self.control.Previous()
	                
	def play_pause(self):
		self.control.PlayPause()

	        
            
    
