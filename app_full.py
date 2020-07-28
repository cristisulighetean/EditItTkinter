import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename,asksaveasfilename


text_contents = dict()                                  #create a dict that will be populated with elements that are the contents of notebooks


def createFile (content="", title='Untitled' ):

    container = ttk.Frame(notebook)
    container.pack()

    text_area = tk.Text(container)                           #create the text area
    text_area.insert('end', content)                    #insert text content to notebook
    text_area.pack(side = 'left' ,fill = 'both', expand = True)    

    notebook.add(container, text = title)               #add the text area to the notebook
    notebook.select(container)                          #select the created text area

    text_contents[str(text_area)] = hash(content)            #evertime we create a file, we add in the dict one hash element
    
    text_scroll = ttk.Scrollbar(container, orient = 'vertical', command = text_area.yview)
    text_scroll.pack(side = 'right', fill = 'y')
    text_area['yscrollcommand'] = text_scroll.set

def check_for_changes():
    current = get_text_widget()
    content = current.get('1.0', 'end-1c')
    name = notebook.tab('current')['text']

    if hash(content) != text_contents[str(current)]:
        if name[-1] != '*':
            notebook.tab('current', text = name + '*' )
    elif name[-1] == '*':
        notebook.tab('current', text = name[:-1] )



def save_file():
    #ask the user where to save the file
    file_path = asksaveasfilename()
    try:
        filename = os.path.basename(file_path)                  #get the name of the file
        text_widget = get_text_widget()
        content = text_widget.get('1.0', 'end-1c')              #get the text of the widget from the 1 line, character 0 to the end, excluding the last character which is already there
        
        with open(file_path, 'w') as file:
            file.write(content)
    except (AttributeError , FileNotFoundError):
        print('Save operation cancelled')
        return

    notebook.tab('current', text = filename)        #change the current name of the notebook tab to the saved one
    text_contents[str(text_widget)] = hash(content)

def open_file():
    #ask the user for the file path
    file_path = askopenfilename()
    try:
        filename = os.path.basename(file_path) #get the name of the file
                
        with open(file_path, 'r') as file:
            content = file.read()
    except (AttributeError , FileNotFoundError):
        print('Open operation cancelled')
        return

    createFile(content, filename)

def confirm_quit():
    unsaved = False
    for tab in notebook.tabs():
        tab_widget = root.nametowidget(tab)
        text_widget = tab_widget.winfo_children()[0]           #gets the text area not the scroll bar
        content = text_widget.get('1.0', 'end-1c')

        if hash(content) != text_contents[str(text_widget)]:
            unsaved = True
            break
    
    if unsaved and not confirm_close():
            return
    
    root.destroy()

def get_text_widget():
    current_tab = notebook.nametowidget(notebook.select())      #get the name of the currently selected widget    
    print(current_tab)
    text_widget = current_tab.winfo_children()[0]               #gets the text area not the scroll bar
    print(text_widget)
    return text_widget


def close_current_tab():
    current = notebook.select()                                 #get current tab
    if current_tab_unsaved() and not confirm_close():
        pass     
    notebook.forget(current)

    if len(notebook.tabs()) == 0:
        createFile()

def current_tab_unsaved():
    text_widget = get_text_widget()
    print(text_widget)
    content = text_widget.get('1.0', 'end-1c')
    return hash(content) != text_contents[str(text_widget)]

def confirm_close():
    return messagebox.askyesno(
        message = 'You have unsaved changes. Are you sure you want to close ?',
        icon = 'question',
        title ='Unsaved Changes'
    )
def show_about_info():
    messagebox.showinfo(
        title = 'About',
        message = 'This is a text editor created to learn Tkinter'
    )



root = tk.Tk()
root.title('Text Editor')
root.option_add('*tearOff', False)   #through option you can change behavior of win (read docs on every option) 


menubar = tk.Menu()                 #create the menu obj
root.config(menu = menubar)

file_menu = tk.Menu(menubar)        #create an child of menubar that will be a dropdown menu
help_menu = tk.Menu(menubar)
menubar.add_cascade( menu = file_menu, label = 'File')          #create the File dropdown
menubar.add_cascade( menu = help_menu, label = 'Help')

file_menu.add_command(label = 'New', command = createFile, accelerator = 'Ctrl+N')
file_menu.add_command(label = 'Open File', command = open_file, accelerator = 'Ctrl+O')
file_menu.add_command(label = 'Save File', command = save_file,  accelerator = 'Ctrl+S')
file_menu.add_command(label = 'Close Tab', command = close_current_tab,  accelerator = 'Ctrl+Q')
file_menu.add_command(label = 'Exit', command = confirm_quit)

help_menu.add_command(label = 'About', command = show_about_info)


main = ttk.Frame (root)
main.pack(fill = 'both', expand = True , padx = 5, pady = (5, 5) )      #create the main frame

notebook = ttk.Notebook(main)                       #create the notebook
notebook.pack(fill = 'both' , expand = True )

createFile()


#bind the func to key presses
root.bind('<KeyPress>', lambda event: check_for_changes())
root.bind('<Control-n>', lambda event: createFile())
root.bind('<Control-o>', lambda event: open_file())
root.bind('<Control-s>', lambda event: save_file())
root.bind('<Control-q>', lambda event: close_current_tab())


root.mainloop()