
#
# ScrollingLabel widget
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

###############
#
# NOTE: this could be done much better, by making the text scroll pixel-by-pixel
#       instead of char-by-char, but it is much more difficult and I couldn't 
#       get a solution to make it work without clearing the background (thus
#       making it writing white on white with SolidBlue theme and clear GTK+
#       themes).
#       However I can provide the code I wrote, if anybody is interested in
#       looking further at this.
#
###############

import gtk, gobject
import pango


class ScrollingLabel(gtk.Label):

    #__gsignals__ = { 'expose_event': 'override' }
    
    #_curr_x = 0
    _scrolling = True
    _to_scroll = False


    def __init__(self, string = None, speed = 0.1):
    
        gtk.Label.__init__(self, "")
        
        self._layout = self.get_layout()
        
        self.set_text(string)
        
        gobject.timeout_add(int(50 / speed), self.draw)

    
    
    def start_scrolling(self):
    
        self._scrolling = True
    
    
    def stop_scrolling(self):
    
        self._scrolling = False
        
    
    
    def set_markup(self, markup):
    
        self.set_text(markup)
    
    
    def set_label(self, label):
    
        self.set_text(label)
    
    
    def set_text(self, label):
        
        l = self._layout
        l.set_markup(label)
        
        w, h = l.get_pixel_size()
        
        rx, ry, rw, rh = self.allocation
        
        if w > rw:

            gtk.Label.set_markup(self, label+" *** ")
            self._to_scroll = True
        
        else:
    
            gtk.Label.set_markup(self, label)    
            self._to_scroll = False
        
        
        
        
    def draw(self):
        
        l = gtk.Label
        
        if self._to_scroll and self._scrolling:
            
            txt = l.get_text(self)[1:] + l.get_text(self)[:1]
            l.set_text(self, txt)
        
        return True
        
        
        
    #def do_expose_event(self, event):
    #
    #    #self.draw()
    #    self.chain(event)
        
        
