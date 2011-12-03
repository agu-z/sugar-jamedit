#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#   activity.py por:
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

import os
import sys

import gtk

import sugar
from sugar.graphics import iconentry
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.toggletoolbutton import ToggleToolButton
from sugar.graphics.toolbarbox import ToolbarBox
from sugar.activity.widgets import EditToolbar, StopButton, \
                                   ActivityToolbarButton, ToolbarButton
from sugar.datastore import datastore
from sugar.activity import activity
from editor import Editor
from filechooser import FileChooserOpen, FileChooserSave


class JAMEdit(activity.Activity):

        def __init__(self, handle):
                activity.Activity.__init__(self, handle, True)

                self.max_participants = 1

                # ****** Editor ******

                self.editor = Editor(self)
                scroll = gtk.ScrolledWindow()
                scroll.add(self.editor)
                scroll.show_all()

                self.set_canvas(scroll)

                # ****** Toolbars ******

                self.toolbar_box = ToolbarBox()

                activity_button = ActivityToolbarButton(self)
                activity_toolbar = activity_button.page

                # Separador / Separator

                separator = gtk.SeparatorToolItem()
                separator.set_draw(True)
                separator.set_expand(False)
                activity_toolbar.insert(separator, -1)

                # ****** Open File button ******
                open_btn = ToolButton("fileopen")
                open_btn.set_tooltip("Abrir achivo")
                open_btn.connect("clicked", self.open_file)
                activity_toolbar.insert(open_btn, -1)

                # ****** Save File button ******
                save_btn = ToolButton("stock_save")
                save_btn.set_tooltip("Guardar este archivo")
                save_btn.connect("clicked", self.save_file)
                activity_toolbar.insert(save_btn, -1)

                activity_toolbar.show_all()
                activity_toolbar.stop.hide()
                activity_toolbar.keep.hide()

                self.toolbar_box.toolbar.insert(activity_button, 0)

                # Edicion / Edit Toolbar

                edit_toolbar = EditToolbar()
                edit_toolbar_button = ToolbarButton(label="Editar",
                                                    page=edit_toolbar,
                                                    icon_name='toolbar-edit')

                edit_toolbar.cut = ToolButton("cut")
                edit_toolbar.cut.set_tooltip("Cortar")
                edit_toolbar.cut.set_accelerator('<ctrl>x')
                edit_toolbar.insert(edit_toolbar.cut, 4)

                separator = gtk.SeparatorToolItem()
                separator.set_draw(False)
                separator.set_expand(True)
                edit_toolbar.insert(separator, -1)

                edit_toolbar.pep8_btn = ToolButton('pep8')
                edit_toolbar.pep8_btn.connect("clicked", self.pep8_check)
                edit_toolbar.insert(edit_toolbar.pep8_btn, -1)

                edit_toolbar.copy.connect("clicked", self.editor._copy_cb)
                edit_toolbar.paste.connect("clicked", self.editor._paste_cb)
                edit_toolbar.undo.connect("clicked", self.editor._undo_cb)
                edit_toolbar.redo.connect("clicked", self.editor._redo_cb)
                edit_toolbar.cut.connect("clicked", self.editor._cut_cb)

                edit_toolbar.show_all()
                edit_toolbar.pep8_btn.hide()

                self.toolbar_box.toolbar.insert(edit_toolbar_button, -1)

                self.edit_toolbar = edit_toolbar

                # Separador / Separator
                separator = gtk.SeparatorToolItem()
                separator.set_draw(False)
                self.toolbar_box.toolbar.insert(separator, -1)

                # Buscar / Search
                search_entry = iconentry.IconEntry()
                search_entry.set_size_request(gtk.gdk.screen_width() / 3, -1)
                search_entry.set_icon_from_name(
                        iconentry.ICON_ENTRY_PRIMARY, 'system-search')
                search_entry.add_clear_button()
                search_entry.connect('activate',
                                     self.editor._search_entry_activate_cb)
                search_entry.connect('changed',
                                     self.editor._search_entry_changed_cb)
                search_item = gtk.ToolItem()
                search_item.add(search_entry)
                self.toolbox.toolbar.insert(search_item, -1)

                self._search_prev = ToolButton('go-previous-paired')
                self._search_prev.set_tooltip('Anterior')
                self._search_prev.connect('clicked',
                                          self.editor._search_prev_cb)
                self.toolbox.toolbar.insert(self._search_prev, -1)

                self._search_next = ToolButton('go-next-paired')
                self._search_next.set_tooltip('Siguiente')
                self._search_next.connect('clicked',
                                          self.editor._search_next_cb)
                self.toolbox.toolbar.insert(self._search_next, -1)

                # Preferencias / preferences

                preferences_toolbar = gtk.Toolbar()

                show_line_numbers = ToggleToolButton('show-numbers')
                show_line_numbers.set_tooltip("Mostrar numeros de linea")

                show_line_numbers.set_active(True)
                show_line_numbers.connect("clicked", \
                                        self.editor._set_show_line_numbers)
                show_line_numbers.show()
                preferences_toolbar.insert(show_line_numbers, -1)

                self.editor._make_languages_combo(preferences_toolbar)

                preferences = ToolbarButton()
                preferences.props.page = preferences_toolbar
                preferences.props.icon_name = 'preferences-system'
                preferences.show_all()

                self.toolbar_box.toolbar.insert(preferences, -1)


                # Separador / Separator

                separator = gtk.SeparatorToolItem()
                separator.set_draw(False)
                separator.set_expand(True)
                self.toolbar_box.toolbar.insert(separator, -1)

                # Boton salir / Stop Button

                exit = StopButton(self)
                self.toolbar_box.toolbar.insert(exit, -1)

                self.toolbar_box.show_all()

                self.set_toolbar_box(self.toolbar_box)

        def pep8_check(self, widget):
                self.editor.pep8.check_file(self.editor._get_all_text(), self.editor)

        def open_file(self, widget):
                fc = FileChooserOpen(self)
                fc.show_all()

        def save_file(self, widget):
                if self.editor.file:
                        file = open(self.editor.file, "w")
                        file.write(self.editor._get_all_text())
                        file.close()
                else:
                        fc = FileChooserSave(self)
                        fc.show_all()

        def write_file(self, file_path):
                if self.editor.lang:
                        lang_mime_type = self.editor.lang.get_mime_types()[0]

                elif not self.editor.lang:
                        lang_mime_type = "text/x-generic"

                self.metadata['mime_type'] = lang_mime_type

                jfile = open(file_path, "w")
                jfile.write(self.editor._get_all_text())
                jfile.close()

        def read_file(self, file_path):
                fpath = open(file_path, "r")
                text = fpath.read()
                fpath.close()

                mime_type = self.metadata["mime_type"]

                self.editor.buffer.set_text(text)
                self.editor._search_and_active_language(mime_type)