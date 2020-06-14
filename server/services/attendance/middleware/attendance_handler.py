import utils

from services.attendance.models.attendance_dao import AttendanceDao
from core.lib.transactional_manager import TransactionalManager


TIME_FREQUENCY_DATE_FUNCTION_MAP = {
    'month': utils.GetCurrentMonthStartAndEndDate, 
    'cummulative': utils.GetCummulativeDates, 
    'today': utils.GetTodaysDateAsStartAndEndDate,
}


class AttendanceHandler():
    def __init__(self):
        pass
    
    def GetStudentAttendance(
            self, student_id: int, start_date: str = None, end_date: str = None, time: str = None):
        """Get the student attendance based on start date and end date."""
        if not student_id:
            return Exception # Return No Student Id exception
        
        # schema validate.
        if time in TIME_FREQUENCY_DATE_FUNCTION_MAP:
            start_date, end_date = TIME_FREQUENCY_DATE_FUNCTION_MAP[time]()
        
        if not start_date or not end_date:
            start_date = end_date = utils.GetTodaysDateAsStartAndEndDate()

        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        attendance_dao = AttendanceDao(db_conn)
        
        # Make dao request to get the data.
        attendance_dates_status_map = attendance_dao.GetAttendanceByStudentId(
                student_id, start_date, end_date)
        # Formulate data.
        # Return formulated data.
        return attendance_dates_status_map   