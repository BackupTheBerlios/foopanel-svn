
#
# Foopanel MUSICCONTROL plugin
# 
# Copyright (C) 2005, Federico Pelloni <federico.pelloni@gmail.com>
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

from foopanel.lib import globals
from foopanel import config
import widgets
import gtk, gtk.gdk, gobject
import os.path



class AbstractPlayerWrapper(gtk.HBox):


    __paused = False
    

    def __init__(self):
        
        gtk.HBox.__init__(self, False, 3)
        
        self.set_size_request(int(globals.height) + 100, 0)
        
        self.coverimg = gtk.Image()
        w = int(globals.height) - 6
        self.coverimg.set_size_request(w, w)
        al = gtk.Alignment(0.5, 0.5)
        al.show()
        self.coverimg.show()
        self.add(al)
        al.add(self.coverimg)
        
        box = gtk.VBox(False, 5)
        box.show()
        self.add(box)
        
        btn_track = gtk.Button()
        btn_track.set_name("EdgeButton")
        btn_track.set_relief(gtk.RELIEF_NONE)
        btn_track.set_size_request(100, -1)
        btn_track.connect("clicked", lambda w: self.focus())
        btn_track.show()
        box.add(btn_track)
        
        self.track_label = widgets.ScrollingLabel(_("Music player"))
        #self.track_label = gtk.Label(_("Music player"))
        self.track_label.show()
        btn_track.add(self.track_label)
        
      
        btnbox = gtk.HBox(False, 2)
        btnbox.show()
        box.add(btnbox)
        
        btn_prev = gtk.Button()
        btn_prev.show()
        btn_prev_img = gtk.Image()
        btn_prev_img.show()
        btn_prev_img.set_from_stock(gtk.STOCK_MEDIA_PREVIOUS, gtk.ICON_SIZE_BUTTON)
        btn_prev.add(btn_prev_img)
        btn_prev.connect("clicked", lambda w: self.previous())
        btnbox.pack_start(btn_prev, False, False)
        
        btn_play = gtk.Button()
        btn_play.show()
        self.play_img = gtk.Image()
        self.play_img.show()
        self.play_img.set_from_stock(gtk.STOCK_MEDIA_PLAY, gtk.ICON_SIZE_BUTTON)
        btn_play.add(self.play_img)
        btn_play.connect("clicked", lambda w: self.play_pause())
        btnbox.pack_start(btn_play, False, False)
        
        btn_next = gtk.Button()
        btn_next.show()
        btn_next_img = gtk.Image()
        btn_next_img.show()
        btn_next_img.set_from_stock(gtk.STOCK_MEDIA_NEXT, gtk.ICON_SIZE_BUTTON)
        btn_next.add(btn_next_img)
        btn_next.connect("clicked", lambda w: self.next())
        btnbox.pack_start(btn_next, False, False)
        
        self._curr_title = None
        self._pango_layout = self.track_label.get_layout()
        self._title_scroll = False
        self._curr_scroll = None
        self._scroll_count = 0
        
        self.set_cover()
        
        self._on_update_functions = [ self._scroll_title ]
               
        self.update()
        gobject.timeout_add(1000, self.update)
    
    
    
    def register_update_function(self, function):
    
        self._on_update_functions.append(function)
    
    
    
    def update(self):
        """ Per-second update function """
    
        for f in self._on_update_functions:
        
            try:
                f()
            except KeyboardInterrupt:
                continue
                
        return True
        
    
    
    def previous(self):
        pass
        
    def play_pause(self):
        pass
    
    def next(self):
        pass
        
    def focus(self):
        pass

    
    
    def set_paused(self, paused = True):
    
        self.__paused = paused
        
        self.track_label._scrolling = not paused
    
        if paused:
            icon = gtk.STOCK_MEDIA_PLAY
        else:
            icon = gtk.STOCK_MEDIA_PAUSE
        
        self.play_img.set_from_stock(icon, gtk.ICON_SIZE_BUTTON)
    
    

    def set_cover(self, c = False):
    
        if not c:
            c = os.path.join(os.path.dirname(__file__), "icon.png")
        try:
            w = int(globals.height) - 6
            cover = gtk.gdk.pixbuf_new_from_file_at_size(c, w, w)
            self.coverimg.set_from_pixbuf(cover)
        except:
            pass

    
        
        
    def set_title(self, artist = None, title = None):
        """ Title manager function """
        
        if artist == None and title == None:
        
            self._title_scroll = False
            self._scroll_count = 0
            self._curr_title = None
            self._curr_scroll = None
            self._curr_song = None
            title = _("Music player")
            
        else:
        
            title = artist + " - " + title

            if title != self._curr_title:
                
                self._title_scroll = False
                self._pango_layout.set_text(title)

                if self._pango_layout.get_pixel_size()[0] > \
                   self.track_label.allocation.width:

                    self._title_scroll = True
                    self._curr_scroll = " " + title + "  *** "
                    self._scroll_count = 0

            self._curr_song = title
            
        self.track_label.set_label(title)
        
        
    
    def _scroll_title(self):
        """ Scroll title routine """
        
        return
        
        if self._title_scroll and not self.__paused:
        
            self._scroll_count += 1
        
            if self._scroll_count > 3:
            
                x = 1
                title = self._curr_scroll[x:] + self._curr_scroll[:x]
                self._curr_scroll = title
                self.btn_track.set_label(title)
        
            
    

