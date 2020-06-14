from core.lib.transactional_manager import TransactionalManager
from services.leave_management.models.leave_dao import LeaveDao


class LeaveHandler:
    "Manages the leaves for a student."
    def __init__(self):
        pass

    def GetStudentLeaves(self, roll_no: int = None, student_id: int = None, class_id: int = None, admission_id: int = None):
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