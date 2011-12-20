#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   activity.py by/por:
#   Agustin Zubiaga <aguzubiaga97@gmail.com>
#   Daniel Francis <santiago.danielfrancis@gmail.com>
#   Sugarlabs - CeibalJAM! - Uruguay

#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
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
#       

import os

import gobject
import gtk

import gtksourceview2
STYLE_MANAGER = gtksourceview2.style_scheme_manager_get_default()
# Style Files extracted from / Archivos Style extraidos de :
# http://live.gnome.org/GtkSourceView/StyleSchemes
STYLE_MANAGER.append_search_path(os.path.join(os.environ["SUGAR_BUNDLE_PATH"],
                                              "styles"))
STYLES = STYLE_MANAGER.get_scheme_ids()
LANGUAGE_MANAGER = gtksourceview2.language_manager_get_default()
LANGUAGES = LANGUAGE_MANAGER.get_language_ids()

from sugar.activity.widgets import EditToolbar, StopButton, \
                                   ActivityToolbarButton, ToolbarButton
from sugar.graphics import iconentry
from sugar.graphics.combobox import ComboBox
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.toggletoolbutton import ToggleToolButton
from sugar.graphics.toolcombobox import ToolComboBox
from sugar.graphics.toolbarbox import ToolbarBox

class MainOptions(ActivityToolbarButton):
        __gsignals__ = {'open-from-journal': (gobject.SIGNAL_RUN_LAST,
                                              gobject.TYPE_NONE,
                                              tuple()),
                        'open-file': (gobject.SIGNAL_RUN_LAST,
                                      gobject.TYPE_NONE,
                                      tuple()),
                        'save-file': (gobject.SIGNAL_RUN_LAST,
                                      gobject.TYPE_NONE,
                                      tuple()),
                        'save-as': (gobject.SIGNAL_RUN_LAST,
                                    gobject.TYPE_NONE,
                                    tuple()),
                        'new-file': (gobject.SIGNAL_RUN_LAST,
                                     gobject.TYPE_NONE,
                                     tuple())}
        def __init__(self, activity):
                ActivityToolbarButton.__init__(self, activity)

                # Abrir objeto / Open object
                self.open_obj_btn = ToolButton("open-from-journal")
                self.open_obj_btn.set_tooltip(_("Open object from journal"))
                self.open_obj_btn.connect_object("clicked", self.emit, 'open-from-journal')
                self.page.insert(self.open_obj_btn, -1)

                # Separador / Separator
                separator = gtk.SeparatorToolItem()
                separator.set_draw(True)
                separator.set_expand(False)
                self.page.insert(separator, -1)

                # Boton de Abrir Archivo / Open File button
                self.open_btn = ToolButton("fileopen")
                self.open_btn.set_tooltip(_("Open File"))
                self.open_btn.set_accelerator('<ctrl>o')
                self.open_btn.connect_object("clicked", self.emit, 'open-file')
                self.page.insert(self.open_btn, -1)

                # ****** Save File button ******
                self.save_btn = ToolButton("stock_save")
                self.save_btn.set_tooltip(_("Save this file"))
                self.save_btn.set_accelerator('<ctrl>s')
                self.save_btn.connect_object("clicked", self.emit, 'save-file')
                self.page.insert(self.save_btn, -1)

                self.page.show_all()
                self.page.stop.hide()

                # Guardar como / Save As
                self.save_as = gtk.MenuItem(_("Save on the file system."))
                self.page.keep.props.palette.menu.append(self.save_as)
                self.save_as.connect_object("activate", self.emit, "save-as")
                self.save_as.show()

                # Nuevo / New
                self.new = ToolButton("new")
                self.new.set_tooltip(_("New file"))
                self.new.set_accelerator('<ctrl>n')
                self.new.connect_object("clicked", self.emit, 'new-file')
                self.page.insert(self.new, 6)
                self.new.show()

                self.page.keep.show()

