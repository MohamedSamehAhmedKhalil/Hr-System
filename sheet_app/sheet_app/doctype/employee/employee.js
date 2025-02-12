// Copyright (c) 2025, mohamed and contributors
// For license information, please see license.txt

//frappe.ui.form.on("Employee", {
 
//});
/*frappe.listview_settings['Employee'] = {
    onload: function(listview) {
        frappe.call({
            method: "frappe.client.get_value",
            args: {
                doctype: "Employee",
                filters: { email: frappe.session.user },
                fieldname: "name"
            },
            callback: function(response) {
                if (response && response.message) {
                    let manager_name = response.message.name;
                    frappe.msgprint(`Showing employees under manager: ${manager_name}`);
                }
            }
        });
    }
};*/







//***************************************************************************************** */
//******************************************************************************************* */
/*
frappe.listview_settings['Employee'] = {
    refresh: function (listview) {
        if (frappe.session.user === 'Administrator') {
            return; // لا تطبق أي فلاتر على المدير العام
        }
        frappe.call({
            method: 'frappe.client.get',
            args: {
                doctype: 'Employee',
                filters: {
                    'email': frappe.session.user
                }
            },
            callback: function (response) {
                if (response.message) {
                    const manager_name = response.message.name;
                    listview.filter_area.add([
                        ['Employee', 'manager', '=', manager_name]
                    ]);
                }
            }
        });
    },
    onload: function (listview) {
        listview.page.add_menu_item(__('View Attendance'), function () {
            if (frappe.session.user === 'Administrator') {
                return; // لا تطبق أي فلاتر على المدير العام
            }
            frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    doctype: 'Employee',
                    filters: {
                        manager: frappe.session.user_fullname // جلب الموظفين الذين يديرهم المستخدم الحالي
                    },
                    fields: ['name'] // استرجاع أسماء الموظفين فقط
                },
                callback: function (response) {
                    if (response.message.length > 0) {
                        const employee_options = response.message.map(emp => ({
                            label: emp.name,
                            value: emp.name
                        }));

                        // عرض Prompt مع الموظفين الذين يديرهم المستخدم
                        frappe.prompt(
                            [
                                {
                                    label: 'Employee',
                                    fieldname: 'employee',
                                    fieldtype: 'Select',
                                    options: employee_options,
                                    reqd: 1
                                }
                            ],
                            function (values) {
                                // فتح قائمة الحضور مفلترة حسب اختيار الموظف
                                frappe.set_route('List', 'Attendance', { employee: values.employee });
                            },
                            __('Select Employee'),
                            __('View')
                        );
                    } else {
                        frappe.msgprint(__('You do not manage any employees.'));
                    }
                }
            });
        });
    }
};

*/


