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



def build(filename, gui):

    #exec("from wrapper_%s import DConfigGuiWrapper" % gui)
    
    from wrapper_gtk import DConfigGuiWrapper
    
    class DConfigEngine(DConfigGuiWrapper):

        def __init__(self, filename):
        
            DConfigGuiWrapper.__init__(self)
        
            self.__filename = filename
            
            self.xml = ElementTree.parse(filename)
            
            root = self.xml.getroot()
            
            for s in root.findall("section"):

                section = self.new_section(s.attrib["name"])
                
                for i in s.getchildren():
                
                    tag = i.tag.lower()
                
                    if tag == "setting":
                    
                        self.parse_setting(i, section)
                            
                    elif tag == "group":
                        
                        g = self.parse_group(i, section)
                        
        
        
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
        
           
                        
        def parse_group(self, item, parent):
        
            g = self.new_group(item.attrib.get("title", None), parent)
            
            for i in item.getchildren():
                
                tag = i.tag.lower()
                
                if tag == "setting":
                    self.parse_setting(i, g)
                elif tag == "group":
                    self.parse_group(i, g)
                
            return g
            
                    
    
    return DConfigEngine(filename)




