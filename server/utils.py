import calendar
import datetime

from typing import Tuple


def GetCurrentMonthStartAndEndDate() -> Tuple[str, str]:
    """Gets the current month start date and end date in iso format."""
    today = datetime.date.today()
    start_date = today.replace(day=1).isoformat()
    end_date = today.replace(day=calendar.monthrange(today.year, today.month)[1]).isoformat()
    return start_date, end_date


def GetTodaysDateAsStartAndEndDate() -> Tuple[str, str]:
    today = datetime.date.today().isoformat()
    return today


def GetCummulativeDates() -> Tuple[str, str]:
    today = datetime.date.today()
    session_start_date = today.replace(day=calendar.monthrange(today.year, 4)[0], month=4).isoformat()
    return session_start_date, today.isoformat()


def check_for_all_fields(**kwargs) -> bool:
    """
    Checks for all the field values
    :param kwargs:
    :return: True if all keys are present with proper values else False
    """

    for field, value in kwargs.items():
        if value == "":
            return False
    return True


def check_file_type(file) -> bool:
    """
    Checks for the file type using headers
    :param headers: byte string
    :return: bool
    """
    with open(file, "rb") as fh:
        headers = fh.read()[:6]
    # print('headers', headers)
    if headers.startswith(b'PK\x03\x04\x14\x00') or headers.startswith(b'%PDF-1') or headers.startswith(
            b'\xd0\xcf\x11\xe0'):
        return True
    return False
