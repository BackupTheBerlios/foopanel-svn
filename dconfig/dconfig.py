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


import ElementTree



def build(gui, file_definition):

    try:
        exec ("from wrapper_%s import DConfigGuiWrapper" % gui) in globals()
    except ImportError:
        print "Wrapper %s not found" % gui
        raise
    
    
    
    class DConfigEngine(DConfigGuiWrapper):
        
        __settings = {}

        def __init__(self, file_definition):
        
            DConfigGuiWrapper.__init__(self)
        
            self.__file_definition = file_definition
            
            #self.__file_storage = file_storage
            
            self.xml = ElementTree.parse(file_definition)
            
            root = self.xml.getroot()
            
            for section in root.findall("section"):
                
                name = section.attrib.get("name", None)
                if not name:
                    continue
                s = self.new_section(str(name))
                self.__settings[str(name).lower()] = {}
                self.parse_struct(section, s, self.__settings[str(name).lower()])
            
        
            
            
        def parse_struct(self, struct, parent, storage):
            
            for child in struct.getchildren():
                
                tag = child.tag.lower()
                
                if tag == "setting":
                    
                    s = self.parse_setting(child, parent)
                    name = child.attrib.get("name", None)
                    if not name:
                        continue
                    storage[name.lower()] = s
                            
                elif tag == "group":
                    
                    group = self.new_group(child.attrib.get("title", None), parent)
                    
                    self.parse_struct(child, group, storage)
                        
            
        
        
        def parse_setting(self, item, parent):
            
            try:
                itype = item.attrib["type"].lower()
            except:
                return
            
            w = None
            
            if itype == "boolean":
                
                default = item.attrib.get("default", "off")
                w = self.new_setting_boolean(item.attrib["description"], parent, default)
            
            
            elif itype == "number":

                smin = item.attrib.get("min", None)
                smax = item.attrib.get("max", None)
                default = item.attrib.get("default", None)
                digits = 0
                if smin != None:
                    p = smin.split(".")
                    if len(p) > 1:
                        digits = len(p[1])
                if smax != None:
                    p = smax.split(".")
                    if len(p) > 1 and len(p[1]) > digits:
                        digits = len(p[1])
                w = self.new_setting_number(item.attrib["description"],\
                                             parent, digits, default, smin, smax)
            
            
            elif itype == "switch":
            
                default = item.attrib.get("default", None)
                
                options = []
                for o in item.findall("option"):
                
                    v = o.attrib.get("value", None)
                    if not v:
                        continue
                    t = o.attrib.get("text", v)
                    options.append((v, t))
                        
                w = self.new_setting_switch(item.attrib["description"], parent, options, default)
                
                   
                        
            elif itype == "text":
            
                default = item.attrib.get("default", None)
                tmax = item.attrib.get("max", 0)
                w = self.new_setting_text(item.attrib["description"], parent, default, tmax)
                  
            
            elif itype == "radio":
            
                default = item.attrib.get("default", None)
                
                options = []
                for o in item.findall("option"):

                    v = o.attrib.get("value", None)
                    if not v:
                        continue
                    options.append((v))
                        
                w = self.new_setting_radio(item.attrib["description"], parent, options, default)
            
            if w:    
                return w
        
        
        def get(self):
           
            out = {}
            for section, settings in self.__settings.iteritems():
                out[section] = {}
                #print "Section \"%s:\"" % section
                for setting, widget in settings.iteritems():
                    value = widget.get()
                    out[section][setting] = value
                #    print " %s = %s" % (setting, value)
                    
            return out
                
        
        def set(self, section, setting, value):
            
            self.__settings[section][setting].set(value)
                                    
    
    return DConfigEngine(file_definition)




