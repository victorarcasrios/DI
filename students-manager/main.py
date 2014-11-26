#! /usr/bin/env python
#-*-coding: UTF-8 -*-

from gi.repository import Gtk
import sqlite3

###########################################################################################

class App():
	"""Main. Starts the app"""

	def __init__(self):
		self.mainWindow = MainWindow()
		

###########################################################################################

class GladeObject():
	"""Data class for inheritance purposes only"""

	glade_file = "main.glade"
	glade = Gtk.Builder()
	glade.add_from_file(glade_file)

	def __init__(self):
		self.users = Users()

		

###########################################################################################

class MainWindow(GladeObject):
	"""Manage main Window"""

	def __init__(self):
		GladeObject.__init__(self)
		self.this_window = self.glade.get_object("MainWindow")
		self.tree_view = TreeView()
		
		self.this_window.connect("destroy", Gtk.main_quit)

		self.this_window.show_all()


###########################################################################################

class TreeView(GladeObject):
	"""Manage users TreeView"""

	def __init__(self):
		GladeObject.__init__(self)
		self.this_tree_view = self.glade.get_object("treeView")
		self.store = self.glade.get_object("store")

		self._prepare_columns()
		self.refresh()

	def _prepare_columns(self):
		column_names = "ID", "Apellido paterno", "Apellido materno", "Nombre", "DNI", "Direccion"
		for index, name in enumerate(column_names):
			self.this_tree_view.append_column(Gtk.TreeViewColumn(name, 
				Gtk.CellRendererText(), text=index))

	def refresh(self):
		self.store.clear()
		users = self.users.list_all()
		for user in users:
			self.store.append(user)

###########################################################################################

class Users:
	"""Model for ´users´ table"""

	def __init__(self):
		self._conn = sqlite3.connect("main.db")
		self._conn.text_factory = str
		self._c = self._conn.cursor()
		self._table = "users"

	def delete(self, userId):
		delete = "DELETE FROM {0} WHERE id = ?".format(self._table)
		self._c.execute(delete, (userId,))
		self._conn.commit()

	def insert(self, data):
		insert = "INSERT INTO {0} VALUES (NULL, ?, ?, ?, ?, ?)".format(self._table)
		self._c.execute(insert, data)
		self._conn.commit()

	def list_all(self):
		self._c.execute("SELECT * FROM {0}".format(self._table))
		return self._c.fetchall()

###########################################################################################

if __name__ == "__main__":
	app = App()
	Gtk.main()	