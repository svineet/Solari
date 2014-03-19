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

from gi.repository import Gtk
from gi.repository import GObject

from sugar3.graphics import style


class Field(Gtk.HBox):

    def __init__(self, label, prepopulate):
        Gtk.HBox.__init__(self)

        lb = Gtk.Label()
        lb.set_markup(
            "<span size='large' foreground='%s'>%s</span>" % (
                style.COLOR_BUTTON_GREY.get_html(),
                label))
        lb.show()
        self.pack_start(lb, True, False, 0)

        self.entry = Gtk.Entry()
        self.entry.set_text(prepopulate)
        self.pack_end(self.entry, True, True, 0)
        self.entry.show()

    def get_value(self):
        return self.entry.get_text()


class StartScreen(Gtk.EventBox):
    __gsignals__ = {
        'connect-clicked': (GObject.SignalFlags.RUN_FIRST,
                            None,
                            ([str, str, int])),
        # nick, server, port
    }

    def __init__(self):
        Gtk.EventBox.__init__(self)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        boxi = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        form = Gtk.VBox()

        self.modify_bg(Gtk.StateType.NORMAL,
                       style.COLOR_WHITE.get_gdk_color())

        self.nick = Field("Nick", "svineet")
        form.pack_start(self.nick, False, False, 0)

        self.server = Field("Server", "irc.freenode.net")
        form.pack_start(self.server, False, False, 0)

        self.port = Field("Port", "6667")
        form.pack_start(self.port, False, False, 0)

        enter = Gtk.Button(label="Connect!")
        enter.connect("clicked", self.__connect_clicked)
        form.add(enter)
        enter.show()

        boxi.pack_start(form, True, False, 0)
        box.pack_start(boxi, True, False, 0)
        self.add(box)
        self.show_all()

    def __connect_clicked(self, button):
        data = {
            "nick": self.nick.get_value(),
            "server": self.server.get_value(),
            "port": int(self.port.get_value())
        }
        self.emit("connect-clicked",
                  data["nick"],
                  data["server"],
                  data["port"])
