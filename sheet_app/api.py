import frappe
@frappe.whitelist()
def can_access_employee(doc, ptype, user):
    if frappe.session.user == "Administrator":
        return True

    user_email = frappe.db.get_value("User", frappe.session.user, "email")
    user_employee = frappe.get_value("Employee Info", {"email": user_email}, "name")

    if not user_employee:
        frappe.throw("You are not linked to any Employee record.")

    subordinates = get_all_subordinates(user_employee)

    if doc.name in subordinates or doc.name == user_employee:
        return True

    frappe.throw("You are not authorized to access this employee.")
    
    
@frappe.whitelist()
def can_access_attendance(doc, ptype, user):
    if frappe.session.user == "Administrator":
        return True

    user_email = frappe.db.get_value("User", frappe.session.user, "email")
    user_employee = frappe.get_value("Employee Info", {"email": user_email}, "name")

    if not user_employee:
        frappe.throw("You are not linked to any Employee record.")

    if ptype == "create":
        #frappe.throw(f'{user_employee } {doc.employee}')
        if not user_employee:
            frappe.throw("You can only create utilization records for yourself.")

    if ptype == "read":
        subordinates = get_all_subordinates(user_employee)
        
        #frappe.throw(f'{user_employee } {doc.name1}')
        if doc.name1 != user_employee and doc.name1 not in subordinates:
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

    if not user_employee:
        frappe.throw("You are not linked to any Employee record.")

    allowed_employees = get_all_subordinates(user_employee)
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
        approved.append(name)

    return {"approved": approved}