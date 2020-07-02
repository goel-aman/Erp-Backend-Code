from datetime import datetime
import pandas as pd
import re

import utils
from services.assignment.models.assignment_dao import AssignmentDao, CheckEmployee
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


    def uploadAssignment(self, employee_id, title, description, deadline, subject, class_, section, list_of_files, manual_marks):
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

        assignment_dao = AssignmentDao(db_conn, class_=class_, section=section, subject=subject, comma_files=comma_files, \
                                       title=title, description=description, deadline=deadline, employee_id=employee_id)

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
