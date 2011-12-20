#!/usr/bin/env python

#   pep8_check.py by/por:
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

import gobject
import gtk

import commands


class PEP8_Check(gobject.GObject):
    __gsignals__ = {"hide-bar": (gobject.SIGNAL_RUN_LAST,
                                 gobject.TYPE_NONE,
                                 tuple()),
                    "show-bar": (gobject.SIGNAL_RUN_LAST,
                                 gobject.TYPE_NONE,
                                 tuple()),
                    "bar-text": (gobject.SIGNAL_RUN_LAST,
                                 gobject.TYPE_NONE,
                                 (gobject.TYPE_STRING,)),}
    def __init__(self):
        gobject.GObject.__init__(self)

    def check_file(self, editor):
        text = editor._get_all_text()
        tmp_file = open("/tmp/jamedit-pep8-chk.py", "w")
        tmp_file.write(text)
        tmp_file.close()

        chk = self.get_check()

        self.highlight_errors(text, chk, editor)

    def highlight_errors(self, text, chk, editor):
        buffer = editor.get_buffer()
        buffer.set_text("")
        num = 0
        for line in text.split("\n"):
            num += 1
            if str(num) in chk:
                line_iter = buffer.get_iter_at_line(num + 2)
                if num == len(text.split("\n")) - 1:
                    buffer.insert_with_tags(line_iter, line, \
                                            editor.error_tag)
                else:
                    buffer.insert_with_tags(line_iter, line + "\n", \
                                            editor.error_tag)
            else:
                line_iter = buffer.get_iter_at_line(num)
                if num == len(text.split("\n")) - 1:
                    buffer.insert_with_tags_by_name(line_iter, line)
                else:
                    buffer.insert_with_tags_by_name(line_iter, \
                                                           line + "\n")
        editor.connect("move-cursor", self.set_bar_text, chk)

    def get_check(self):
        (status, output) = commands.getstatusoutput(
                "pep8 --repeat /tmp/jamedit-pep8-chk.py")
        check = self.interpret_output(output)
        return check

    def interpret_output(self, output):
        checks = {}
        outputs = output.split("\n")
        for out in outputs:
            try:
                splits = out.split(":")
                line = splits[1]
                character = splits[2]
                error = splits[3]
                if line not in checks:
                    checks[line] = '%s:%s' % (character, error)
                else:
                    checks[line] = '%s; %s:%s' % (
                        checks[line], character, error)
            except:
                pass

        return checks

    def set_bar_text(self, widget, step_size, count, extend_selection, check):
        cursor_position = widget.buffer.get_property("cursor-position")
        offset_iter = widget.buffer.get_iter_at_offset(cursor_position)
        line = offset_iter.get_line()
        if str(line) in check:
            this_line_error = check[str(line)]
            char = this_line_error.split(":")[0]
            this_line_error = this_line_error.split(":")[1]
            self.emit("bar-text",
                      str(line) + ":" + char + " " + this_line_error)
            print this_line_error
            self.emit("show-bar")
        else:
            pass

    def check_exit(self, buffer, text):
        buffer.set_text("")
        num = 0
        for line in text.split("\n"):
            num += 1
            line_iter = buffer.get_iter_at_line(num)
            if num == len(text.split("\n")) - 1:
                buffer.insert_with_tags_by_name(line_iter, line)
            else:
                buffer.insert_with_tags_by_name(line_iter, line + "\n")

        self.emit("hide-bar")
        self.emit("bar-text", "")

