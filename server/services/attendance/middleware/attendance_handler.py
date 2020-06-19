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
    
    # CRUD OPERATIONS RELATED TO SINGLE STUDENT


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
    
    

    def PostStudentAttendance(
            self, student_id: int, start_date: str = None, end_date: str = None, status: str = None, time: str = None):
        """Post the student attendance based on start date and end date and student id"""
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
        attendance_dates_status_map = attendance_dao.PostAttendanceByStudentId(
                student_id, start_date, end_date, status)
        # Formulate data.
        # Return formulated data.
        
        #return attendance_dates_status_map
        return "ok"
    
    def PutStudentAttendance(
            self, student_id: int, start_date: str = None, end_date: str = None, status: str = None, time: str = None):
        """Put the student attendance based on start date and end date and student id"""
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

        # JUST SOME TESTING

        print("         attendance handler put     ")
        print(student_id,start_date,end_date,status)


        # Make dao request to get the data.
        attendance_dates_status_map = attendance_dao.PutAttendanceByStudentId(
                student_id, start_date, end_date, status)
        # Formulate data.
        # Return formulated data.
        return 'ok'
        #return attendance_dates_status_map
    
    def DeleteStudentAttendance(
            self, student_id: int, start_date: str = None, end_date: str = None, time: str = None):
        """Put the student attendance based on start date and end date and student id"""
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
        attendance_dates_status_map = attendance_dao.DeleteAttendanceByStudentId(
                student_id, start_date, end_date)
        # Formulate data.
        # Return formulated data.
        return 'ok'
        #return attendance_dates_status_map
    
    # CRUD OPERATIONS FOR THE WHOLE CLASS
    
    def GetStudentsAttendance(
            self, class_id: int, start_date: str = None, end_date: str = None, time: str = None):
        """Get the student attendance based on start date and end date."""
        if not class_id:
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
        attendance_dates_status_map = attendance_dao.GetAttendanceByClassId(
                class_id, start_date, end_date)
        # Formulate data.
        # Return formulated data.
        
        return attendance_dates_status_map

    def PostStudentsAttendance(
            self, class_id: int, roll_no: int, start_date: str = None, end_date: str = None, status: str = None, time: str = None):
        """Post the student attendance based on start date and end date and student id"""
        if not class_id:
            return Exception # Return No Student Id exception
        
        # schema validate.
        if time in TIME_FREQUENCY_DATE_FUNCTION_MAP:
            start_date, end_date = TIME_FREQUENCY_DATE_FUNCTION_MAP[time]()
        
        if not start_date or not end_date:
            start_date = end_date = utils.GetTodaysDateAsStartAndEndDate()

        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        attendance_dao = AttendanceDao(db_conn)

        #JUST SOME TESTING

        print("    attendance_handler class post working    ")
        print(class_id,roll_no,start_date,end_date,status)


        # Make dao request to get the data.
        attendance_dates_status_map = attendance_dao.PostAttendanceByClassId(
                class_id, roll_no, start_date, end_date, status)
        # Formulate data.
        # Return formulated data.
        
        return attendance_dates_status_map
    
    def UpdateStudentsAttendance(
            self, class_id: int, roll_no: int, start_date: str = None, end_date: str = None, status: str = None, time: str = None):
        """Post the student attendance based on start date and end date and student id"""
        if not class_id:
            return Exception # Return No Student Id exception
        
        # schema validate.
        if time in TIME_FREQUENCY_DATE_FUNCTION_MAP:
            start_date, end_date = TIME_FREQUENCY_DATE_FUNCTION_MAP[time]()
        
        if not start_date or not end_date:
            start_date = end_date = utils.GetTodaysDateAsStartAndEndDate()

        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        attendance_dao = AttendanceDao(db_conn)

        # JUST SOME TESTING 

        print("    attendance_handler class put working    ")
        print(class_id,roll_no,start_date,end_date,status)


        # Make dao request to get the data.
        attendance_dates_status_map = attendance_dao.UpdateAttendanceByClassId(
                class_id, roll_no, start_date, end_date, status)
        # Formulate data.
        # Return formulated data.
        
        return attendance_dates_status_map

    def DeleteStudentsAttendance(
            self, class_id: int, start_date: str = None, end_date: str = None, time: str = None):
        """Post the student attendance based on start date and end date and student id"""
        if not class_id:
            return Exception # Return No Student Id exception
        
        # schema validate.
        if time in TIME_FREQUENCY_DATE_FUNCTION_MAP:
            start_date, end_date = TIME_FREQUENCY_DATE_FUNCTION_MAP[time]()
        
        if not start_date or not end_date:
            start_date = end_date = utils.GetTodaysDateAsStartAndEndDate()

        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        attendance_dao = AttendanceDao(db_conn)

        #JUST SOME TESTING

        print("    attendance_handler class delete working    ")
        print(class_id,start_date,end_date)

        
        # Make dao request to get the data.
        attendance_dates_status_map = attendance_dao.DeleteAttendanceByClassId(
                class_id, start_date, end_date)
        # Formulate data.
        # Return formulated data.
        return 'ok'
        #return attendance_dates_status_map