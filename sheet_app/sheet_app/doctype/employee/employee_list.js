//frappe.ui.form.on('Employee', {
    /*refresh: function(frm) {
        if (frappe.session.user !== "Administrator") {
            frappe.call({
                method: "sheet_app.sheet_app.doctype.employee.employee.get_employees_under_manager",
                args: {
                    manager_email: frappe.session.user  
                },
                callback: function(r) {
                    if (r.message && r.message.length > 0) {
                        let employees = r.message;
                        let html = "<h3>Employees Under Your Supervision:</h3><ul>";
                        employees.forEach(emp => {
                            html += `<li>${emp.employee_name} (${emp.designation}) - ${emp.email}</li>`;
                        });
                        html += "</ul>";

                        frm.dashboard.add_section(html);
                    } else {
                        frm.dashboard.add_section("<h3>No employees under your supervision.</h3>");
                    }
                }
            });
        }
    },*/

    /*onload: function(frm) {
        if (frappe.session.user !== "Administrator") {
            frappe.call({
                method: "sheet_app.sheet_app.doctype.employee.employee.get_employee_details",
                args: {
                    employee_name: frm.doc.name
                },
                callback: function(r) {
                    if (!r.message) {
                        frappe.msgprint("You are not authorized to view this employee.");
                        frappe.set_route("List", "Employee");  
                    }
                }
            });
        }
    },*/
    /*after_save: function (frm) {
        frm.add_custom_button(__('View Attendance'), function () {
            frappe.set_route('List', 'Attendance', { employee: frm.doc.name });
        },); 
    }*/

//});