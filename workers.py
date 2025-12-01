#cd OneDrive\Desktop\HomeWorks




import sqlite3


class Database:
	def __init__(self):
		with sqlite3.connect('Workers.db') as connection:
			cursor = connection.cursor()

			cursor.execute(""" CREATE TABLE IF NOT EXISTS Employee(
								Eid INTEGER PRIMARY KEY AUTOINCREMENT,
								fname TEXT NOT NULL,
								lname TEXT NOT NULL,
								age INTEGER NOT NULL,
								position INTEGER NOT NULL, 
								salary INTEGER NOT NULL,
								addressid INTEGER NOT NULL,
								FOREIGN KEY(position) REFERENCES Positions(Pid),
								FOREIGN KEY(addressid) REFERENCES Address(Aid)) """)



			cursor.execute(""" CREATE TABLE IF NOT EXISTS Positions(
								Pid INTEGER PRIMARY KEY AUTOINCREMENT,
								Pname TEXT NOT NULL) """)



			cursor.execute(""" CREATE TABLE IF NOT EXISTS Address(
								Aid INTEGER PRIMARY KEY AUTOINCREMENT,
								Country TEXT NOT NULL,
								City TEXT NOT NULL,
								Town TEXT NOT NULL) """)





	def add_address_db(self, address):
		with sqlite3.connect('Workers.db') as connection:
			cursor = connection.cursor()

			cursor.execute(""" INSERT INTO Address(Country, City, Town) VALUES (?,?,?) """, (address.country, address.city, address.town))
			
			connection.commit()

			print('\n\nAddress has been added')
			
			return cursor.lastrowid






	def view_all_addresses_db(self):
		with sqlite3.connect('Workers.db') as connection:
			cursor = connection.cursor()

			cursor.execute(""" SELECT * FROM Address """)

			addresses = cursor.fetchall()

			if not addresses:
				print('\n\nNo address found\n')
				return False
			else:
				print(f'\n{"^"*25} Addresses {"^"*25}\n')
				for address in addresses:
					print(f'\n\n\n  {"^"*25} ID: {address[0]} {"^"*25}\n\nCountry: {address[1]}\nCity: {address[2]}\nTown: {address[3]}\n\n{"^" * 59}')
				return True




	def get_addressID_db(self, column, value):  # getting address ID and its employees.

	    with sqlite3.connect('Workers.db') as connection:
	        cursor = connection.cursor()

	        cursor.execute(f"""SELECT Aid FROM Address WHERE LOWER({column}) = ? """, (value.lower(),))

	        addresses = cursor.fetchall()

	        if addresses:
	            found_any = False  

	            for address in addresses:
	                aid = address[0]

	                cursor.execute("SELECT Eid, fname, lname, age FROM Employee WHERE addressid = ?", (aid,))
	                employees = cursor.fetchall()

	                if employees:
	                    found_any = True  

	                    print(f"\n\n{'^'*19} Employees with {column} '{value}' {'^'*19}\n")
	                    for emp in employees:
	                        print(
	                            f'\n  {"^"*25} ID: {emp[0]} {"^"*25}\n'
	                            f' Name: {emp[1]}\n'
	                            f' Lname: {emp[2]}\n'
	                            f' Age: {emp[3]}\n'
	                            f'{"^"*61}\n'
	                        )

	            if not found_any:
	                print(f'\n\nNo employees are registered under the {column} "{value}".\n')

	        else:
	            print(f'\n\nNo address found with {column} "{value}".\n')





	def delete_address_db(self, aidchoice):
		with sqlite3.connect('Workers.db') as connection:
			cursor = connection.cursor()

			cursor.execute("DELETE FROM Address WHERE Aid = ?", (aidchoice,))

			connection.commit()

			print('\nAddress has been deleted.')






	def add_position_db(self,poss):
		with sqlite3.connect('Workers.db') as connection:
			cursor = connection.cursor()

			cursor.execute(""" INSERT INTO Positions(Pname) VALUES (?) """,(poss.Pname,))

			connection.commit()

			print('\n\nPosition has been added\n')


	def get_position_name(self, pid):
		with sqlite3.connect('Workers.db') as connection:
			cursor = connection.cursor()
			cursor.execute("SELECT Pname FROM Positions WHERE Pid = ?", (pid,))

			result = cursor.fetchone()

			if result:
				return result[0]
			else:
				return None


	def view_all_positions_db(self):
		with sqlite3.connect('Workers.db') as connection:
			cursor = connection.cursor()

			cursor.execute('SELECT * FROM Positions')

			positions = cursor.fetchall()

			if not positions:

				print('\n\nNo position found\n')
				return False

			else:
				print(f'\n{"^"*25} Positions {"^"*25}\n')

				for position in positions:

					print(f'\n\n\n  {"^"*25} ID: {position[0]} {"^"*25}\n\n Name: {position[1]}')

				return True



	def check_position_db(self, checkPosition):
		with sqlite3.connect('Workers.db') as connection:
			cursor = connection.cursor()

			cursor.execute("SELECT 1 FROM Positions WHERE LOWER(Pname) = ?", (checkPosition.lower(),))

			return cursor.fetchone() is not None



	def change_position_db(self, pid, PosNewName):
		with sqlite3.connect('Workers.db') as connection:
			cursor = connection.cursor()

			old_name = self.get_position_name(pid)

			cursor.execute("UPDATE Positions SET Pname = ? WHERE Pid = ?", (PosNewName, pid))

			connection.commit()

			print(f'\n\nPosition "{old_name}" has been changed to "{PosNewName}"\n')



	def get_emp_bye_position(self, pid):
		with sqlite3.connect('Workers.db') as connection:
			cursor = connection.cursor()

			cursor.execute("SELECT Eid FROM Employee WHERE position = ?", (pid,))
			return cursor.fetchall()



	def delete_position_db(self, pid):
		with sqlite3.connect('Workers.db') as connection:
			cursor = connection.cursor()

			old_name = self.get_position_name(pid)

			cursor.execute("DELETE FROM Positions WHERE Pid = ?", (pid,))
			connection.commit()
			print(f"\n\nPosition '{old_name}' with ID {pid} has been removed from database.\n")




	def get_position_id(self, PosNewName):
		with sqlite3.connect('Workers.db') as connection:

			cursor = connection.cursor()
			cursor.execute("SELECT Pid FROM Positions WHERE LOWER (Pname) = ?", (PosNewName.lower(),))
			result = cursor.fetchone()
			if result:
				return result[0]  # აბრუნებს ახალ pid-ს
			else:
				print("\nError retrieving position ID.\n")
				return None





	def add_emploee_db(self, employee):
		with sqlite3.connect('Workers.db') as connection:
			cursor = connection.cursor()

			cursor.execute(""" INSERT INTO Employee(fname, lname, age, position, salary, addressid) 
								VALUES (?,?,?,?,?,?)""",
								(employee.fname, employee.lname, employee.age, employee.position, employee.salary, employee.address))

			connection.commit()

			print('\n\nEmployee has been added!\n')



	def view_all_employees_db(self):
		with sqlite3.connect('Workers.db') as connection:
			cursor = connection.cursor()

			cursor.execute('SELECT Eid, fname, lname, age FROM Employee')

			employees = cursor.fetchall()

			if not employees:
				print('\n\nNo employee found.\n\n')
				return False
			else:
				print(f'\n{"^"*25} Employee {"^"*25}\n')
				for employee in employees:
					print(
						    f'\n  {"^"*25} ID: {employee[0]} {"^"*25}\n'
						    f' Name: {employee[1]}\n'
						    f' Lname: {employee[2]}\n'
						    f' Age: {employee[3]}\n'
						    f'{"^"*61}\n'
						)
				return True


	def view_all_employees_info_db(self):
		with sqlite3.connect('Workers.db') as connection:
			cursor = connection.cursor()

			cursor.execute("""
							SELECT E.Eid, E.Fname, E.lname, E.age, P.Pname, E.salary, A.Country, A.City, A.Town
							FROM Employee E
							Join Positions P ON E.position = P.Pid
							Join Address A ON E.addressid = A.Aid
							""")


			results = cursor.fetchall()

			if not results:
				print('\n\nNo result found.\n')
			else:
				print(f"\n\n{"^"*19} Employee's Information {"^"*19}\n")
				for result in results:
					print(
						    f'\n  {"^"*25} ID: {result[0]} {"^"*25}\n'
						    f' Name: {result[1]} {result[2]}\n'
						    f' Age: {result[3]}\n'
						    f' Position: {result[4]}\n'
						    f' Salary: {result[5]}\n'
						    f' Address: {result[6]}, {result[7]}, {result[8]}\n'
						    f'{"^"*61}\n'
						)
				return True


	def update_employee_info_db(self, eid, field, new_value):
		with sqlite3.connect('Workers.db') as connection:
			cursor = connection.cursor()

			cursor.execute(f" UPDATE Employee SET {field} = ? WHERE Eid = ? ", (new_value, eid))

			connection.commit()

			print('\n\nEmployee has been updated!\n')





	def id_exists(self, table, column, id_value):
		with sqlite3.connect('Workers.db') as connection:
			cursor = connection.cursor()

			cursor.execute(f"SELECT 1 FROM {table} WHERE {column} = ?", (id_value,))
			return cursor.fetchone() is not None



	def view_info_db(self, eid):

		with sqlite3.connect('Workers.db') as connection:
			cursor= connection.cursor()
			
			cursor.execute("""
							SELECT E.Eid, E.Fname, E.lname, E.age, P.Pname, E.salary, A.Country, A.City, A.Town
							FROM Employee E
							Join Positions P ON E.position = P.Pid
							Join Address A ON E.addressid = A.Aid
							WHERE E.Eid = ?""", (eid,))


			results = cursor.fetchall()

			if not results:
				print('\n\nNo result found.\n')
			else:
				print(f"\n\n{"^"*19} Employee's Information {"^"*19}\n")
				for result in results:
					print(
						    f'\n  {"^"*25} ID: {result[0]} {"^"*25}\n'
						    f' Name: {result[1]}\n'
						    f' Lname: {result[2]}\n'
						    f' Age: {result[3]}\n'
						    f' Position: {result[4]}\n'
						    f' Salary: {result[5]}\n'
						    f' Address: {result[6]}, {result[7]}, {result[8]}\n'
						    f'{"^"*61}\n'
						)




	def delete_employee_db(self, eid):
		with sqlite3.connect('Workers.db') as connection:
			cursor= connection.cursor()

			cursor.execute("DELETE FROM Employee WHERE Eid = ?", (eid,))

			connection.commit()

			print("\nEmployee has been removed\n")


	def get_employee_name_db(self, eid):
		with sqlite3.connect('Workers.db') as connection:
			cursor= connection.cursor()

			cursor.execute("SELECT fname, lname FROM Employee WHERE Eid = ?", (eid,))
			result = cursor.fetchone()
			if result:
				return f"{result[0]} {result[1]}"
			else:
				return None



	def view_all_employees_in_positions_db(self, pid, posnamee):
		
		with sqlite3.connect('Workers.db') as connection:
			cursor= connection.cursor()

			cursor.execute(""" SELECT Eid, fname, lname, age FROM Employee where position = ? """, (pid,))

			results = cursor.fetchall()

			if not results:
				print(f'\n\nThere are no employees assigned to the position "{posnamee}" \n')
			else:
				print(f"\n\n{"^"*19} Employees assigned to the position '{posnamee}' {"^"*19}\n")
				for result in results:
					print(
						    f'\n  {"^"*25} ID: {result[0]} {"^"*25}\n'
						    f' Name: {result[1]}\n'
						    f' Lname: {result[2]}\n'
						    f' Age: {result[3]}\n'
						    f'{"^"*61}\n'
						)





	def employee_exists_on_address_db(self, aidchoice):

		with sqlite3.connect('Workers.db') as connection:
			cursor= connection.cursor()

			cursor.execute("SELECT Eid, fname, lname, age FROM Employee WHERE addressid = ?", (aidchoice,))

			results = cursor.fetchall()
			if results:
				return results
			else:
				return None




	def delete_employee_aid_db(self, aidchoice):
		with sqlite3.connect('Workers.db') as connection:
			cursor= connection.cursor()

			cursor.execute("DELETE FROM Employee WHERE addressid = ?", (aidchoice,))

			connection.commit()

			print(f'\nEmployee with addressID "{aidchoice}" have been deleted\n')



