conn = sqlite3.connect('users.db')
c = conn.cursor()

#uses built-in hashlib library to generate hash for password for storage in database
def make_pw_hash(password):
	return str(hashlib.sha256(str.encode(password)).hexdigest())

# Create table
try:
	c.execute('''CREATE TABLE users
		     (username text, password text, isAdmin integer)''')

	# Insert a row of data
	c.execute("INSERT INTO users VALUES ('a','{}',1)".format(make_pw_hash("myPassw0rd")))
	c.execute("INSERT INTO users VALUES ('b','{}',0)".format(make_pw_hash("hello123")))
except:
	print("Table already created")

adminList = ["a"]

# Save (commit) the changes
conn.commit()
conn.close

