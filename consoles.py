#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#       consoles.py by/por:
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

from signal import SIGTERM
import os

import pango
import gtk
import vte

from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.colorbutton import ColorToolButton
from sugar.graphics.tray import VTray

class Console(gtk.HBox):
        def __init__(self):
                gtk.HBox.__init__(self)
                self.terminal = vte.Terminal()
                self.bgcolor = gtk.gdk.color_parse("#000000")
                self.fgcolor = gtk.gdk.color_parse("#FFFFFF")
                self.scrollbar = gtk.VScrollbar(self.terminal.get_adjustment())
                self.terminal.show()
                self.scrollbar.show()
                self.pack_start(self.terminal, True, True, 0)
                self.pack_end(self.scrollbar, False, True, 0)
                self.terminal.grab_focus()
        
        def set_font(self, font):
                self.terminal.set_font(font)
        
        def set_bgcolor(self, color):
                self.terminal.set_colors(self.fgcolor, color, [])
                self.bgcolor = color
        
        def set_fgcolor(self, color):
                self.terminal.set_colors(color, self.bgcolor, [])
                self.fgcolor = color
        
        def copy(self):
                if self.terminal.get_has_selection():
                        self.terminal.copy_clipboard()
        
        def paste(self):
                self.terminal.paste_clipboard()
        
        def stop(self):
                try:
                        os.kill(self.process_id, SIGTERM)
                        self._clear_console()
                except Exception, err:
                        print err
        
        def _clear_console(self):
                self.terminal.grab_focus()
                self.terminal.feed("\x1B[H\x1B[J\x1B[0;39m")
        
        def run_command(self, command=None, args=None):
                self.process_id = self.terminal.fork_command(command=command, argv=args)

class Terminal(gtk.HBox):
        def __copy_cb(self, button):
                self.console.copy()
        
        def __paste_cb(self, button):
                self.console.paste()
        
        def _fgcolor_cb(self, button, pspec):
                newcolor = button.get_color()
                self.console.set_fgcolor(newcolor)
        
        def _bgcolor_cb(self, button, pspec):
                newcolor = button.get_color()
                self.console.set_bgcolor(newcolor)
        
        def update_font(self, widget, font_selection):
                font = pango.FontDescription(font_selection.get_font_name())
                self.console.set_font(font)
        
        def reset(self, widget):
                self.console.stop()
                self.console.run_command()
        
        def __init__(self):
                gtk.HBox.__init__(self)
                self.toolbar = VTray()
                
                copy = ToolButton("edit-copy")
                copy.set_tooltip('Copy')
                copy.connect("clicked", self.__copy_cb)
                copy.show()
                self.toolbar.add_item(copy, -1)
                paste = ToolButton("edit-paste")
                paste.set_tooltip("Paste")
                paste.connect("clicked", self.__paste_cb)
                paste.show()
                self.toolbar.add_item(paste, -1)
                
                fgcolor = ColorToolButton()
                fgcolor.get_child()._title = "Font Color"
                self.toolbar.add_item(fgcolor, -1)
                fgcolor.connect('notify::color', self._fgcolor_cb)
                fgcolor.show_all()
                bgcolor = ColorToolButton()
                bgcolor.get_child()._title = "Background Color"
                bgcolor.connect('notify::color', self._bgcolor_cb)
                self.toolbar.add_item(bgcolor, -1)
                bgcolor.show_all()
                
                self.console = Console()
                self.console.set_bgcolor(gtk.gdk.color_parse("#FFFFFF"))
                self.console.set_fgcolor(gtk.gdk.color_parse("#000000"))
                bgcolor.set_color(gtk.gdk.color_parse("#FFFFFF"))
                fgcolor.set_color(gtk.gdk.color_parse("#000000"))
                self.console.show()
                
                font = ToolButton("format-text")
                font.set_tooltip("Console Font")
                fontselection = gtk.FontSelection()
                fontselection.get_family_list().get_selection().connect("changed", self.update_font, fontselection)
                fontselection.get_face_list().get_selection().connect("changed", self.update_font, fontselection)
                fontselection.get_size_entry().connect("changed", self.update_font, fontselection)
                fontselection.get_size_entry().connect("activate", self.update_font, fontselection)
                fontselection.show()
                font.props.palette.set_content(fontselection)
                fontselection.set_font_name("Monospace Regular 10")
                font.show()
                self.toolbar.add_item(font, -1)
                
                reset = ToolButton("view-refresh")
                reset.set_tooltip("Reset Console")
                reset.connect("clicked", self.reset)
                reset.show()
                self.toolbar.add_item(reset, -1)
                self.toolbar.show()
                self.pack_start(self.toolbar, False, True, 0)
                
                self.console.run_command()
                self.pack_start(self.console)

