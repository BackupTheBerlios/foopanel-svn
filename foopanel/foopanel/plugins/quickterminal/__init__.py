
#
# Foopanel "QuickTerminal" plugin
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


name = "QuickTerminal"
version = "0.1"
description = "An always-ready terminal on Foopanel"
authors = ["Federico Pelloni <federico.pelloni@gmail.com>"]
requires = {"vte": "vte"}
expand = False


from foopanel.lib import abstract
import gtk
import vte



class TerminalWindow(abstract.PopupWindow):
    
    def __init__(self):

        abstract.PopupWindow.__init__(self, 3, gtk.WINDOW_TOPLEVEL)

        self.set_header("QuickTerminal", "Your terminal always ready.")
        
        terminal = vte.Terminal()

        self.connect("focus-in-event", lambda w,e: terminal.grab_focus())
        
        #terminal.set_background_transparent(True)
        terminal.set_emulation("xterm")
        terminal.set_font_from_string("monospace 9")
        terminal.set_allow_bold(True)
        terminal.set_scrollback_lines(100)

        terminal.show()

        box = gtk.HBox(False, 2)
        self.add(box)

        box.add(terminal)
        box.show()

        scrollbar = gtk.VScrollbar()
        scrollbar.show()
    	scrollbar.set_adjustment(terminal.get_adjustment())

        box.add(scrollbar)

        terminal.fork_command()
        
        terminal.connect("child-exited", self.__cb_exited)
        
    
    def __cb_exited(self, terminal):
        
        terminal.fork_command()
        self.toggle()







class Plugin(abstract.AbstractPlugin):

    def __init__(self, settings):
        
        abstract.AbstractPlugin.__init__(self)

        self._twindow = TerminalWindow()

        btn = gtk.ToggleButton()
        btn.set_name("EdgeButton")
        btn.connect("toggled", self._twindow.toggle)
        self.add(btn)

        box = gtk.VBox(False, 2)
        btn.add(box)

        img = gtk.image_new_from_icon_name("terminal", gtk.ICON_SIZE_BUTTON)
        box.add(img)

        lbl = gtk.Label(_("Terminal"))
        box.add(lbl)

        self.show_all()