class EditOptions(ToolbarButton):
        __gsignals__ = {'pep8-check': (gobject.SIGNAL_RUN_LAST,
                                       gobject.TYPE_NONE,
                                       tuple()),
                        'insert-datetime': (gobject.SIGNAL_RUN_LAST,
                                            gobject.TYPE_NONE,
                                            tuple()),
                        'copy': (gobject.SIGNAL_RUN_LAST,
                                 gobject.TYPE_NONE,
                                 tuple()),
                        'paste': (gobject.SIGNAL_RUN_LAST,
                                  gobject.TYPE_NONE,
                                  tuple()),
                        'undo': (gobject.SIGNAL_RUN_LAST,
                                 gobject.TYPE_NONE,
                                 tuple()),
                        'redo': (gobject.SIGNAL_RUN_LAST,
                                 gobject.TYPE_NONE,
                                 tuple()),
                        'cut': (gobject.SIGNAL_RUN_LAST,
                                gobject.TYPE_NONE,
                                tuple())}

        def __init__(self):
                self._toolbar = EditToolbar()
                ToolbarButton.__init__(self, label=_("Edit"), page=self._toolbar, icon_name='toolbar-edit')

                self.cut = ToolButton("cut")
                self.cut.set_tooltip(_("Cut"))
                self.cut.set_accelerator('<ctrl>x')
                self._toolbar.insert(self.cut, 4)

                separator = gtk.SeparatorToolItem()
                separator.set_draw(False)
                separator.set_expand(True)
                self._toolbar.insert(separator, -1)

                self.pep8_btn = ToolButton('pep8')
                self.pep8_btn.set_tooltip(_("PEP 8 Check"))
                self.pep8_btn.connect_object("clicked", self.emit, 'pep8-check')
                self._toolbar.insert(self.pep8_btn, -1)

                self.pep8_datetime_separator = gtk.SeparatorToolItem()
                self.pep8_datetime_separator.set_draw(True)
                self._toolbar.insert(self.pep8_datetime_separator, -1)

                self.insert_datetime = ToolButton("insert-datetime")
                self.insert_datetime.connect_object("clicked", self.emit, 'insert-datetime')
                #                             self.editor._insert_date_time)
                self.insert_datetime.set_tooltip(_("Insert date and time"))
                self._toolbar.insert(self.insert_datetime, -1)
                self.insert_datetime.show_all()

                self._toolbar.copy.connect_object("clicked", self.emit, 'copy')
                self._toolbar.paste.connect_object("clicked", self.emit, 'paste')
                self._toolbar.undo.connect_object("clicked", self.emit, 'undo')
                self._toolbar.redo.connect_object("clicked", self.emit, 'redo')
                self.cut.connect_object("clicked", self.emit, 'cut')

                self._toolbar.show_all()
                self.pep8_btn.set_sensitive(False)
                self.pep8_datetime_separator.set_draw(False)
        
        def set_pep8_sensitive(self, sensitive):
                self.pep8_btn.set_sensitive(sensitive)

