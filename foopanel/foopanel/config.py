
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
        
        self.__count += 1
                
        return (name, settings)
        


class FooConfig:
    
            
    reserved = ['_FooConfig__reserved', '_FooConfig__xml', 'plugins', 'gui']

    def __init__(self):
        
        self.__xml = ElementTree.parse(os.path.realpath(storage))
        #self.__xml = xml.getroot()
        
        self.plugins = PluginList(self.__xml)
        
        gtk.quit_add(0, self.__dump)
        
        
        
        
    def __setattr__(self, key, value):
        
        if key in self.reserved:
            self.__dict__[key] = value
            return
            
        try:
            item = self.__xml.find("settings/%s" % key)
            
            try:
                item.text = str(value)
            except:
                node = ElementTree.Element(key)
                node.text = str(value)
                self.__xml.find("settings").append(node)
                
        except:
            raise
                
    
        
    
    def __getattr__(self, key):
        
            try:
                item = self.__xml.find("settings/%s" % key)
                if not isinstance(item, ElementTree._ElementInterface):
                    if key == "debug":
                        return False
                    raise AttributeError, "Foopanel configuration has no setting \"%s\"" % key
                return item.text
            except:
                raise
    
    
    def __dump(self):
        
        if self.debug:
            print "Final dump!"
        f = open(os.path.realpath(storage), "w")
        self.__xml.write(f)
        f.close()
        
            
        
        
    
