#!/usr/bin/env python

# Pylint config
#
# DBus methods are CamelCase by convention, which pylint doesn't
# like.
#
#     pylint: disable=locally-disabled,invalid-name
#
#
# I don't have a solid understanding of what this warning
# means. Patches welcome!
#
#     pylint: disable=locally-disabled,interface-not-implemented

"""Example D-Bus service using python-dbus."""

from datetime import datetime, timedelta

import dbus
from dbus.exceptions import DBusException
import dbus.service
import dbus.mainloop.glib

import gobject

SERVICE_NAME = 'com.example.ExampleService'
INTERFACE_NAME = 'com.example.ExampleInterface'

class SimpleTimer(dbus.service.Object):
    """D-Bus object representing a simple timer."""

    def __init__(self, main_loop, bus):
        self.is_running = False
        self.tag = None
        self.duration = None
        self.start_time = None

        name = dbus.service.BusName(SERVICE_NAME, bus=bus)
        dbus.service.Object.__init__(self, name, '/SimpleTimer')

    @dbus.service.method(INTERFACE_NAME,
                         in_signature='us')
    def Start(self, duration_in_s, tag):
        if self.is_running:
            raise DBusException('already running', self.tag)
        else:
            self.tag = tag
            self.is_running = True
            self.duration = timedelta(seconds=duration_in_s)
            self.start_time = datetime.now()
            gobject.timeout_add(250, self.update)

    @dbus.service.signal(INTERFACE_NAME, signature='s')
    def Progress(self, output):
        return output

    def stop(self):
        self.is_running = False

    def update(self):
        now = datetime.now()
        self.Progress('{}s out of {}s'.format(
            (datetime.now() - self.start_time).seconds,
            self.duration.seconds))

        done = now >= (self.start_time + self.duration)
        if done:
            self.stop()
        return not done


def main():
    """Initialize service and start event loop."""
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    main_loop = gobject.MainLoop()
    bus = dbus.SessionBus()

    SimpleTimer(main_loop, bus)

    main_loop.run()


if __name__ == '__main__':
    main()
