
storage = "foopanel/config.xml"

from lib import globals
from lib.elementtree import ElementTree
import gtk, gtk.glade
import os, os.path



class PluginSettings:
    
    def __init__(self, node):
        self.__node = node
        
    def __getattr__(self, key):
        setting = self.__node.findtext(key)
        if setting == None:
            raise AttributeError, "There is no setting \"%s\" for plugin \"%s\"" \
                  % (key, self.__node.get("name"))
        return setting


class PluginList:
    
    __xml = None
    __plist = None
    __count = 0
    
    def __init__(self, xml):
        self.__xml = xml
        
    def __iter__(self):
        self.__plist = self.__xml.findall("plugins/plugin")
        self.__count = 0
        return self
    
    def next(self):
        
        if self.__count >= len(self.__plist):
            raise StopIteration
        
        item = self.__plist[self.__count]
        
        name = item.get("name")
        settings = PluginSettings(item)
        
        self.__count = self.__count + 1
                
        return (name, settings)
        


class FooConfig:
    
    class ConfDialog:
        
        def __init__(self, parent):
        
            self.__path_here = os.path.dirname(__file__)
            self.__parent = parent
        
            file = os.path.join(self.__path_here, "lib", "config_ui.glade")
        
            glade = gtk.glade.XML(file)
        
            self.dialog = glade.get_widget("configdialog")
            self.dialog.set_transient_for(globals.window)
            
            self.__notebook = glade.get_widget("notebook")
            self.__page_settings = self.__notebook.page_num(glade.get_widget("page_settings"))
            self.__page_plugins = self.__notebook.page_num(glade.get_widget("page_plugins"))
            
            self.__thememodel = gtk.ListStore(str)
            self.__themecombo = glade.get_widget("combo_themes")
            self.__themecombo.set_model(self.__thememodel)
            cr = gtk.CellRendererText()
            self.__themecombo.pack_start(cr, True)
            self.__themecombo.add_attribute(cr, 'text', 0)
            
            self.__heightscale = glade.get_widget("scale_height")
            
            self.__radiotop = glade.get_widget("radio_pos_top")
            self.__radiobtm = glade.get_widget("radio_pos_bottom")
            
            self.__checkontop = glade.get_widget("check_ontop")
            
            self.__set_values_to_gui()
                        
        
        def __set_values_to_gui(self):
            
            # Theme
            self.__thememodel.clear()
            for t in os.listdir(os.path.join(self.__path_here, "themes")):
            
                d = os.path.join(self.__path_here, "themes", t)
            
                if not os.path.isdir(d):
                    continue
                if not "gtkrc" in os.listdir(d):
                    continue
            
                iter = self.__thememodel.append([t])
            
                if t == str(self.__parent.theme):
                    self.__themecombo.set_active_iter(iter)
            
        
            # Height
            if not self.__parent.height:
                self.__parent.height = 60
            self.__heightscale.set_value(int(self.__parent.height))
        
        
            # Position
            if not self.__parent.position:
                self.__parent.position = "bottom"
            if str(self.__parent.position).lower() == "top":
                self.__radiotop.set_active(True)
            else:
                self.__radiobtm.set_active(True)
            
        
            # Keep on top
            if not self.__parent.ontop:
                self.__parent.ontop = True
            self.__checkontop.set_active(bool(self.__parent.ontop))
            
            
        def __run(self, mode):
            """ Run the configuration ui in the specified mode """
            self.__notebook.set_current_page(mode)
        
            response = self.dialog.run()
        
            self.dialog.hide()
        
            if response == gtk.RESPONSE_CANCEL:
                self.__set_values_to_gui()
                return
            
            if response == gtk.RESPONSE_OK:
                
                self.__parent.theme = self.__thememodel[self.__themecombo.get_active()][0]
                
                self.__parent.height = str(int(self.__heightscale.get_value()))
                
                if self.__radiotop.get_active():
                    pos = "top"
                else:
                    pos = "bottom"
                self.__parent.position = pos
                
                self.__parent.ontop = str(self.__checkontop.get_active())
                
                return
    
    
        def run_settings(self):
            """ Open the config ui at the settings page """
            self.__run(self.__page_settings)
        
    
        def run_plugins(self):
            """ Open the config ui at the plugins page """
            self.__run(self.__page_plugins)
            
            
        
            
            
            
    reserved = ['_FooConfig__reserved', '_FooConfig__xml', 'plugins', 'gui']

    def __init__(self):
        
        self.__xml = ElementTree.parse(os.path.realpath(storage))
        #self.__xml = xml.getroot()
        
        self.plugins = PluginList(self.__xml)
        
        self.gui = self.ConfDialog(self)
        
        #globals.window.connect("destroy", lambda w: self.__dump())
        gtk.quit_add(0, self.__dump)
        
        
        
        
    def __setattr__(self, key, value):
        
        if key in self.reserved:
            self.__dict__[key] = value
            return
            
        try:
            item = self.__xml.find("settings/%s" % key)
                
            if item:
                item.text = str(value)
                    
            else:
                node = ElementTree.Element(key)
                node.text = str(value)
                self.__xml.find("settings").append(node)
                
            print key, self.__xml.findtext("settings/%s" % key)
                
        except:
            raise
                
    
        
    
    def __getattr__(self, key):
        
            try:
                item = self.__xml.findtext("settings/%s" % key)
                if not item:
                    if key == "debug":
                        return False
                    raise AttributeError, "Foopanel configuration has no setting \"%s\"" % key
                return item
            except:
                raise
    
    
    def __dump(self):
        
        if self.debug:
            print "Final dump!"
        f = open(os.path.realpath(storage), "w")
        self.__xml.write(f)
        f.close()
        
            
        
        
    
