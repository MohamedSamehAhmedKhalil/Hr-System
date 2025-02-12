# Copyright (c) 2025, mohamed and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta


class EmployeeInfo(Document):
	def calculate_age(self):
		if self.birthday:
			try:
				birth_date = datetime.strptime(self.birthday, "%Y-%m-%d")
				today = datetime.now()
				self.age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
			except ValueError:
				frappe.throw("Invalid date format in Birthday. Please use YYYY-MM-DD.")                
				

	def set_ending_date(self):
		if self.actual_position == "Training" and self.joining_date:
			try:
				start_date = datetime.strptime(self.joining_date, "%Y-%m-%d")
				self.ending_date = (start_date + timedelta(days=90)).strftime("%Y-%m-%d")
			except ValueError:
				frappe.throw("Invalid date format in Joining Date. Please use YYYY-MM-DD.")
	
	def validate(self):
		if self.national_id:
			if not self.national_id.isdigit():
				frappe.throw("National ID must contain only numbers.")
			if len(self.national_id) != 14:
				frappe.throw("National ID must be exactly 14 digits long.")     
		self.calculate_age()
		self.set_ending_date()
		self.full_name = self.first_name +" " + self.middle_name +" " + self.last_name
		if frappe.db.exists("Employee Info", {"code" : self.code , "name" : ["!=", self.name]}):
			frappe.throw(f"code {self.code} already exists")
		

	#def before_save(self):
		#self.full_name = self.first_name + " " + self.last_name
		

	def autoname(self):
		if self.middle_name:
			self.name = self.first_name +" " + self.middle_name +" " + self.last_name
		else:
			self.name = self.first_name + " " + self.last_name

	def after_insert(self):
		if not self.email or not self.password:
			frappe.msgprint(
				"Employee created successfully, but User was not created due to missing email or password.",
				alert=True
			)
			return

		if frappe.db.exists("User", self.email):
			frappe.msgprint(f"User with email {self.email} already exists.")
			return

		try:
			new_user = frappe.get_doc({
				"doctype": "User",
				"email": self.email,
				"first_name": self.first_name,
				"middle_name": self.middle_name,
				"last_name": self.last_name,
				"enabled": 1,
				"send_welcome_email": 0,  
				"user_type": "System User",
				"role_profile_name": self.role,  
				"new_password": self.password,  
				"module_profile": "employee",
				"default_workspace": "ISoft",
			})
			new_user.insert(ignore_permissions=True)

			frappe.msgprint(f"User {self.email} has been created successfully.")
		except Exception as e:
			frappe.throw(f"Error while creating user: {str(e)}")


"""
@frappe.whitelist()
def get_employee_list(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""
        # SELECT full_name 
        # FROM `tabEmployee Info`
        # WHERE full_name LIKE %(txt)s
        # ORDER BY code ASC
    #""", {"txt": f"%{txt}%"})





				
                
