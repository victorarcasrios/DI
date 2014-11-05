#! /usr/bin/env python
#-*-coding: UTF-8 -*-

from gi.repository import Gtk
import sqlite3

## TODO implement methods
class App:

	def __init__(self):
		self._model = Model()
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

class Model:

	def __init__(self):
		self._conn = sqlite3.connect("practica2.db")
		self._conn.text_factory = str
		self._c = self._conn.cursor()
		self._table = "users"

	def insert(self, nick, password, email, name, surname, address):
		insert = "INSERT INTO {0} VALUES (NULL, ?, ?, ?, ?, ?, ?)".format(self._table)
		self._c.execute(insert, (nick, password, email, name, surname, address));
		self._conn.commit();

	def listAll(self):
		self._c.execute("SELECT * FROM {0}".format(self._table))
		return self._c.fetchall()

if __name__ == "__main__":
	app = App()
	Gtk.main()			