#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#       view_changes.py by/por:
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

import os
import shutil
import gtksourceview2

LANGUAGE_MANAGER = gtksourceview2.language_manager_get_default()
DIFF_LANG = LANGUAGE_MANAGER.get_language("diff")
STYLE_MANAGER = gtksourceview2.style_scheme_manager_get_default()
STYLE_MANAGER.append_search_path(os.path.join(os.environ["PWD"],
                                              "styles"))
JAMEDIT_CHANGES_STYLE = STYLE_MANAGER.get_scheme("jamedit-changes")

TMP = "/tmp/"


class View_Changes():
    
    def __init__(self):
        self.tmp_file = None
        self.patch_name = None
    
    def save_old_file(self, file):
        tmp_file = os.path.join(TMP, "jamedit-changes-file-1")
        num = 0
        
        # If tmp_file exists:
        while os.path.exists(tmp_file):
            num += 1
            tmp_file = os.path.join(TMP, "jamedit-changes-file-"+str(num))
            
        shutil.copyfile(file, tmp_file)
        
        self.old_file = tmp_file
        
    def get_patch_name(self):
        num = self.old_file.split("-")[-1]
        patch = os.path.join(TMP, "jamedit-changes-patch-"+num+".patch")
        self.patch_name = patch
        
        return patch
        
    def get_changes(self, new_file):
        os.system("diff %s %s > %s" % (self.old_file, 
                                       new_file, 
                                       self.get_patch_name()))
        
        os.remove(self.old_file)
        self.old_file = new_file
                                       
        changes = open(self.patch_name, "r")
        changes_text = changes.read()
        changes.close()
        
        os.remove(self.patch_name)
        
        return changes_text
        
    def get_changes_with_textview(self, new_file):
        changes = self.get_changes(new_file)
        
        textview = gtksourceview2.View()
        textview.buffer = gtksourceview2.Buffer()
        textview.set_buffer(textview.buffer)
        textview.buffer.set_text(changes)
        textview.set_editable(False)
        textview.set_cursor_visible(False)
        textview.buffer.set_highlight_syntax(True)
        textview.buffer.set_language(DIFF_LANG)
        textview.buffer.set_style_scheme(JAMEDIT_CHANGES_STYLE)
        textview.show_all()

        return textview
