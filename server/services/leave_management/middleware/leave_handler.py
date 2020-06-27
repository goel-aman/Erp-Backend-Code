from core.lib.transactional_manager import TransactionalManager
from services.leave_management.models.leave_dao import LeaveDao
from datetime import datetime


class LeaveHandler:
    "Manages the leaves for a student."

    def __init__(self):
        pass

    def GetStudentLeaves(self, roll_no: int = None, student_id: int = None, class_id: int = None,
                         admission_id: int = None):
        # Initiate Transaction manager
        transaction_manager = TransactionalManager()
        try:
            db_conn = transaction_manager.GetDatabaseConnection("READ")
            leave_dao = LeaveDao(db_conn)
            student_leaves = None
            if admission_id:
                student_leaves = leave_dao.GetLeavesByAdmissionNo(admission_id)
            elif roll_no:
                if class_id:
                    student_leaves = leave_dao.GetLeavesByStudentClassId(roll_no, class_id)
                else:
                    raise Exception('Class id is required with student roll no.')
            elif student_id:
                student_leaves = leave_dao.GetStudentLeavesById(student_id)
            transaction_manager.end()
            return student_leaves
        # Add specific exceptions.
        except Exception:
            # Log exception.
            print("Exception occurred while fetching leaves for a user.")
            transaction_manager.end()
            raise

    def post_leave(self, user_id: int, start_date: str, end_date: str, type_of_leave: str, reason: str):

        """ this function is used to post a leave given the employee_id, start_date, end_date, type_of_leave
        reason"""

        transaction_manager = TransactionalManager()
        db_conn = transaction_manager.GetDatabaseConnection("READWRITE")
        leave_dao = LeaveDao(db_conn)
        leave_dao.post_leave(user_id, start_date, end_date, type_of_leave, reason)
        transaction_manager.save()

    def get_leave_record(self, user_id: int):
        """ to get the leave records based on the user id"""

        transaction_manager = TransactionalManager()
        db_conn = transaction_manager.GetDatabaseConnection("READWRITE")
        leave_dao = LeaveDao(db_conn)
        records = leave_dao.get_leave(user_id)
        for leave_records in records:
            leave_records['start_date'] = leave_records['start_date'].strftime('%Y-%m-%d')
            leave_records['end_date'] = leave_records['end_date'].strftime('%Y-%m-%d')
        return records

    def post_leave_status_admin(self, leave_id: int, status: str):
        """ this function is used to update the status of the leave given by employee """

        transaction_manager = TransactionalManager()
        db_conn = transaction_manager.GetDatabaseConnection("READWRITE")
        leave_dao = LeaveDao(db_conn)
        leave_dao.post_leave_status_admin(leave_id, status)
        transaction_manager.save()

    def get_leave_record_admin(self, leave_id):
        """this function return the leave record of an employee given the leave id """
        transaction_manager = TransactionalManager()
        db_conn = transaction_manager.GetDatabaseConnection("READWRITE")
        leave_dao = LeaveDao(db_conn)
        records = leave_dao.get_leave_record_admin(leave_id)
        for leave_records in records:
            leave_records['start_date'] = leave_records['start_date'].strftime('%Y-%m-%d')
            leave_records['end_date'] = leave_records['end_date'].strftime('%Y-%m-%d')
        return records

    def get_leave_history_record_teacher(self, employee_id: int):
        transaction_manager = TransactionalManager()
        db_conn = transaction_manager.GetDatabaseConnection("READWRITE")
        leave_dao = LeaveDao(db_conn)
        records = leave_dao.get_leave_history_record_teacher(employee_id)
        for leave_records in records:
            leave_records['attendance_date'] = leave_records['attendance_date'].strftime("%Y-%m-%d")
            if leave_records['type_of_leave'] == None:
                leave_records['type_of_leave'] = "N/A"
        return records

    def get_leave_category_record_teacher(self, employee_id: int):
        transaction_manager = TransactionalManager()
        db_conn = transaction_manager.GetDatabaseConnection("READWRITE")
        leave_dao = LeaveDao(db_conn)
        records = leave_dao.get_leave_category_record_teacher(employee_id)
        return records

    def UpdateStudentLeavesByParent(self, student_id: int = None, leave_date: str = None, remarks: str = None):
        transaction_manager = TransactionalManager()
        try:
            db_conn = transaction_manager.GetDatabaseConnection("READWRITE")
            leave_dao = LeaveDao(db_conn)
            status = None
            if student_id and leave_date and remarks:
                status = leave_dao.UpdateStudentLeaves(student_id, leave_date, remarks)
            transaction_manager.save()
            return status
        # Add specific exceptions.
        except Exception:
            # Log exception.
            print("Exception occurred while fetching leaves for a user.")
            transaction_manager.end()
            raise
