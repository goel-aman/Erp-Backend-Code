from datetime import datetime
import pandas as pd
import re

import utils
from services.assignment.models.assignment_dao import AssignmentDao, CheckEmployee, AssignmentSubmitDao
from core.lib.transactional_manager import TransactionalManager


class AssignmentHandler():
    """
    """

    def __init__(self):
        pass

    def checkEmployee(self, employee_id):
        """

        :return:
        """
        return_val = None
        return_msg = None
        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READ")

        check = CheckEmployee(db_conn)
        return_val = check.checkEmployee(employee_id)
        return_msg = return_val[0]
        transaction_mgr.end()

        return (return_msg, True) if return_val[1] else (return_msg, False)

    def uploadAssignment(self, employee_id, title, description, deadline, subject, class_, section, list_of_files):
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

        assignment_dao = AssignmentDao(db_conn, class_, section, subject, comma_files, title, description, deadline,
                                       employee_id)

        for file in list_of_files:
            type = re.search('__[\w]+?__', file)
            type = file[type.start(0) + 2:type.end(0) - 2]
            file_ext = file.split('.')[1]
            if type == "manual":
                return_val = ("Inserted Manual Document", True)
            elif type == "subjective" and file_ext.startswith("xls"):
                return_val = assignment_dao.uploadSubjective(employee_id, title, description, deadline, file,
                                                             comma_files, type)
            elif type == "mcq" and file_ext.startswith("xls"):
                return_val = assignment_dao.uploadMCQ(employee_id, title, description, deadline, file, comma_files,
                                                      type)
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

    def assignment_submit(self, student_id: int, assignment_sol):
        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        assignment_dao = AssignmentSubmitDao(db_conn)
        for solutions in assignment_sol:
            question_type = assignment_dao.check_question_type(solutions['question_pool_id'])
            if question_type[0]['question_type_id'] != 3:
                assignment_dao.submit_assignment(student_id, solutions['question_pool_id'], solutions['solution'])
            else:
                assignment_dao.submit_assignment_manual(student_id, solutions['question_pool_id'],
                                                        solutions['solution'])
        assignment_dao.submit_assignment_student(student_id, assignment_sol[0]['question_pool_id'])
        transaction_mgr.save()

    def get_student_assignment_solution(self, assignment_id: int, student_id: int):
        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        assignment_dao = AssignmentSubmitDao(db_conn)
        records = assignment_dao.get_student_assignment_solution(assignment_id, student_id)
        return records

    def get_assignment_history(self, student_id: int):
        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        assignment_dao = AssignmentSubmitDao(db_conn)
        records1 = assignment_dao.get_student_teacher_name(student_id)
        records2 = assignment_dao.get_student_assignment_count(student_id)
        records3 = assignment_dao.get_student_late_assignments(student_id)
        records4 = assignment_dao.get_student_average_marks(student_id)
        records5 = assignment_dao.get_assignment_status(student_id)

        record6 = dict()
        for index in range(0, len(records1)):
            records7 = dict()
            records7.update(
                {"teacher-name": records1[index]['name'], "assignment-count": records2[index]['no_of_assignments'],
                 "late-submission": records3[index]['late_submission'],
                 "average_marks": records4[index]['average_marks'], "status": records5[index]['is_evaluated']})
            record6[records2[index]['name']] = records7

        return (record6)

    def post_assignment_marks(self, teacher_id: int, student_marks):
        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        assignment_dao = AssignmentSubmitDao(db_conn)
        total = 0
        question_pool_id = student_marks[0]['question_pool_id']
        for marks in student_marks:
            total = total + int(marks['marks'])
            question_type = assignment_dao.check_question_type(marks['question_pool_id'])
            if question_type[0]['question_type_id'] != 3:
                assignment_dao.submit_marks(marks['question_pool_id'], marks['student_id'], marks['marks'])
            else:
                assignment_dao.submit_marks_manual(marks['question_pool_id'], marks['student_id'], marks['marks'],
                                                   marks['evaluated_sheet_link'])
        assignment_dao.submit_marks_in_map(total,teacher_id, question_pool_id, student_marks[0]['student_id'])

        transaction_mgr.save()
