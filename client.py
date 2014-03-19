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

from oyoyo.client import IRCClient
from oyoyo.cmdhandler import DefaultCommandHandler
from oyoyo import helpers

channels = []


class BasicHandler(DefaultCommandHandler):

    def privmsg(self, nick, channel, msg):
        print msg


def connect_cb(cli):
    global channels
    for c in channels:
        helpers.join(cli, c)


def get_connected_client(handler, host, port, nick, channels1):
    global channels
    channels = channels1.split(",")
    cli = IRCClient(
        handler,
        host=host,
        port=port,
        nick=nick,
        connect_cb=connect_cb)
    conn = cli.connect()
    return conn


def run_example():
    h = get_connected_client(
        BasicHandler,
        "irc.freenode.net",
        6667, "svineet_test_oyoyo",
        "#sugar,#meeting-test")
    while True:
        h.next()

if __name__ == "__main__":
    run_example()
