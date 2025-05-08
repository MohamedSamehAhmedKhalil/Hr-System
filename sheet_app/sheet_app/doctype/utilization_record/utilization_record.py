# Copyright (c) 2025, mohamed and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta


class UtilizationRecord(Document):
	"""def calc_total_time(self):
		if isinstance(self.login_time, str):
			self.login_time = datetime.strptime(self.login_time, "%H:%M:%S").time()
		
		if isinstance(self.logout_time, str):
			self.logout_time = datetime.strptime(self.logout_time, "%H:%M:%S").time()

		today = datetime.today()
		in_datetime = datetime.combine(today, self.login_time)
		out_datetime = datetime.combine(today, self.logout_time)
		
		time_difference = out_datetime - in_datetime
    	total_seconds = time_difference.total_seconds()

		hours = int(total_seconds // 3600)
    	minutes = int((total_seconds % 3600) // 60)

		self.total_time = f"{hours} ساعة و {minutes} دقيقة"

		if self.total_time < 0:
				frappe.throw("Logout time must be later than login time.")"""
	
	def calc_total_time(self):
		if isinstance(self.login_time, str):
			self.login_time = datetime.strptime(self.login_time, "%H:%M:%S").time()
		
		if isinstance(self.logout_time, str):
			self.logout_time = datetime.strptime(self.logout_time, "%H:%M:%S").time()

		today = datetime.today()
		in_datetime = datetime.combine(today, self.login_time)
		out_datetime = datetime.combine(today, self.logout_time)

		if out_datetime < in_datetime:
			frappe.throw("Logout time must be later than login time.")

		time_difference = out_datetime - in_datetime

		self.total_time = str(time_difference)

	def update_employee_report(self):
		report_name = frappe.db.get_value("Report Sheet", {"sheet": self.name}, "name")
		
		if report_name:
			frappe.db.set_value("Report Sheet", report_name, {
				"daydate": self.daydate,
				"in_time": self.login_time,
				"out_time": self.logout_time,
				"total_working_hours": self.total_time,
			})

	def before_save(self):
		self.calc_total_time()
		self.update_employee_report()
		#if self.status == "Approved":
			#frappe.throw("Cannot edit approved record.")

	def after_save(self):
		self.update_employee_report()

	def before_insert(self):
		user_email = frappe.db.get_value("User", frappe.session.user, "email")
		user_employee = frappe.get_value("Employee Info", {"email": user_email}, "name")
		if user_employee:
			self.name1 = user_employee
		else:
			frappe.throw(f"{user_employee}")
			frappe.throw("لا يمكن العثور على موظف مرتبط بالبريد الإلكتروني الخاص بك.")

	def after_insert(self):
		user_email = frappe.db.get_value("User", frappe.session.user, "email")
		user_employee = frappe.get_value("Employee Info", {"email": user_email}, "name")
		dep_employee = frappe.get_value("Employee Info", {"email": user_email}, "department")
		code_employee = frappe.get_value("Employee Info", {"email": user_email}, "code")


		self.calc_total_time()

		#frappe.throw(f'{user_employee} {dep_employee}')

		new_record = frappe.get_doc({
			"doctype": "Report Sheet",
			"code" :code_employee,
			"employee_name": user_employee,
			"department": dep_employee,
			"sheet": self.name,
			"daydate": self.daydate,
			"in_time":self.login_time ,
			"out_time": self.logout_time,
			"total_working_hours": self.total_time,
			
		})
		new_record.insert(ignore_permissions=True)
		#frappe.publish_realtime("refresh_employee_report")




