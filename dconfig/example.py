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

DEFINITION = "conf-example.xml"
#DEFINITION = "foopanel.conf.xml"

STORAGE = "settings.conf"

GUI_WRAPPER="gtk"

import gtk
import os.path
import dconfig

# Test window
w = gtk.Window()
w.connect("destroy", gtk.main_quit)
w.set_title("D-Config")

# Create a DConfig object
x = dconfig.build(GUI_WRAPPER, DEFINITION)

# Add it to the window
x.set_border_width(3)
w.add(x)


# Use it in together with ConfigParser
from ConfigParser import SafeConfigParser

# Now create a ConfigParser object
cp = SafeConfigParser()
# and parse the STORAGE file
cp.read(STORAGE)

# For each setting in each section try to set the value saved
for section in cp.sections():
    for setting, value in cp.items(section):
        try:
            x.set(section, setting, value)
        except:
            pass


# Run the window
w.show_all()
gtk.main()

# Get the settings from the GUI
settings = x.get()

# Update them in the ConfigParser object
for section, settings in settings.iteritems():
    if not cp.has_section(section):
        cp.add_section(str(section))
    for setting, value in settings.iteritems():
        cp.set(str(section), str(setting), str(value))

# Finally, save them
file = open(STORAGE, "w")
cp.write(file)
file.close()
    
