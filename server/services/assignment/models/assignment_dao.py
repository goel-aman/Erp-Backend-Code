import datetime
import calendar
import pandas as pd


class AssignmentDao():

    def __init__(self, db_conn, class_, section, subject, comma_files, title, description, deadline, employee_id):
        self.db_conn = db_conn

        # Fetch class Id,
        self.class_ids = list()
        if len(section) > 1:
            for i in section:
                query = "select class_id from class where standard=%s and section='%s';" % (class_, i)
                records = self.db_conn.processquery(query=query, fetch=True)
                if len(records) > 0:
                    self.class_ids.append(records[0].get("class_id"))

        # Fetch subject Id,
        self.subject_id = None
        query = "select subject_id from subject where name='%s';" % (subject)
        records = self.db_conn.processquery(query=query, fetch=True)
        if len(records) > 0:
            self.subject_id = records[0].get("subject_id")

        # Initiation Date,
        self.today = datetime.datetime.now().strftime("%Y-%m-%d")

        """
            Insert Assignment records, and should be done for only one time for all the Uploads,
            This function also handles manual document uploading, as there is no questions to them,
        """
        for c_id in self.class_ids:
            query = "insert into assignment (title, file_link, description, initiation_date, " \
                    "submission_date, subject_id, class_id, uploaded_by) values " \
                    "('%s', '%s', '%s', '%s', '%s', %s, %s, %s);" % (
                        title, comma_files, description, self.today, deadline, self.subject_id, c_id, employee_id)
            records = self.db_conn.processquery(query=query, fetch=False)

    def uploadSubjective(self, employee_id, title, description, deadline, file, list_of_files, type):
        # try:
        # Query Question Type to fetch the Id with the type,
        query = "select id from question_type where question_type='%s';" % (type)
        records = self.db_conn.processquery(query=query, fetch=True)
        type_id = None
        if len(records) > 0:
            type_id = records[0].get("id")

        return_val = None
        # Insert assignment records for Subjective type,

        excel_data = pd.read_excel(file)
        # creating dataframe,
        df = pd.DataFrame(excel_data)
        # Check if it any value is missing,
        if df.isnull().values.any():
            return_val = "Missing some mandatory values in the rows"
            # drop processing the excel
            return (return_val, False)

        ques_list = df['Questions'].to_list()
        marks_list = df['Marks'].to_list()
        expected_no_of_words = df['No of words'].to_list()

        # Get Assignment Ids for the all sections,
        assign_ids = list()
        for c_id in self.class_ids:
            query = "select assignment_id from assignment where file_link='%s' and class_id=%s;" % (list_of_files, c_id)
            records = self.db_conn.processquery(query=query, fetch=True)
            if len(records) == 1:
                assign_ids.append(records[0].get("assignment_id", ""))

        # Insert into question_pool with the appropriate assignment ids,
        for assign_id in assign_ids:
            for i in range(len(ques_list)):
                query = "insert into question_pool (question_type_id, question, " \
                        "assignment_id, marks, answer, expected_no_of_words) " \
                        "values (%s, '%s', %s, %s, '', %s);" % (
                            type_id, ques_list[i], assign_id, marks_list[i], expected_no_of_words[i])
                records = self.db_conn.processquery(query=query, fetch=False)
        return_val = "Inserted Subjective document"
        return (return_val, True)
        # except:
        #     return "Some error happened!"

    def uploadMCQ(self, employee_id, title, description, deadline, file, list_of_files, type):
        # try:
        # Query Question Type to fetch the Id with the type,
        query = "select id from question_type where question_type='%s';" % (type)
        records = self.db_conn.processquery(query=query, fetch=True)
        type_id = None
        if len(records) > 0:
            type_id = records[0].get("id")

        return_val = None
        """
            Insert assignment records for MCQ type and creating dataframe,
        """
        excel_data = pd.read_excel(file)
        df = pd.DataFrame(excel_data)
        # check if atleast 2 choice column is available
        if df["Choice1"].isnull().values.any() or df["Choice2"].isnull().values.any() \
                or df["Marks"].isnull().values.any() or df["Questions"].isnull().values.any() \
                or df["Answers"].isnull().values.any():
            return_val = "Missing mandatory Column values in the Excel"
            # drop processing the excel
            return (return_val, False)

        # converting nan to None
        # df = pd.where(pd.notnull(df), None)
        df.fillna('None', inplace=True)
        # Converting columns to list
        questions = df['Questions'].to_list()
        marks = df['Marks'].to_list()
        choice1 = df["Choice1"].to_list()
        choice2 = df["Choice2"].to_list()
        choice3 = df["Choice3"].to_list()
        choice4 = df["Choice4"].to_list()
        choice5 = df["Choice5"].to_list()
        choice6 = df["Choice6"].to_list()
        answers = df["Answers"].to_list()

        # Manually converting nan to None, because I just can't run the `where` function,
        # tried uninstalling pandas and reinstalled it still `Attribute Error` raises,
        # that's why this fix.
        for x in range(len(choice3)):
            if choice3[x] == 'None':
                choice3[x] = eval(choice3[x])
            if choice4[x] == 'None':
                choice4[x] = eval(choice4[x])
            if choice5[x] == 'None':
                choice5[x] = eval(choice5[x])
            if choice6[x] == 'None':
                choice6[x] = eval(choice6[x])

        # Get Assignment Ids for the all sections,
        assign_ids = list()
        for c_id in self.class_ids:
            query = "select assignment_id from assignment where file_link='%s' and class_id=%s;" % (list_of_files, c_id)
            records = self.db_conn.processquery(query=query, fetch=True)
            if len(records) == 1:
                assign_ids.append(records[0].get("assignment_id", ""))

        # Insert into question_pool with assignment ids
        for id in assign_ids:
            for i in range(len(questions)):
                choice_3 = "" if choice3[i] == None else choice3[i]
                choice_4 = "" if choice4[i] == None else choice4[i]
                choice_5 = "" if choice5[i] == None else choice5[i]
                choice_6 = "" if choice6[i] == None else choice6[i]
                query = "insert into question_pool (question_type_id, question, " \
                        "assignment_id, marks, choice1, choice2, choice3, choice4, " \
                        "choice5, choice6, answer) values (%s, '%s', %s, %s, '%s', " \
                        "'%s', '%s', '%s', '%s', '%s', '%s');" % (
                            type_id, questions[i], id, marks[i], choice1[i], choice2[i], choice_3, choice_4, choice_5,
                            choice_6, answers[i])
                records = self.db_conn.processquery(query=query, fetch=False)

        return_val = " Inserted MCQ document"
        return (return_val, True)


