#!/usr/bin/env python

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

class JAMEdit(activity.Activity):

        def __init__(self, handle):
                activity.Activity.__init__(self, handle, True)

                # ****** Editor ******

                self.editor = Editor(self)
                self.set_canvas(self.editor)

                # ****** Toolbars ******

                self.toolbar_box = ToolbarBox()

                activity_button = ActivityToolbarButton(self)
                activity_toolbar = activity_button.page

                self.toolbar_box.toolbar.insert(activity_button, 0)

                # Edicion / Edit Toolbar

                edit_toolbar = EditToolbar()
                edit_toolbar_button = ToolbarButton(label="Editar",
                                                    page=edit_toolbar,
                                                    icon_name='toolbar-edit')

                edit_toolbar.cut = ToolButton("cut")
                edit_toolbar.insert(edit_toolbar.cut, -1)

                separator = gtk.SeparatorToolItem()
                separator.set_draw(True)
                separator.set_expand(False)
                #edit_toolbar.insert(separator, -1)


                edit_toolbar.copy.connect("clicked", self.editor._copy_cb)
                edit_toolbar.paste.connect("clicked", self.editor._paste_cb)
                edit_toolbar.undo.connect("clicked", self.editor._undo_cb)
                edit_toolbar.redo.connect("clicked", self.editor._redo_cb)
                edit_toolbar.cut.connect("clicked", self.editor._cut_cb)

                edit_toolbar.show_all()

                self.toolbar_box.toolbar.insert(edit_toolbar_button, -1)

                # Buscar / Search
                search_btn = ToolbarButton()
                search_tlb = gtk.Toolbar()
                search_btn.props.page = search_tlb
                search_btn.props.icon_name = "search-icon"

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
                search_tlb.insert(search_item, -1)

                self._search_prev = ToolButton('go-previous-paired')
                self._search_prev.set_tooltip('Anterior')
                self._search_prev.connect('clicked', 
                                          self.editor._search_prev_cb)
                search_tlb.insert(self._search_prev, -1)

                self._search_next = ToolButton('go-next-paired')
                self._search_next.set_tooltip('Siguiente')
                self._search_next.connect('clicked', 
                                          self.editor._search_next_cb)
                search_tlb.insert(self._search_next, -1)

                search_btn.show_all()
                search_tlb.show_all()
                self.toolbox.toolbar.insert(search_btn, -1)

                # Preferencias / preferences

                preferences_toolbar = gtk.Toolbar()

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

        #def abrir_archivo(self, widget)

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