class PythonConsole(gtk.HBox):
        def __copy_cb(self, button):
                self.console.copy()
        
        def __paste_cb(self, button):
                self.console.paste()
        
        def _fgcolor_cb(self, button, pspec):
                newcolor = button.get_color()
                self.console.set_fgcolor(newcolor)
        
        def _bgcolor_cb(self, button, pspec):
                newcolor = button.get_color()
                self.console.set_bgcolor(newcolor)
        
        def update_font(self, widget, font_selection):
                font = pango.FontDescription(font_selection.get_font_name())
                self.console.set_font(font)
        
        def reset(self, widget):
                self.console.stop()
                self.console.run_command("python")
        
        def __init__(self):
                gtk.HBox.__init__(self)
                self.toolbar = VTray()
                
                copy = ToolButton("edit-copy")
                copy.set_tooltip('Copy')
                copy.connect("clicked", self.__copy_cb)
                copy.show()
                self.toolbar.add_item(copy, -1)
                paste = ToolButton("edit-paste")
                paste.set_tooltip("Paste")
                paste.connect("clicked", self.__paste_cb)
                paste.show()
                self.toolbar.add_item(paste, -1)
                
                fgcolor = ColorToolButton()
                fgcolor.get_child()._title = "Font Color"
                self.toolbar.add_item(fgcolor, -1)
                fgcolor.connect('notify::color', self._fgcolor_cb)
                fgcolor.show_all()
                bgcolor = ColorToolButton()
                bgcolor.get_child()._title = "Background Color"
                bgcolor.connect('notify::color', self._bgcolor_cb)
                self.toolbar.add_item(bgcolor, -1)
                bgcolor.show_all()
                
                self.console = Console()
                self.console.set_bgcolor(gtk.gdk.color_parse("#FFFFFF"))
                self.console.set_fgcolor(gtk.gdk.color_parse("#000000"))
                bgcolor.set_color(gtk.gdk.color_parse("#FFFFFF"))
                fgcolor.set_color(gtk.gdk.color_parse("#000000"))
                self.console.show()
                
                font = ToolButton("format-text")
                font.set_tooltip("Console Font")
                fontselection = gtk.FontSelection()
                fontselection.get_family_list().get_selection().connect("changed", self.update_font, fontselection)
                fontselection.get_face_list().get_selection().connect("changed", self.update_font, fontselection)
                fontselection.get_size_entry().connect("changed", self.update_font, fontselection)
                fontselection.get_size_entry().connect("activate", self.update_font, fontselection)
                fontselection.show()
                font.props.palette.set_content(fontselection)
                fontselection.set_font_name("Monospace Regular 10")
                font.show()
                self.toolbar.add_item(font, -1)
                
                reset = ToolButton("view-refresh")
                reset.set_tooltip("Reset Console")
                reset.connect("clicked", self.reset)
                reset.show()
                self.toolbar.add_item(reset, -1)
                self.toolbar.show()
                self.pack_start(self.toolbar, False, True, 0)
                
                self.console.run_command("python")
                self.pack_start(self.console)

if __name__ == "__main__":
        w = gtk.Window()
        term = Terminal()
        term.show()
        w.add(term)
        w.show()
        w.set_resizable(True)
        gtk.main()
