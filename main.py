import gi
from datetime import datetime

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

def matchFunc(taskListStore, iterr, data=None):
    searchEntry = builder.get_object("searchEntry")
    query = searchEntry.get_text()
    value = taskListStore.get_value(iterr, 1)


    if query == "":
        return True
    elif query in value.lower():
        return True
    return False

def onEntryRefilter():
    taskListFilter = builder.get_object("taskListFilter")
    taskListFilter.refilter()


def onTreeViewToggled(cell, path, taskListStore, *ignore):
    row = taskListStore.get_iter(path)

    taskListStore = builder.get_object("taskListStore")
    taskTreeView = builder.get_object("taskTreeView")

    taskListStore.remove(row)
    taskTreeView.show_all()
    # if path is not None:
    #     it = taskListStore.get_iter(path)
    #     print(model[it][0])
    #     model[it][0].set_active(True)

def renderTreeView():
    searchEntry = builder.get_object("searchEntry")
    taskTreeView = builder.get_object("taskTreeView")
    taskListStore = builder.get_object("taskListStore")

    taskTreeView.set_search_entry(searchEntry)

    taskListFilter = builder.get_object("taskListFilter")
    taskListFilter.set_visible_func(matchFunc)

    names = ('Completed', 'Task', 'Description', 'Due Date', 'Task priority')
    for i in range(1):
        toggle = Gtk.CellRendererToggle()
        toggle.set_activatable(True)
        toggle.connect("toggled", onTreeViewToggled, taskListStore)
        column = Gtk.TreeViewColumn(names[i], toggle)
        taskTreeView.append_column(column)
    for i in range(1, 5):
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
        today = datetime.today().strftime('%Y-%m-%d')

        dateEntry.set_text(today)

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

        taskListStore.append([Gtk.CellRendererToggle(), taskName, taskDescription, taskDate, 1])
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

    def onSearchEntryChanged(self, entry):
        #searchQuery = entry.get_text()
        onEntryRefilter()


builder = Gtk.Builder()
builder.add_from_file("todo.ui")
builder.connect_signals(Handler())

window = builder.get_object("MainWindow")
window.show_all()

renderTreeView()

Gtk.main()
