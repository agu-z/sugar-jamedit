#!/usr/bin/env python
#! -*- coding: UTF-8 -*-

#   filechooser.py por:
#   Agustin Zubiaga <aguzubiaga97@gmail.com>
#   Sugarlabs - CeibalJAM! - Uruguay

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import gtk
import os

from sugar import mime

class FileChooserOpen(gtk.FileChooserDialog):

        def __init__(self, activity):

                gtk.FileChooserDialog.__init__(self, title=None,
                                               parent=None,
                                               action=gtk.FILE_CHOOSER_ACTION_OPEN, 
                                               buttons=None,
                                               backend=None)

                self.set_title("Seleccionar Archivo - JAMEdit")
                
                open = gtk.Button("Abrir")
                open.connect("clicked", self.ok)
                exit = gtk.Button("Salir")
                exit.connect("clicked", self.salir)
                button_box = gtk.HButtonBox()
                button_box.set_layout(gtk.BUTTONBOX_END)
                button_box.add(open)
                button_box.add(exit)

                self.set_extra_widget(button_box)

                self.activity = activity

                self.show_all()


        def ok(self, widget):
                archivo = self.get_filename()
                self.activity.set_title(archivo.split("/")[-1])
                mime_type = mime.get_from_file_name(archivo)            
                self.activity.metadata["mime_type"] = mime_type

                file = open(archivo, "r")

                self.activity.editor.buffer.set_text(file.read())
                self.activity.editor.file = archivo
                self.activity.editor._search_and_active_language(mime_type)

                file.close()
                
                self.destroy()

        def salir(self, widget): self.destroy()


class FileChooserSave(gtk.FileChooserDialog):

        def __init__(self, activity):

                gtk.FileChooserDialog.__init__(self, title=None,
                                               parent=None,
                                               action=gtk.FILE_CHOOSER_ACTION_SAVE, 
                                               buttons=None,
                                               backend=None)

                self.set_title("Guardar Archivo - JAMEdit")
                
                open = gtk.Button("Guardar")
                #open.connect("clicked", self.ok)
                exit = gtk.Button("Salir")
                #exit.connect("clicked", self.salir)
                button_box = gtk.HButtonBox()
                button_box.set_spacing(3)
                button_box.set_layout(gtk.BUTTONBOX_END)
                button_box.add(open)
                button_box.add(exit)

                self.set_extra_widget(button_box)

                self.activity = activity

                self.show_all()
