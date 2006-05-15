
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



import globals, dconfig
import sys, os.path
import gtk

import abstract


def load_plugin(p, settings = None, reload_module = False, position = -1):

    errmsg = None
        
    try:
        
        if reload_module:
            reload(reload_module)
            plugin = reload_module
            action_verb = 'Reloading'
        else:
            exec("import plugins.%s as plugin" % p)
            action_verb = 'Loading'
            
        if bool(int(globals.config.debug)):
            print _("%s '%s'...") % (action_verb, plugin.name)

        
        not_satisfied = []
                    
        for package, test in plugin.requires.iteritems():
            try:
                __import__(test)
            except:
                not_satisfied.append(package)
                
        if len(not_satisfied) > 0:
            errmsg = _("It requires packages: %s") % string.join(not_satisfied, ", ")
            raise
        
        plugwidget = plugin.Plugin()
        #plug.build()
        
        expand = getattr(plugin, "expand", False)
        
        if hasattr(plugin, "register_functions"):
            for event, functions in plugin.register_functions.iteritems():
                for f in functions:
                    try:
                        globals.registered_functions[event].append(getattr(plugwidget, f))
                    except:
                        raise
        
        #gtk.threads_enter()
        globals.plugin_manager.pack_start(plugwidget, expand, expand)
        
        pobject = abstract.PluginObject(name      = plugin.name, 
                                        module    = plugin, 
                                        widget    = plugwidget, 
                                        settings  = settings)
        
        dconfig.DConfigLoad(pobject)
        
        if position > -1:
            globals.plugin_manager.reorder_child(plug, position)
            globals.plugins.insert(position, pobject)
        else:
            globals.plugins.append(pobject)
        #gtk.threads_leave()
        
        if bool(int(globals.config.debug)):
            print _("    ...done")
            
        pobject.widget.show()
            
        return pobject
        
    except:
        
        print _("Warning: Unable to load plugin '%s'") % p
        
        if errmsg:
            print errmsg
            
        if bool(int(globals.config.debug)):
            raise



def reload_plugin(index):

    plugin = globals.plugins[index]
    
    pos = globals.plugin_manager.get_children().index(plugin.widget)
        
    globals.plugin_manager.remove(plugin.widget)
    
    del(globals.plugins[index])

    return load_plugin(plugin.name, plugin.settings, plugin.module, pos)



def remove_plugin(plugin):
    
    globals.plugin_manager.remove(plugin.widget)
    
    globals.plugins.remove(plugin)
    
    if globals.config.debug:
        print _("Plugin '%s' removed" % plugin.name)



def move_plugin(plugin, position):
    
    children = globals.plugin_manager.get_children()
    curpos = children.index(plugin.widget)
    newpos = None
    
    if position == "top":
        newpos = 1
    elif position == "up":
        newpos = max(curpos - 1, 1)
    elif position == "down":
        newpos = min(curpos + 1, len(children) - 1)
    elif position == "bottom":
        newpos = -1
    
    if newpos != curpos:
        globals.plugin_manager.reorder_child(plugin.widget, newpos)
        return newpos
    else:
        return False
    



def load_theme(theme):
    try:
        if globals.config.debug:
            print _("Loading theme %s") % theme
        path = None
        for p in globals.paths.themes:
            try:
                path = os.path.join(p, theme, "gtkrc")
                if os.path.isfile(path):
                    break
                else:
                    path = None
            except:
                path = None
        if path is None or not os.path.isfile(path):
            raise
        gtk.rc_reset_styles(gtk.settings_get_default())
        gtk.rc_parse(path)
    except:
        print _("Warning: unable to load theme %s, using default" % theme)



def execute_registered(event):
    
    try:
        for f in globals.registered_functions[event]:
            f()
    except:
        pass

