
#
# Foopanel "CLOCK" plugin
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


name = "Clock"
version = "0.1"
description = "Draw a digital clock and print today's date on the panel"
authors = ["Federico Pelloni <federico.pelloni@gmail.com>"]
copyright = "Copyright (C) 2005 - 2006, Federico Pelloni"
requires = {}


config_scheme = [
    {
     'type':     'boolean',
     'label':    'Show time',
     'bind':     ('show_time', 'set_show_time'),
     'default':  True
    },
    {
     'type':     'text',
     'label':    'Time format',
     'bind':     ('time_format', 'set_time_format'),
     'default':  '%X'
    },
    {
     'type':     'boolean',
     'label':    'Show date',
     'bind':     ('show_date', 'set_show_date'),
     'default':  True
    },
    {
     'type':     'text',
     'label':    'Date format',
     'bind':     ('date_format', 'set_date_format'),
     'default':  '%x'
    },
    {
     'type':     'label',
     'label':    'See http://www.php.net/strftime\nfor help about the format string'
    }
]


from foopanel.lib import abstract
import gtk, gobject
import time


class Plugin(abstract.AbstractPlugin):
    
    __format_time = "%X"
    __format_date = "%x"

    def __init__(self):
        
        abstract.AbstractPlugin.__init__(self)
    
        self.set_border_width(5)
        
        box = gtk.VBox(False, 0)
        box.show()
        self.add(box)
        
        self.label_time = gtk.Label()
        self.label_time.set_alignment(0.5, 1)
        self.label_time.set_name("DigitLabel")
        self.label_time.show()
        self.label_date = gtk.Label()
        self.label_date.set_alignment(0.5, 0)
        self.label_date.set_name("DigitLabel")
        self.label_date.show()
        
        self.update()
        
        w = max(self.label_time.get_layout().get_pixel_size()[0],\
              self.label_date.get_layout().get_pixel_size()[0]) + 10
              
        self.set_size_request(w, -1)
        
        box.add(self.label_time)
        box.add(self.label_date)
        
        gobject.timeout_add(1000, self.update)
        
        
    def update(self):
    
        try:
            now = time.localtime()
            ctime = "<span size=\"larger\" weight=\"bold\">%s</span>" % time.strftime(self.__format_time, now)
            cdate = time.strftime(self.__format_date, now)
            
            self.label_time.set_markup(ctime)
            self.label_date.set_text(cdate)
            
        except KeyboardInterrupt:
            pass
        
        return True
    
    def set_show_time(self, show): 
        if show: self.label_time.show()
        else: self.label_time.hide()
        
    def set_show_date(self, show): 
        if show: self.label_date.show()
        else: self.label_date.hide()
        
    def set_time_format(self, format):
        self.__format_time = format
    
    def set_date_format(self, format):
        self.__format_date = format

