#
# Foopanel "MENU" plugin
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


# TODO: 
#  - implement an optional FAM monitor to watch changes to menu



name           = "Menu"
version        = "0.1.1"
description    = "A new-concept auto-generated menu focused on ease-of-use."
requires       = {"pyxdg": "xdg"}
authors        = ["Federico Pelloni <federico.pelloni@gmail.com>"]
copyright = "Copyright (C) 2005 - 2006, Federico Pelloni"


from foopanel.lib import abstract, globals
import xdg.Menu, xdg.IconTheme
import gtk, gtk.gdk
import os, re




class FoopanelMenuWindow(abstract.PopupWindow):

    __is_size_set = False

    def __init__(self, name, description, icon):
    
        abstract.PopupWindow.__init__(self)
        
        self.set_header(name, description, icon)
        
        self.scroll = gtk.ScrolledWindow()
        self.scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        self.scroll.set_shadow_type(gtk.SHADOW_NONE)
        self.scroll.show()
        self.add(self.scroll, True)

        self.buttons = gtk.VBox(True, 0)
        self.buttons.show()
        self.scroll.add_with_viewport(self.buttons)
        #self.add(self.buttons, True)
        

    def append(self, obj):
    
        self.buttons.add(obj)
        obj.show()
        
        
    def toggle(self, widget):
    
        if not self.__is_size_set:
            w, h = self.buttons.size_request()
            self.scroll.set_size_request(w, \
                        min(h + 5, gtk.gdk.screen_height() - int(globals.height) - 200))
            self.__is_size_set = True
        
        self.scroll.get_vadjustment().set_value(0)
        
        abstract.PopupWindow.toggle(self, widget)
   
       




class item(gtk.Button):

    class item_info:
    
        name = None
        description = None
        command = None
        icon = None
        terminal = False
        

    def __init__(self, obj):
    
        gtk.Button.__init__(self)
        
        self.info = self.item_info()
        self.info.name = obj.getName().replace('&', '&amp;')
        self.info.description = obj.getComment().replace('&', '&amp;')
        self.info.command = obj.getExec()
        self.info.icon = xdg.IconTheme.getIconPath(obj.getIcon(), 24)
        self.info.terminal = obj.getTerminal()
        
        self.set_relief(gtk.RELIEF_NONE)
        
        cont = gtk.HBox(False, 10)
        cont.set_border_width(3)
        cont.show()
        self.add(cont)
   
        image = gtk.Image()
        try:
            pb = gtk.gdk.pixbuf_new_from_file_at_size(self.info.icon, 24, 24)
            #w = pb.get_width()
            #h = pb.get_height()
            #if h != 24:
            #    pb = pb.scale_simple(24, 24, gtk.gdk.INTERP_BILINEAR)
            image.set_from_pixbuf(pb)
        except:
            image.set_from_stock(gtk.STOCK_EXECUTE, gtk.ICON_SIZE_LARGE_TOOLBAR)
            image.set_pixel_size(24)
            
        image.show()
        cont.pack_start(image, False, False)
        
        label = gtk.Label()
        label.show()
        label.set_property("xalign", 0)
        label.set_markup("<b>%s</b>\n%s" % (self.info.name, self.info.description))
        cont.pack_start(label, True, True)
        
        



class separator(gtk.HSeparator):

    def __init__(self):
    
        gtk.HSeparator.__init__(self)
        
  



