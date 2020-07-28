import os
import tkinter as tk
from tkinter import ttk, messagebox 
from tkinter.filedialog import askopenfilename,asksaveasfilename

MAX_SIZE = (1980, 1080)
MIN_SIZE = (640, 400)


class TextEditor():
    

    def __init__(self, win_title = 'EditIT'):
        #Create the window
        self.root = tk.Tk()             
        self.root.title('EditIT')
        self.root.iconbitmap('icon.ico')
        self.root.maxsize(*MAX_SIZE)   #set the max size using tuple unpacking
        self.root.minsize(*MIN_SIZE)     #set the min size
        self.root.option_add('*tearOff', False)   #through option you can change behavior of win (read docs on every option)

        self.text_contents = dict() #dict populated with the elem that are contents of the notebook

        self.main = ttk.Frame(self.root)
        self.main.pack(fill = 'both', expand = True , padx = 5, pady = (5, 5) )

        self.notebook = ttk.Notebook(self.main)                     
        self.notebook.pack(fill = 'both' , expand = True )
    
        
    def createFile (self, content="", title='Untitled' ):
        self.container = ttk.Frame(self.notebook)
        self.container.pack()

        text_area = tk.Text(self.container)                           #create the text area
        text_area.insert('end', content)                              #insert text content to notebook
        text_area.pack(side = 'left' ,fill = 'both', expand = True)    

        self.notebook.add(self.container, text = title)               #add the text area to the notebook
        self.notebook.select(self.container)                          #select the created text area

        self.text_contents[str(text_area)] = hash(content)            #evertime we create a file, we add in the dict one hash element
        
        #Create the scroll bar
        text_scroll = ttk.Scrollbar(self.container, orient = 'vertical', command = text_area.yview)
        text_scroll.pack(side = 'right', fill = 'y')
        text_area['yscrollcommand'] = text_scroll.set

    def save_file(self):
        #ask the user where to save the file
        file_path = asksaveasfilename()
        try:
            filename = os.path.basename(file_path)                  #get the name of the file
            text_widget = self.get_text_widget
            content = text_widget.get('1.0', 'end-1c')              #get the text of the widget from the 1 line, character 0 to the end, excluding the last character which is already there
            
            with open(file_path, 'w') as file:
                file.write(content)
        except (AttributeError , FileNotFoundError):
            print('Save operation cancelled')
            return

        self.notebook.tab('current', text = filename)        #change the current name of the notebook tab to the saved one
        self.text_contents[str(text_widget)] = hash(content)


    def open_file(self):
        #ask the user for the file path
        file_path = askopenfilename()
        try:
            filename = os.path.basename(file_path) #get the name of the file
                    
            with open(file_path, 'r') as file:
                content = file.read()
        
        except (AttributeError , FileNotFoundError):
            print('Open operation cancelled')
            return

        self.createFile(content, filename)

    @property
    def confirm_quit(self):
        unsaved = False
        for tab in self.notebook.tabs():
            tab_widget = self.root.nametowidget(tab)
            text_widget = tab_widget.winfo_children()[0]           #gets the text area not the scroll bar
            content = text_widget.get('1.0', 'end-1c')

            if hash(content) != self.text_contents[str(text_widget)]:
                unsaved = True
                break
        
        if unsaved and not self.confirm_close:
                return
        
        self.root.destroy()

    @property
    def close_current_tab(self):
        current = self.notebook.select()
        if not self.confirm_close:
            return    
        self.notebook.forget(current)

        if len(self.notebook.tabs()) == 0:
            self.createFile()

    @property
    def current_tab_unsaved(self):
        text_widget = self.get_text_widget
        content = text_widget.get('1.0', 'end-1c')
        return hash(content) != self.text_contents[str(text_widget)]

    @property
    def confirm_close(self):
        return messagebox.askyesno(
            message = 'You have unsaved changes. Are you sure you want to close ?',
            icon = 'question',
            title ='Unsaved Changes'
        )

    @property 
    def show_about_info(self):
        messagebox.showinfo(
            title = 'About',
            message = 'This is a text editor created to learn Tkinter'
        )

    @property
    def check_for_changes(self):
        '''
        If there is any difference between the content in\n
        text_content and this display an asterix
        '''
        current = self.get_text_widget                          #get the name of the notebook
        content = current.get('1.0', 'end-1c')                  #get the content of the selected notebook
        name = self.notebook.tab('current')['text']             #get the name

        if hash(content) != self.text_contents[str(current)]:            
            if name[-1] != '*':
                self.notebook.tab('current', text = name + '*' )
        elif name[-1] == '*':
            self.notebook.tab('current', text = name[:-1] )

    @property
    def get_text_widget(self):
        name = self.notebook.select()
        current_tab = self.notebook.nametowidget(name)        #get the name of the currently selected widget    
        extra = current_tab.winfo_children()[0]
        #text_widget = extra.tab('text')                      #gets the text area not the scroll bar
        return extra


    @property
    def drop_menu(self):
        self.menubar = tk.Menu()                 #create the menu obj
        self.root.config(menu = self.menubar)    #add the menu to the root parent

        self.file_menu = tk.Menu(self.menubar)        #create an child of menubar that will be a dropdown menu
        help_menu = tk.Menu(self.menubar)
        self.menubar.add_cascade( menu = self.file_menu, label = 'File')          #create the File dropdown
        self.menubar.add_cascade( menu = help_menu, label = 'Help')

        self.file_menu.add_command(label = 'New', command = self.createFile, accelerator = 'Ctrl+N')
        self.file_menu.add_command(label = 'Open File', command = self.open_file, accelerator = 'Ctrl+O')
        self.file_menu.add_command(label = 'Save File', command = self.save_file,  accelerator = 'Ctrl+S')
        self.file_menu.add_command(label = 'Close Tab', command = self.close_current_tab,  accelerator = 'Ctrl+Q')
        self.file_menu.add_command(label = 'Exit', command = self.confirm_quit)

        help_menu.add_command(label = 'About', command = self.show_about_info)

        #bind func to key press
        self.root.bind('<KeyPress>', lambda event: self.check_for_changes)
        self.root.bind('<Control-n>', lambda event: self.createFile())
        self.root.bind('<Control-o>', lambda event: self.open_file())
        self.root.bind('<Control-s>', lambda event: self.save_file())
        self.root.bind('<Control-q>', lambda event: self.close_current_tab)


#run the app individually

if __name__ == "__main__":
    editor = TextEditor()
    editor.drop_menu
    editor.createFile()

    editor.root.mainloop()