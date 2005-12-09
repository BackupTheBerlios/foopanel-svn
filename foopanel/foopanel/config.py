
storage = "foopanel/config.xml"

from lib import globals
from lib.elementtree import ElementTree
import os.path

import gtk


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

    def __init__(self):
        
        self.dialog = gtk.Dialog(_("Foopanel settings"), globals.window, \
                            gtk.DIALOG_DESTROY_WITH_PARENT, \
                            (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,\
                             gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))

        self.__xml = ElementTree.parse(os.path.realpath(storage))
        #self.__xml = xml.getroot()
        
        self.plugins = PluginList(self.__xml)
        
    
    def __getattr__(self, key):
        
        try:
            item = self.__xml.findtext("settings/%s" % key)
            if not item:
                raise AttributeError, "Foopanel configuration has no setting \"%s\"" % key
            return item
        except:
            raise
        
    
    
