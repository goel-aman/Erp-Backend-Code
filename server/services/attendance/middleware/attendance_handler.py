import utils
import holidays
import datetime
from datetime import datetime
import holidays

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
            self, student_id: int, start_date: str = None, end_date: str = None):
        """Get the student attendance based on start date and end date."""
        if not start_date or not end_date:
            start_date = end_date = utils.GetTodaysDateAsStartAndEndDate()

        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        attendance_dao = AttendanceDao(db_conn)

        # Make dao request to get the data.
        attendance_dates_status_map = attendance_dao.GetAttendanceByStudentId(
            student_id, start_date, end_date)
        for attendance_records in attendance_dates_status_map:
            attendance_records['attendance_date'] = attendance_records['attendance_date'].strftime("%Y-%m-%d")

        return attendance_dates_status_map

    def PostStudentAttendance(self, student_id: int, updated_by: int, start_date: str = None, end_date: str = None,
                              status: str = None):
        """Post the student attendance based on start date and end date and student id"""
        if not start_date or not end_date:
            start_date = end_date = utils.GetTodaysDateAsStartAndEndDate()

        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        attendance_dao = AttendanceDao(db_conn)

        # Make dao request to get the data.
        attendance_dates_status_map = attendance_dao.PostAttendanceByStudentId(
            student_id, updated_by, start_date, end_date, status, )
        transaction_mgr.save()

    def PutStudentAttendance(
            self, student_id: int, start_date: str = None, end_date: str = None, status: str = None):
        """Put the student attendance based on start date and end date and student id"""
        if not start_date or not end_date:
            start_date = end_date = utils.GetTodaysDateAsStartAndEndDate()

        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        attendance_dao = AttendanceDao(db_conn)
        attendance_dates_status_map = attendance_dao.PutAttendanceByStudentId(
            student_id, start_date, end_date, status)
        transaction_mgr.save()

    def DeleteStudentAttendance(
            self, student_id: int, start_date: str = None, end_date: str = None):
        """Put the student attendance based on start date and end date and student id"""
        if not start_date or not end_date:
            start_date = end_date = utils.GetTodaysDateAsStartAndEndDate()

        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        attendance_dao = AttendanceDao(db_conn)

        # Make dao request to get the data.
        attendance_dates_status_map = attendance_dao.DeleteAttendanceByStudentId(
            student_id, start_date, end_date)
        transaction_mgr.save()

    # CRUD OPERATIONS FOR THE WHOLE CLASS

    def GetStudentsAttendance(
            self, class_id: int, start_date: str = None, end_date: str = None):
        """Get the student attendance based on start date and end date."""
        if not start_date or not end_date:
            start_date = end_date = utils.GetTodaysDateAsStartAndEndDate()

        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        attendance_dao = AttendanceDao(db_conn)

        # Make dao request to get the data.
        attendance_dates_status_map = attendance_dao.GetAttendanceByClassId(
            class_id, start_date, end_date)
        for attendance_records in attendance_dates_status_map:
            attendance_records['attendance_date'] = attendance_records['attendance_date'].strftime("%Y-%m-%d")
        # Formulate data.
        # Return formulated data.

        return attendance_dates_status_map

    def PostStudentsAttendance(
            self, class_id: int, updated_by: int, roll_no: int, start_date: str = None, end_date: str = None,
            status: str = None):
        """Post the student attendance based on start date and end date and student id"""
        if not start_date or not end_date:
            start_date = end_date = utils.GetTodaysDateAsStartAndEndDate()

        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        attendance_dao = AttendanceDao(db_conn)

        attendance_dates_status_map = attendance_dao.PostAttendanceByClassId(
            class_id, updated_by, roll_no, start_date, end_date, status)
        transaction_mgr.save()
        # Formulate data.
        # Return formulated data.

    def UpdateStudentsAttendance(self, class_id: int, roll_no: int, start_date: str = None, end_date: str = None,
                                 status: str = None):
        """Post the student attendance based on start date and end date and student id"""
        if not start_date or not end_date:
            start_date = end_date = utils.GetTodaysDateAsStartAndEndDate()

        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        attendance_dao = AttendanceDao(db_conn)

        attendance_dates_status_map = attendance_dao.UpdateAttendanceByClassId(
            class_id, roll_no, start_date, end_date, status)
        # Formulate data.
        # Return formulated data.
        transaction_mgr.save()

    def DeleteStudentsAttendance(
            self, class_id: int, start_date: str = None, end_date: str = None):
        """Post the student attendance based on start date and end date and student id"""
        if not start_date or not end_date:
            start_date = end_date = utils.GetTodaysDateAsStartAndEndDate()

        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        attendance_dao = AttendanceDao(db_conn)

        attendance_dates_status_map = attendance_dao.DeleteAttendanceByClassId(
            class_id, start_date, end_date)
        transaction_mgr.save()

    def DashboardDataCard1(self, student_id: int):
        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        attendance_dao = AttendanceDao(db_conn)

        card1_data = attendance_dao.DashboardCard1(student_id)
        return card1_data

    def DashboardDataCard2(self, student_id: int):
        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        attendance_dao = AttendanceDao(db_conn)

        card2_data = attendance_dao.DashboardCard2(student_id)

        for leave_record in card2_data:
            leave_record['attendance_date'] = leave_record['attendance_date'].strftime(
                '%Y-%m-%d')

        return card2_data

    def dashboard_data_card3(self, student_id: int):
        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        attendance_dao = AttendanceDao(db_conn)
        card3_data_absent_days = attendance_dao.dashboard_card3_absent_days(
            student_id)
        for absent_days_record in card3_data_absent_days:
            absent_days_record['attendance_date'] = absent_days_record['attendance_date'].strftime(
                '%Y-%m-%d')
        card3_data_late_days = attendance_dao.dashboard_card3_late_days(
            student_id)
        for late_days_record in card3_data_late_days:
            late_days_record['attendance_date'] = late_days_record['attendance_date'].strftime(
                '%Y-%m-%d')

        holiday_list = []
        for ptr in holidays.India(years=2020).items():
            holiday_list.append(ptr[0].strftime('%Y-%m-%d'))
        card3_data_holidays = holiday_list
        card3_data = {"absent_days": card3_data_absent_days,
                      "late_days": card3_data_late_days, "holidays": card3_data_holidays}
        return card3_data

    def DashboardDataCard4(self, student_id: int):
        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        attendance_dao = AttendanceDao(db_conn)

        card4_data_your_attendance = attendance_dao.DashboardCard4your_attendance(
            student_id)
        card4_data_highest_attendance = attendance_dao.dashboard_card4_highest_attendance(
            student_id)
        card4_data_average_attendance = attendance_dao.dashboard_card4_average_attendance(
            student_id)
        card4_data = {"your_attendance": card4_data_your_attendance, "highest_attendance":
            card4_data_highest_attendance, "average_attendance": card4_data_average_attendance}
        return card4_data

    def GetStudentLatestDateAttendance(self):
        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        attendance_dao = AttendanceDao(db_conn)

        modified_attendance = []
        modified_record = {}
        student_daily_attendance = attendance_dao.GetStudentLatestDateAttendance()

        for record in student_daily_attendance:
            value = float("{:.2f}".format(record['count'] * 100 / student_daily_attendance[-1]['count']))
            if record['status'] == 'A':
                modified_record['Absent'] = value
            elif record['status'] == 'P':
                modified_record['Present'] = value
            elif record['status'] == 'L':
                modified_record['Late'] = value

        if 'Present' not in modified_record:
            modified_record['Present'] = 0
        if 'Absent' not in modified_record:
            modified_record['Absent'] = 0
        if 'Late' not in modified_record:
            modified_record['Late'] = 0

        modified_attendance.append(modified_record)
        return modified_attendance

    def GetStudentLatestDateAttendanceDetails(self):
        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        attendance_dao = AttendanceDao(db_conn)

        student_latest_attendance_details = attendance_dao.GetStudentLatestDateAttendanceDetails()
        for record in student_latest_attendance_details:
            record['student_name'] = f"{record['student_fname']} {record['student_lname']}"
            record['class_name'] = f"{record['standard']} - {record['section']}"
            record['parent_notified'] = "Informed" if record['parent_notified'] == 1 else "Uninformed"
            record['parent_acknowledged'] = "Acknowledged" if record['parent_acknowledged'] == 1 else "Unacknowledged"
            record.pop('student_fname')
            record.pop('student_lname')
            record.pop('standard')
            record.pop('section')
        return student_latest_attendance_details

    def GetStudentsLowAttendance(self):
        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        attendance_dao = AttendanceDao(db_conn)

        low_attendance = attendance_dao.GetStudentsLowAttendance()
        for record in low_attendance:
            record['percent'] = float("{:.2f}".format(record['present'] * 100 / record['working']))
            record['student_name'] = f"{record['student_fname']} {record['student_lname']}"
            record['class_name'] = f"{record['standard']} - {record['section']}"
            record.pop('standard')
            record.pop('section')
            record.pop('student_fname')
            record.pop('student_lname')
            record.pop('present')
            record.pop('working')

        return low_attendance

    def GetStudentAttendanceByName(self, student_name: str):

        student_fname, student_lname = student_name.split(' ')

        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        attendance_dao = AttendanceDao(db_conn)

        attendance_by_name = attendance_dao.GetStudentAttendanceByName(student_fname, student_lname)
        for record in attendance_by_name:
            record['attendance_date'] = record['attendance_date'].strftime("%Y-%m-%d")
            record['percent'] = float("{:.2f}".format(record['present'] * 100 / record['working']))
            record['acknowledged'] = "Yes" if record['parent_acknowledged'] is 1 else "No"
            record['student_name'] = f"{record['student_fname']} {record['student_lname']}"
            record.pop('student_fname')
            record.pop('student_lname')
            record.pop('parent_acknowledged')
            record.pop('present')
            record.pop('working')

        return attendance_by_name

    def PostTeacherAttendance(self, form):

        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        attendance_dao = AttendanceDao(db_conn)

        attendance_dao.PostTeacherAttendance(form)

        transaction_mgr.save()

    def GetTeacherLatestDateAttendance(self):

        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        attendance_dao = AttendanceDao(db_conn)

        modified_attendance = []
        modified_record = {}
        teacher_daily_attendance = attendance_dao.GetTeacherLatestDateAttendance()

        for record in teacher_daily_attendance:
            value = float("{:.2f}".format(record['count'] * 100 / teacher_daily_attendance[-1]['count']))
            if record['status'] == 'A':
                modified_record['Absent'] = value
            elif record['status'] == 'P':
                modified_record['Present'] = value
            elif record['status'] == 'L':
                modified_record['Late'] = value

        if 'Present' not in modified_record:
            modified_record['Present'] = 0
        if 'Absent' not in modified_record:
            modified_record['Absent'] = 0
        if 'Late' not in modified_record:
            modified_record['Late'] = 0

        modified_attendance.append(modified_record)
        return modified_attendance

    def GetTeacherLatestDateAttendanceDetails(self):
        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        attendance_dao = AttendanceDao(db_conn)

        teacher_latest_attendance_details = attendance_dao.GetTeacherLatestDateAttendanceDetails()

        return teacher_latest_attendance_details

    def GetTeacherAttendanceByName(self, teacher_name: str):

        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        attendance_dao = AttendanceDao(db_conn)

        attendance_by_name = attendance_dao.GetTeacherAttendanceByName(teacher_name)
        for record in attendance_by_name:
            record['attendance_date'] = record['attendance_date'].strftime("%Y-%m-%d")

        return attendance_by_name

    def TeacherDashboardLineGraph(self, class_id: int):
        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        attendance_dao = AttendanceDao(db_conn)
        highest_attendance = attendance_dao.teacher_dashboard_highest_attendance(class_id)
        average_attendance = attendance_dao.teacher_dashboard_average_attendance(class_id)
        lowest_attendance = attendance_dao.teacher_dashboard_worst_attendance(class_id)
        return {"highest_attendance": highest_attendance, "average_attendance": average_attendance,
                "lowest_attendance": lowest_attendance}

    def GetTeacherAttendanceReport(self):

        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        attendance_dao = AttendanceDao(db_conn)

        teacher_attendance_report = attendance_dao.GetTeacherAttendanceReport()

        return teacher_attendance_report

    def GetTeacherAttendanceReportByName(self, emp_id):

        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        attendance_dao = AttendanceDao(db_conn)

        teacher_attendance_report_name = attendance_dao.GetTeacherAttendanceReportByName(emp_id)

        for record in teacher_attendance_report_name:
            record['attendance_date'] = record['attendance_date'].strftime("%Y-%m-%d")

        return teacher_attendance_report_name