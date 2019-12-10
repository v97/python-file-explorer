from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
#from functions import *
import shutil         
import os
import unicodedata
from django.utils.text import get_valid_filename
import hashlib
import sqlite3
    
root = Tk()

clipBoard = None

fileListBox = None
textArea = None

curPathText = StringVar()
curPathText.set(os.getcwd())

conn = sqlite3.connect('users.db')
c = conn.cursor()

adminList = ["a"]
	
#for clearing the window
def all_children (window) :
	_list = window.winfo_children()
	for item in _list:
		if item.winfo_children():
			_list.extend(item.winfo_children())
	return _list

#uses built-in hashlib library to generate hash for password for storage in database
def make_pw_hash(password):
	return str(hashlib.sha256(str.encode(password)).hexdigest())

#authenticates user according to information from database
def check_pw_hash(password, user): #user object === (username, password, isAdmin)
	if(make_pw_hash(password) == user[1]):
		return True
	return False

def clear_root():
	widgets = all_children(root)
	for widget in widgets:
		widget.pack_forget() #clear all widgets from window

def clear_credentials():
	username = ""
	password = ""

def isAdmin(username): #checks whether user is allowed to edit files
	c.execute("SELECT * FROM users WHERE username='{}'".format(username))
	arr = c.fetchall()

	if(len(arr) > 0):
		isAdminVal = arr[0][2]
		return isAdminVal == 1 #using integer as boolean

	return False

def login_verification(username,input_pwd):
	global users

	c.execute("SELECT * FROM users WHERE username='{}'".format(username))
	arr = c.fetchall()

	if(len(arr) > 0):
		if(check_pw_hash(input_pwd, arr[0])):
			file_mgr(username)
		else:
			messagebox.showerror("Failed login","Incorrect credentials")
	else:
		messagebox.showerror("Failed login","User doesn't exist")

def newFile(parent):
	name = get_valid_filename(simpledialog.askstring("Input", "Please enter the file name:",
                                parent=parent))
	if(name is None):
		return	
	print("New file", name)
	f = open(name,"w+")
	f.write("")
	f.close()
	reloadFiles(name)

def newFolder(parent):
	name = get_valid_filename(simpledialog.askstring("Input", "Please enter the file name:",
                                parent=parent))
	if not os.path.exists(name):
		os.makedirs(name)

def renameSelectedFile(parent):
	fileName = curPathText.get() + "\\" + fileListBox.get(fileListBox.curselection())
	in_ = get_valid_filename(simpledialog.askstring("Input", "Please enter the new file name:", parent=parent))
	if(in_ is None):
		return
	newName = curPathText.get() + "\\" + in_
	os.rename(fileName, newName)
	reloadFiles(newName)

def saveSelectedFile():
	print("Save file")
	try:
		fileName = fileListBox.get(fileListBox.curselection())
		fullFileName = curPathText.get() + "\\" + fileName
		f = open(fullFileName,"w+")
		f.write(textArea.get("1.0",END))
		f.close()
		messagebox.showinfo("Information","Saved " + fileName + " successfully!")
	except:
		messagebox.showinfo("Information", "Make a new file before saving, or select existing file")

def deleteSelectedFile():
	fileName = fileListBox.get(fileListBox.curselection())
	confirmDelete = messagebox.askokcancel("Question","Really delete " + fileName + "?")
	if(confirmDelete):
		os.remove(curPathText.get() + "\\" + fileName)
		print(fileName, "deleted")
		reloadFiles(0)

def enterFolder():
	global curPathText
	try:
		folderName = fileListBox.get(fileListBox.curselection())
		newPath = curPathText.get() + "\\" + folderName
		if(os.path.isdir(newPath)):
			curPathText.set(newPath)
			reloadFiles()
		else:
			messagebox.showinfo("Error", folderName + " is not a folder")
	except:
		messagebox.showinfo("Error", "Unable to enter folder")

def upward():
	curPathText.set(('\\').join(curPathText.get().split("\\")[:-1]))
	reloadFiles()

def copy():
	global clipBoard
	global transferMode
	clipBoard = curPathText.get() + "\\" + fileListBox.get(fileListBox.curselection())
	transferMode = "copy"
	print("Copied", clipBoard)

def cut():
	global clipBoard
	global transferMode
	clipBoard = curPathText.get() + "\\" + fileListBox.get(fileListBox.curselection())
	transferMode = "cut"
	print("Cut", clipBoard)

def paste():
	global clipBoard
	global transferMode
	fileName = clipBoard.split("\\")[-1]
	print("y", fileName)
	try:
		if(transferMode == "copy"):
			[fileName, fileType] = fileName.split(".")
			fileName = fileName + "_copy." + fileType
	except:
		pass
	destination = curPathText.get() + "\\" + fileName
	print("Pasting", clipBoard, "to", destination)
	if(transferMode == "cut"):
		shutil.move(clipBoard, destination)
		notif = "Moving"
	elif(transferMode == "copy"):
		shutil.copyfile(clipBoard, destination)
		notif = "Copying"
	messagebox.showinfo("Paste", notif + " " + clipBoard + " to " + destination)
	reloadFiles()

