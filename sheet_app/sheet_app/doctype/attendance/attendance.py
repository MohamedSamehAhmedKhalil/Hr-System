from frappe.model.document import Document
import frappe
from datetime import datetime


class Attendance(Document):
    
    def calc_total_time(self):
        if isinstance(self.in_time, str):
            self.in_time = datetime.strptime(self.in_time, "%H:%M:%S").time()
        
        if isinstance(self.out_time, str):
            self.out_time = datetime.strptime(self.out_time, "%H:%M:%S").time()

        today = datetime.today()
        in_datetime = datetime.combine(today, self.in_time)
        out_datetime = datetime.combine(today, self.out_time)

        time_difference = (out_datetime - in_datetime).total_seconds() / 3600  
        self.total_time = round(time_difference, 2)
    
    def before_save(self):
        self.calc_total_time()
        self.update_employee_report()


    def after_save(self):
        self.update_employee_report()

    def before_insert(self):
        user_email = frappe.db.get_value("User", frappe.session.user, "email")
        user_employee = frappe.get_value("Employee", {"email": user_email}, "name")
        if user_employee:
            self.employee = user_employee
        else:
            frappe.throw("لا يمكن العثور على موظف مرتبط بالبريد الإلكتروني الخاص بك.")


    def after_insert(self):
        user_email = frappe.db.get_value("User", frappe.session.user, "email")
        user_employee = frappe.get_value("Employee", {"email": user_email}, "name")
        dep_employee = frappe.get_value("Employee", {"email": user_email}, "designation")
        
        self.calc_total_time()
        
        #frappe.throw(f'{user_employee} {dep_employee}')
        
        new_record = frappe.get_doc({
            "doctype": "Employee Report",
            "employee_name": user_employee,
            "designation": dep_employee,
            "attendance": self.name,
            "day": self.date,
            "in_time":self.in_time ,
            "out_time": self.out_time,
            "total_time": self.total_time,
            
        })
        new_record.insert(ignore_permissions=True)
        #frappe.publish_realtime("refresh_employee_report")


    def update_employee_report(self):
        report_name = frappe.db.get_value("Employee Report", {"attendance": self.name}, "name")
        
        if report_name:
            frappe.db.set_value("Employee Report", report_name, {
                "day": self.date,
                "in_time": self.in_time,
                "out_time": self.out_time,
                "total_time": self.total_time
            })
        #frappe.publish_realtime("refresh_employee_report")

        #else:
            #frappe.throw("لا يوجد تقرير مرتبط بهذا الحضور لتحديثه.")


        





        



    """@frappe.whitelist()
    def get_manager_employees():
        current_user = frappe.session.user

        manager_employee = frappe.db.get_value("Employee", {"user_id": current_user}, "name")

        if not manager_employee:
            frappe.throw("You are not linked to any employee record.")

        managed_employees = frappe.get_all("Employee", filters={"manager": manager_employee}, pluck="name")
        return managed_employees
    

    def validate(doc, method):
        current_user = frappe.session.user

        manager_employee = frappe.db.get_value("Employee", {"user_id": current_user}, "name")

        if doc.employee and frappe.db.get_value("Employee", doc.employee, "manager") != manager_employee:
            frappe.throw("You are not authorized to access this record.")
    """
