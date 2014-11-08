#! /usr/bin/env python
#-*-coding: UTF-8 -*-

from gi.repository import Gtk
import sqlite3

class GtkClass:

	def __init__(self):
		self._model = Model()
		self._gladeFile = "userSigninForm.glade"
		self._glade = Gtk.Builder()
		self._glade.add_from_file(self._gladeFile)

###########################################################################################

## TODO hide not filled message and show only when user tries to save data with empty fields
class App(GtkClass):

	def __init__(self):
		GtkClass.__init__(self);

		## Widgets
		self.mainWindow = self._glade.get_object("mainWindow")
		self.listAllButton = self._glade.get_object("listAllButton")
		self.saveButton = self._glade.get_object("saveButton")
		self.okButton = self._glade.get_object("okButton")

		## Handlers
		self.mainWindow.connect("destroy", Gtk.main_quit)
		self.listAllButton.connect("clicked", self._listAllUsers)
		self.saveButton.connect("clicked", self._saveData)
		self.okButton.connect("clicked", Gtk.main_quit)

		self.mainWindow.show_all()

	def _listAllUsers(self, widget):
		listWindow = ListWindow()

	def _saveData(self, widget):
		data = (
			self._glade.get_object("nickEntry").get_text(),
			self._glade.get_object("passwordEntry").get_text(),
			self._glade.get_object("emailEntry").get_text(),
			self._glade.get_object("nameEntry").get_text(),
			self._glade.get_object("surnameEntry").get_text(),
			self._glade.get_object("addressEntry").get_text()
			)
		if(self._isProperUserData(data)):
			self._model.insert(data)

	def _isProperUserData(self, data):
		for datum in data:
			if not datum:
				return False
		return True

###########################################################################################

class ListWindow(GtkClass):

	def __init__(self):
		GtkClass.__init__(self);
	
		self.listWindow = self._glade.get_object("listWindow")
		self.treeView = self._glade.get_object("treeView")

		self.listStore = Gtk.ListStore(str, str, str, str, str, str)
		users = self._model.listAll()
		for user in users:
			self.listStore.append(user)

		columnNames = "Usuario", "Contraseña", "Email", "Nombre", "Apellidos", "Dirección"
		for i in range(0, len(columnNames)):
			self.treeView.append_column(Gtk.TreeViewColumn(columnNames[i], Gtk.CellRendererText(), text=i))
		
		self.treeView.set_model(self.listStore)

		self.listWindow.show_all()

###########################################################################################

class Model:

	def __init__(self):
		self._conn = sqlite3.connect("practica2.db")
		self._conn.text_factory = str
		self._c = self._conn.cursor()
		self._table = "users"

	def insert(self, data):
		insert = "INSERT INTO {0} VALUES (NULL, ?, ?, ?, ?, ?, ?)".format(self._table)
		self._c.execute(insert, data);
		self._conn.commit();

	def listAll(self):
		self._c.execute("SELECT nick, password, email, name, surname, address FROM {0}".format(self._table))
		return self._c.fetchall()

###########################################################################################

if __name__ == "__main__":
	app = App()
	Gtk.main()			