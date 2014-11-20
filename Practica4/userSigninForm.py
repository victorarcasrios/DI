#! /usr/bin/env python
#-*-coding: UTF-8 -*-

from gi.repository import Gtk
import sqlite3

## TODO 
## - Display not filled message when user tries to save data with empty fields
## - Display succesful insertion message when record was properly inserted
## - Implement refresh button and automatically refresh listWindow treeView 
##		when new record was inserted
## - Display unique restriction exception message when it happens

class GtkClass:
	"""Data class for inheritance purposes only"""
	def __init__(self):
		self._model = Model()
		self._gladeFile = "userSigninForm.glade"
		self._glade = Gtk.Builder()
		self._glade.add_from_file(self._gladeFile)

###########################################################################################

class App(GtkClass):
	"""Manage mainWindow"""
	def __init__(self):
		GtkClass.__init__(self);

		## Widgets
		self.mainWindow = self._glade.get_object("mainWindow")
		self.listAllButton = self._glade.get_object("listAllButton")
		self.saveButton = self._glade.get_object("saveButton")
		self.closeButton = self._glade.get_object("closeButton")

		self.entries = (
			self._glade.get_object("nickEntry"),
			self._glade.get_object("passwordEntry"),
			self._glade.get_object("emailEntry"),
			self._glade.get_object("nameEntry"),
			self._glade.get_object("surnameEntry"),
			self._glade.get_object("addressEntry")
			)

		## Handlers
		self.mainWindow.connect("destroy", Gtk.main_quit)
		self.listAllButton.connect("clicked", lambda obj: ListWindow())
		self.saveButton.connect("clicked", self._saveData)
		self.closeButton.connect("clicked", Gtk.main_quit)

		self.mainWindow.show_all()

	def _saveData(self, widget):
		data = self._getData()
		if(self._isProperUserData(data)):
			self._model.insert(data)
			self._emptyEntries()

	def _getData(self):
		return tuple(entry.get_text() for entry in self.entries)
	
	def _isProperUserData(self, data):
		for datum in data:
			if not datum:
				return False
		return True

	def _emptyEntries(self):
		tuple(entry.set_text("") for entry in self.entries)

###########################################################################################

class ListWindow(GtkClass):
	"""Manage ListWindow"""

	def __init__(self):
		GtkClass.__init__(self);

		## Widgets
		self.listWindow = self._glade.get_object("listWindow")		
		self.deleteUserAction = self._glade.get_object("deleteUserAction")
		self.treeView = self._glade.get_object("treeView")
		
		self.listStore = Gtk.ListStore(int, str, str, str, str, str, str)
		self.treeView.set_model(self.listStore)
		## Menu
		self.openAction = self._glade.get_object("openAction")
		self.refreshAction = self._glade.get_object("refreshAction")
		self.closeAction = self._glade.get_object("closeAction")
		self.exitAction = self._glade.get_object("exitAction")
		self.deleteMenuAction = self._glade.get_object("deleteMenuAction")
		self.aboutAction = self._glade.get_object("aboutAction")

		self._prepareTreeView()
		self._refreshList()
		self.treeViewSelection = self.treeView.get_selection()

		## Handlers
		self.treeViewSelection.connect("changed", self._onTreeViewSelectionChanged)
		self.deleteUserAction.connect("clicked", self._onDeleteUserActionClicked)
		## Menu
		self.openAction.connect("activate", self._refreshList)
		self.refreshAction.connect("activate", self._refreshList)
		self.closeAction.connect("activate", self._emptyList)
		self.exitAction.connect("activate", lambda obj: self.listWindow.destroy())
		self.deleteMenuAction.connect("activate", self._onDeleteUserActionClicked)
		self.aboutAction.connect("activate", lambda obj: AboutDialog())

		self.listWindow.show_all()

	def _prepareTreeView(self):
		columnNames = "ID", "Usuario", "Contraseña", "Email", "Nombre", "Apellidos", "Dirección"
		for i in range(1, len(columnNames)):
			self.treeView.append_column(Gtk.TreeViewColumn(columnNames[i], Gtk.CellRendererText(), text=i))

	def _refreshList(self, obj = False):
		self.listStore.clear()
		users = self._model.listAll()
		for user in users:
			self.listStore.append(user)
		self._onListStoreFilled()

	def _onListStoreFilled(self):
		self.openAction.set_sensitive(False)
		self.refreshAction.set_sensitive(True)

	def _emptyList(self, obj):		
		self.listStore.clear()
		self._onListStoreCleared()

	def _onListStoreCleared(self):
		self.openAction.set_sensitive(True)
		self.refreshAction.set_sensitive(False)		

	def _onTreeViewSelectionChanged(self, selection):
		model, self._selectedIter = selection.get_selected()
		hasSelected = self._selectedIter != None

		self.deleteUserAction.set_sensitive(True if hasSelected else False)
		self.deleteMenuAction.set_sensitive(True if hasSelected else False)

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

class AboutDialog(GtkClass):

	def __init__(self):
		GtkClass.__init__(self)

		## Widgets
		self.dialog = self._glade.get_object("aboutDialog")
		self._closeButton = self._glade.get_object("aboutDialogButtonBox").get_children()[0]

		## Handlers
		self._closeButton.connect("clicked", lambda obj: self.dialog.destroy())

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