""" Programme to create and manage employee database for ABC Company"""

# import sqlite3 library
import sqlite3

# Create connection object that represents the database
conn = sqlite3.connect("DBName.db")

# Create Cursor object to run commands and communicate with the database
c = conn.cursor()


# DBOperation class to manage all data into the database
class DBOperations:

    @staticmethod
    def create_table():
        """Create table to hold employee data autoincrement automatically generates employee ID"""

        with conn:
            try:
                c.execute(""" CREATE TABLE employees (
					employee_id integer PRIMARY KEY AUTOINCREMENT,
					empTitle text NOT NULL,
					forename text NOT NULL,
					surname text NOT NULL,
					email text NOT NULL,
					salary integer NOT NULL
					)""")
                print("\nThe table 'employees' has been created successfully")
            except sqlite3.OperationalError:
                print("Warning table already exists!")

    @staticmethod
    def insert_data(emp):
        """Insert new employee data into database"""

        with conn:
            try:
                c.execute(
                    """INSERT INTO employees VALUES (:employee_id, :emp_title, :forename, :surname, :email, :salary)""",
                    {'employee_id': emp.employee_id, 'emp_title': emp.emp_title, 'forename': emp.forename,
                     'surname': emp.surname, 'email': emp.email, 'salary': "£" + emp.salary})
                print("\nInserted data successfully\n")
            except Exception as e:
                print(e)

    @staticmethod
    def update_surname(employee_id, surname):
        """Update employee surname"""

        with conn:
            try:
                c.execute(""" UPDATE employees SET surname = :surname WHERE  employee_id = :employee_id""",
                          {'employee_id': employee_id, 'surname': surname})
            except Exception as e:
                print(e)

    @staticmethod
    def update_forename(employee_id, forename):
        """Update employee forename"""

        with conn:
            try:
                c.execute("""UPDATE employees SET forename = :forename WHERE  employee_id = :employee_id """,
                          {'employee_id': employee_id, 'forename': forename})
            except Exception as e:
                print(e)

    @staticmethod
    def update_email(employee_id, email):
        """ Update employee email address """

        with conn:
            try:
                c.execute("""UPDATE employees SET email = :email WHERE  employee_id = :employee_id  """,
                          {'employee_id': employee_id, 'email': email})
            except Exception as e:
                print(e)

    @staticmethod
    def update_salary(employee_id, salary):
        """ Update employee salary """

        with conn:
            try:
                c.execute("""UPDATE employees SET salary = :salary WHERE  employee_id = :employee_id   """,
                          {'employee_id': employee_id, 'salary': '£' + salary})
            except Exception as e:
                print(e)

    @staticmethod
    def update_title(employee_id, emp_title):
        """Update employee title """

        with conn:
            try:
                c.execute(""" UPDATE employees SET emp_title = :emp_title WHERE employee_id = :employee_id""",
                          {'employee_id': employee_id, 'emp_title': emp_title})
            except Exception as e:
                print(e)

    @staticmethod
    def delete_data(employee_id):
        """Delete particular employee's data in totality """

        with conn:
            try:
                c.execute(""" DELETE FROM employees WHERE employee_id = :employee_id""",
                          {'employee_id': employee_id})
                print("\nEmployee successfully deleted\n")
            except sqlite3.OperationalError as e:
                print(e)

    @staticmethod
    def delete_table():
        """ Delete the whole table of data"""

        with conn:
            try:
                c.executescript("DROP TABLE employees")
                print("\nTable successfully deleted\n")
            except Exception as e:
                print(e)

    @staticmethod
    def view_database():
        """Display the whole table of employee data  """

        try:
            c.execute("SELECT * FROM employees")
            results = c.fetchall()
            print('\nemployees:\n')
            for i in results:
                print(i, "\n")
        except Exception as e:
            print(e)

    @staticmethod
    def search_by_id(employee_id):
        """ Search for employee data by id and display it  """

        try:
            c.execute("""SELECT * FROM employees WHERE employee_id = :employee_id""",
                      {'employee_id': employee_id})
            return c.fetchone()
        except Exception as e:
            print(e)


# Employee class to obtain all employee properties
class Employee:

    def __init__(self, employee_id, emp_title, forename, surname, salary):
        self.employee_id = employee_id
        self.emp_title = emp_title
        self.forename = forename
        self.surname = surname
        self.salary = salary

    """Automatically generates email address with employee forename and surname"""

    @property
    def email(self):
        return f"{self.forename.lower()}.{self.surname.lower()}@abc.com"