'''

def get_employee_by_Aid(Aid):
	with sqlite3.connect('Workers.db') as connection:
		cursor= connection.cursor()

		cursor.execute("SELECT Eid, fname, lname, age FROM Employee WHERE addressid = ?", (Aid,))

		results = cursor.fetchall()
		if not results:
			print(f'\n\nThere are no employees with the address "{name}" \n')
		else:
			print(f"\n\n{"^"*19} Employees with address '{name}' {"^"*19}\n")
			for result in results:
				print(
					    f'\n  {"^"*25} ID: {result[0]} {"^"*25}\n'
					    f' Name: {result[1]}\n'
					    f' Lname: {result[2]}\n'
					    f' Age: {result[3]}\n'
					    f'{"^"*61}\n'
					)


'''



class Employee:
	def __init__(self,fname, lname, age, position, salary, address):
		self.fname = fname
		self.lname = lname
		self.age = age
		self.position = position
		self.salary = salary
		self.address = address


class Position:
	def __init__(self, Pname):
		self.Pname = Pname

class Address:
	def __init__(self, country, city, town):
		self.country = country
		self.city = city
		self.town = town

class EmployeeManager:
	def __init__(self, db):
		self.db = db

	def add_emploee(self, employee):
		self.db.add_emploee_db(employee)


	def view_all_employees(self):
		return self.db.view_all_employees_db()


	def view_info(self, eid):
		self.db.view_info_db(eid)


	def delete_employee(self, eid):
		self.db.delete_employee_db(eid)


	def view_all_employees_info(self):
		return self.db.view_all_employees_info_db()


	def view_all_employees_in_positions(self, pid, posnamee):
		return self.db.view_all_employees_in_positions_db(pid, posnamee)


	def employee_exists_on_address(self, aidchoice):
		return self.db.employee_exists_on_address_db(aidchoice)

	def delete_employee_aid(self, aidchoice):
		self.db.delete_employee_aid_db(aidchoice)



