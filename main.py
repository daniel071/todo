# Todo
# A simple Todo app made with GTK3 and Python.

# Solution requirements implemented (Task 1)
# - The program must allow the user to enter and store tasks that are input as strings.
# - The program must allow the user to enter a due date for each task.
# - The program must display all tasks stored since the program started.
# - The format of the display should include the due date and then a space followed by a description of the task.
# - Each task must appear on a separate line of the final display field.

# Solution requirements NOT implemented (Task 2)
# - When a task is entered where the due date is prior to the current date the task and due date must display “Overdue”.
# - When a task is entered where the due date is the current date the task and due date must display “Due Today”.
# - When a task is entered where the due date after the current date the task and due date must display “Due After Today”.
# - A count of the total number of tasks should be displayed at the end of the program.
# (Task 3)
# - When a task is stored it must be appended to a file called tasks in the local directory, where the program executable is stored.
# - When the program starts the read only fields of previous tasks must be populated based on the contents on the tasks file.
# - The tasks must be classified into the relevant read only field based on the due date recorded in the file, relative to the current date.


# Necessary dependencies for the program to run
import gi
from datetime import datetime

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# Used to manage the priority of tasks, and allow the user to change it.
# 0: Not specified
# 1: Normal priority
# 2: Important priority
# 3: Urgent priority

taskPriority = 0

# Function that uses search query from search entry and filters the main
# list of tasks that only matches the query.
def matchFunc(taskListStore, iterr, data=None):
    # Get searchEntry object and get query text from it
    searchEntry = builder.get_object("searchEntry")
    query = searchEntry.get_text()

    # Get the text of the row to compare with query
    # A for loop is not used here as GTK calls this function multiple times
    value = taskListStore.get_value(iterr, 1)

    # If the query matches, do not hide the row. If the query does not match,
    # hide the result.
    if query == "":
        return True
    elif query in value.lower():
        return True
    return False

# Handle formatting for priority text. e.g. "Urgent" is bold red to highlight
# it's importance
def formatFunc(col, renderer_text, taskListStore, titer, data):
    # Get fifth row (0, 1, 2, 3, 4), which is task priority
    val = taskListStore.get_value(titer, 4)

    # Set text colour and bold for each value.
    if val == "Unspecified":
        renderer_text.set_property("foreground", "lightgray")
        renderer_text.set_property("weight", 300)

    elif val == "Normal":
        renderer_text.set_property("foreground", "white")
        renderer_text.set_property("weight", 400)

    elif val == "Important":
        renderer_text.set_property("foreground", "orange")
        renderer_text.set_property("weight", 600)

    elif val == "Urgent":
        renderer_text.set_property("foreground", "red")
        renderer_text.set_property("weight", 700)


# Required to keep the task list up-to-date
def onEntryRefilter():
    taskListFilter = builder.get_object("taskListFilter")
    taskListFilter.refilter()

# When the checkbox on a task is clicked, this function is called.
def onTreeViewToggled(cell, path, taskListStore, *ignore):
    # Get current row of where checkbox was clicked.
    row = taskListStore.get_iter(path)

    # Get objects.
    taskListStore = builder.get_object("taskListStore")
    taskTreeView = builder.get_object("taskTreeView")

    # Remove "Completed" task.
    taskListStore.remove(row)

    # Update task list.
    taskTreeView.show_all()

# Render the main list of tasks.
def renderTreeView():
    # Get all objects necessary.
    searchEntry = builder.get_object("searchEntry")
    taskTreeView = builder.get_object("taskTreeView")
    taskListStore = builder.get_object("taskListStore")

    # Set the search entry for the treeView, so text entered in the search bar
    # is handled.
    taskTreeView.set_search_entry(searchEntry)

    # Set the function to sort and filter rows. GTK calls this function for
    # each row, no for loop required.
    taskListFilter = builder.get_object("taskListFilter")
    taskListFilter.set_visible_func(matchFunc)

    # Specify the titles of each column
    names = ('Completed', 'Task', 'Description', 'Due Date', 'Task priority')

    # Range from index 0 to 0
    for i in range(1):
        # Create a new checkbox
        toggle = Gtk.CellRendererToggle()
        # Make the checkbox clickable
        toggle.set_activatable(True)
        # Connect the checkbox to the onTreeViewToggled handler
        toggle.connect("toggled", onTreeViewToggled, taskListStore)
        # Add this as a column
        column = Gtk.TreeViewColumn(names[i], toggle)
        taskTreeView.append_column(column)

    # Range from index 1 to 4
    for i in range(1, 4):
        # Create a new CellRendererText object
        renderer_text = Gtk.CellRendererText()

        # Code reads input fields and appropriately populates read-only field.
        # Requirement in rubric.
        renderer_text.set_property("editable", False)

        # Add it as a new column
        column = Gtk.TreeViewColumn(names[i], renderer_text, text=i)
        taskTreeView.append_column(column)

    # Range from index 5 to 5
    for i in range(4, 5):
        # Create a new CellRendererText object
        renderer_text = Gtk.CellRendererText()

        # Allow text to be formatted
        renderer_text.set_property("weight_set", True)
        renderer_text.set_property("foreground_set", True)

        # Add it as a new column
        column = Gtk.TreeViewColumn(names[i], renderer_text, text=i)
        column.set_cell_data_func(renderer_text, formatFunc)
        taskTreeView.append_column(column)

