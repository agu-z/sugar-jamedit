#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk

def open_file_dialog():
	dialog = gtk.FileChooserDialog(_("Open..."),
								   None,
								   gtk.FILE_CHOOSER_ACTION_OPEN,
								   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
									gtk.STOCK_OPEN, gtk.RESPONSE_OK))
	dialog.set_default_response(gtk.RESPONSE_OK)
	
	filter = gtk.FileFilter()
	filter.set_name(_("All files"))
	filter.add_pattern("*")
	dialog.add_filter(filter)
	
	filter = gtk.FileFilter()
	filter.set_name(_("All text files"))
	filter.add_mime_type("text/*")
	dialog.add_filter(filter)
	
	lang_ids = langs
	for i in lang_ids:
		lang = langsmanager.get_language(i)
		filter = gtk.FileFilter()
		filter.set_name(lang.get_name())
		for m in lang.get_mime_types():
			filter.add_mime_type(m)
		dialog.add_filter(filter)
	response = dialog.run()
	if response == gtk.RESPONSE_OK:
		to_return = dialog.get_filename()
	elif response == gtk.RESPONSE_CANCEL:
		to_return = None
	dialog.destroy()
	return to_return

def confirm_overwrite(widget):
	dialog = gtk.MessageDialog(type=gtk.MESSAGE_QUESTION)
	dialog.add_buttons(gtk.STOCK_NO, gtk.RESPONSE_CANCEL, gtk.STOCK_YES, gtk.RESPONSE_ACCEPT)
	dialog.set_markup("<b>%s</b>" % _("This file name already exists"))
	dialog.format_secondary_text(_("Overwrite the file?"))
	response = dialog.run()
	dialog.destroy()
	if response == gtk.RESPONSE_ACCEPT:
		return gtk.FILE_CHOOSER_CONFIRMATION_ACCEPT_FILENAME
	else:
		return gtk.FILE_CHOOSER_CONFIRMATION_SELECT_AGAIN

def save_file_dialog():
	dialog = gtk.FileChooserDialog(_("Save..."),
								   None,
								   gtk.FILE_CHOOSER_ACTION_SAVE,
								   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
									gtk.STOCK_SAVE, gtk.RESPONSE_OK))
	dialog.set_default_response(gtk.RESPONSE_OK)
	dialog.set_do_overwrite_confirmation(True)
	dialog.connect("confirm-overwrite", confirm_overwrite)
	
	filter = gtk.FileFilter()
	filter.set_name(_("All files"))
	filter.add_pattern("*")
	dialog.add_filter(filter)
	
	filter = gtk.FileFilter()
	filter.set_name(_("All text files"))
	filter.add_mime_type("text/*")
	dialog.add_filter(filter)
	
	lang_ids = langs
	for i in lang_ids:
		lang = langsmanager.get_language(i)
		filter = gtk.FileFilter()
		filter.set_name(lang.get_name())
		for m in lang.get_mime_types():
			filter.add_mime_type(m)
		dialog.add_filter(filter)
	response = dialog.run()
	if response == gtk.RESPONSE_OK:
		to_return = dialog.get_filename()
	elif response == gtk.RESPONSE_CANCEL:
		to_return = None
	dialog.destroy()
	return to_return
