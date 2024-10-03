"""

https://www.tutorialspoint.com/pygtk/pygtk_hello_world.htm
https://github.com/heldersepu/GMapCatcher/tree/master/gmapcatcher
https://github.com/TomSchimansky/TkinterMapView/tree/main/tkintermapview
"""

import gtk
import pygtk
class PyApp(gtk.Window):
   def __init__(self):
      super(PyApp, self).__init__()
      self.set_default_size(300,200)
      self.set_title("Hello World in PyGTK")
      label = gtk.Label("Hello World")
      self.add(label)
      self.show_all()
PyApp()
gtk.main()