
#
# Foopanel
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



import globals
import sys, os.path

sys.path.append(os.path.realpath('./foopanel/'))


def load_plugin(p, settings = None, reload_module = False, position = -1):

    errmsg = None
        
    try:
    
        if reload_module:
            reload(reload_module)
            plugin = reload_module
        else:
            exec("import plugins.%s as plugin" % p)
        
        not_satisfied = []
                    
        for package, test in plugin.requires.iteritems():
            try:
                __import__(test)
            except:
                not_satisfied.append(package)
                
        if len(not_satisfied) > 0:
            errmsg = _("It requires packages: %s") % string.join(not_satisfied, ", ")
            raise
        
        plug = plugin.Plugin(settings)
        plug.show()
        #plug.build()
        
        expand = getattr(plugin, "expand", False)
        
        if hasattr(plugin, "register_functions"):
            for event, functions in plugin.register_functions.iteritems():
                for f in functions:
                    try:
                        globals.registered_functions[event].append(getattr(plug, f))
                    except:
                        raise

        globals.plugin_manager.pack_start(plug, expand, expand)
        
        if position > -1:
            globals.plugin_manager.reorder_child(plug, position)
            globals.plugins.insert(position, (plugin.name, plugin, plug))
        else:
            globals.plugins.append((plugin.name, plugin, plug))
        
        if reload_module:
            s = 'reloaded'
        else:
            s = 'loaded'
        
        if globals.config.debug:
            print _("Plugin '%s' %s.") % (plugin.name, s)
            
        return True
        
    except:
        
        print _("Warning: Unable to load plugin '%s'") % p
        
        if errmsg:
            print errmsg
            
        if globals.config.debug:
            raise



def reload_plugin(index):

    name, module, widget = globals.plugins[index]
    
    pos = globals.plugin_manager.get_children().index(widget)
        
    globals.plugin_manager.remove(widget)
    
    del(globals.plugins[index])

    return load_plugin(name, widget.__settings, module, pos)



