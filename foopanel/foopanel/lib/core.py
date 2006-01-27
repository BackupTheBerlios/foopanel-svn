
#
# Foopanel
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


import gtk, gtk.gdk, gobject
import sys, os.path, string

import globals, functions, abstract, config


path_here = os.path.dirname(__file__)
pluginpath = os.path.realpath(os.path.join(path_here, "..", "plugins"))


class PluginManager(gtk.HBox):


    def __init__(self):

        gtk.HBox.__init__(self, False, 5)

        self.set_name("PluginManager")

        globals.plugin_manager = self
        
        self.pack_start(FooMenu(), False, False)

        for p in globals.config.plugins:

                functions.load_plugin(p[0], p[1])
                continue

        self.show()

        functions.execute_registered('on_finish')
        


            
class Gui(abstract.FoopanelWindow):

    def __init__(self):

        abstract.FoopanelWindow.__init__(self, True)

        self.set_title("Foopanel")
        self.set_name("FoopanelWindow")
        self.resize()
        
        self.set_keep_above(bool(globals.config.ontop))
        
        globals.window = self
        
    
    def resize(self):
        
        try:
            cwidth = int(globals.config.width)
        except:
            cwidth = 100
        width = max(1, int(gtk.gdk.screen_width() * cwidth / 100))
        height = max(1, int(globals.config.height))
        abstract.FoopanelWindow.resize(self, width, height)
        
        globals.requested_size = (width, height)
        globals.width, globals.height = self.get_size()
        
        self.reposition()
        
        functions.execute_registered('on_resize')
        
    
    def reposition(self):

        try: hpos = globals.config.hposition.lower()
        except: hpos = "center"
        
        try: vpos = globals.config.vposition.lower()
        except: vpos = "bottom"
        
        if hpos == "left": x = 0
        elif hpos == "right": x = int(gtk.gdk.screen_width() - globals.width)
        else: x = int((gtk.gdk.screen_width() - globals.width)/2)
            
        if vpos == "top": y = 0
        else: y = gtk.gdk.screen_height() - int(globals.height)

        self.move(x, y)
        globals.window_x = x
        globals.window_y = y
        
        try:
            globals.opened_popup.reposition()
        except:
            pass


    def run(self):

        self.show()

        gtk.main()



class AboutWindow(gtk.AboutDialog):

    def __init__(self):
    
        gtk.AboutDialog.__init__(self)
        
        for i in dir(globals.app):
            if i[0] != "_":
                eval("self.set_%s(globals.app.%s)" % (i, i))
                
                


globals.aboutwindow = AboutWindow()
globals.tooltips = gtk.Tooltips()
globals.tooltips.enable()


class FooMenu(gtk.ToggleButton):

    class FooMenuWindow(abstract.PopupWindow):
    
        class button(gtk.Button):
        
            def __init__(self, stock):
            
                gtk.Button.__init__(self, None, stock)
                self.set_relief(gtk.RELIEF_NONE)
                self.set_alignment(0, 0.5)
                
    
        def __init__(self):
        
            abstract.PopupWindow.__init__(self)
            
            #self.set_header("Foopanel", "Settings and information")
            
            box = gtk.HBox(False, 0)
            box.set_border_width(0)
            self.add(box)
            
            plugins = gtk.Button()
            plugins.connect("clicked", lambda w: globals.config.gui.run_plugins())
            plugins.set_relief(gtk.RELIEF_NONE)
            b = gtk.HBox(False, 1)
            plugins.add(b)
            b.pack_start(gtk.image_new_from_stock(gtk.STOCK_HARDDISK, gtk.ICON_SIZE_BUTTON))
            lbl = gtk.Label(_("_Plugins"))
            lbl.set_use_underline(True)
            b.add(lbl)
            box.add(plugins)
            
            settings = self.button(gtk.STOCK_PREFERENCES)
            settings.connect("clicked", lambda w: globals.config.gui.run_settings())
            box.add(settings)
            
            about = self.button(gtk.STOCK_ABOUT)
            about.connect("clicked", lambda w: globals.aboutwindow.run())
            box.add(about)
            
            exit = self.button(gtk.STOCK_QUIT)
            exit.connect("clicked", gtk.main_quit)
            box.add(exit)
            
            box.show_all()
        
        

    def __init__(self):
    
        gtk.ToggleButton.__init__(self)
        
        globals.tooltips.set_tip(self, _("Foopanel menu"))
        
        self.set_name("EdgeButton")
        
        if globals.config.vposition == "top":
            arr_dir = gtk.ARROW_DOWN
        else:
            arr_dir = gtk.ARROW_UP
        arrow = gtk.Arrow(arr_dir, gtk.SHADOW_IN)
        self.add(arrow)
        
        self.menu = self.FooMenuWindow()
        self.connect("toggled", self.menu.toggle)
        
        self.show_all()


