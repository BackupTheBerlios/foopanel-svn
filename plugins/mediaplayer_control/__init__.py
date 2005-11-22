
#
# Foopanel MEDIACONTROL plugin
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

name = "MediaPlayer control"
version = "0.1"
description = "Multimedia controls for media player"
authors = ["Federico Pelloni <federico.pelloni@gmail.com>"]
requires = {}


# The player to control
# (file "player_wrapper.py" must exist)
player = "quodlibet"


exec("from %s_wrapper import Plugin" % player)