#load the menu bar
def menu_bar(root, isAdmin):
	menuBar = Menu(root)
	fileMenu = Menu(menuBar, tearoff=0)
	navMenu = Menu(menuBar, tearoff=0)

	if(isAdmin):
		fileMenu.add_command(label="New file", command=lambda: newFile(root))
		fileMenu.add_command(label="New folder", command=lambda: newFolder(root))
		fileMenu.add_command(label="Rename", command=lambda: renameSelectedFile(root))	
		
	fileMenu.add_command(label="Copy", command=copy)
		
	if(isAdmin):
		fileMenu.add_command(label="Cut", command=cut)
	
	fileMenu.add_command(label="Paste", command=paste)
		
	if(isAdmin):	
		fileMenu.add_command(label="Save", command=saveSelectedFile)
		fileMenu.add_command(label="Delete", command=deleteSelectedFile)
	
	fileMenu.add_separator()
	fileMenu.add_command(label="Logout", command=login)
	fileMenu.add_command(label="Exit", command=root.quit)

	navMenu.add_command(label="Reload", command=reloadFiles)
	navMenu.add_command(label="Enter", command=enterFolder)
	navMenu.add_command(label="Up", command=upward)

	menuBar.add_cascade(label="Menu", menu=fileMenu)
	menuBar.add_cascade(label="Nav", menu=navMenu)
	root.config(menu=menuBar)

#populates file listbox with files in directory
def reloadFiles(fileToSelect = None):
	fileListBox.delete(0,END)
	flist = os.listdir(curPathText.get())
	selectionInd = 0
	added = 0
	for ind, item in enumerate(flist):
		if(item in ["explorer.py", "db.py", "users.db"]): #this software!
			#or
			#os.path.isdir(item)): #is a folder
			continue #skip items
		if(not (fileToSelect is None)):
			if(fileToSelect == item):
				selectionInd = added
		fileListBox.insert(END, item)
		added += 1
	fileListBox.selection_set(selectionInd)
	print("Selecting", selectionInd)

#when user selects a file, show it in the text-editor
def onSelect(evt):
	w = evt.widget
	index = int(w.curselection()[0])
	fileName = w.get(index)
	fullFileName = curPathText.get() + "\\" + fileName
	print('You selected item %d: "%s"' % (index, fullFileName))
	if(os.path.exists(fullFileName) and os.path.isdir(fullFileName)):
		content = "Contents of " + fileName + ":\n\n" + str('\n'.join(os.listdir(fullFileName)))
	#update text area
	else:
		with open(fullFileName) as f:
			content = f.readlines()
	textArea.delete('1.0', END)
	textArea.insert(END, content)
		
#main file explorer window
def file_mgr(username):
	clear_root()
	
	global fileListBox #lists files
	global textArea #text editor for edits
	
	file_mgr = root
	file_mgr.title("Files for " + username)
	file_mgr.geometry("800x500")
	
	Label(file_mgr, text="Welcome to file manager, " + username).pack()
	curPathLabel = Label(file_mgr, textvariable=curPathText)
	curPathLabel.pack()

	m = PanedWindow(file_mgr,orient="horizontal")
	m.pack(fill=BOTH, expand=1)
	
	fileListBox = Listbox(m, name='fileListBox')
	fileListBox.bind('<<ListboxSelect>>', onSelect)	
	reloadFiles() #populate

	m.add(fileListBox)

	textArea = Text(file_mgr, font=("ubuntu", 12))
	scroll = Scrollbar(textArea, command=textArea.yview)
	scroll.pack(side=RIGHT, fill=Y)
	textArea.configure(yscrollcommand=scroll.set)
	if(not isAdmin(username)):	
		textArea.bind("<Key>", lambda e: "break") #make text window read-only

	m.add(textArea)

	menu_bar(file_mgr, isAdmin(username))

#login window
def login():
	clear_root()
	clear_credentials()	
	
	login_screen = root
	login_screen.title("Login")
	login_screen.geometry("300x250")
	Label(login_screen, text="Please enter credentials below to login").pack()
	Label(login_screen, text="").pack()
 
	username_verify = StringVar()
	password_verify = StringVar()

	Label(login_screen, text="Username * ").pack()
	username_login_entry = Entry(login_screen, textvariable=username_verify)
	username_login_entry.pack()
	Label(login_screen, text="").pack()
	Label(login_screen, text="Password * ").pack()
	password__login_entry = Entry(login_screen, textvariable=password_verify, show= '*') #password field hides characters
	password__login_entry.pack()
	Label(login_screen, text="").pack()
	
	Button(login_screen, text="Login", width=10, height=1, command=lambda: login_verification(username_verify.get(),password_verify.get())).pack()

if(__name__ == "__main__"):
	login()
	root.mainloop()
	conn.close()