class AssignmentQuestionsDao():

    def __init__(self, db_conn):
        self.db_conn = db_conn

    def get_assignment_dao(self, assignment_id):

        # To get all the questions of a particular assignment
        query = "select question_pool.id, question_type, question, marks, " \
                "choice1, choice2, choice3, choice4, choice5, choice6 " \
                "from question_pool join question_type " \
                "on question_pool.question_type_id = question_type.id " \
                "where assignment_id = %s" % assignment_id

        question_paper = self.db_conn.processquery(query=query, fetch=True)
        return question_paper

    def get_pending_assignments_dao(self, student_id):

        # To get the pending assignments of a particular student
        query = "select assignment_id, title, description, initiation_date, submission_date, name " \
                "from assignment join subject on assignment.subject_id = subject.subject_id " \
                "where class_id = (select class_id from student_class_mapping where student_id = %s) " \
                "and assignment_id not in (select assignment_id from student_assignment_map where student_id = %s )"\
                % (student_id, student_id)

        pending_assignment = self.db_conn.processquery(query=query, fetch=True)
        return pending_assignment

    def get_completed_assignments_dao(self, student_id, subject_id):

        # To get the pending assignments of a particular student
        query = "select assignment.assignment_id, title, initiation_date, submission_date as deadline, " \
                "submission_datetime, student_assignment_map.marks as scored_marks, sum(question_pool.marks) as total_marks " \
                "from question_pool, assignment, student_assignment_map " \
                "where assignment.assignment_id = student_assignment_map.assignment_id " \
                "and assignment.assignment_id = question_pool.assignment_id " \
                "and student_id = %s and subject_id = %s " \
                "group by assignment.assignment_id" %(student_id, subject_id)

        completed_assignment = self.db_conn.processquery(query=query, fetch=True)
        return completed_assignment

class CheckEmployee():

    def __init__(self, db_conn):
        self.db_conn = db_conn

    def checkEmployee(self, employee_id):
        query = "select username, is_active from users where user_id=%s;" % (employee_id)
        records = self.db_conn.processquery(query=query, fetch=True)

        if len(records) > 0 and records[0].get("is_active") == 1:
            return_val = (records[0], True)
            return return_val

        return ("User doesn't exist", False)