class PreferencesOptions(ToolbarButton):
        __gsignals__ = {'show-line-numbers': (gobject.SIGNAL_RUN_LAST,
                                              gobject.TYPE_NONE,
                                              (gobject.TYPE_BOOLEAN,)),
                        'language-changed': (gobject.SIGNAL_RUN_LAST,
                                             gobject.TYPE_NONE,
                                             (gobject.TYPE_STRING,
                                              gobject.TYPE_PYOBJECT)),
                        'style-changed': (gobject.SIGNAL_RUN_LAST,
                                          gobject.TYPE_NONE,
                                          (gobject.TYPE_PYOBJECT,))}
        def __init__(self):
                ToolbarButton.__init__(self)
                self._toolbar = gtk.Toolbar()

                self.show_line_numbers = ToggleToolButton('show-numbers')
                self.show_line_numbers.set_tooltip(_("Show line numbers"))
                self.show_line_numbers.set_active(True)
                self.show_line_numbers.connect("clicked", (lambda w,s: s.emit('show-line-numbers', w.get_active())), self)
                #                     self.editor._set_show_line_numbers)
                self.show_line_numbers.show()
                self._toolbar.insert(self.show_line_numbers, -1)

                #Languages Combo Box
                self.lang_combo = ComboBox()
                self.lang_combo.append_item(None, _("Plain text"))
                self.lang_combo.set_active(0)
                for lang in LANGUAGES:
                        self.lang_combo.append_item(None, lang.capitalize())
                self.lang_combo.connect("changed", self._lang_changed)
                self.lang_item = ToolComboBox(self.lang_combo)
                self._toolbar.insert(self.lang_item, -1)
                self.lang_item.show()

                self.style_combo = ComboBox()
                count = 0
                classic = 0
                for style in STYLES:
                        self.style_combo.append_item(None, style.capitalize())
                        if style == "classic":
                                classic = count
                        count += 1
                self.style_combo.set_active(classic)
                self.style_combo.connect("changed", (lambda w,s: self.emit('style-changed', STYLE_MANAGER.get_scheme(STYLES[w.get_active()]))), self)
                self.style_item = ToolComboBox(self.style_combo)
                self._toolbar.insert(self.style_item, -1)
                self.style_item.show_all()
                
                self.props.page = self._toolbar
                self.props.icon_name = 'preferences-system'

        def _lang_changed(self, widget):
                name = widget.get_active()
                if name != 0:
                        id = LANGUAGES[name - 1]
                        lang = LANGUAGE_MANAGER.get_language(id)
                else:
                        id = None
                        lang = None
                self.emit('language-changed', id, lang)
        
        def set_active_lang(self, index):
                self.lang_combo.set_active(index)

class FontOptions(ToolbarButton):
        __gsignals__ = {'font-changed': (gobject.SIGNAL_RUN_LAST,
                                         gobject.TYPE_NONE,
                                         (gobject.TYPE_STRING,
                                          gobject.TYPE_STRING,
                                          gobject.TYPE_INT))}

        def __init__(self, context):
                ToolbarButton.__init__(self)
                self.context = context
                self.toolbar = gtk.Toolbar()
                self.props.page = self.toolbar
                self.props.icon_name = 'format-text'
                self.family = "Monospace"
                self.current_face = "Regular"
                self.family_combo = ComboBox()
                family_renderer = gtk.CellRendererText()
                family_renderer.set_property("family-set", True)
                self.family_combo.pack_start(family_renderer)
                self.family_combo.add_attribute(family_renderer, 'text', 0)
                self.family_combo.add_attribute(family_renderer, 'family', 0)
                self.family_model = gtk.ListStore(str)
                monospace_index = 0
                count = 0
                self.faces = {}
                
                for i in self.context.list_families():
                        name = i.get_name()
                        monospace_index = count if name == "Monospace" else 0
                        count += 1
                        self.family_model.append([name])
                        family_faces = gtk.ListStore(str, str)
                        for face in i.list_faces():
                                face_name = face.get_face_name()
                                family_faces.append([face_name,
                                                     "%s %s" %
                                                     (name, face_name)])
                        self.faces[name] = family_faces
                self.family_combo.set_model(self.family_model)
                self.family_combo.set_active(monospace_index)
                self.family_combo.connect("changed", self.family_changed)
                self.family_combo.show()
                self.family_tool_item = ToolComboBox(self.family_combo)
                self.family_tool_item.show()
                self.toolbar.insert(self.family_tool_item, -1)

                self.face_combo = ComboBox()
                face_renderer = gtk.CellRendererText()
                face_renderer.set_property("family-set", True)
                self.face_combo.pack_start(face_renderer)
                self.face_combo.add_attribute(face_renderer, 'text', 0)
                self.face_combo.add_attribute(face_renderer, 'font', 1)
                current_model = self.faces["Monospace"]
                self.face_combo.set_model(current_model)
                self.face_combo.set_active(0)
                self.face_combo.connect("changed", self.face_changed)
                self.face_combo.show()
                self.face_tool_item = ToolComboBox(self.face_combo)
                self.face_tool_item.show()
                self.toolbar.insert(self.face_tool_item, -1)

                self.size_adj = gtk.Adjustment(value=10, lower=5,
                                               upper=100, step_incr=1)
                self.size_adj.connect("value-changed", self.size_changed)
                self.size_spin = gtk.SpinButton(self.size_adj)
                self.size_spin.show()
                self.size_spin_item = gtk.ToolItem()
                self.size_spin_item.add(self.size_spin)
                self.size_spin_item.show()
                self.toolbar.insert(self.size_spin_item, -1)

                self.toolbar.show()

        def size_changed(self, adjustment):
                self.emit("font-changed", self.family,
                          self.current_face, adjustment.get_value())

        def face_changed(self, widget):
                iter = widget.get_active_iter()
                self.current_face = self.faces[self.family].get_value(iter, 0)
                self.emit('font-changed', self.family,
                          self.current_face, self.size_adj.get_value())

        def family_changed(self, widget):
                iter = widget.get_active_iter()
                self.family = self.family_model.get_value(iter, 0)
                self.face_combo.set_model(self.faces[self.family])
                self.face_combo.set_active(0)
                

