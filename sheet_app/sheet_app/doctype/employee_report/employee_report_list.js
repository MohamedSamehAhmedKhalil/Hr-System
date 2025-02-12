frappe.listview_settings['Employee Report'] = {
    onload: function(listview) {
        frappe.realtime.on("refresh_employee_report", function() {
            listview.refresh(); 
        });
    }
};
