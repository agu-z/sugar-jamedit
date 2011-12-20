#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#   editor.py by/por:
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
import datetime
import time
import locale

import gobject
import pango
import gtk
import gtksourceview2

from sugar.graphics.combobox import ComboBox
from sugar.graphics.toolcombobox import ToolComboBox

LANGUAGE_MANAGER = gtksourceview2.language_manager_get_default()

class Editor(gtksourceview2.View):
        __gsignals__ = {"pep8-aviable": (gobject.SIGNAL_RUN_LAST,
                                         gobject.TYPE_NONE,
                                         (gobject.TYPE_BOOLEAN,)),
                        "language-changed": (gobject.SIGNAL_RUN_LAST,
                                             gobject.TYPE_NONE,
                                             (gobject.TYPE_STRING,)),}
        def __init__(self):
                gtksourceview2.View.__init__(self)

                self.lang = None
                self.file = None

                self.set_show_line_numbers(True)

                pangoFont = pango.FontDescription('Monospace 10')
                self.modify_font(pangoFont)

                bgcolor = gtk.gdk.color_parse('#FFFFFF')
                self.modify_base(gtk.STATE_NORMAL, bgcolor)

                self._tagtable = gtk.TextTagTable()
                hilite_tag = gtk.TextTag('search-hilite')
                hilite_tag.props.background = '#FFFFB0'
                self._tagtable.add(hilite_tag)
                select_tag = gtk.TextTag('search-select')
                select_tag.props.background = '#B0B0FF'
                self._tagtable.add(select_tag)
                self.error_tag = gtk.TextTag('pep8-error')
                self.error_tag.props.background = '#FF0000'
                self._tagtable.add(self.error_tag)

                self.buffer = gtksourceview2.Buffer(tag_table=self._tagtable)
                self.buffer.set_highlight_syntax(True)
                self.set_buffer(self.buffer)

                self.show_all()

        def set_style(self, style):
                self.buffer.set_style_scheme(style)

        def _set_show_line_numbers(self, widget, active):
                self.set_show_line_numbers(active)

        def _copy_cb(self, widget):
                clipboard = gtk.Clipboard()

                self.buffer.copy_clipboard(clipboard)

        def _cut_cb(self, widget):
                clipboard = gtk.Clipboard()

                self.buffer.copy_clipboard(clipboard)
                self.buffer.delete_selection(True, True)

        def _paste_cb(self, widget):
                clipboard = gtk.Clipboard()
                text = clipboard.wait_for_text()

                self.buffer.insert_at_cursor(text)

        def _undo_cb(self, widget):
                self.buffer.undo()

        def _redo_cb(self, widget):
                self.buffer.redo()

        def set_language(self, lang):
                self.lang = lang
                self.buffer.set_language(lang)

        def _search_and_active_language(self, mimetype):
                encontrado = False
                for id in LANGUAGES:
                        lang = LANGUAGE_MANAGER.get_language(id)
                        if len(lang.get_mime_types()):
                                mime = lang.get_mime_types()[0]
                                if mimetype == mime:
                                        self.buffer.set_language(lang)
                                        list_num = LANGUAGES.index(id)
                                        self.emit("language-changed", list_num + 1)
                                        encontrado = True

                                        if id == "python":
                                                self.emit("pep8-aviable", True)
                                        else:
                                                self.emit("pep8-aviable", False)
                if not encontrado:
                        self.buffer.set_language(None)
                        self.emit("language-changed", 0)
                        self.lang = None
                        self.emit("pep8-aviable", False)

        def _get_all_text(self):
                start = self.buffer.get_start_iter()
                end = self.buffer.get_end_iter()
                text = self.buffer.get_text(start, end, True)
                return text

        def _insert_date_time(self, widget):
                today = datetime.date.today()
                today = today.strftime("%d/%m/%y")
                _time = time.strftime("%H:%M:%S")
                zone = locale.getdefaultlocale()[0]
                date_time = str(today) + " " + _time + "-" + zone
                self.buffer.insert_at_cursor(date_time)

        def _search_prev_cb(self, button):
                self.search_next('backward')
                self._update_search_buttons()

        def _search_next_cb(self, button):
                self.search_next('forward')
                self._update_search_buttons()

        def _update_search_buttons(self,):
                if len(self.search_text) == 0:
                        self.activity._search_prev.props.sensitive = False
                        self.activity._search_next.props.sensitive = False
                else:
                        prev_result = self.get_next_result('backward')
                        next_result = self.get_next_result('forward')
                        _1 = prev_result != None
                        _2 = next_result != None
                        self.activity._search_prev.props.sensitive = \
                                                              prev_result != _1
                        self.activity._search_next.props.sensitive = \
                                                              next_result != _1

        def set_search_text(self, text):
                self.search_text = text

                _buffer = self.get_buffer()

                start, end = _buffer.get_bounds()
                _buffer.remove_tag_by_name('search-hilite', start, end)
                _buffer.remove_tag_by_name('search-select', start, end)

                text_iter = _buffer.get_start_iter()
                while True:
                        next_found = text_iter.forward_search(text, 0)
                        if next_found is None:
                                break
                        start, end = next_found
                        _buffer.apply_tag_by_name('search-hilite', start, end)
                        text_iter = end

                if self.get_next_result('current'):
                        self.search_next('current')
                elif self.get_next_result('backward'):
                        self.search_next('backward')

        def get_next_result(self, direction):
                _buffer = self.get_buffer()

                if direction == 'forward':
                        text_iter = \
                                  _buffer.get_iter_at_mark(_buffer.get_insert(
                                                                             ))
                        text_iter.forward_char()
                else:
                        text_iter = \
                                  _buffer.get_iter_at_mark(_buffer.get_insert(
                                                                             ))

                if direction == 'backward':
                        return text_iter.backward_search(self.search_text, 0)
                else:
                        return text_iter.forward_search(self.search_text, 0)

        def search_next(self, direction):
                next_found = self.get_next_result(direction)
                if next_found:
                        _buffer = self.get_buffer()

                        start, end = _buffer.get_bounds()
                        _buffer.remove_tag_by_name('search-select', start, end)

                        start, end = next_found
                        _buffer.apply_tag_by_name('search-select', start, end)

                        _buffer.place_cursor(start)

                        self.scroll_to_iter(start, 0.1)

                        self.scroll_to_iter(end, 0.1)