'''
	def update_employee_info(eid):
		self.db.update_employee_info_db(eid)
'''


	

class PositionManager:
	def __init__(self, db):
		self.db = db

	def add_position(self, poss):
		self.db.add_position_db(poss)

	def view_all_positions(self):
		return self.db.view_all_positions_db()

	def check_position(self, checkPosition):
		return self.db.check_position_db(checkPosition)

	def change_position(self, pid, PosNewName):
		if self.check_position(PosNewName.lower()):
			print('\n\nPosition with this name already exists.\n')
			return
		self.db.change_position_db(pid, PosNewName)

	def delete_position(self, pid):
		old_name = self.db.get_position_name(pid)

		employees = self.db.get_emp_bye_position(pid)# თანამშრომლების აიდების მიღება პოზიციის მიხედვით
		if not employees:
			print(f'\n\nNo employees found for position "{old_name}"\n')
		else:
			print(f'\n\nDeleting employees with position "{old_name}":\n')
			#ყველა თანამშრომლის წაშლა არსებულ პოზიციაზე
			for (eid,) in employees:
				name = self.db.get_employee_name_db(eid)
				print(f' - {name} (ID: {eid})')



				self.db.delete_employee_db(eid)


		self.db.delete_position_db(pid)




class AddressManager:
	def __init__(self, db):
		self.db = db

	def add_address(self, address):
		return self.db.add_address_db(address)

	def view_all_addresses(self):
		return self.db.view_all_addresses_db()

	def delete_address(self, aidchoice):
		self.db.delete_address_db(aidchoice)





