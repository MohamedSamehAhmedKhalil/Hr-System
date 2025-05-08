// Copyright (c) 2025, mohamed and contributors
// For license information, please see license.txt

frappe.ui.form.on('Utilization Record', {
    onload: function(frm) {
        if (!frm.doc.daydate) {
            frm.set_value('daydate', frappe.datetime.get_today());
        }
    },
    
    refresh: function (frm) {
        if (frm.doc.docstatus === 0 && frm.doc.status === 'Approved') {
            frm.set_read_only();
        }

        // زر الموافقة يظهر فقط بعد الحفظ
        if (!frm.is_new() && frm.doc.status === 'Pending') {
            frappe.call({
                method: "sheet_app.api.get_all_subordinates",
                args: {
                    manager: frappe.session.user_email
                },
                callback: function (r) {
                    let subs = r.message || [];
                    if (frm.doc.owner === frappe.session.user || subs.includes(frm.doc.name1)) {
                        frm.add_custom_button(__('Approve'), function () {
                            frappe.call({
                                method: "sheet_app.api.approve_utilization",
                                args: { names: [frm.doc.name] },
                                callback: function () {
                                    frappe.msgprint("Record Approved");
                                    frm.reload_doc();
                                }
                            });
                        });
                    }
                }
            });
        }
    }
});