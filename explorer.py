from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
#from functions import *
import shutil         
import os
    
root = Tk()

fileListBox = None
textArea = None

def isValidFileName(fileName):
	return True

def login_verification(username,password,login_window):
	users = {"a":"myponyisnice", "b":"hello123"}
	if(username in users):
		if(users[username] == password):
			print("Logging in")
			login_window.destroy()
			file_mgr(username)
		else:
			print("Incorrect password")
	else:
		print("User not found")

def newFile(parent):
	name = simpledialog.askstring("Input", "Please enter the file name:",
                                parent=parent)
	if(name is None or (not isValidFileName(name))):
		return	
	print("New filew", name)
	f = open(name,"w+")
	f.write("")
	f.close()
	addFiles(name)

def renameSelectedFile(parent):
	fileName = fileListBox.get(fileListBox.curselection())
	newName = simpledialog.askstring("Input", "Please enter the new file name:",
                                parent=parent)
	if(newName is None or (not isValidFileName(newName))):
		return
	os.rename(fileName, newName)
	addFiles(newName) 	
	print("Renamed", fileName, "to", newName)
	

def saveSelectedFile():
	print("Save file")

def deleteSelectedFile():
	fileName = fileListBox.get(fileListBox.curselection())
	confirmed = messagebox.askokcancel("Question","Really delete " + fileName + " ?")
	if(confirmed):
		os.remove(fileName)
		print(fileName, "deleted")
		addFiles(0)

def menu_bar(root):
	menuBar = Menu(root)
	fileMenu = Menu(menuBar, tearoff=0)

	fileMenu.add_command(label="New", command=lambda: newFile(root))	
	fileMenu.add_command(label="Rename", command=lambda: renameSelectedFile(root))
	fileMenu.add_command(label="Save", command=saveSelectedFile)
	fileMenu.add_command(label="Delete", command=deleteSelectedFile)
	fileMenu.add_separator()
	fileMenu.add_command(label="Exit", command=root.quit)
	menuBar.add_cascade(label="File", menu=fileMenu)
	root.config(menu=menuBar)

def addFiles(fileToSelect = None):
	fileListBox.delete(0,END)
	flist = os.listdir()
	selectionInd = 0
	added = 0
	for ind, item in enumerate(flist):
		if(item == "explorer.py" or os.path.isdir(item)):
			continue
		if(not (fileToSelect is None)):
			if(fileToSelect == item):
				selectionInd = added
		fileListBox.insert(END, item)
		added += 1
	fileListBox.selection_set(selectionInd)
	print("Selecting", selectionInd)

def onselect(evt):
	w = evt.widget
	index = int(w.curselection()[0])
	fileName = w.get(index)
	print('You selected item %d: "%s"' % (index, fileName))
	with open(fileName) as f:
		lines = f.readlines()
		textArea.delete('1.0', END)
		textArea.insert(END, lines)
		

def file_mgr(username):
	global fileListBox
	global textArea	
	
	file_mgr = Toplevel(root)

	file_mgr.title("Files for " + username)
	file_mgr.geometry("600x500")
	Label(file_mgr, text="Welcome to file mgr").pack()
	Label(file_mgr, text="").pack()

	m = PanedWindow(file_mgr,orient="horizontal")
	m.pack(fill=BOTH, expand=1)
	
	fileListBox = Listbox(m, name='fileListBox')
	fileListBox.bind('<<ListboxSelect>>', onselect)
	fileListBox.pack()
	
	addFiles()	

	m.add(fileListBox)

	textArea = Text(file_mgr, font=("ubuntu", 12))
	m.add(textArea)
	
	scroll = Scrollbar(file_mgr, command=textArea.yview)
	textArea.configure(yscrollcommand=scroll.set)
	textArea.pack(side=LEFT, fill=BOTH, expand=True)
	scroll.pack(side=RIGHT, fill=Y)
	menu_bar(file_mgr)
	
def login():
    login_screen = Toplevel(root)
    login_screen.title("Login")
    login_screen.geometry("300x250")
    Label(login_screen, text="Please enter details below to login").pack()
    Label(login_screen, text="").pack()
 
    global username_verify
    global password_verify
 
    username_verify = StringVar()
    password_verify = StringVar()
 
   
    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password__login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
    password__login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1,
    command=lambda: login_verification(username_verify.get(),password_verify.get(),login_screen)).pack()

file_mgr("user")

root.mainloop()

