#!/usr/bin/env python

# Solari Activity is an activity which makes IRC simple.
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

"""Solari Activity: An activity that makes IRC fun and simple"""

from gi.repository import Gtk
from gi.repository import GObject

from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.graphics.toolbutton import ToolButton
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.activity.widgets import StopButton

from widgets import StartScreen
from widgets import IRCWidget

from client import get_connected_client
from client import BasicHandler

from oyoyo.client import IRCClient
from oyoyo.cmdhandler import DefaultCommandHandler
from oyoyo import helpers


class Solari(activity.Activity):

    def __init__(self, handle):
        """Set up the activity."""
        activity.Activity.__init__(self, handle)
        self.max_participants = 1

        self._connection = None
        self._nick_lists = {}

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

    def _next_con(self):
        self._connection.next()
        GObject.idle_add(self._next_con)

    def connect_cb(self, cli):
        for c in self.channels:
            helpers.join(cli, c)

    def _start(self, widget, nick, server, channels, port):
        self.channels = [c.strip() for c in channels.split(",")]

        client = IRCClient(
            BasicHandler,
            host=server,
            port=port,
            nick=nick,
            connect_cb=self.connect_cb)
        client.get_handler().set_activity(self)

        self._connection = client.connect()
        GObject.idle_add(self._next_con)

        self.irc_widget = IRCWidget()
        self.set_canvas(self.irc_widget)

    def clean_nick(self, nick):
        return nick.split("!")[0]

    # IRC event handling starts here
    def privmsg(self, nick, channel, msg):
        nick = self.clean_nick(nick)
        self.irc_widget.add_privmsg(nick, msg)

    def joined(self, nick, channel):
        pass