class menu(gtk.ToggleButton):

    def __init__(self, obj):
    
        gtk.ToggleButton.__init__(self)
        
        self.set_relief(gtk.RELIEF_NONE)
        
        self.set_name("EdgeButton")
        
        self.show()
        
        icon = obj.getIcon()
        try:
            image = gtk.Image()
            pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(\
                        xdg.IconTheme.getIconPath(icon, 24), 24, 24)
            image.set_from_pixbuf(pixbuf)
            image.show()
        except:
            image = gtk.image_new_from_stock(gtk.STOCK_EXECUTE, gtk.ICON_SIZE_BUTTON)
            image.show()
            pixbuf = None
        self.add(image)
        
        self.menu_name = obj.getName().replace('&', '&amp;')
        self.menu_description = obj.getComment().replace('&', '&amp;')
        
        self.items = FoopanelMenuWindow(self.menu_name, 
                                         self.menu_description, pixbuf)
        
        for i in obj.getEntries():
        
            ib = None
            if isinstance(i, xdg.Menu.Separator):
                ib = separator()
            elif hasattr(i, "DesktopEntry"):
                ib = item(i.DesktopEntry)
                if len(i.DesktopEntry.getOnlyShowIn()) > 0:
                    del(ib)
                    continue
                ib.connect("button-release-event", self.cb_clicked)
            
            if ib:
                self.items.append(ib)

         
        
    def cb_clicked(self, entry, event):
        
        exp = re.compile("\%[FU]{1}")
        
        if event.button == 1:
            
            cmd = exp.sub("", entry.info.command, 1)
            
        elif event.button == 3:
        
            dialog = gtk.FileChooserDialog(_("Select file to open with %s") %\
                            entry.info.name, 
                            globals.window, gtk.FILE_CHOOSER_ACTION_OPEN,
                            (gtk.STOCK_CANCEL, gtk.RESPONSE_NONE,
                             gtk.STOCK_OPEN, gtk.RESPONSE_ACCEPT))
            dialog.set_current_folder(os.environ["HOME"])
            r = dialog.run()
            
            if r == gtk.RESPONSE_NONE:
                dialog.destroy()
                self.close()
                return
                
            path = dialog.get_filename()
            
            dialog.destroy()
        
            cmd = exp.sub("%s", entry.info.command, 1) % path
            
        
        else:
        
            return
            
        self.close()
        
        if entry.info.terminal:
        
            try:
                term = os.environ["TERMCMD"]
            except:
                try:
                    term = os.environ["TERM"]
                except:
                    term = "xterm"
                    
            cmd = "%s -e %s" % (term, cmd)
        
                
        
        if bool(globals.config.debug):
            print _("Foopanel menu: launching %s (%s)") % \
                    (entry.info.name, cmd)

        
        #os.system(cmd+" &")
        os.spawnlp(os.P_NOWAIT, cmd, "&")
        
        

    
    def open(self):
    
        self.items.open(self)
        self.set_active(True)

        
        
    def close(self):
    
        self.items.hide()
        self.set_active(False)






class Plugin(abstract.Plugin):

    def __init__(self):
        
        abstract.Plugin.__init__(self)
        
        box = gtk.VBox(False, 1)
        box.show()
        self.add(box)
        
        al1 = gtk.Alignment(0.5, 0.0)
        al1.show()
        
        self.menu = gtk.HBox(False, 0)
        self.menu.show()
        al1.add(self.menu)
        
        self.description = gtk.Label("\n")
        self.description.set_justify(gtk.JUSTIFY_CENTER)
        pangolayout = self.description.get_layout()
        d_width = 0
        
        if str(globals.config.vposition) == "top":
            box.pack_start(self.description, False, False)
            box.pack_start(al1, True, True)
        else:
            box.pack_start(al1, True, True)
            box.pack_start(self.description, False, False)
            
        
        settings = self.get_settings()
        theme = settings.get_property("gtk-icon-theme-name")
        if theme:
            xdg.Config.setIconTheme(theme)
        
        
        for m in xdg.Menu.parse().getEntries():
            
            try:
                obj = menu(m)
            except:
                continue
            obj.connect("toggled", obj.items.toggle)
            obj.connect("enter-notify-event", self.manage_mouse_in)
            obj.connect("leave-notify-event", self.manage_mouse_out)
            pangolayout.set_markup("<b>%s</b>\n%s" %\
                                   (obj.menu_name, obj.menu_description))
            w = pangolayout.get_pixel_size()[0]
            d_width = max(d_width, w)
            self.menu.pack_start(obj, False, False)
            
        self.description.set_size_request(d_width, -1)
        self.description.show()
    
      
    
    def manage_mouse_in(self, widget, event):
    
        self.description.set_markup("<b>%s</b>\n%s" %\
             (widget.menu_name, widget.menu_description))
    
    
    def manage_mouse_out(self, widget, event):
    
        self.description.set_text("\n")
    
            
            
        
        


