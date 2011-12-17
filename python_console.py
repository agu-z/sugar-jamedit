#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#       python_console.py by/por:
#       Agustin Zubiaga <aguszs97@gmail.com>
#       Daniel Francis <santiago.danielfrancis@gmail.com>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 3 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.


import gtk
import vte

from signal import SIGTERM

import os
import sys


class PythonConsole(vte.Terminal):

    def __init__(self):
        vte.Terminal.__init__(self)

        self.fork_command("python")
        
        self.set_size_request(800, 150)
        
    def _clear_console(self):
        self.grab_focus()
        self.feed("\x1B[H\x1B[J\x1B[0;39m")

class PythonCodeRun(vte.Terminal):
    
    def __init__(self):
        vte.Terminal.__init__(self)
        
        self.set_size_request(800, 150)

    def _run(self, file):
        self.process_id = self.fork_command \
                          (command = "/bin/sh",
                           argv = ["/bin/sh", "-c",
                                   "python %s; sleep 1" % file])
    def _stop(self):
        try:
            os.kill(self.process_id, SIGTERM)
            self._clear_console()
        except:
            pass

    def _clear_console(self):
        self.grab_focus()
        self.feed("\x1B[H\x1B[J\x1B[0;39m")
