// Copyright (c) 2025, mohamed and contributors
// For license information, please see license.txt

frappe.ui.form.on('Utilization Record', {
    onload: function(frm) {
        if (!frm.doc.daydate) {
            frm.set_value('daydate', frappe.datetime.get_today());
        }
    },
    refresh: function (frm) {
        if (frm.doc.status === 'Approved') {
            /*frm.set_df_property("daydate", "read_only", 1);
            frm.set_df_property("login_time", "read_only", 1);
            frm.set_df_property("logout_time", "read_only", 1);
            frm.set_df_property("total_time", "read_only", 1);
            frm.set_df_property("vacation", "read_only", 1);
            frm.set_df_property("connectivity_during_the_day", "read_only", 1);
            frm.set_df_property("issues_and_problems_in_connectivity_happened", "read_only", 1);
            frm.set_df_property("output", "read_only", 1);*/
            

            frm.set_read_only();
            //frm.disable_save()
            
        }
        if (!frm.is_new() && frm.doc.status === 'Pending') {
            frappe.call({
                method: "sheet_app.api.get_approver_access",
                args: {
                    employee_name: frm.doc.name1
                },
                callback: function (r) {
                    if (r.message === true){ 
                        frm.add_custom_button(__('Approve'), function () {
                            frappe.call({
                                method: "sheet_app.api.approve_utilization",
                                args: { docnames: [frm.doc.name] },
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