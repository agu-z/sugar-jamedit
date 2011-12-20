#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#   activity.py by/por:
#   Agustin Zubiaga <aguzubiaga97@gmail.com>
#   Daniel Francis <santiago.danielfrancis@gmail.com>
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

import gettext
LOCALE_DIR = os.path.join(".", "locale")
TRANSLATION_DOMAIN = "jamedit"
gettext.install(TRANSLATION_DOMAIN, LOCALE_DIR)

import pango
import gtk

import sugar
from sugar import mime
from sugar.graphics import iconentry
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.toggletoolbutton import ToggleToolButton
from sugar.graphics.toolbarbox import ToolbarBox
from sugar.activity.widgets import EditToolbar, StopButton, \
                                   ActivityToolbarButton, ToolbarButton
from sugar.datastore import datastore
from sugar.activity import activity

from pep8_check import PEP8_Check
import options
from editor import Editor
from python_console import PythonConsole
import file_choosers
file_choosers.langsmanager = options.LANGUAGE_MANAGER
file_choosers.langs = options.LANGUAGES


class JAMEdit(activity.Activity):

        def __init__(self, handle):
                activity.Activity.__init__(self, handle, True)

                self.max_participants = 1

                # ****** Editor ******

                self.editor = Editor()
                self.editor.connect("pep8-aviable", self.enable_pep8)
                self.editor.connect('language-changed', self.language_changed)
                
                self.editor.set_size_request(800, 790)
                scroll = gtk.ScrolledWindow()
                scroll.set_policy(gtk.POLICY_AUTOMATIC,
                                  gtk.POLICY_AUTOMATIC)
                scroll.add(self.editor)
                scroll.show_all()

                vbox = gtk.VBox()
                vpaned = gtk.VPaned()
                vpaned.pack1(scroll)
                vbox.pack_start(vpaned, True, True, 0)

                self.set_canvas(vbox)

                # ****** Toolbars ******

                self.toolbar_box = options.OptionWidget(self, self.editor.get_pango_context())
                self.toolbar_box.connect('open-from-journal', file_choosers.open_from_journal, None, self)
                self.toolbar_box.connect('open-file', self.open_file)
                self.toolbar_box.connect('save-file', self.save_file)
                self.toolbar_box.connect('save-as', self.save_file_as)
                self.toolbar_box.connect('new-file', self.new)
                self.toolbar_box.connect('pep8-check', self.pep8_check)
                self.toolbar_box.connect('insert-datetime', self.editor._insert_date_time)
                self.toolbar_box.connect('copy', self.editor._copy_cb)
                self.toolbar_box.connect('paste', self.editor._paste_cb)
                self.toolbar_box.connect('undo', self.editor._undo_cb)
                self.toolbar_box.connect('redo', self.editor._redo_cb)
                self.toolbar_box.connect('cut', self.editor._cut_cb)
                self.toolbar_box.connect('search-text', self._search_text)
                self.toolbar_box.connect('search-prev', self.editor._search_prev_cb)
                self.toolbar_box.connect('search-next', self.editor._search_next_cb)
                self.toolbar_box.connect('show-line-numbers', self.editor._set_show_line_numbers)
                self.toolbar_box.connect('language-changed', self.change_language)
                self.toolbar_box.connect('style-changed', self.change_style)
                self.toolbar_box.connect('font-changed', self.change_font)
                self.toolbar_box.show_all()
                self.set_toolbar_box(self.toolbar_box)
                
                # Barra de estado de PEP8 / PEP8 status bar
                self.pep8 = PEP8_Check()
                
                self.pep8_bar = gtk.Statusbar()
                self.pep8.connect("show-bar", (lambda w, bar: bar.show_all()), self.pep8_bar)
                self.pep8.connect("hide-bar", (lambda w, bar: bar.hide()), self.pep8_bar)
                self.pep8_bar.label = gtk.Label()
                self.pep8.connect("bar-text", (lambda w, t, l: l.set_text(t)), self.pep8_bar.label)
                self.pep8_bar.add(self.pep8_bar.label)
                vbox.pack_end(self.pep8_bar, False, True, 0)
                
                self.python_console = PythonConsole()
                self.python_console.show()
                vpaned.pack2(self.python_console)
                vpaned.show_all()
                vbox.show_all()

        def change_style(self, widget, style):
                self.editor.set_style(style)
        
        def language_changed(self, widget, new_lang):
                self.toolbar_box.set_active_lang(int(new_lang))
        
        def change_language(self, widget, id, language):
                if id == "python":
                        self.enable_pep8(None, True)
                else:
                        self.enable_pep8(None, False)
                self.editor.set_language(language)

        def show_python_console(self, widget):
                if not self.python_console.showed:
                    self.python_console.show()
                    self.python_console.showed = True
                    
                else:
                    self.python_console.hide()
                    self.python_console.showed = False

        def _search_text(self, widget, text):
                self.editor.set_search_text(text)
                self.update_search_buttons()
        
        def update_search_buttons(self):
                if len(self.editor.search_text) == 0:
                        self._search_prev.props.sensitive = False
                        self._search_next.props.sensitive = False
                else:
                        prev_result = self.editor.get_next_result('backward')
                        next_result = self.editor.get_next_result('forward')
                        _1 = prev_result != None
                        _2 = next_result != None
                        self._search_prev.props.sensitive = prev_result != _1
                        self._search_next.props.sensitive = next_result != _1

        def enable_pep8(self, widget, active):
                self.toolbar_box.set_pep8_sensitive(active)
        
        def change_font(self, widget, family, face, size):
                self.editor.modify_font(pango.FontDescription("%s %s %d" %
                                                              (family,
                                                               face,
                                                               size)))

        def pep8_check(self, widget):
                self.pep8.check_file(self.editor)

        def close(self, skip_save=False):
                close = True
                if not self.editor.file:
                        close = self.save_file(None, type="exit", mode=2)
                if close:
                        activity.Activity.close(self)

        def open_file(self, widget, from_journal=False):
                self.pep8.check_exit(self.editor.buffer, self.editor._get_all_text())
                self.save_file(None, type="exit")
                if not from_journal:
                        file_path, remember = file_choosers.open_file_dialog()
                        if file_path != None:
                                self.set_title(os.path.split(file_path)[-1])
                                mime_type = mime.get_from_file_name(file_path)
                                self.metadata["mime_type"] = mime_type

                                file = open(file_path, "r")
                                self.editor.buffer.set_text(file.read())
                                if remember:
                                        self.editor.file = file_path
                                self.editor._search_and_active_language(
                                                                     mime_type)
                                file.close()

                if from_journal:
                        file_path = from_journal
                        mime_type = mime.get_from_file_name(file_path)
                        self.metadata["mime_type"] = mime_type

                        file = open(file_path, "r")
                        self.editor.buffer.set_text(file.read())
                        self.editor.file = file_path
                        self.editor._search_and_active_language(mime_type)
                        file.close()

        def new(self, widget):
                self.pep8.check_exit(self.editor.get_buffer(), self.editor._get_all_text())
                _continue = self.save_file(None, type="exit")
                if _continue:
                        self.metadata["mime_type"] = mime.GENERIC_TYPE_TEXT
                        self.editor.lang = None
                        self.editor.file = None
                        self.toolbar_box.set_active_lang(0)
                        self.editor.buffer.set_highlight_syntax(False)
                        self.toolbar_box.set_pep8_sensitive(False)
                        self.editor.buffer.set_text("")
                        self.set_title(_("New"))

        def save_file_as(self, widget):
                file_path = file_choosers.save_file_dialog()
                if file_path:
                        self.editor.file = file_path
                        file = open(self.editor.file, "w")
                        file.write(self.editor._get_all_text())
                        file.close()

                        self.set_title(os.path.split(file_path)[-1])
                        mime_type = mime.get_from_file_name(file_path)
                        self.metadata["mime_type"] = mime_type
                        self.editor.file = file_path
                        self.editor._search_and_active_language(mime_type)

        def save_file(self, widget, type=None, mode=1):
                if not type:
                        if self.editor.file:
                                file = open(self.editor.file, "w")
                                file.write(self.editor._get_all_text())
                                file.close()
                        else:
                                file_path = file_choosers.save_file_dialog()
                                if file_path:
                                        self.editor.file = file_path
                                        file = open(self.editor.file, "w")
                                        file.write(self.editor._get_all_text())
                                        file.close()
                if type == "exit":
                        dialog = gtk.MessageDialog(type=gtk.MESSAGE_QUESTION)
                        dialog.add_buttons(gtk.STOCK_CANCEL,
                                           gtk.RESPONSE_CANCEL,
                                           gtk.STOCK_NO,
                                           gtk.RESPONSE_NO,
                                           gtk.STOCK_YES,
                                           gtk.RESPONSE_YES)

                        dialog.set_markup("<b>%s</b>" % _("Save changes..."))
                        if mode == 1:
                                dialog.format_secondary_text(
                                            _("Do you want to save changes?"))
                        elif mode == 2:
                                dialog.format_secondary_text(
                        _("Do you want to save changes\nin the file system?"))
                        response = dialog.run()
                        dialog.destroy()
                        if not response == gtk.RESPONSE_CANCEL:
                                if response == gtk.RESPONSE_YES:
                                        if self.editor.file:
                                                file = open(
                                                         self.editor.file, "w")
                                                file.write(
                                                   self.editor._get_all_text())
                                                file.close()
                                        else:
                                                file_path = \
                                        file_choosers.save_file_dialog()
                                                if file_path:
                                                        self.editor.file = \
                                                                      file_path
                                                        file = open(
                                                         self.editor.file, "w")
                                                        file.write(
                                                   self.editor._get_all_text())
                                                        file.close()
                                return True
                        else:
                                return False

        def write_file(self, file_path):
                if self.editor.lang:
                        lang_mime_type = self.editor.lang.get_mime_types()[0]

                elif not self.editor.lang:
                        lang_mime_type = mime.GENERIC_TYPE_TEXT

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
