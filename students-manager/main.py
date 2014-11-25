#! /usr/bin/env python
#-*-coding: UTF-8 -*-

from gi.repository import Gtk
import sqlite3

###########################################################################################

class App():

	def __init__(self):
		self.mainWindow = MainWindow()
		

###########################################################################################

class GladeObject():

	def __init__(self):
		self.users = Users()

		glade_file = "main.glade"
		self.glade = Gtk.Builder()
		self.glade.add_from_file(glade_file)

###########################################################################################

class MainWindow(GladeObject):

	def __init__(self):
		GladeObject.__init__(self)
		self.this_window = self.glade.get_object("MainWindow")
		self.tree_view = TreeView()
		
		self.this_window.connect("destroy", Gtk.main_quit)

		self.this_window.show_all()

###########################################################################################

class TreeView(GladeObject):

	def __init__(self):
		GladeObject.__init__(self)
		self.this_tree_view = self.glade.get_object("treeView")
		self.store = Gtk.ListStore(int, str, str, str, int, str)
		self.this_tree_view.set_model(self.store)

		self._prepare_columns()
		self.refresh()
		

	def _prepare_columns(self):
		column_names = "ID", "Apellido paterno", "Apellido materno", "Nombre", "DNI", "Direccion"
		for i in range(1, len(column_names)):
			self.this_tree_view.append_column(Gtk.TreeViewColumn(column_names[i], 
				Gtk.CellRendererText(), text=i))

	def refresh(self):
		print "HI"
		self.store.clear()
		users = self.users.list_all()
		for user in users:
			self.store.append(user)

###########################################################################################

class Users:
	"""Model for ´users´ table"""

	def __init__(self):
		self._conn = sqlite3.connect("practica2.db")
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