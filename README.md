# Purpose

Quick example of how to use python-dbus to make a service. Putting it
up on Github for my own future reference, and if anyone else finds
this and wants to contribute improvements to improve or expand the
example, feedback and patches welcome!

# Resources

http://dbus.freedesktop.org/doc/dbus-python/doc/tutorial.html

http://dbus.freedesktop.org/doc/dbus-python/api/dbus-module.html

http://0pointer.net/blog/the-new-sd-bus-api-of-systemd.html

# Usage

Start the service:
`./example_service.py`

Call the Start method:

`dbus-send --print-reply --type=method_call --dest=com.example.ExampleService /SimpleTimer com.example.ExampleInterface.Start uint64:10 string:my-tag`

Watch the progress:
`dbus-monitor`