class OptionWidget(ToolbarBox):
        __gsignals__ = {'open-from-journal': (gobject.SIGNAL_RUN_LAST,
                                              gobject.TYPE_NONE,
                                              tuple()),
                        'open-file': (gobject.SIGNAL_RUN_LAST,
                                      gobject.TYPE_NONE,
                                      tuple()),
                        'save-file': (gobject.SIGNAL_RUN_LAST,
                                      gobject.TYPE_NONE,
                                      tuple()),
                        'save-as': (gobject.SIGNAL_RUN_LAST,
                                    gobject.TYPE_NONE,
                                    tuple()),
                        'new-file': (gobject.SIGNAL_RUN_LAST,
                                     gobject.TYPE_NONE,
                                     tuple()),
                        'pep8-check': (gobject.SIGNAL_RUN_LAST,
                                       gobject.TYPE_NONE,
                                       tuple()),
                        'insert-datetime': (gobject.SIGNAL_RUN_LAST,
                                            gobject.TYPE_NONE,
                                            tuple()),
                        'copy': (gobject.SIGNAL_RUN_LAST,
                                 gobject.TYPE_NONE,
                                 tuple()),
                        'paste': (gobject.SIGNAL_RUN_LAST,
                                  gobject.TYPE_NONE,
                                  tuple()),
                        'undo': (gobject.SIGNAL_RUN_LAST,
                                 gobject.TYPE_NONE,
                                 tuple()),
                        'redo': (gobject.SIGNAL_RUN_LAST,
                                 gobject.TYPE_NONE,
                                 tuple()),
                        'cut': (gobject.SIGNAL_RUN_LAST,
                                gobject.TYPE_NONE,
                                tuple()),
                        'search-text': (gobject.SIGNAL_RUN_LAST,
                                        gobject.TYPE_NONE,
                                        (gobject.TYPE_STRING,)),
                        'search-prev': (gobject.SIGNAL_RUN_LAST,
                                        gobject.TYPE_NONE,
                                        tuple()),
                        'search-next': (gobject.SIGNAL_RUN_LAST,
                                        gobject.TYPE_NONE,
                                        tuple()),
                        'show-line-numbers': (gobject.SIGNAL_RUN_LAST,
                                              gobject.TYPE_NONE,
                                              (gobject.TYPE_BOOLEAN,)),
                        'language-changed': (gobject.SIGNAL_RUN_LAST,
                                             gobject.TYPE_NONE,
                                             (gobject.TYPE_STRING,
                                              gobject.TYPE_PYOBJECT)),
                        'style-changed': (gobject.SIGNAL_RUN_LAST,
                                          gobject.TYPE_NONE,
                                          (gobject.TYPE_PYOBJECT,)),
                        'font-changed': (gobject.SIGNAL_RUN_LAST,
                                         gobject.TYPE_NONE,
                                         (gobject.TYPE_STRING,
                                          gobject.TYPE_STRING,
                                          gobject.TYPE_INT))}
        def __init__(self, activity, context):
                ToolbarBox.__init__(self)

                self.main_options = MainOptions(activity)
                self.main_options.connect_object('open-from-journal', self.emit, 'open-from-journal')
                self.main_options.connect_object('open-file', self.emit, 'open-file')
                self.main_options.connect_object('save-file', self.emit, 'save-file')
                self.main_options.connect_object('save-as', self.emit, 'save-as')
                self.main_options.connect_object('new-file', self.emit, 'new-file')
                self.toolbar.insert(self.main_options, 0)

                self.edit_options = EditOptions()
                self.edit_options.connect_object('pep8-check', self.emit, 'pep8-check')
                self.edit_options.connect_object('insert-datetime', self.emit,'insert-datetime')
                self.edit_options.connect_object('copy', self.emit, 'copy')
                self.edit_options.connect_object('paste', self.emit, 'paste')
                self.edit_options.connect_object('undo', self.emit, 'undo')
                self.edit_options.connect_object('redo', self.emit, 'redo')
                self.edit_options.connect_object('cut', self.emit, 'cut')
                self.toolbar.insert(self.edit_options, -1)
                
                # Separador / Separator
                separator = gtk.SeparatorToolItem()
                separator.set_draw(False)
                self.toolbar.insert(separator, -1)
                
                # Buscar / Search
                self.search_entry = iconentry.IconEntry()
                self.search_entry.set_size_request(gtk.gdk.screen_width() / 3, -1)
                self.search_entry.set_icon_from_name(
                        iconentry.ICON_ENTRY_PRIMARY, 'system-search')
                self.search_entry.add_clear_button()
                self.search_entry.connect('activate', (lambda w,s: self.emit('search-text', w.props.text)), self)
                #                     self._search_entry_activate_cb)
                self.search_entry.connect('changed', (lambda w,s: self.emit('search-text', w.props.text)), self)
                #                     self._search_entry_changed_cb)
                self.search_item = gtk.ToolItem()
                self.search_item.add(self.search_entry)
                self.toolbar.insert(self.search_item, -1)

                self._search_prev = ToolButton('go-previous-paired')
                self._search_prev.set_tooltip(_('Previous'))
                self._search_prev.connect_object('clicked', self.emit, 'search-prev')
                #                          self.editor._search_prev_cb)
                self.toolbar.insert(self._search_prev, -1)

                self._search_next = ToolButton('go-next-paired')
                self._search_next.set_tooltip(_('Next'))
                self._search_next.connect_object('clicked', self.emit, 'search-next')
                #                          self.editor._search_next_cb)
                self.toolbar.insert(self._search_next, -1)

                self.preferences_options = PreferencesOptions()
                self.preferences_options.connect('show-line-numbers', (lambda w,a,s: s.emit('show-line-numbers', a)), self)
                self.preferences_options.connect('language-changed', (lambda w,i,l,s: s.emit('language-changed', i, l)), self)
                self.preferences_options.connect('style-changed', (lambda w,st,s: s.emit('style-changed', st)), self)
                self.preferences_options.show_all()
                self.toolbar.insert(self.preferences_options, -1)

                self.font_options = FontOptions(context)
                self.font_options.connect("font-changed", (lambda w,fav,fac,siz,s: s.emit('font-changed', fav, fac, siz)), self)
                self.toolbar.insert(self.font_options, -1)
                self.font_options.show()

                # Separador / Separator

                separator = gtk.SeparatorToolItem()
                separator.set_draw(False)
                separator.set_expand(True)
                self.toolbar.insert(separator, -1)

                # Boton salir / Stop Button

                exit = StopButton(activity)
                self.toolbar.insert(exit, -1)
                
                self.set_active_lang = self.preferences_options.set_active_lang
                self.set_pep8_sensitive = self.edit_options.set_pep8_sensitive
        
        def set_search_prev_sensitive(self, sensitive):
                self._search_prev.set_sensitive(sensitive)
        
        def set_search_next_sensitive(self, sensitive):
                self._search_next.set_sensitive(sensitive)
