from base64 import encode
import sqlite3
import os, sys
from tqdm import tqdm
from tabulate import tabulate
# from password_generator import password
# from encode_password import encrypt_me
from drive_api import *

con = sqlite3.connect("password.db")
cur = con.cursor()

class PasswordManager:
	def __init__(self):
		super().__init__()
		pass

	# Base Function
	def choose_option(self):
		print("\n")
		print("-----------+MENU+-------------")
		headers = [["1. Add New Item"], 
					["2. Delete An Id"], 
					["3. Update An Id"], 
					["4. View All Your Password"], 
					["5. Find A User"],
					["6. Upload In Drive"],
					["7. Exit"]]
		print(tabulate(headers, tablefmt="grid"))
		print("------------------------------")
		print("\n")
		option = int(input("Choose An Option : "))
		if option == 1:
			self.add = self.create_table()
		elif option == 2:
			self.delete = self.delete_task()
		elif option == 3:
			self.update = self.update_task()
		elif option == 4:
			self.retrive = self.fetch_all_data()
		elif option == 5:
			self.search = self.search_from_db()
		elif option == 6:
			self.exit = self.upload_db()
		elif option == 7:
			self.exit = self.exit_from_db()

		if option > 7 or option < 1:
			print(f"Choose Right Option")
			self.choose_option()

	@staticmethod
	def protection_for_database():
		directory = os.path.join(os.getcwd(), "password")
		if not os.path.exists(directory):
			directory_file = os.mkdir(os.path.join(os.getcwd(), "password"))
			directory_loacation = os.path.join(os.getcwd() + "//password")
			if not os.path.isfile(os.path.join(directory_loacation + "password.txt")):
				generated_password = password()
				with open(os.path.join(directory_loacation + "/password.txt"), "w") as file:
					file.write(f"{generated_password}")
			else:
				pass
		return directory


	def create_table(self):
		try:
			_ = self.protection_for_database()				
			cur.execute("CREATE TABLE IF NOT EXISTS password (id INTEGER PRIMARY KEY AUTOINCREMENT, website_name TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL)")
			website_name = input("ENTER WEBSITE NAME: ")
			email = input("ENTER EMAIL ADDRESS: ")
			password = input("YOUR PASSWORD: ")
			# byte_pass = bytes(password, 'utf-8')
			# encoded_pass = encrypt_me(byte_pass)
			datas = [
				(website_name, email, password),
			]
			cur.executemany("INSERT INTO password(website_name, email, password) VALUES (?, ?, ?)", datas)
			con.commit()
			print("Want To Add More?")
			yes_or_no = input("Type Y/y for YES/yes, If no press any key: ")
			if yes_or_no == "Y" or yes_or_no == "y":
				self.create_table()
			else:
				self.choose_option()
			
		except Exception as e:
			print(e)


	def delete_task(self):
		data = []
		cur = con.cursor()
		headers = ["id", "Domain", "Email"]
		for row in cur.execute('SELECT * FROM password'):
			data.append([row[0], row[1], row[2]])
		print(tabulate(data, headers, tablefmt="github"))
		id_ = [row[0] for row in cur.execute('SELECT * FROM password')]
		input_id = int(input("Enter A Delete Id: "))
		id = input_id
		if id in id_:
			cur.execute("DELETE FROM password WHERE id=?", (id,))
			con.commit()

			main_menu = input("Enter B to Back Main Menu OR enter any key: ")
			print("\n")
			if main_menu == "B" or main_menu == "b":
				self.choose_option()
			else:
				self.delete_task()
		else:
			if len(id_) == 0:
				print("Database Cleaned. Add Something First")
				self.choose_option()
			print("No Match Found")
		self.delete_task()

	def update_task(self):
		self.fetch_for_update()
		cur = con.cursor()
		id = int(input("Enter Id No.: "))
		website_name = input("Enter Web Domain Name: ")
		email = input("Enter Email: ")
		password = input("Enter Password: ")
		cur.execute("UPDATE password SET website_name=?, email=?, password=? where id=?", (website_name, email, password, id,))
		con.commit()
		self.choose_option()


	def search_from_db(self):
		cur = con.cursor()
		email = input("Enter email: ")
		cur.execute("SELECT * FROM password where email=?", (email,))
		records = cur.fetchmany(5)
		headers = ["Domain", "Email", "Password"]
		data = []
		for record in records:
			data.append([record[1], record[2], record[3]])
		print("\n")
		print(tabulate(data, headers, tablefmt="github"))
		self.choose_option()

	def exit_from_db(self):
		print("Bye Bye")
		return sys.exit()


	@staticmethod
	def fetch_for_update():
		data = []
		headers = ["id", "Domain", "Email"]
		for row in cur.execute('SELECT * FROM password'):
			data.append([row[0], row[1], row[2]])
		print(tabulate(data, headers, tablefmt="github"))

	def master_password(self):
		directory_loacation = self.protection_for_database()
		password_db = input("Enter Your Database Password: ")
		with open(os.path.join(directory_loacation + "/password.txt"), "r") as file:
			if password_db == file.read():
				print("\n")
				print("Password Match")
			else:
				print("\n")
				print("Password Not Matched")
				self.choose_option()

	def fetch_all_data(self):
		# database fetch using password..
		self.master_password()
		data = []
		headers = ["id", "Domain", "Email", "Password"]
		for row in cur.execute('SELECT * FROM password'):
			data.append([row[0], row[1], row[2], row[3]])
		print(tabulate(data, headers, tablefmt="github"))
		self.choose_option()

	def upload_file(self):
		filepath = os.getcwd()
		db_path = os.path.join(filepath, "password.db")
		db_file = DriveAPI().FileUpload(filepath=db_path)
		return db_file

	def upload_db(self):
		print("Create A New Folder Or Not?")
		agree = input("Enter C/c to Create\nOr Enter Any Key To Not Create: ")
		if agree == "C" or agree == "c":
			folder = input("Enter Folder Name||Try A Unique Name: ")
			driver = DriveAPI().createRemoteFolder(folderName=folder)
			print("Connecting...")
			print(f"{folder} Folder Created In Your Drive")
		else:
			print("Upload Your Database")
			print(self.upload_file())

if __name__ == "__main__":
	new = PasswordManager()
	new.choose_option()