def add_position_flow(Pmanager): #Created function of add positions to decrease codewriting
	Pname = requiredInput('\nPosition name: ')

	poss = Position(Pname)

	Pmanager.add_position(poss)

	with sqlite3.connect('Workers.db') as connection:
		cursor = connection.cursor()
		cursor.execute("SELECT Pid FROM Positions WHERE Pname = ?", (Pname,))
		result = cursor.fetchone()
		if result:
			return result[0]
		else:
			print("\nError retrieving new position ID.\n")
			return None
	


def requiredInput(prompt):
	while True:
		value = input(prompt).strip()
		if value == '':
			print("\n\nField Can not be empty. Please enter something.\n")
		else:
			return value

def valueChecker(prompt):
	while True:
		value = input(prompt).strip()

		if value == '':
			print("\n\nField Can not be empty. Please enter something.\n")
			
			continue

		try:
			return int(value)
		except ValueError:
			print("\n\nPlease enter a valid number\n")

def get_pid(prompt, db):
	while True:
		pid = valueChecker(prompt)
		if not db.id_exists('Positions', 'Pid', pid):
			print('\nID DOES NOT EXIST, TRY AGAIN\n')
		else:
			
			return pid


'''
def position_exist(Pmanager):
	position_exist = Pmanager.view_all_positions()
	if not position_exist:
		print('\nNo positions found.\n')
		return False
	return True
'''




