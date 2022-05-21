import sys
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        #self.win.present()
        builder = Gtk.Builder()
        builder.add_from_file("todo.ui")
        window = builder.get_object("window1")
        window.present()

app = MyApp(application_id="com.example.GtkApplication")
app.run(sys.argv)
