from openpyxl import Workbook


SERVICE_USER_DATA_SHEET_NAME = "Service User Data"
SIGN_OFF_SHEET_NAME = "Sign Off Sheet"

ALL_SHEET_NAMES = [SERVICE_USER_DATA_SHEET_NAME, SIGN_OFF_SHEET_NAME]


def check_workbook_has_needed_worksheets(wb: Workbook) -> None:
    for sheet_name in ALL_SHEET_NAMES:
        assert (
            sheet_name in wb.get_sheet_names()
        ), f"Expected worksheet called '{sheet_name}' but couldn't find it - did you change a sheet name?"
