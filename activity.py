#!/usr/bin/env python

# SimpleIRC Activity is an activity which makes IRC simple.
# Copyright (C) 2014  Sai Vineet

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""SimpleIRC Activity: An activity that makes IRC fun and simple"""

from gi.repository import Gtk
# import logging

# from gettext import gettext as _

from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.graphics.toolbutton import ToolButton
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.activity.widgets import StopButton

from widgets import StartScreen
# from widgets import IRCWidget


class SimpleIRC(activity.Activity):

    def __init__(self, handle):
        """Set up the activity."""
        activity.Activity.__init__(self, handle)

        # we do not have collaboration features
        # make the share option insensitive
        self.max_participants = 1

        # toolbar with the new toolbar redesign
        toolbar_box = ToolbarBox()

        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()

        clear_all = ToolButton("clear")
        toolbar_box.toolbar.insert(clear_all, -1)
        # clear_all.show()

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        # Start Screen, etc. starts here

        self.start_screen = StartScreen()
        self.start_screen.connect("connect-clicked", self._start)
        self.set_canvas(self.start_screen)

    def _start(self, widget, *data):
        print data
