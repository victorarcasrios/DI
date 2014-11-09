#! /usr/bin/env python
#-*-coding: UTF-8 -*-

from gi.repository import Gtk

## TODO
## 		- refactor comboBoxCreation, convert _fillComboBox function and other logic of comboBox
## 		creation in App class in a new discountComboBox class

class App():

	con = "con"

	def __init__(self):
		self._discounts = 5, 10, 20

		self._gladeFile = "calculadora.glade"
		self._glade = Gtk.Builder()
		self._glade.add_from_file(self._gladeFile)
		
		## Widgets
		self.mainWindow = self._glade.get_object("mainWindow")
		self.priceEntry = self._glade.get_object("priceEntry")
		self.comboBox = self._glade.get_object("discountComboBox")
		self.finalPriceOutput = self._glade.get_object("finalPriceOutput")
		self.discountedOutput = self._glade.get_object("discountedOutput")

		self._fillComboBox()
		
		## Event Handlers
		self.mainWindow.connect("destroy", Gtk.main_quit)
		self.priceEntry.connect("changed", self._onPriceEntryChanged)
		self.comboBox.connect("changed", self._calculateAndDisplay)

		self.mainWindow.show_all()	

	def _fillComboBox(self):
		store = Gtk.ListStore(int)
		for discount in self._discounts:
			store.append([discount])

		cellRendererText = Gtk.CellRendererText()
		self.comboBox.set_model(store)
		self.comboBox.pack_start(cellRendererText, True)
		self.comboBox.add_attribute(cellRendererText, "text", 0)

	def _onPriceEntryChanged(self, obj):
		if not isNumeric(self.priceEntry.get_text()):
			print "ERROR"
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

		if price is None or treeIter is None:
			return False, False, False
		else:
			return True, float(price), float(self.comboBox.get_model()[treeIter][0])

## TODO mix this class implementation with todo xml glade file
class NotNumericErrorDialog(Gtk.MessageDialog):

	def __init__(self):
		Gtk.MessageDialog.__init__(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, "No es un número válido")
		self.format_secundary_text("Hola")
		self.run()

def isNumeric(value):
	try:
		float(value)
		return True
	except ValueError:
		return False

if __name__ == "__main__":
	app = App()
	Gtk.main()