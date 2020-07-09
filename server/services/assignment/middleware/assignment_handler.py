from datetime import datetime
import pandas as pd
import re

import utils
from services.assignment.models.assignment_dao import AssignmentDao, CheckUser, AssignmentView, AssignmentSubmitDao, AssignmentQuestionsDao
from core.lib.transactional_manager import TransactionalManager


class AssignmentHandler:
    """
    """
    def __init__(self):
        pass

    def check_user(self, employee_id="", teacher_id=""):
        """
        :return:
        """
        return_val = None
        return_msg = None
        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READ")

        if employee_id != "":
            check = CheckUser(db_conn)
            return_val = check.check_employee(employee_id)
            return_msg = return_val[0]
        elif teacher_id != "":
            check = CheckUser(db_conn)
            return_val = check.check_teacher(teacher_id)
            return_msg = return_val[0]

        transaction_mgr.end()

        return (return_msg, True) if return_val[1] else (return_msg, False)

    def upload_assignment(self, user_id, title, description, deadline, subject, class_, section, list_of_files, manual_marks):
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
                return_val = assignment_dao.upload_manual(file, comma_files, mark, type)
            elif type == "subjective" and file_ext.startswith("xls"):
                return_val = assignment_dao.upload_subjective(file, comma_files, type)
            elif type == "mcq" and file_ext.startswith("xls"):
                return_val = assignment_dao.upload_MCQ(file, comma_files, type)
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

    def delete_assignment(self, user_id, assignment_id):
        """

        :param employee_id:
        :param assignment_id:
        :return:
        """
        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")

        assignment_dao = AssignmentDao(db_conn)
        return_val = assignment_dao.delete_assignment_dao(user_id, assignment_id)

        if return_val[1]:
            transaction_mgr.save()
            return return_val

        transaction_mgr.end()
        return return_val

    def active_assignments(self, user_id):
        """
        :param user_id:
        :return:
        """
        return_val = None
        transaction_manager = TransactionalManager()
        db_conn = transaction_manager.GetDatabaseConnection("READWRITE")

        assignment_view = AssignmentDao(db_conn)
        return_val = assignment_view.active_assignment_by_userid(user_id)

        if return_val[1] == True:
            transaction_manager.save()
            return return_val[0]

        transaction_manager.end()
        return return_val[0]


class AssignmentViewHandler:
    """
    """
    def __init__(self):
        pass

    def teacher_assignment_view(self, user_id, teacher_id, class_, section, subject):
        """
        :return:
        """
        return_val = None
        transaction_manager = TransactionalManager()
        db_conn = transaction_manager.GetDatabaseConnection("READWRITE")

        assignment_view = AssignmentView(db_conn)
        return_val = assignment_view.assignment_by_class_subject_id(user_id, teacher_id, class_, section, subject)

        if return_val[1] == True:
            transaction_manager.save()
            return return_val[0]

        transaction_manager.end()
        return return_val[0]

    def assignment_student_detail_view(self, assignment_id, teacher_id):
        """
        :param assignment_id:
        :return:
        """
        return_val = None
        transaction_manager = TransactionalManager()
        db_conn = transaction_manager.GetDatabaseConnection("READ")

        assignment_view = AssignmentView(db_conn)
        return_val = assignment_view.student_submissions_view_by_assignment(assignment_id, teacher_id)

        if return_val[1] == True:
            transaction_manager.save()
            return return_val[0]

        transaction_manager.end()
        return return_val[0]

    def assignment_submit(self, student_id: int, assignment_sol):
        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        assignment_dao = AssignmentSubmitDao(db_conn)
        for solutions in assignment_sol:
            question_type = assignment_dao.check_question_type(solutions['question_pool_id'])
            if question_type[0]['question_type_id'] != 3:
                assignment_dao.submit_assignment(student_id, solutions['question_pool_id'], solutions['solution'])
            else:
                assignment_dao.submit_assignment_manual(student_id, solutions['question_pool_id'], solutions['solution'])
        assignment_dao.submit_assignment_student(student_id, assignment_sol[0]['question_pool_id'])
        transaction_mgr.save()

    def get_student_assignment_solution(self, assignment_id: int, student_id: int):
        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        assignment_dao = AssignmentSubmitDao(db_conn)
        records = assignment_dao.get_student_assignment_solution(assignment_id, student_id)
        return records

    def get_assignment(self, assignment_id):

        # Creating a connection with the database
        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        assignment_dao = AssignmentQuestionsDao(db_conn)

        # Calling the DAO
        question_paper = assignment_dao.get_assignment_dao(assignment_id)

        # To store the non-null or non-empty records
        modified_question_paper = []
        for record in question_paper:
            new_record = {}
            for key, value in record.items():
                if value is not None and value != "":
                    new_record[key] = value
            modified_question_paper.append(new_record)

        return modified_question_paper

    def get_pending_assignment_handler(self, student_id):

        # Creating a connection with the database
        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        assignment_dao = AssignmentQuestionsDao(db_conn)

        # Calling the DAO
        pending_assignment = assignment_dao.get_pending_assignments_dao(student_id)

        # Modifying the date to appropriate format
        for record in pending_assignment:
            record['initiation_date'] = record['initiation_date'].strftime("%Y-%m-%d")
            record['submission_date'] = record['submission_date'].strftime("%Y-%m-%d")

        return pending_assignment

    def get_completed_assignment_handler(self, student_id, subject_id):

        # Creating a connection with the database
        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")
        assignment_dao = AssignmentQuestionsDao(db_conn)

        # Calling the DAO
        completed_assignment = assignment_dao.get_completed_assignments_dao(student_id, subject_id)

        # Modifying the date to appropriate format and adding the percentage
        for record in completed_assignment:
            record['initiation_date'] = record['initiation_date'].strftime("%Y-%m-%d")
            record['deadline'] = record['deadline'].strftime("%Y-%m-%d")
            record['submission_datetime'] = record['submission_datetime'].strftime("%Y-%m-%d")
            record['total_marks'] = float("{:.2f}".format(record['total_marks']))
            record['percentage'] = float("{:.2f}".format(record['scored_marks']*100/record['total_marks']))

        return completed_assignment

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
