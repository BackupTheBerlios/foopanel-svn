
storage = "foopanel/config.xml"

from lib import ElementTree, globals
import os.path

import gtk


class FooConfig(gtk.Dialog):

    def __init__(self):
        
        gtk.Dialog.__init__(self, "Foopanel settings", globals.window, \
                            gtk.DIALOG_DESTROY_WITH_PARENT, \
                            (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,\
                             gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))

        self.__xml = ElementTree.parse(os.path.realpath(storage))
        #self.__xml = xml.getroot()
        
    
    def __getattr__(self, key):
        
        if hasattr(self, key):
            #return getattr(self, key)
            return FooConfig.__getattr__(self, key)
        
        try:
            item = self.__xml.findall("plugins/plugin")
            if not item:
                raise AttributeError, "Foopanel configuration has no setting \"%s\"" % key
            print item
            return
        except:
            raise
        
    
    # This is an unused method made to quickly (de)comment this code
    def fake__comment(self):
                
        globals.config = FooConfigExported()

        root = xml.getroot()

        for setting in root.find("settings").getchildren():
            
            name = setting.tag
            value = setting.text
            
            #exec("self.%s = \"%s\"" % (name, value))
            globals.config.__dict__[name] = value
            
        
        globals.config.plugins = []
        
        for plugin in root.find("plugins").getchildren():
            
            name = plugin.get("name")
            if not name:
                continue
            
            settings = {}
            for setting in plugin.getchildren():
                
                key = setting.tag
                value = setting.text
                
                #exec("settings['%s'] = '%s'" % (key, value))
                settings[key] = value
                      
            pluginobj = (name, settings)
            
            globals.config.plugins.append(pluginobj)
            
        
        



if __name__ == "__main__":
    
    cfg = FooConfig()
    
    for i in dir(cfg):
        print i, getattr(cfg, i)