def get_or_add_position(Pmanager, db):
	#db = Database()
	while True:
		position_exist = Pmanager.view_all_positions()

		if not position_exist:
			print("\nLet's add one.")
			return add_position_flow(Pmanager)
			
		print(f"\n\n{15*'-'}> Type 0 to add a new position <{15*'-'}\n")
		pid = valueChecker('\nChoose position ID or add new: ')

		if pid == 0:
			while True:
				PosNewName = requiredInput('\nNew position name: ')
				if db.check_position_db(PosNewName.lower()):
					print(f"\nPosition already exists with the name '{PosNewName}'.\n"
							"\nWould you like to:\n\n"
							"1) Use this existing position\n"
							"2) Enter a different name to add as a new position\n"
							)
					choiceposs = None
					while True:
						choiceposs = requiredInput('\nPlease choose 1 or 2: ')
						if choiceposs == '1':
							return db.get_position_id(PosNewName)

						elif choiceposs == '2':
							print('\nYou choose to add new position.')
							break

						else:
							print('\nInvalid input. Try again\n')
				else:
					poss = Position(PosNewName)
					Pmanager.add_position(poss)
					
					return db.get_position_id(PosNewName)
					break

		if db.id_exists('Positions', 'Pid', pid):
			return pid
		else:
			print('\n\nID DOES NOT EXIST, TRY AGAIN\n')
			
			

def add_address_flow(Amanager): ##Created function of add addresses to decrease codewriting
	country = requiredInput("\nCountry: ")
	city = requiredInput("\nCity: ")
	town = requiredInput("\nTown/street: ")

	address = Address(country, city, town)

	aid = Amanager.add_address(address)

	return aid




def get_or_add_address(Amanager, db):
	#db = Database()
	while True:
		address_exist = Amanager.view_all_addresses()

		if not address_exist:
			print("\nLet's add one.")
			return add_address_flow(Amanager)
			
		print(f"\n\n{15*'-'}> Type 0 to add a new address <{15*'-'}\n")
		aid = valueChecker('\nChoose address ID or add new: ')

		if aid == 0:
			return add_address_flow(Amanager)
	

		if db.id_exists('Address', 'Aid', aid):
			return aid
		else:
			print('\n\nID DOES NOT EXIST, TRY AGAIN\n')
			

def filter_employees_by_salary():
	salary_filter = None
	while salary_filter not in ('1', '2'):
		salary_filter = requiredInput(
										'\nHow do you want to filter?\n'
										'\n1) Above a value\n'
										'2) Below a value\n'
										'\nChoose: ')



	salary_value = valueChecker('\nEnter salary value: ')

	with sqlite3.connect('Workers.db') as connection:
		cursor = connection.cursor()

		operator = '>=' if salary_filter == '1' else '<='
		cursor.execute(f"""
						SELECT Eid, fname, lname, salary 
						FROM Employee WHERE salary {operator} ?
						""", (salary_value,))


		results = cursor.fetchall()

		if not results:
			print('\n\nNo employees found for this filter.\n')
		else:
			print(f'\n\n{"^"*25} Filtered employees {"^"*25}\n')
			for emp in results:
				print(f'{"^"*25}\nID: {emp[0]}\nName: {emp[1]} {emp[2]}\nSalary: {emp[3]}\n{"^"*25}\n')



			
