"""This script will pull in the Business Service Offerings (PTC Products) worksheet and store as needed

This script will extract the service offerings table from an Excel worksheet that contains the table
and export that to a JSON format to be used by other processes.

"""
from excel_models import ExcelWorkbook

if __name__ == "__main__":
    service_offering_excel_workbook = "C:\\Users\\dhartman\\Documents\\Support\\AWS-Resources-Production.xlsx"
    business_services_worksheet_name = "BusinessServivces"
    business_services_table = "BUSINESS_SERVICE_OFFERINGS"

    wb = ExcelWorkbook(workbook_filename=service_offering_excel_workbook)

    service_offerings_table = get_worksheet_table(ws, "SERVICE_OFFERINGS")
    filtered_offerings_list = [row for row in service_offerings_table
                               if "INNIO" in row['COMPANY'].upper()]
    print(str(filtered_offerings_list))
