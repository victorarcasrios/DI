#! /usr/bin/env python
#-*-coding: UTF-8 -*-

from gi.repository import Gtk

class App():

	def __init__(self):
		self._gladeFile = "calculadora.glade"
		self._glade = Gtk.Builder()
		self._glade.add_from_file(self._gladeFile)
		
		## Widgets
		self.mainWindow = self._glade.get_object("mainWindow")

		## Event Handlers
		self.mainWindow.connect("destroy", Gtk.main_quit)

		self.mainWindow.show_all()	


if __name__ == "__main__":
	app = App()
	Gtk.main()