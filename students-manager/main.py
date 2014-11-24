from gi.repository import Gtk
import sqlite3

class App():

	def __init__(self):
		self.mainWindow = MainWindow()

class GladeObject():

	def __init__(self):
		glade_file = "main.glade"
		self.glade = Gtk.Builder()
		self.glade.add_from_file(glade_file)

class MainWindow(GladeObject):

	def __init__(self):
		GladeObject.__init__(self)
		self = self.glade.get_object("MainWindow")
		
		self.connect("destroy", Gtk.main_quit)

		self.show_all()

if __name__ == "__main__":
	app = App()
	Gtk.main()	