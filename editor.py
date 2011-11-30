#!/usr/bin/env python
#! -*- coding: UTF-8 -*-

import os
import sys

import gtk
import gtksourceview2
import pango

from sugar.graphics.combobox import ComboBox
from sugar.graphics.toolcombobox import ToolComboBox

LANGUAGE_MANAGER = gtksourceview2.language_manager_get_default()
LANGUAGES = LANGUAGE_MANAGER.get_language_ids()

class Editor(gtksourceview2.View):

        def __init__(self, activity):
                gtksourceview2.View.__init__(self)   

                self.lang = None

                pangoFont = pango.FontDescription('Mono')
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

                self.buffer = gtksourceview2.Buffer(tag_table=self._tagtable)
                self.set_buffer(self.buffer)      

                self.activity = activity

                self.show_all()

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

        def _make_languages_combo(self, toolbar):
                self.lang_combo = ComboBox()
                self.lang_combo.append_item(None, "Texto Simple")
                self.lang_combo.set_active(0)

                for lang in LANGUAGES:
                        self.lang_combo.append_item(None, lang.capitalize())

                self.lang_combo.connect("changed", self._set_language)
                        
                tool_item = ToolComboBox(self.lang_combo)
                        
                toolbar.insert(tool_item, -1)

                tool_item.show()

        def _set_language(self, combo):
                name = self.lang_combo.get_active()
                if name != 0:
                        id = LANGUAGES[name-1]
                        self.lang = LANGUAGE_MANAGER.get_language(id)
                        self.buffer.set_highlight_syntax(True)
                        self.buffer.set_language(self.lang)

                elif name == 0:
                        self.buffer.set_highlight_syntax(False)
                        self.lang = None
 
        def _search_and_active_language(self, mimetype):
                for id in LANGUAGES:
                        lang = LANGUAGE_MANAGER.get_language(id)
                        if len(lang.get_mime_types()):
                                mime = lang.get_mime_types()[0]
                                if mimetype == mime:
                                        self.buffer.set_highlight_syntax(True)
                                        self.buffer.set_language(lang)
                                        self.lang_combo.set_active(id+1)
                                        
                        
        def _get_all_text(self):
                start = self.buffer.get_start_iter()
                end = self.buffer.get_end_iter()
                text = self.buffer.get_text(start, end, True)
                return text

        def _search_entry_activate_cb(self, entry):
                self.set_search_text(entry.props.text)
                self._update_search_buttons()

        def _search_entry_changed_cb(self, entry):
                self.set_search_text(entry.props.text)
                self._update_search_buttons()

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
                        self.activity._search_prev.props.sensitive = prev_result != None
                        self.activity._search_next.props.sensitive = next_result != None

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
                        text_iter = _buffer.get_iter_at_mark(_buffer.get_insert())
                        text_iter.forward_char()
                else:
                        text_iter = _buffer.get_iter_at_mark(_buffer.get_insert())

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
