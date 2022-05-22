import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

def renderTreeView():
    taskTreeView = builder.get_object("taskTreeView")
    names = ('Task', 'Description', 'Due Date', 'Task priority')
    for i in range(4):
        renderer_text = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(names[i], renderer_text, text=i)
        taskTreeView.append_column(column)

class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()

    def onMenuBtnClicked(self, button):
        aboutDialog = builder.get_object("aboutDialog")
        aboutDialog.show_all()

    def onAboutCloseBtnClicked(self, button):
        aboutDialog = builder.get_object("aboutDialog")
        aboutDialog.hide()

    def onSearchBtnToggled(self, button):
        toggleState = button.get_active()
        searchBar = builder.get_object("searchBar")
        searchBar.set_search_mode(toggleState)

    def onAddBtnClicked(self, button):
        addDialog = builder.get_object("addDialog")
        addDialog.show_all()

    def onTodayBtnClicked(self, button):
        dateEntry = builder.get_object("dateEntry")
        dateEntry.set_text("Today")

    def onCancelTaskBtnClicked(self, button):
        addDialog = builder.get_object("addDialog")
        addDialog.hide()

    def onAddTaskBtnClicked(self, button):
        addDialog = builder.get_object("addDialog")
        dateEntry = builder.get_object("dateEntry")
        nameEntry = builder.get_object("nameEntry")
        descriptionEntry = builder.get_object("descriptionEntry")
        taskListStore = builder.get_object("taskListStore")
        taskTreeView = builder.get_object("taskTreeView")

        taskDate = dateEntry.get_text()
        taskName = nameEntry.get_text()
        taskDescription = descriptionEntry.get_text()

        taskListStore.append([taskName, taskDescription, taskDate, 1])
        taskTreeView.show_all()
        addDialog.hide()


    def onOpenBtnToggled(self, button):
        toggleState = button.get_active()
        closedBtn = builder.get_object("closedBtn")

        if toggleState == False:
            closedBtn.set_active(True)
        elif toggleState == True:
            closedBtn.set_active(False)

    def onClosedBtnToggled(self, button):
        toggleState = button.get_active()
        openBtn = builder.get_object("openBtn")

        if toggleState == False:
            openBtn.set_active(True)
        elif toggleState == True:
            openBtn.set_active(False)

builder = Gtk.Builder()
builder.add_from_file("todo.ui")
builder.connect_signals(Handler())

window = builder.get_object("MainWindow")
window.show_all()

renderTreeView()

Gtk.main()