def delete_address_flow(Amanager, Emanager, db):
	if not Amanager.view_all_addresses():
		return
	
	while True:
		aidchoice = valueChecker('\nSelect address ID to delete\n'
								'Choice: ')
		if not db.id_exists('Address', 'Aid', aidchoice):
			print("\nID DOES NOT EXIST, TRY AGAIN")
		else:
			break


	employees_on_address = Emanager.employee_exists_on_address(aidchoice)


	if employees_on_address:
		while True:
			deletechoice = requiredInput('\nThere are employees registered at this address.\n'
											'\nWhat would you like to do?\n\n'
											'1) Delete all employees with this address\n'
											'2) Assign a new address to these employees instead\n'
											'\nChoice: ')


			if deletechoice == '1': #Delete all employees with this address
				Emanager.delete_employee_aid(aidchoice)
				Amanager.delete_address(aidchoice)
				break

				
			elif deletechoice == '2':# Assign a new address to these employees instead
				newAid = add_address_flow(Amanager)
				for employee in employees_on_address:
					eid = employee[0]
					db.update_employee_info_db(eid, 'addressid', newAid)

				print(f"\n\nAll employees have been updated to the new address.\n")
				Amanager.delete_address(aidchoice)
				break
				
			else:
				print('\nInvalid input. Try again\n')
				continue

	else:
		print('\nThere are no employees registerd at this address')
		Amanager.delete_address(aidchoice)




		

