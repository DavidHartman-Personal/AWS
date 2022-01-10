from excel_utilities import excel_workbook

if __name__ == "__main__":
    service_offering_excel_workbook = "C:\\Users\\dhartman\\Documents\\Support\\AWS-Resources-Production.xlsx"
    # Run the function to return a dictionary of all tables in the Excel workbook
    # tables_dict = get_all_tables(filename=service_offering_excel_workbook)
    wb = excel_workbook.list_worksheets(service_offering_excel_workbook)