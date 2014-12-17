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
                            ([str, str, str, int])),
        # nick, server, channels, port
    }

    def __init__(self):
        Gtk.EventBox.__init__(self)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        boxi = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        form = Gtk.VBox()

        self.modify_bg(Gtk.StateType.NORMAL,
                       style.COLOR_WHITE.get_gdk_color())

        self.nick = Field("Nick", "solari_user")
        form.pack_start(self.nick, False, False, 5)

        self.server = Field("Server", "irc.freenode.net")
        form.pack_start(self.server, False, False, 5)

        self.port = Field("Port", "6667")
        form.pack_start(self.port, False, False, 5)

        self.channels = Field("Channels", "#solari-testing")
        form.pack_start(self.channels, False, False, 5)

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
            "channels": self.channels.get_value(),
            "port": int(self.port.get_value())
        }
        self.emit("connect-clicked",
                  data["nick"],
                  data["server"],
                  data["channels"],
                  data["port"])


class IRCTextView(Gtk.VBox):

    def __init__(self):
        Gtk.VBox.__init__(self)

        self.modify_bg(Gtk.StateType.NORMAL,
                       style.COLOR_WHITE.get_gdk_color())
        self.show_all()

    def add_message(self, from_whom, msg):
        hbox = Gtk.HBox()

        from_ = Gtk.Label()
        from_.set_width_chars(20)
        from_.set_label(from_whom)
        from_.set_justify(Gtk.Justification.LEFT)
        hbox.pack_start(from_, False, False, 5)

        message_box = Gtk.Label()
        message_box.set_line_wrap(True)
        message_box.set_label(msg)
        message_box.set_justify(Gtk.Justification.LEFT)
        hbox.pack_start(message_box, True, True, 5)

        self.pack_start(hbox, False, False, 5)
        hbox.show_all()

    def add_info_message(self, message):
        lb = Gtk.Label()
        lb.set_label(message)
        lb.set_justify(Gtk.Justification.LEFT)
        lb.set_line_wrap(True)
        self.pack_start(lb, False, False, 5)
        lb.show()


class ChannelNotebook(Gtk.Notebook):

    def __init__(self, activity):
        Gtk.Notebook.__init__(self)

        self._activity = activity
        self.channel_list = []

    def add_page(self, channel):
        


class IRCWidget(Gtk.HPaned):

    def __init__(self, ):
        Gtk.HPaned.__init__(self)

        self.text_place = Gtk.VBox()

        self.show_all()

    def add_privmsg(self, from_, msg):
        buffer_ = self.text_view.get_buffer()
        buffer_.insert(buffer_.get_end_iter(),
                       from_.ljust(20)+msg)