# AdminMenu class handles all the menus the administrator uses to input data
class AdminMenu:

    @staticmethod
    def delete_menu():
        """ Delete menu obtains input from admin to delete data"""

        while True:
            input("Press enter to continue delete menu: ")
            print("\nWhat would you like to delete?")
            print(""" 
            1. Delete existing employee
            2. Delete whole table
            3. Return to main menu
            """)

            delete_input = input("Enter selection: ")
            if delete_input == '1':
                employee_id = input("Enter employee ID: ")
                if DBOperations.search_by_id(employee_id) != None:
                    DBOperations.delete_data(employee_id)
                else:
                    print("\nCannot find this record in the database\n")
            elif delete_input == '2':
                DBOperations.delete_table()
            elif delete_input == '3':
                AdminMenu.main_menu()
            else:
                print("Invalid choice please try again")
                continue

    @staticmethod
    def search_menu():
        """ Obtains data from admin to search for employee data """

        print("\nWhich employee would you like to search for?")
        employee_id = input("Enter employee ID: ")
        results = (DBOperations.search_by_id(employee_id))
        if type(results) == type(tuple()):
            for index, detail in enumerate(results):
                if index == 0:
                    print("Employee ID: " + str(detail))
                elif index == 1:
                    print("Employee Title: " + detail)
                elif index == 2:
                    print("Employee Name: " + detail)
                elif index == 3:
                    print("Employee Surname: " + detail)
                elif index == 4:
                    print("Employee Email: " + detail)
                else:
                    print("Salary: " + str(detail))

        else:
            print("No Record")

    @staticmethod
    def update_menu():
        """ Update menu obtains data from admin to update employee data """

        while True:
            input("\nPress enter to continue update menu: ")
            print("\nWhat data would you like to update?")
            print(""" 
             1. Employee Surname
             2. Employee Forename
             3. Employee Email
             4. Employee Salary
             5. Employee Title
             6. Return to main menu
             """)

            update_input = input("Enter selection: ")
            if update_input == '1':
                employee_id = input("Enter employee ID: ")
                surname = input("Enter Surname: ")
                if employee_id == "" or surname == "":
                    print("\nFail Please try again")
                else:
                    DBOperations.update_surname(employee_id, surname)
                    print("\nSurname successfully updated to " + surname)
            elif update_input == '2':
                employee_id = input("Enter employee ID: ")
                forename = input("Enter employee Forename: ")
                if employee_id == "" or forename == "":
                    print("\nFail Please try again")
                else:
                    DBOperations.update_forename(employee_id, forename)
                    print("\nForename successfully updated to " + forename)
            elif update_input == '3':
                employee_id = input("Enter employee ID: ")
                forename = input("Enter forename: ")
                surname = input("Enter surname: ")
                if employee_id == "" or forename == "" or surname == "":
                    print("\nFail Please try again")
                else:
                    email = f"{forename.lower()}.{surname.lower()}@abc.com"
                    DBOperations.update_email(employee_id, email)
                    print("\nEmail successfully updated to " + email)
            elif update_input == '4':
                employee_id = input("Enter employee ID: ")
                salary = input("Enter salary: ")
                if employee_id == "" or salary == "":
                    print("\nFail Please try again")
                else:
                    DBOperations.update_salary(employee_id, salary)
                    print("\nSalary successfully updated to £" + salary)
            elif update_input == '5':
                employee_id = input("Enter employee ID: ")
                title = input("Enter employee title: ")
                if employee_id == "" or title == "":
                    print("\nFail Please try again")
                else:
                    DBOperations.update_title(employee_id, title)
                    print("\nTitle Successfully updated to " + title)
            elif update_input == '6':
                AdminMenu.main_menu()
            else:
                print("\nInvalid choice please try again")
                continue

    @staticmethod
    def input_for_new_emp():
        """ Obtains data from admin to create new employee data """

        print("Please enter the following details")
        employee_id = None
        emp_tittle = input("Enter title: ")
        forename = input("Enter forename: ")
        surname = input("Enter surname: ")
        salary = input("Enter salary: ")
        new_employee = Employee(employee_id, emp_tittle, forename, surname, salary)
        DBOperations.insert_data(new_employee)

    @staticmethod
    def main_menu():
        """ Administrator main menu interface"""

        while True:
            input('\nPress enter to continue to the main menu: ')
            print('\nWelcome to the database menu')
            print("""
                    Please choose from the following options:
                    1 - Create employee table
                    2 - Insert a new employee into table
                    3 - Display the entire employee database
                    4 - Update an employees details
                    5 - Search the database
                    6 - Delete an existing employee
                    7 - Exit
            """)

            menu_selection = input("Enter your choice: ")
            if menu_selection == '1':
                DBOperations.create_table()
            elif menu_selection == '2':
                AdminMenu.input_for_new_emp()
            elif menu_selection == '3':
                DBOperations.view_database()
            elif menu_selection == '4':
                AdminMenu.update_menu()
            elif menu_selection == '5':
                AdminMenu.search_menu()
            elif menu_selection == '6':
                AdminMenu.delete_menu()
            elif menu_selection == '7':
                exit(0)
            else:
                print("\nInvalid choice please try again")
                continue


# to run programme
AdminMenu.main_menu()
