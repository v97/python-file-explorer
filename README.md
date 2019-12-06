====== Python / Tkinter File Explorer ======

To run: pip install any modules necessary, then run "python explorer.py" in the containing directory.

Login with username and password. There are two accounts.

Admin account: a / myPassw0rd
Non-admin account: b / hello123

These accounts are added to a SQLite3 database through a db.py script. Hashing is used for protection.

Non-admin users are presented with a file explorer. By clicking on filenames on the left pane, they may view different file contents on the right pane. There is also a drop-down menu through which they can logout or exit the application.

Admin users have additional options available to them in the menu . They may:

  1) Create a new file in the working directory, and specify its name
  2) Save, after editing the text contents of a file
  3) Rename a file
  4) Delete a file
  
So far, tested in Ubuntu 18.04 with Python 3.7
