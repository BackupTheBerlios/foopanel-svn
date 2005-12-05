#!/usr/bin/python

#
# D-Config
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

FILE = "conf-example.xml"
#FILE="foopanel.conf.xml"

GUI_WRAPPER="gtk"

import gtk
import dconfig

w = gtk.Window()
w.connect("destroy", gtk.main_quit)
w.set_title("D-Config")

x = dconfig.build(FILE, GUI_WRAPPER)
x.set_border_width(3)
w.add(x)

w.show_all()
gtk.main()