class ConfDialog:
    
   
    def __init__(self):
    
        file = os.path.join(path_here, "config_ui.glade")
    
        glade = gtk.glade.XML(file)
    
        self.dialog = glade.get_widget("configdialog")
        #self.dialog.set_transient_for(globals.window)
        
        self.__notebook = glade.get_widget("notebook")
        self.__page_settings = self.__notebook.page_num(glade.get_widget("page_settings"))
        self.__page_plugins = self.__notebook.page_num(glade.get_widget("page_plugins"))
        
        
        ### SETTING: THEME
        self.__thememodel = gtk.ListStore(str)
        self.__themecombo = glade.get_widget("combo_themes")
        self.__themecombo.set_model(self.__thememodel)
        cr = gtk.CellRendererText()
        self.__themecombo.pack_start(cr, True)
        self.__themecombo.add_attribute(cr, 'text', 0)
                
        def cb_change_theme(combo):
            """ CB: load the new theme and save it into preferences """
            theme = self.__thememodel[combo.get_active()][0]
            if theme != globals.config.theme:
                if theme == "None":
                    gtk.rc_reset_styles(gtk.settings_get_default())
                else:
                    functions.load_theme(theme)
                globals.config.theme = theme
        
        self.__themecombo.connect("changed", cb_change_theme)
        
        
        ### SETTING: HEIGHT
        def cb_change_height(scale):
            height = int(scale.get_value())
            globals.config.height = height
            globals.window.resize()
        self.__heightscale = glade.get_widget("scale_height")
        self.__heightscale.connect("value-changed", cb_change_height)
        
        
        ### SETTING: WIDTH
        def cb_change_width(scale):
            width = int(scale.get_value())
            globals.config.width = width
            globals.window.resize()
        self.__widthscale = glade.get_widget("scale_width")
        self.__widthscale.connect("value-changed", cb_change_width)
        
        
        ### SETTING: VERTICAL POSITION
        def cb_change_vpos(btn):
            if btn.get_active():
                 vpos = "top"
            else:
                 vpos = "bottom"
            globals.config.vposition = vpos
            globals.window.reposition()
        self.__radiotop = glade.get_widget("radio_pos_top")
        self.__radiobtm = glade.get_widget("radio_pos_bottom")
        self.__radiotop.connect("toggled", cb_change_vpos)
        
        
        ### SETTING: HORIZONTAL POSITION
        def cb_change_hpos(btn):
            if self.__radiolft.get_active():
                hpos = "left"
            elif self.__radiorgt.get_active():
                hpos = "right"
            else:
                hpos = "center"
            globals.config.hposition = hpos
            globals.window.reposition()
        self.__radiolft = glade.get_widget("radio_pos_left")
        self.__radiocnt = glade.get_widget("radio_pos_center")
        self.__radiorgt = glade.get_widget("radio_pos_right")
        self.__radiolft.connect("toggled", cb_change_hpos)
        self.__radiocnt.connect("toggled", cb_change_hpos)
        
        
        ### SETTING: KEEP ON TOP
        def cb_change_kot(btn):
            kot = btn.get_active()
            globals.config.ontop = str(kot)
            globals.window.set_keep_above(kot)
        self.__checkontop = glade.get_widget("check_ontop")
        self.__checkontop.connect("toggled", cb_change_kot)
        
        
        ### PLUGINS ###
        import gobject
        self.__pluginstore = gtk.ListStore(gobject.TYPE_PYOBJECT, str)
        self.__plugintree = glade.get_widget("tree_plugins")
        self.__plugintree.set_headers_visible(False)
        self.__plugintree.set_model(self.__pluginstore)
        column = gtk.TreeViewColumn("Plugin")
        self.__plugintree.append_column(column)
        crend = gtk.CellRendererText()
        column.pack_start(crend, True)
        column.add_attribute(crend, 'text', 1)
        
        self.__frmselplug = glade.get_widget("frame_selected_plugin")
        
        selection = self.__plugintree.get_selection()
        
        def cb_plugin_selected(sel):
            model, iter = sel.get_selected()
            if iter is None:
                self.__frmselplug.set_sensitive(False)
            else:
                self.__frmselplug.set_sensitive(True)
        
        selection.connect("changed", cb_plugin_selected)
        
        ### Utility: get selected plugin
        def sel_get_plugin():
            model, iter = selection.get_selected()
            plugin = model.get_value(iter, 0)
            return plugin
        
        
        ### PLUGIN: ADD
        self.__addplmodel = gtk.ListStore(str, str)
        self.__comboaddpl = glade.get_widget("combo_add_plugin")
        self.__comboaddpl.set_model(self.__addplmodel)
        crend2 = gtk.CellRendererText()
        self.__comboaddpl.pack_start(crend2, True)
        self.__comboaddpl.add_attribute(crend2, 'markup', 0)
        
        def cb_plugin_add(btn):
            c = self.__comboaddpl
            model = c.get_model()
            plugin = model[c.get_active()][1]
            settings = globals.config.plugins.append(plugin)
            functions.load_plugin(plugin, settings)
            #self.__parse_plugin(plugin)
            iter = self.__pluginstore.append((globals.plugins[-1], globals.plugins[-1][0]))
            selection.select_iter(iter)
        self.__buttnaddpl = glade.get_widget("button_add_plugin")
        self.__buttnaddpl.connect("clicked", cb_plugin_add)
        
        
        ### PLUGIN: INFO
        def cb_plugin_info(btn):
            plugin = sel_get_plugin()[1]
            w = gtk.AboutDialog()
            w.set_name(plugin.name)
            w.set_comments(plugin.description)
            w.set_version(plugin.version)
            w.set_authors(plugin.authors)
            w.run()
        self.__btnpluginfo = glade.get_widget("button_plugin_about")
        self.__btnpluginfo.connect("clicked", cb_plugin_info)
        
        self.__btnplugsettings = glade.get_widget("button_plugin_settings")
        
        ### PLUGIN: REMOVE
        def cb_plugin_remove(btn):
            plugin = sel_get_plugin()
            functions.remove_plugin(plugin)
            self.__pluginstore.remove(selection.get_selected()[1])
            del globals.config.plugins[plugin[3]]
        self.__btnplugremove = glade.get_widget("button_plugin_remove")
        self.__btnplugremove.connect("clicked", cb_plugin_remove)
        
        ### PLUGIN: MOVE
        def cb_plugin_move(btn, where):
            plugin = sel_get_plugin()
            pos = functions.move_plugin(plugin, where)
            if pos:
                model, iter = selection.get_selected()
                if where == "top":
                    model.move_after(iter, None)
                elif where == "up":
                    model.move_before(iter, model.get_iter((model.get_path(iter)[0]-1)))
                elif where == "down":
                    model.move_after(iter, model.iter_next(iter))
                elif where == "bottom":
                    model.move_before(iter, None)
                globals.config.plugins.move(plugin[3], pos - 1)
        # Top
        self.__btnplugtop = glade.get_widget("button_plugin_top")
        self.__btnplugtop.connect("clicked", cb_plugin_move, "top")
        # Up
        self.__btnplugup = glade.get_widget("button_plugin_up")
        self.__btnplugup.connect("clicked", cb_plugin_move, "up")
        # Down
        self.__btnplugdown = glade.get_widget("button_plugin_down")
        self.__btnplugdown.connect("clicked", cb_plugin_move, "down")
        # Bottom
        self.__btnplugbtm = glade.get_widget("button_plugin_bottom")
        self.__btnplugbtm.connect("clicked", cb_plugin_move, "bottom")
        
        self.__set_values_to_gui()
        
                    
    
    def __set_values_to_gui(self):
        
        # Theme
        self.__thememodel.clear()
        activeiter = self.__thememodel.append(["None"])
        
        for t in os.listdir(os.path.join(path_here, "..", "themes")):
        
            d = os.path.join(path_here, "..", "themes", t)
        
            if not os.path.isdir(d):
                continue
            if not "gtkrc" in os.listdir(d):
                continue
        
            iter = self.__thememodel.append([t])
        
            if t == str(globals.config.theme):
                activeiter = iter
        
        self.__themecombo.set_active_iter(activeiter)
        
        # Width
        if globals.config.width is None:
            globals.config.width = 100
        self.__widthscale.set_value(int(globals.config.width))
        
        # Height
        if globals.config.height is None:
            globals.config.height = 60
        self.__heightscale.set_value(int(globals.config.height))
    
    
        # Position
        if globals.config.vposition is None:
            globals.config.vposition = "bottom"
        if str(globals.config.vposition).lower() == "top":
            self.__radiotop.set_active(True)
        else:
            self.__radiobtm.set_active(True)
            
        if globals.config.hposition is None:
            globals.config.hposition = "center"
        if str(globals.config.vposition).lower() == "left":
            self.__radiolft.set_active(True)
        elif str(globals.config.vposition).lower() == "right":
            self.__radiorgt.set_active(True)
        else:
            self.__radiocnt.set_active(True)
        
    
        # Keep on top
        if globals.config.ontop is None:
            globals.config.ontop = True
        self.__checkontop.set_active(bool(globals.config.ontop))
        
        
        self.__init_pluginview()
        
    
    def __parse_plugin(self, t):
        
        d = os.path.join(pluginpath, t)

        if not os.path.isdir(d):
            return False
        if not "__init__.py" in os.listdir(d):
            return False
        
        try:
            exec("import plugins.%s as plugin" % t)
            self.__addplmodel.append( ("<b>%s</b>\n%s" % (plugin.name, plugin.description), t) )
        except:
            raise
    
    
    def __init_pluginview(self):
        
        self.__frmselplug.set_sensitive(False)
    
        self.__pluginstore.clear()
        
        for p in globals.plugins:
            
            self.__pluginstore.append((p, p[0]))
        
        
        self.__addplmodel.clear()
        
        for t in os.listdir(pluginpath):
        
            self.__parse_plugin(t)
        
        
        
    
    
    def __run(self, mode):
        """ Run the configuration ui in the specified mode """
        
        self.__notebook.set_current_page(mode)
        
        self.__set_values_to_gui()
    
        response = self.dialog.run()
    
        self.dialog.hide()
    
        #        if response == gtk.RESPONSE_CANCEL:
        #            self.__set_values_to_gui()
        #            return
        #        
        #        if response == gtk.RESPONSE_OK:
        #            
        #            globals.config.theme = self.__thememodel[self.__themecombo.get_active()][0]
        #            
        #            globals.config.height = str(int(self.__heightscale.get_value()))
        #            
        #            if self.__radiotop.get_active():
        #                vpos = "top"
        #            else:
        #                vpos = "bottom"
        #            globals.config.vposition = vpos
        #            
        #            if self.__radiolft.get_active():
        #                hpos = "left"
        #            elif self.__radiorgt.get_active():
        #                hpos = "right"
        #            else:
        #                hpos = "center"
        #            globals.config.hposition = hpos
        #            
        #            globals.config.ontop = str(self.__checkontop.get_active())
            
        return


    def run_settings(self):
        """ Open the config ui at the settings page """
        self.__run(self.__page_settings)
    

    def run_plugins(self):
        """ Open the config ui at the plugins page """
        self.__run(self.__page_plugins)
