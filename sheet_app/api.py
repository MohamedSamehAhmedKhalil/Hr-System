import frappe
@frappe.whitelist()
def can_access_employee(doc, ptype, user):
    if frappe.session.user == "Administrator":
        return True

    user_email = frappe.db.get_value("User", frappe.session.user, "email")
    user_employee = frappe.get_value("Employee Info", {"email": user_email}, "name")
    user_role = frappe.db.get_value("User", frappe.session.user, "role_profile_name")

    if not user_employee:
        frappe.throw("You are not linked to any Employee record.")

    subordinates = get_all_subordinates(user_employee)

    if doc.name in subordinates or doc.name == user_employee or user_role == "HR":
        return True

    frappe.throw("You are not authorized to access this employee.")
    
    
@frappe.whitelist()
def can_access_attendance(doc, ptype, user):
    if frappe.session.user == "Administrator":
        return True

    user_email = frappe.db.get_value("User", frappe.session.user, "email")
    user_employee = frappe.get_value("Employee Info", {"email": user_email}, "name")
    user_role = frappe.db.get_value("User", frappe.session.user, "role_profile_name")

    if not user_employee:
        frappe.throw("You are not linked to any Employee record.")

    if ptype == "create":
        #frappe.throw(f'{user_employee } {doc.employee}')
        if not user_employee:
            frappe.throw("You can only create utilization records for yourself.")

    if ptype == "read":
        subordinates = get_all_subordinates(user_employee)
        
        #frappe.throw(f'{user_employee } {doc.name1}')
        if doc.name1 != user_employee and doc.name1 not in subordinates and user_role != "HR":
            frappe.throw("You are not authorized to view this utilization record.")

    #if ptype in ["write", "delete"]:
     #   frappe.throw("You are not authorized to modify or delete this utilization record.")

    return True

    
@frappe.whitelist()
def get_all_subordinates(manager):
    subordinates = []

    def get_subordinates(manager_name):
        employees = frappe.get_all(
            'Employee Info',
            filters={'manager': manager_name},
            fields=['name']
        )
        for emp in employees:
            subordinates.append(emp['name'])
            get_subordinates(emp['name'])  

    get_subordinates(manager)
    return subordinates


@frappe.whitelist()
def approve_utilization(docnames):
    if isinstance(docnames, str):
        docnames = frappe.parse_json(docnames)


    user_email = frappe.db.get_value("User", frappe.session.user, "email")
    user_employee = frappe.get_value("Employee Info", {"email": user_email}, "name")
    user_role = frappe.db.get_value("User", frappe.session.user, "role_profile_name")

    if not user_employee:
        frappe.throw("You are not linked to any Employee record.")

    allowed_employees = get_all_subordinates(user_employee)
    if (not allowed_employees) and (user_role != "HR"):
            frappe.throw("You are not authorized to approve records because you are not a manager.")

    allowed_employees.append(user_employee)  # Include self

    approved = []
    for name in docnames:
        doc = frappe.get_doc("Utilization Record", name)

        if doc.status != "Pending":
            continue

        if doc.name1 not in allowed_employees:
            continue

        doc.status = "Approved"
        doc.save()

        create_or_update_report_sheet(doc)
        approved.append(name)

    return {"approved": approved}

@frappe.whitelist()
def get_approver_access(employee_name):
    user_email = frappe.db.get_value("User", frappe.session.user, "email")
    user_employee = frappe.get_value("Employee Info", {"email": user_email}, "name")
    user_role = frappe.db.get_value("User", frappe.session.user, "role_profile_name")

    if not user_employee:
        return False

    allowed_employees = get_all_subordinates(user_employee)
    #allowed_employees.append(user_employee)  # Include self
    if (not allowed_employees) and (user_role != "HR"):
        return False
    
    return employee_name in allowed_employees or employee_name == user_employee

def create_or_update_report_sheet(doc):
    emp_info = frappe.get_doc("Employee Info", doc.name1)

    report = frappe.new_doc("Report Sheet")
    report.employee_name = emp_info.name
    report.department = emp_info.department
    report.code = emp_info.code
    report.sheet = doc.name
    report.daydate = doc.daydate
    report.in_time = doc.login_time
    report.out_time = doc.logout_time
    report.total_working_hours = doc.total_time
    #report.connectivity = doc.connectivity_during_the_day
    #report.issues = doc.issues_and_problems_in_connectivity_happened
    #report.output = doc.output

    report.insert(ignore_permissions=True)