def menu():

	db = Database()

	Emanager = EmployeeManager(db)
	Pmanager = PositionManager(db)
	Amanager = AddressManager(db)


	choice = None
	while choice != '0':
		print(f'\n\n{18*'^'} Please Choose An Option {18*'^'}\n')

		print("\n1) Add employee\n")
		print("2) View employee info \n")
		print("3) Update employee info\n ")
		print("4) Delete employee\n")
		print("5) List all employees with filtering by salary (e.g., above/below a value)\n")
		print("6) View list of positions\n")
		print("7) Add / Check / Change / Delete positions\n")
		print("8) List all employees with filtering by position\n")
		print("9) View list of addresses\n")
		print("10) List all employees with filtering by address\n")
		print("11) Delete address and replace it\n")
		print("0) Exit\n")

		choice = requiredInput('type ---> ')

		if choice == '1':#Add employee
			
			fname = requiredInput('\nName: ')
			lname = requiredInput('\nLast name: ')
			
			while True:
				age = valueChecker('\nAge: ')

				if 16 <= age <= 90 :
					break
				
				print("\n\nAge must be between 16 and 90\n")
					



			print(f"\n\n{25*'^'} Choose Employee's Position {25*'^'}\n")
			pid = get_or_add_position(Pmanager, db)


			salary = valueChecker("\nSalary: ")

			print('\n\nAdd your address\n')

			aid = get_or_add_address(Amanager,db)
	
			employee = Employee(fname, lname, age, pid, salary, aid)
			
			Emanager.add_emploee(employee)




		elif choice == '2':#View employee info
			
			if not Emanager.view_all_employees_info():
				continue

							
		elif choice == '3':#Update employee info
			if not Emanager.view_all_employees_info():
				continue
			while True:
				eid = valueChecker('\nChoose employee ID to change info: ')
									
				if not db.id_exists('Employee', 'Eid', eid):
					print("\nID DOES NOT EXIST, TRY AGAIN\n")
				else:
					break

			choiceInfo = None
			
			print(f'\nWhat would you like to change? \n'
					f'\nPlease answer with digit!\n\n')
			while choiceInfo not in ('1', '2', '3', '4', '5'):
				
				choiceInfo = requiredInput(
											f'1) Name\n'
											f'2) Age\n'
											f'3) Position\n'
											f'4) Salary\n'
											f'5) Address'
											f'\n\nChoose number: '
											)

				if choiceInfo == '1':#Name
					NewfName = requiredInput('\nNew name: ')
					Newlname = requiredInput('\nNew lname: ')

					db.update_employee_info_db(eid, 'fname', NewfName)
					db.update_employee_info_db(eid, 'lname', Newlname)

				elif choiceInfo == '2':#Age
					while True:
						NewAge = valueChecker('\nInput new age: ')

						if 16 <= NewAge <= 90 :
							break

						print("\n\nAge must be between 16 and 90\n")

					db.update_employee_info_db(eid, 'age', NewAge)

				

				elif choiceInfo == '3':#Position
					new_pid = get_or_add_position(Pmanager, db)
					db.update_employee_info_db(eid, 'position', new_pid)

				

				elif choiceInfo == '4':#Salary
					new_salary = valueChecker('\nNew salary: ')
					db.update_employee_info_db(eid, 'salary', new_salary)

				

				elif choiceInfo == '5':#Address
					aid = get_or_add_address(Amanager,db)

					db.update_employee_info_db(eid, 'addressid', aid )

				



				else:
					print(f'\n\nInvalid input. Try again\n')



		elif choice == '4':#Delete employee
			if not Emanager.view_all_employees():
				continue


			while True:
				eid = valueChecker('\nChoose ID: ')
									
				if not db.id_exists('Employee', 'Eid', eid):
					print("\nID DOES NOT EXIST, TRY AGAIN")
				else:
					break

			Emanager.delete_employee(eid)


		elif choice == '5':#List all employees with filtering by salary (e.g., above/below a value)
			filter_employees_by_salary()



		elif choice == '6':#View list of positions
			Pmanager.view_all_positions()



		elif choice == '7':# Add / check / change / delete positions
			print('\n1) Add position\n')
			print('2) Check position if exists\n')
			print('3) Change position\n')
			print('4) Delete position\n')

			PosChoice = None

			while PosChoice not in ('1', '2', '3', '4'):
				PosChoice = requiredInput('\nYour choice: ')

				if PosChoice == '1':
					add_position_flow(Pmanager)


				elif PosChoice == '2': #check if exist
					Pname = requiredInput('\nType position name to check: ').lower()

					if Pmanager.check_position(Pname):
						print('\nPosition exists.\n')
					else:
						addchoice = None
						print(
							'\nPosition does not exist.\n'
							'\nWould you like to add that position?\n\n'
							'1) Yes\n'
							'2) No\n')
						while True:
							addchoice = requiredInput('Choise: ')
							if addchoice == '1':
								poss = Position(Pname)
								Pmanager.add_position(poss)
								
								break

							elif addchoice == '2':
								print('\n\nYou choose to not add position.\n')
								break
							else:
								print('\n\nInvalid input\n')
								continue


					



				elif PosChoice == '3': #change
					if not Pmanager.view_all_positions():
						continue

					pid = get_pid('\nChoose P.id to change: ', db)

					PosNewName = requiredInput('\nNew possition name: ')

					Pmanager.change_position(pid, PosNewName)



				elif PosChoice == '4': #delete
					if not Pmanager.view_all_positions():
						continue
					pid = get_pid('\nChoose P.id to Delete: ', db)

					Pmanager.delete_position(pid)

				else:
					print('\n\nInvalid Input. Try again\n')






		elif choice == '8':#List all employees with filtering by position
			Pmanager.view_all_positions()
			pid = get_pid('\n\nChoose P.id ', db)
			posnamee = db.get_position_name(pid)
			Emanager.view_all_employees_in_positions(pid, posnamee)





		elif choice == '9':#View list of addresses
			Amanager.view_all_addresses()




		elif choice == '10':#List all employees with filtering by address
			address_type = None
			while address_type not in ('1', '2', '3'):
				address_type = requiredInput(
												'\n1)Filter by country\n'
												'\n2)Filter by city\n'
												'\n3)Filter by town\n'
												'\nChoice: ')

				if address_type == '1':#Filter by country
					address_choice = requiredInput('\nType country name: ').lower()

					db.get_addressID_db('Country', address_choice)
					
					

				elif address_type == '2':#Filter by city
					address_choice = requiredInput('\nType city name: ').lower()

					db.get_addressID_db('City', address_choice)

				elif address_type == '3':#Filter by town
					address_choice = requiredInput('\nType town name: ').lower()

					db.get_addressID_db('Town', address_choice)

				

		elif choice == '11':#Delete address and replace it
			delete_address_flow(Amanager, Emanager, db)

		elif choice == '0':
			print('\n\nBye-bye!\n\n')
				
		else:
			print('\n\nInvalid Input. Try again\n')
menu()


"""



"""


