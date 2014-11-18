#! /usr/bin/env python
#-*-coding: UTF-8 -*-

from gi.repository import Gtk
import sqlite3

class GtkClass:
	"""Data class for inheritance purposes only"""
	def __init__(self):
		self._model = Model()
		self._gladeFile = "userSigninForm.glade"
		self._glade = Gtk.Builder()
		self._glade.add_from_file(self._gladeFile)

###########################################################################################

## TODO hide not filled message and show only when user tries to save data with empty fields
class App(GtkClass):
	"""Manage mainWindow"""
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
	"""Manage ListWindow"""

	def __init__(self):
		GtkClass.__init__(self);
	
		## Widgets
		self.listWindow = self._glade.get_object("listWindow")
		self.deleteUserAction = self._glade.get_object("deleteUserAction")
		self.treeView = self._glade.get_object("treeView")

		self._prepareTreeView()
		self._refreshList()
		self.treeViewSelection = self.treeView.get_selection()

		## Handlers
		self.treeViewSelection.connect("changed", self._onTreeViewSelectionChanged)
		self.deleteUserAction.connect("clicked", self._onDeleteUserActionClicked)

		self.listWindow.show_all()

	def _prepareTreeView(self):
		columnNames = "ID", "Usuario", "Contraseña", "Email", "Nombre", "Apellidos", "Dirección"
		for i in range(1, len(columnNames)):
			self.treeView.append_column(Gtk.TreeViewColumn(columnNames[i], Gtk.CellRendererText(), text=i))

	def _refreshList(self):
		self.listStore = Gtk.ListStore(int, str, str, str, str, str, str)
		users = self._model.listAll()
		for user in users:
			self.listStore.append(user)
		
		self.treeView.set_model(self.listStore)

	def _onTreeViewSelectionChanged(self, selection):
		model, self._selectedIter = selection.get_selected()
		self.deleteUserAction.set_sensitive(True if self._selectedIter != None else False)

	def _onDeleteUserActionClicked(self, obj):
		if self._selectedIter != None:
			self._selectedUserId = self.listStore[self._selectedIter][0]
			self.confirmDeleteDialog = ConfirmDeleteDialog(self)

	def _onConfirmDeleteButtonClicked(self, obj):
		self._model.delete(self._selectedUserId)
		self._refreshList()
		self.confirmDeleteDialog.dialog.destroy()

###########################################################################################

class ConfirmDeleteDialog(GtkClass):
	"""Manage confirmDeleteDialog"""

	def __init__(self, listDialog):
		GtkClass.__init__(self)

		## Widgets
		self.listDialog = listDialog
		self.dialog = self._glade.get_object("confirmDeleteDialog")
		self.confirmDeleteButton = self._glade.get_object("confirmDeleteButton")
		self.cancelDeleteButton = self._glade.get_object("cancelDeleteButton")

		## Handlers
		self.confirmDeleteButton.connect("clicked", listDialog._onConfirmDeleteButtonClicked)
		self.cancelDeleteButton.connect("clicked", lambda obj: self.dialog.destroy())

		self.dialog.show_all()

###########################################################################################

class Model:
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
		insert = "INSERT INTO {0} VALUES (NULL, ?, ?, ?, ?, ?, ?)".format(self._table)
		self._c.execute(insert, data)
		self._conn.commit()

	def listAll(self):
		self._c.execute("SELECT * FROM {0}".format(self._table))
		return self._c.fetchall()

###########################################################################################

if __name__ == "__main__":
	app = App()
	Gtk.main()			