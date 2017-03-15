# MIT License
#
# Copyright (c) 2017 Ricardo Velhote
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import gi
import logging

gi.require_version('Gtk', '3.0')
logging.basicConfig(level=logging.WARNING)

from gi.repository import GLib as glib


class QueryLoop():
    """QueryLoop accepts the indicator to which the result will be written and an exchange to obtain the results from.
    To define an exchange you only need to implement the query method and return the results in a pre-determined
    format so that it will be consistent."""

    def __init__(self, indicator, exchange):
        """Initialize the query loop with the indicator and the exchange to get the data from."""
        self.indicator = indicator
        self.exchange = exchange
        self.last_known = {"last": "0.00"}

    def loop(self):
        """Loop calls it-self forever and ever and will consult the exchange for the most current value and update
        the indicator's label content."""
        result = self.exchange.query()

        if result is not None:
            self.indicator.set_label("{} EUR".format(result["last"]))
            self.last_known = result
        else:
            self.indicator.set_label("Last Known: {} EUR (Error)".format(self.last_known["last"]))

        glib.timeout_add_seconds(5, self.loop)

    def start(self):
        """Starts the query loop it does not do anything else. It's merely a matter of naming because
        when initializing the loop in the main() point of entry."""
        self.loop()
