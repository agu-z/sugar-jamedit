#!/usr/bin/env python

import logging

log = logging.getLogger('EditJam')
log.setLevel(logging.DEBUG)
logging.basicConfig()
import commands

class PEP8_Check():

    def check_file(self, text, editor):
        tmp_file = open("/tmp/jamedit-pep8-chk.py", "w")
	tmp_file.write(text)
	tmp_file.close()

	chk = self.get_check()

	self.highlight_errors(editor, chk)

    def highlight_errors(self, editor, chk):
        for key in chk.keys():
            # Here highlight errors whit tag pep8-error
            log.debug('%s: %s' % (key, chk[key]))

    def get_check(self):
        (status, output) = commands.getstatusoutput(
		"pep8 -r /tmp/jamedit-pep8-chk.py")
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
	    except: pass

	return checks
