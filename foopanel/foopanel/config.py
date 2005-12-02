
# Foopanel 0.0.2 - configuration file

# Enable the debug mode, with verbose error reporting
debug = True

# The panel height
height = 60
    
# Panel position, either "bottom" or "top"
position = "bottom"

# Whether to keep the panel over all windows
ontop = True

# The theme used to draw the panel and its components
# You must write the theme directory name under themes/ (e.g. "SolidBlue")
# To use the default GTK theme, just set to "None" (without quotes)
theme = "SolidBlue-png"
#theme = None

# List of components to load
# They'll be placed in this order, starting from left
# Currently available: see in components/ directory (write the file name
# without ".py")
plugins = [ 
            #"quickterminal",
            #"embedder",
            #"menu", 
            "flexible_space", 
            "windowlist",
            "pager",
            #"separator",
            #"searchbox", 
            #"reloader", 
            #"separator", 
            #"mediaplayer_control", 
            #"separator", 
            "clock"
          ]
    

