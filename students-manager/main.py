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

class GladeContainer():
	"""Data class for inheritance purposes only"""

	glade_file = "main.glade"

	def __init__(self):		
		self.builder = Gtk.Builder()
		self.builder.add_from_file(self.glade_file)

###########################################################################################

class MainWindow(GladeContainer):
	"""Manage MainWindow Gtk.Window"""

	_registration_window = None

	def __init__(self):
		GladeContainer.__init__(self)
		self.this_window = self.builder.get_object("MainMenuWindow")

		self.this_window.connect("destroy", Gtk.main_quit)
		self.builder.get_object("closeImageMenuItem").connect("activate", Gtk.main_quit)
		self.builder.get_object("aboutImageMenuItem").connect(
			"activate", lambda widget: AboutDialog())
		self.builder.get_object("registrationToolButton").connect(
			"clicked", self._openRegistrationWindow)

		self.this_window.show_all()

	def _openRegistrationWindow(self, widget):
		if not self._registration_window:
			self._registration_window = RegistrationWindow()
			self._registration_window.this_window.connect("destroy", self._unset_registration_window)

	def _unset_registration_window(self, widget):
		self._registration_window = None

###########################################################################################

class RegistrationWindow(GladeContainer):
	"""Manage RegistrationWindow Gtk.Window"""

	def __init__(self):
		GladeContainer.__init__(self)
		self.this_window 	= self.builder.get_object("RegistrationWindow")
		self.tree_view 		= TreeView(self.builder)
		self.entries = {
			"surname"		: self.builder.get_object("surnameEntry"),
			"motherSurname"	: self.builder.get_object("motherSurnameEntry"),
			"name"			: self.builder.get_object("nameEntry"),
			"dni"			: self.builder.get_object("dniEntry"),
			"address"		: self.builder.get_object("addressEntry")
		}
		self.buttons = {
			"new"			: self.builder.get_object("newUserButton"),
			"save"			: self.builder.get_object("saveUserButton"),
			"cancel"		: self.builder.get_object("cancelUserButton"),
			"update"		: self.builder.get_object("updateUserButton"),
			"delete"		: self.builder.get_object("deleteUserButton"),
			"close"			: self.builder.get_object("closeWindowButton")
		}		
		self.tree_view.selection.connect("changed", self._on_tree_view_selection_changed)
		{entry.connect("changed", self._on_entry_changed) for k, entry in self.entries.iteritems()}
		self.buttons["new"].connect("clicked", self._prepare_to_create)
		self.buttons["save"].connect("clicked", self._save_data)
		self.buttons["update"].connect("clicked", self._update_data)
		self.buttons["cancel"].connect("clicked", self._on_cancel_clicked)
		self.buttons["delete"].connect("clicked", self._on_delete_clicked)
		self.buttons["close"].connect("clicked", lambda widget: self.this_window.destroy())

		## Set buttons sensitivity initial state
		self._on_tree_view_selection_changed(self.tree_view.selection)
		self._on_entry_changed(self.buttons['new'])

		self.this_window.show_all()

	def _prepare_to_create(self, widget):
		self._clear_entries()
		self.entries["surname"].grab_focus()
		self.tree_view.selection.unselect_iter(self._selected_iter)	

	def _save_data(self, widget):
		data = self._get_data()
		if self._is_proper_user_data(data):
			Students.insert(data)
			self._clear_entries()
			self.tree_view.refresh()

	def _update_data(self, widget):
		user_id = self.tree_view.store[self._selected_iter][0]
		data = self._get_data()
		if self._is_proper_user_data(data):
			Students.update(user_id, data)
			self.tree_view.refresh()

	def _on_delete_clicked(self, widget):
		self.confirmDialog = ConfirmDeleteDialog(self)

	def _delete_user(self):		
		user_id = self.tree_view.store[self._selected_iter][0]
		Students.delete(user_id)	
		self.tree_view.refresh()

	def _on_cancel_clicked(self, widget):
		if self._hasSelected:
			self._fill_entries_with(self.tree_view.store[self._selected_iter])
		else:
			self._clear_entries()

	## Create and update HELPERS
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
				AlertDialog("Todos los datos son obligatorios")
				return False
		return True
	## End Create or update HELPERS

	## CHANGED Event Handlers
	def _on_entry_changed(self, entry):
		self.buttons["cancel"].set_sensitive(False if self._entries_are_empty() else True)

	def _entries_are_empty(self):
		for key, entry in self.entries.iteritems():
			if entry.get_text():
				return False
		return True

	def _on_tree_view_selection_changed(self, selection):
		model, self._selected_iter = selection.get_selected()
		self._hasSelected = self._selected_iter != None

		if self._hasSelected:
			self._fill_entries_with(model[self._selected_iter])
			self._set_buttons_UD_mode()
		else:
			self._clear_entries()
			self._set_buttons_creation_mode()

	def _fill_entries_with(self, data):
		self.entries["surname"].set_text(data[1])
		self.entries["motherSurname"].set_text(data[2])
		self.entries["name"].set_text(data[3])
		self.entries["dni"].set_text(data[4])
		self.entries["address"].set_text(data[5])

	def _set_buttons_creation_mode(self):
		self.buttons["new"].set_sensitive(False)
		self.buttons["save"].set_sensitive(True)
		self.buttons["update"].set_sensitive(False)
		self.buttons["delete"].set_sensitive(False)

	def _set_buttons_UD_mode(self):
		self.buttons["new"].set_sensitive(True)
		self.buttons["save"].set_sensitive(False)
		self.buttons["update"].set_sensitive(True)
		self.buttons["delete"].set_sensitive(True)

	## END CHANGED Events Handlers

	def _clear_entries(self):
		tuple(entry.set_text("") for key, entry in self.entries.iteritems())

