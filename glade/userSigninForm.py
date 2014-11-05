#! /usr/bin/env python
#-*-coding: UTF-8 -*-

from gi.repository import Gtk

class App:

	def __init__(self):
		self._gladeFile = "userSigninForm.glade"
		self._glade = Gtk.Builder()
		self._glade.add_from_file(self._gladeFile)
		
		## Widgets
		self.mainWindow = self._glade.get_object("window")
		self.listAllButton = self._glade.get_object("listAllButton")
		## Handlers
		self.mainWindow.connect("destroy", Gtk.main_quit)
		self.listAllButton.connect("clicked", self.on_listAllButton_clicked)

		self.mainWindow.show_all()


	def on_listAllButton_clicked(self, widget):
		pass
	
	def on_okButton_activate(self):
		pass

	def on_saveButton_clicked(self):
		pass

##TODO implement db connection on init, list and insert methods
# class Model:

# 	def __init__(self):


if __name__ == "__main__":
	app = App()
	Gtk.main()			