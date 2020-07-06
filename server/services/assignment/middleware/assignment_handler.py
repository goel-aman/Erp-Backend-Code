from datetime import datetime
import pandas as pd
import re

import utils
from services.assignment.models.assignment_dao import AssignmentDao, CheckEmployee, AssignmentQuestionsDao
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
