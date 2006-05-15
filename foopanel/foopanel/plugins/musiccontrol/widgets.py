
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


import gtk, gobject
import pango


class ScrollingLabel(gtk.Label):
	
	_scrolling = True
	_to_scroll = False
	_x = 0
	
	def __init__(self, string = None, speed = 0.1):
		gtk.Label.__init__(self, "")
		self.set_text(string)
		self.connect("expose-event", self.expose)
		self.speed = speed
	
	def start_scrolling(self): 
		self._scrolling = True
		gobject.timeout_add(int(15/self.speed), self.redraw)
	def stop_scrolling(self): self._scrolling = False
	
	def set_scrolling(self, scroll):
		if scroll: self.start_scrolling()
		else: self.stop_scrolling()	
	
	def set_markup(self, text): self.set_text(text)
	def set_label(self, text): self.set_text(text)
	
	def set_text(self, label):
		l = self.get_layout()
		l.set_text(label)
		w, h = l.get_pixel_size()
		rx, ry, rw, rh = self.allocation
		if w > rw:
		    gtk.Label.set_markup(self, label+"  ***  ")
		    self._to_scroll = True
		else:
		    gtk.Label.set_markup(self, label)    
		    self._to_scroll = False
	
	def redraw(self):
		self.queue_draw()
		return self._scrolling
		
	def expose(self, widget, event):
		self.context = widget.window.cairo_create()
		self.event = event
		self.context.rectangle(event.area.x, event.area.y,
							   event.area.width, event.area.height)
		self.context.clip()
		self.draw(self.context)
		return True
	
	def draw(self, c):
		l = self.get_layout()
		w, h = l.get_pixel_size()
		if abs(self._x) >= w:
			self._x = 0
		x = self._x + self.event.area.x
		y = self.event.area.y + int(float(self.event.area.height - h)/2)
		c.set_source_color(self.style.fg[self.state])
		c.move_to(x, y)
		c.show_layout(l)
		c.move_to(x + w, y)
		c.show_layout(l)
		if self._to_scroll and self._scrolling:
			self._x -= 1
		