###########################################################################################

class TreeView():
	"""Manage students TreeView"""

	def __init__(self, container_builder):
		self.builder 		= container_builder
		self.this_tree_view = self.builder.get_object("treeView")
		self.store 			= self.builder.get_object("store")
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
		users = Students.list_all()
		for user in users:
			self.store.append(user)

###########################################################################################

class AlertDialog(GladeContainer):
	"""Manage AlertDialog Gtk.Dialog"""
	
	def __init__(self, message):
		GladeContainer.__init__(self)

		self._this_dialog = self.builder.get_object("AlertDialog")
		self._this_dialog.format_secondary_text(message)

		self.builder.get_object("alertDialogActionArea").get_children()[0].connect(
			"clicked", lambda widget: self._this_dialog.destroy())
		self._this_dialog.show_all()

###########################################################################################

class ConfirmDeleteDialog(GladeContainer):
	"""Manage ConfirmDeleteDialog Gtk.Dialog"""

	def __init__(self, registrationWindow):
		GladeContainer.__init__(self)
		
		self._registration_window = registrationWindow
		self._this_dialog = self.builder.get_object("ConfirmDeleteDialog")
		self._confirmButton = self.builder.get_object("confirmDeleteButton")
		self._cancelButton = self.builder.get_object("cancelDeleteButton")

		self._confirmButton.connect("clicked", self._on_delete_confirmed)
		self._cancelButton.connect("clicked", lambda widget: self._this_dialog.destroy())

		self._this_dialog.show_all()

	def _on_delete_confirmed(self, widget):
		self._registration_window._delete_user()
		self._this_dialog.destroy()

###########################################################################################

class AboutDialog(GladeContainer):
	"""Manage AboutDialog Gtk.Dialog"""

	def __init__(self):
		GladeContainer.__init__(self)

		self._this_dialog = self.builder.get_object("AboutDialog")
		self._close_button = self.builder.get_object("AboutDialogActionArea").get_children()[0]

		self._close_button.connect("clicked", lambda widget: self._this_dialog.destroy())

		self._this_dialog.show_all()

###########################################################################################

class Students:
	"""Model for ´students´ table"""

	_conn = sqlite3.connect("main.db")
	_conn.text_factory = str
	_c = _conn.cursor()
	_table = "students"

	@classmethod
	def delete(cls, student_id):
		delete = "DELETE FROM {0} WHERE id = ?".format(cls._table)
		cls._c.execute(delete, (student_id,))
		cls._conn.commit()

	@classmethod
	def insert(cls, data):
		insert = "INSERT INTO {0} VALUES (NULL, ?, ?, ?, ?, ?)".format(cls._table)
		cls._c.execute(insert, data)
		cls._conn.commit()

	@classmethod
	def list_all(cls):
		cls._c.execute("SELECT * FROM {0}".format(cls._table))
		return cls._c.fetchall()

	@classmethod
	def update(cls, student_id, data):
		update = """UPDATE {0} set surname = ?, mother_surname = ?, name = ?, dni = ?, 
			address = ? WHERE id = ?""".format(cls._table)
		data += (student_id,)
		cls._c.execute(update, data)
		cls._conn.commit()

###########################################################################################

if __name__ == "__main__":
	app = App()
	Gtk.main()	