# --- MAIN HANDLER CLASS ---
# This class manages every single interaction with the UI buttons
class Handler:
    # Handle the close button being pushed.
    def onDestroy(self, *args):
        # Close the application.
        Gtk.main_quit()

    # When the button with the three lines is pressed.
    def onMenuBtnClicked(self, button):
        # Get aboutDialog and display it to the user
        aboutDialog = builder.get_object("aboutDialog")
        aboutDialog.show_all()

    # When the "close" button is pushed in the about dialog.
    def onAboutCloseBtnClicked(self, button):
        aboutDialog = builder.get_object("aboutDialog")
        aboutDialog.hide()

    # The search button on the main window is toggled.
    def onSearchBtnToggled(self, button):
        # Show or hide searchbar depending on state
        toggleState = button.get_active()
        searchBar = builder.get_object("searchBar")
        searchBar.set_search_mode(toggleState)

    # When the plus icon is pressed in the main window.
    def onAddBtnClicked(self, button):
        # Display the add task dialog
        addDialog = builder.get_object("addDialog")
        addDialog.show_all()

    # In the add task dialog, "Today" button is pressed.
    def onTodayBtnClicked(self, button):
        # Get date in YYYY-MM-DD format.
        dateEntry = builder.get_object("dateEntry")
        today = datetime.today().strftime('%Y-%m-%d')

        # Set it to the date entry field.
        dateEntry.set_text(today)

    # In the add task dialog, "Cancel" button is pressed.
    def onCancelTaskBtnClicked(self, button):
        # Close the add task dialog
        addDialog = builder.get_object("addDialog")
        addDialog.hide()

    # In the add task dialog, "Add" button is pressed.
    def onAddTaskBtnClicked(self, button):
        # Used to prevent "UnboundLocalError: local variable 'taskPriority'
        # referenced before assignment" error
        global taskPriority

        # Get all required objects for this function:
        addDialog = builder.get_object("addDialog")
        dateEntry = builder.get_object("dateEntry")
        nameEntry = builder.get_object("nameEntry")
        descriptionEntry = builder.get_object("descriptionEntry")
        taskListStore = builder.get_object("taskListStore")
        taskTreeView = builder.get_object("taskTreeView")

        # Get user entries and place them in variables
        taskDate = dateEntry.get_text()
        taskName = nameEntry.get_text()
        taskDescription = descriptionEntry.get_text()

        # Convert priority numbers into text that can be displayed to the user.
        if taskPriority == 0:
            priorityText = "Unspecified"

        elif taskPriority == 1:
            priorityText = "Normal"

        elif taskPriority == 2:
            priorityText = "Important"

        elif taskPriority == 3:
            priorityText = "Urgent"

        # Add this in the list of tasks, stored in a Gtk.ListStore object,
        # which is displayed in Gtk.TreeView object.
        # Names are the following:
        # 'Completed', 'Task', 'Description', 'Due Date', 'Task priority'

        taskListStore.append([Gtk.CellRendererToggle(), taskName, taskDescription, taskDate, priorityText])

        # Required to keep the task list up-to-date
        taskTreeView.show_all()

        # Close the add task dialog
        addDialog.hide()

        # Reset taskPriority back to zero, as this task has already been added.
        taskPriority = 0

    # When the "Open" tasks button in the main window is pressed:
    def onOpenBtnToggled(self, button):
        # Get required objects for this function.
        toggleState = button.get_active()
        closedBtn = builder.get_object("closedBtn")

        # Set other button to opposite state, so only one button is selected
        # at a time.
        if toggleState == False:
            closedBtn.set_active(True)
        elif toggleState == True:
            closedBtn.set_active(False)

    # When the "Closed" tasks button in the main window is pressed:
    def onClosedBtnToggled(self, button):
        # Get required objects for this function.
        toggleState = button.get_active()
        openBtn = builder.get_object("openBtn")

        # Set other button to opposite state, so only one button is selected
        # at a time
        if toggleState == False:
            openBtn.set_active(True)
        elif toggleState == True:
            openBtn.set_active(False)

    # Required to keep task list up-to-date
    def onSearchEntryChanged(self, entry):
        onEntryRefilter()

    # Set the priority buttons in the add task dialog to set taskPriorty
    # 0: Not specified
    # 1: Normal priority
    # 2: Important priority
    # 3: Urgent priority

    def onPriorityBtn1Clicked(self, button):
        # Used to prevent "UnboundLocalError: local variable 'taskPriority'
        # referenced before assignment" error
        global taskPriority

        # Set the taskPriority to be later added in the ListStore field.
        taskPriority = 1

    def onPriorityBtn2Clicked(self, button):
        # Used to prevent "UnboundLocalError: local variable 'taskPriority'
        # referenced before assignment" error
        global taskPriority

        # Set the taskPriority to be later added in the ListStore field.
        taskPriority = 2

    def onPriorityBtn3Clicked(self, button):
        # Used to prevent "UnboundLocalError: local variable 'taskPriority'
        # referenced before assignment" error
        global taskPriority

        # Set the taskPriority to be later added in the ListStore field.
        taskPriority = 3


# Load UI elements from a file. Program "Glade" used to design program.
builder = Gtk.Builder()
builder.add_from_file("todo.ui")

# Connect buttons to emit signals when pushed, handled by the Handler class
builder.connect_signals(Handler())

# Get the window object
window = builder.get_object("MainWindow")

# Display the window object
window.show_all()

# Once the window is shown, the lists of tasks are called here to be rendered.
renderTreeView()

# Begin the main GTK loop.
Gtk.main()
