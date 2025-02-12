# Copyright (c) 2025, mohamed and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document

class Employee(Document):

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
				"first_name": self.first_name or self.employee_name,
				#"middle_name": self.middle_name,
				"last_name": self.last_name,
				"enabled": 1,
				"send_welcome_email": 0,  
				"user_type": "System User",
				"role_profile_name": self.role,  
				"new_password": self.password,  
				"module_profile": self.module_profile,
				"default_workspace": "sheet",
			})
			new_user.insert(ignore_permissions=True)

			frappe.msgprint(f"User {self.email} has been created successfully.")
		except Exception as e:
			frappe.throw(f"Error while creating user: {str(e)}")


























"""
def get_employee_list(doc,user):
	current_user = frappe.session.user
	user_email = frappe.db.get_value("User", user, "email")
	user_name = frappe.db.get_value("User", user, "first_name")

	manager = frappe.get_value("Employee",doc.manager)
	manager_email = frappe.get_value("Employee",manager,"email")

	return frappe.get_list('Employee', filters={'manager': user_name})




def validate_employee_permission(doc, user):
	# جلب البريد الإلكتروني للمستخدم
	user_email = frappe.db.get_value("User", user, "email")
	user_name = frappe.db.get_value("User", user, "first_name")

	manager = frappe.get_value("Employee",doc.manager)
	manager_email = frappe.get_value("Employee",manager,"email")
	#frappe.throw(f'{manager_email} - {manager}')
	#frappe.throw(f'{manager_email} - {user_email}- {manager} - {user_name}')
	# تحقق إذا كان المستخدم مديرًا للموظف
	if (frappe.session.user != "Administrator" and manager != None):
		#frappe.msgprint(f'${user_name} ${manager_email} {manager} {user_email}')
		if manager_email != user_email and manager != user_name:
			#frappe.throw(f'${user_name} ${manager_email} {manager} {user_email}')
			frappe.throw("You are not authorized to access this employee.")



# استدعاء الصلاحية أثناء عملية عرض البيانات
@frappe.whitelist()
def get_employee_details(employee_name):
	employee = frappe.get_doc("Employee", employee_name)
	validate_employee_permission(employee, frappe.session.user)
	#get_employee_list(employee,frappe.session.user)
	return employee



@frappe.whitelist()  # للسماح باستدعاء الدالة من خلال JavaScript
def get_employees_under_manager(manager_email):
    # التحقق من صحة البريد الإلكتروني
    if not manager_email:
        frappe.throw("Manager email is required")

    # البحث عن المدير في سجل الموظفين
    manager_employee = frappe.db.get_value("Employee", {"email": manager_email}, "name")
    if not manager_employee:
        frappe.throw("No manager found with the provided email")

    # جلب الموظفين الذين يشرف عليهم هذا المدير
    employees = frappe.db.get_list(
        "Employee",
        filters={"manager": manager_employee},
        fields=["name", "employee_name", "designation", "email"]
    )

    return employees


@frappe.whitelist()
def get_list(doctype, *args, **kwargs):
	import json
	frappe.msgprint(f"{doctype}")

	# الحصول على البريد الإلكتروني للمستخدم الحالي
	user_email = frappe.session.user

	# البحث عن اسم الموظف المرتبط بالبريد الإلكتروني
	manager_name = frappe.db.get_value("Employee", {"email": user_email}, "name")

	# إذا كان المستخدم هو مدير، قم بتصفية الموظفين الذين يشرف عليهم
	if manager_name:
		# تحويل kwargs إلى قاموس إذا لم يكن كذلك
		if isinstance(kwargs, str):
			kwargs = json.loads(kwargs)

		# التأكد من أن kwargs يحتوي على مفتاح "filters" كقاموس
		if not isinstance(kwargs.get("filters"), dict):
			kwargs["filters"] = {}

		# Add the manager filter only if querying the Employee doctype
		if doctype == "Employee":
			kwargs["filters"]["manager"] = manager_name

	# Remove any unexpected 'cmd' argument if present
	kwargs.pop('cmd', None)

	# استدعاء دالة get_list الافتراضية.
	frappe.msgprint(f"{doctype}")
	return frappe.get_list(doctype, *args, **kwargs)
"""


