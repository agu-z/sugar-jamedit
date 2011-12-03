#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import commands

class PEP8_Check():

        def check_file(self, text, editor):
                tmp_file = open("/tmp/jamedit-pep8-chk.py", "w")
                tmp_file.write(text)
                chk = self.get_check()
                
                tmp_file.close()

                self.highlight_errors(editor, chk)

        def highlight_errors(self, editor, chk):
                for key in chk.keys():
			# Here highlight errors whit tag pep8-error
			pass

        def get_check(self):
                output = commands.getoutput("pep8 /tmp/jamedit-pep8-chk.py")
                check = self.interpret_output(output)
                return check

        def interpret_output(self, output):
                checks = {}
                outputs = output.split("\n")
                for out in outputs:
                        try:
                                splits = out.split(":") 
                                line = splits[1]
                                error = splits[3]
                                checks[line] = error
                        except: pass

                return checks
