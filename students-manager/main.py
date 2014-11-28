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

## TODO refactor to data class w/ constructor. 
##		Model variable users may be a class var, not an instance one
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
		self.this_window 	= self.glade.get_object("MainWindow")
		self.tree_view 		= TreeView()
		self.entries = {
			"surname"		: self.glade.get_object("surnameEntry"),
			"motherSurname"	: self.glade.get_object("motherSurnameEntry"),
			"name"			: self.glade.get_object("nameEntry"),
			"dni"			: self.glade.get_object("dniEntry"),
			"address"		: self.glade.get_object("addressEntry")
		}
		self.buttons = {
			"new"			: self.glade.get_object("newUserButton"),
			"save"			: self.glade.get_object("saveUserButton"),
			"cancel"		: self.glade.get_object("cancelUserButton"),
			"update"		: self.glade.get_object("updateUserButton"),
			"delete"		: self.glade.get_object("deleteUserButton"),
			"close"			: self.glade.get_object("closeUserButton")
		}		
		self.this_window.connect("destroy", Gtk.main_quit)
		self.tree_view.selection.connect("changed", self._on_tree_view_selection_changed)
		{entry.connect("changed", self._on_entry_changed) for k, entry in self.entries.iteritems()}
		self.buttons["new"].connect("clicked", self._saveData)

		## Set buttons sensitivity initial state
		self._on_tree_view_selection_changed(self.tree_view.selection)
		self._on_entry_changed(self.buttons['new'])

		self.this_window.show_all()

	## TODO Refactor to warning about unsuccesful insertion
	def _saveData(self, widget):
		data = self._get_data()
		if self._is_proper_user_data(data):
			self.users.insert(data)
			self._empty_entries()
			self.tree_view.refresh()

	def _get_data(self):
		return (
			self.entries["surname"].get_text(),
			self.entries["motherSurname"].get_text(),
			self.entries["name"].get_text(),
			self.entries["dni"].get_text(),
			self.entries["address"].get_text()
		)
	
	def _is_proper_user_data(self, data):
		for datum in data:
			if not datum:
				return False
		return True

	def _empty_entries(self):
		tuple(entry.set_text("") for key, entry in self.entries.iteritems())

	def _on_entry_changed(self, entry):
		self.buttons["cancel"].set_sensitive(False if self._buttons_are_empty() else True)

	def _buttons_are_empty(self):
		for key, entry in self.entries.iteritems():
			if entry.get_text():
				return False
		return True

	def _on_tree_view_selection_changed(self, selection):
		model, self._selected_iter = selection.get_selected()
		self._hasSelected = self._selected_iter != None

		self._set_buttons_mode()

	def	_set_buttons_mode(self):
		if self._hasSelected:
			self._set_buttons_UD_mode()
		else:
			self._set_buttons_creation_mode()

	def _set_buttons_creation_mode(self):
		self.buttons["new"].set_sensitive(True)
		self.buttons["save"].set_sensitive(False)
		self.buttons["update"].set_sensitive(False)
		self.buttons["delete"].set_sensitive(False)

	def _set_buttons_UD_mode(self):
		self.buttons["new"].set_sensitive(False)
		self.buttons["save"].set_sensitive(True)
		self.buttons["update"].set_sensitive(True)
		self.buttons["delete"].set_sensitive(True)

###########################################################################################

class TreeView(GladeObject):
	"""Manage users TreeView"""

	def __init__(self):
		GladeObject.__init__(self)
		self.this_tree_view = self.glade.get_object("treeView")
		self.store 			= self.glade.get_object("store")
		self.selection 		= self.this_tree_view.get_selection()
		
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