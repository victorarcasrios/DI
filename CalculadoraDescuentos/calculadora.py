#! /usr/bin/env python
#-*-coding: UTF-8 -*-

from gi.repository import Gtk
from gi.repository import Gdk

## TODO
## 		- refactor comboBoxCreation, convert _fillComboBox function and other logic of comboBox
## 		creation in App class in a new discountComboBox class

class MyGtkObject():
	"""Data class from whom inherit only for generalization purposes"""
	def __init__(self):
		self._gladeFile = "calculadora.glade"
		self._glade = Gtk.Builder()
		self._glade.add_from_file(self._gladeFile)

###################################################################################################

class App(MyGtkObject):
	"""Manage mainWindow view"""
	def __init__(self):
		MyGtkObject.__init__(self)
		self._discounts = 5, 10, 20
		
		## Widgets
		self.mainWindow = self._glade.get_object("mainWindow")
		self.quitAction = self._glade.get_object("quitImageMenuItem")
		self.aboutAction = self._glade.get_object("aboutImageMenuItem")
		self.priceEntry = self._glade.get_object("priceEntry")
		self.comboBox = self._glade.get_object("discountComboBox")
		self.finalPriceOutput = self._glade.get_object("finalPriceOutput")
		self.discountedOutput = self._glade.get_object("discountedOutput")

		self._fillComboBox()
		
		## Event Handlers
		self.mainWindow.connect("destroy", Gtk.main_quit)
		self.mainWindow.connect("key_press_event", self._onKeyPressEvent)
		self.quitAction.connect("activate", Gtk.main_quit)
		self.aboutAction.connect("activate", lambda obj: AboutDialog())
		self.priceEntry.connect("changed", self._onPriceEntryChanged)
		self.comboBox.connect("changed", self._calculateAndDisplay)

		self.mainWindow.show_all()	

	def _onKeyPressEvent(self, obj, event):
		if(event.state & Gdk.ModifierType.CONTROL_MASK and event.keyval == 113):
			Gtk.main_quit()			

	def _fillComboBox(self):
		store = Gtk.ListStore(int)
		for discount in self._discounts:
			store.append([discount])

		cellRendererText = Gtk.CellRendererText()
		self.comboBox.set_model(store)
		self.comboBox.pack_start(cellRendererText, True)
		self.comboBox.add_attribute(cellRendererText, "text", 0)

	def _onPriceEntryChanged(self, obj):
		value = self.priceEntry.get_text()
		if value and not isNumeric(value):
			dialog = NotNumericErrorDialog()
		else:
			self._calculateAndDisplay(obj)


	def _calculateAndDisplay(self, obj):
		hasData, price, discount = self._getData()
		if not hasData:
			self.finalPriceOutput.set_text("")
			self.discountedOutput.set_text("")
		else:
			discounted = float(price * discount / 100)
			self.finalPriceOutput.set_text("{0}€".format(price - discounted))
			self.discountedOutput.set_text("{0}€".format(discounted))

	def _getData(self):
		price = self.priceEntry.get_text()
		treeIter = self.comboBox.get_active_iter()

		if not price or not treeIter:
			return False, False, False
		else:
			return True, float(price), int(self.comboBox.get_model()[treeIter][0])

###################################################################################################

class AboutDialog(MyGtkObject):
	"""Manage the AboutDialog window"""

	def __init__(self):
		MyGtkObject.__init__(self)
		self.aboutDialog = self._glade.get_object("aboutDialog")
		self.aboutDialogButtonBox = self._glade.get_object("aboutDialogButtonBox")
		
		self._closeButton = self.aboutDialogButtonBox.get_children()[0]
		self._closeButton.connect( "clicked", lambda obj: self.aboutDialog.destroy() )

		self.aboutDialog.run()

###################################################################################################

class NotNumericErrorDialog(MyGtkObject):
	"""Manage the inputErrorMessageDialog view"""
	def __init__(self):
		MyGtkObject.__init__(self)
		self.messageDialog = self._glade.get_object("inputErrorMessageDialog");
		self.button = self._glade.get_object("messageDialogButton")

		self.button.connect( "clicked", lambda obj: self.messageDialog.destroy() )
		
		self.messageDialog.run()

###################################################################################################

def isNumeric(value):
	try:
		float(value)
		return True
	except ValueError:
		return False

if __name__ == "__main__":
	app = App()
	Gtk.main()