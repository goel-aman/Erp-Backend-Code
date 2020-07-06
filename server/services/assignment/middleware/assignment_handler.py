from datetime import datetime
import pandas as pd
import re

import utils
from services.assignment.models.assignment_dao import AssignmentDao, CheckUser, AssignmentView
from core.lib.transactional_manager import TransactionalManager


class AssignmentHandler:
    """
    """
    def __init__(self):
        pass

    def checkUser(self, employee_id="", teacher_id=""):
        """
        :return:
        """
        return_val = None
        return_msg = None
        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READ")

        if employee_id != "":
            check = CheckUser(db_conn)
            return_val = check.checkEmployee(employee_id)
            return_msg = return_val[0]
        elif teacher_id != "":
            check = CheckUser(db_conn)
            return_val = check.checkTeacher(teacher_id)
            return_msg = return_val[0]

        transaction_mgr.end()

        return (return_msg, True) if return_val[1] else (return_msg, False)

    def uploadAssignment(self, user_id, title, description, deadline, subject, class_, section, list_of_files, manual_marks):
        """
        :return:
        """
        return_val = None
        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")

        section = re.findall('\w+', section)
        return_msg = ""

        # comma separate all files
        comma_files = str()
        for file_count in range(0, len(list_of_files)):
            comma_files = comma_files + list_of_files[file_count]
            if file_count <= len(list_of_files) - 2:
                comma_files += ", "

        assignment_dao = AssignmentDao(db_conn, class_=class_, section=section, subject=subject, \
                                       comma_files=comma_files, title=title, description=description, \
                                       deadline=deadline, user_id=user_id)

        for file in list_of_files:
            # Fetching assignment type,
            type = re.search('__[\w]+?__', file)
            type = file[type.start(0)+2:type.end(0)-2]
            file_ext = file.split('.')[1]
            # Fetching file number for manual marks,
            file_num = re.search('_file\d{1}?_', file)
            file_num = file[file_num.start(0)+1 : file_num.end(0)-1]
            if type == "manual":
                mark = manual_marks.get(file_num, "")
                return_val = assignment_dao.uploadManual(file, comma_files, mark, type)
            elif type == "subjective" and file_ext.startswith("xls"):
                return_val = assignment_dao.uploadSubjective(file, comma_files, type)
            elif type == "mcq" and file_ext.startswith("xls"):
                return_val = assignment_dao.uploadMCQ(file, comma_files, type)
            # Break if any one fails
            if return_val[1] == True:
                return_msg += " " + return_val[0]
            else:
                break

        if return_val[1] == True:
            transaction_mgr.save()
            return return_msg

        transaction_mgr.end()
        return return_msg

    def deleteAssignment(self, user_id, assignment_id):
        """

        :param employee_id:
        :param assignment_id:
        :return:
        """
        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")

        assignment_dao = AssignmentDao(db_conn)
        return_val = assignment_dao.deleteAssignment(user_id, assignment_id)

        if return_val[1]:
            transaction_mgr.save()
            return return_val

        transaction_mgr.end()
        return return_val


class AssignmentViewHandler:
    """
    """
    def __init__(self):
        pass

    def TeacherAssignmentView(self, user_id, teacher_id, class_, section, subject):
        """
        :return:
        """
        return_val = None
        transaction_manager = TransactionalManager()
        db_conn = transaction_manager.GetDatabaseConnection("READWRITE")

        assignment_view = AssignmentView(db_conn)
        return_val = assignment_view.assignmentByClassSubjectId(user_id, teacher_id, class_, section, subject)

        if return_val[1] == True:
            transaction_manager.save()
            return return_val[0]

        transaction_manager.end()
        return return_val[0]

    def AssignmentStudentDetailView(self, assignment_id, teacher_id):
        """
        :param assignment_id:
        :return:
        """
        return_val = None
        transaction_manager = TransactionalManager()
        db_conn = transaction_manager.GetDatabaseConnection("READ")

        assignment_view = AssignmentView(db_conn)
        return_val = assignment_view.studentSubmissionsViewByAssignment(assignment_id, teacher_id)

        if return_val[1] == True:
            transaction_manager.save()
            return return_val[0]

        transaction_manager.end()
        return return_val[0]
