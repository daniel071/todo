import sys
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

@Gtk.Template.from_file("/home/daniel/code/todo/todo.ui")
class headerbar(Gtk.HeaderBar):
    __gtype_name__ = "headerbar"

    aboutBtn = Gtk.Template.Child("aboutBtn")
    print(aboutBtn)

    @Gtk.Template.Callback("aboutBtn_button_clicked")
    def aboutBtn_button_clicked(self, *args):
        print("Hello!")

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app) or headerbar(application=self)

        builder = Gtk.Builder()
        builder.set_current_object(self)
        builder.add_from_file("/home/daniel/code/todo/todo.ui")
        print(builder.get_objects())
        #
        # handlers = {
        #     "onButtonPressed": onButtonPressed
        # }
        #builder.connect_signals(handlers)

        window = builder.get_object("MainWindow")
        window.present()

app = MyApp(application_id="com.example.GtkApplication")
app.run(sys.argv)
