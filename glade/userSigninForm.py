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
		self.mainWindow = self._glade.get_object("mainWindow")
		self.listAllButton = self._glade.get_object("listAllButton")
		self.saveButton = self._glade.get_object("saveButton")
		self.okButton = self._glade.get_object("okButton")

		## Handlers
		self.mainWindow.connect("destroy", Gtk.main_quit)
		self.listAllButton.connect("clicked", self._listAllUsers)
		self.saveButton.connect("clicked", self._saveData)
		self.okButton.connect("activate", Gtk.main_quit)

		self.mainWindow.show_all()

	def _listAllUsers(self, widget):
		listWindow = ListWindow()

	def _saveData(self, widget):
		pass
	
	def _accept(self, widget):
		pass

###########################################################################################

class ListWindow:

	def __init__(self):
		self._model = Model()

		self.listStore = Gtk.ListStore(str, str, str, str, str, str)
		users = self._model.listAll()
		for user in users:
			self.listStore.append(user)

		self.treeView = Gtk.TreeView(self.listStore)
		self.listWindow = Gtk.Window()
		self.listWindow.add(self.treeView);

		self.listWindow.connect("destroy", Gtk.main_quit)
		self.listWindow.show_all()

###########################################################################################

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
		self._c.execute("SELECT nick, password, email, name, surname, address FROM {0}".format(self._table))
		return self._c.fetchall()

###########################################################################################

if __name__ == "__main__":
	app = App()
	Gtk.main()			