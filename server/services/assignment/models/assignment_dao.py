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


class AssignmentSubmitDao():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def submit_assignment(self, student_id, question_pool_id, solution):
        query = "insert into quiz_response (student_id, question_pool_id, answer) values " \
                "(%s, %s,'%s')" % (student_id, question_pool_id, solution)
        self.db_conn.processquery(query=query, fetch=False)

    def submit_assignment_manual(self, student_id: int, question_pool_id, solution):
        query = "insert into quiz_response (student_id, question_pool_id, response_sheet_link) values " \
                "(%s, %s,'%s')" % (student_id, question_pool_id, solution)
        self.db_conn.processquery(query=query, fetch=False)

    def submit_assignment_student(self, student_id: int, question_pool_id: int):
        query = "select assignment_id from question_pool where id=%s" % (question_pool_id)
        records1 = self.db_conn.processquery(query=query, fetch=True)
        query = "select class_id from student_class_mapping where student_id = %s " % (student_id)
        records2 = self.db_conn.processquery(query=query, fetch=True)
        query = "insert into student_assignment_map (assignment_id, class_id, student_id, submission_datetime)" \
                " values (%s, %s, %s, now())" % (records1[0]['assignment_id'], records2[0]['class_id'], student_id)
        self.db_conn.processquery(query=query, fetch=False)

    def check_question_type(self, question_pool_id: int):
        query = "select qp.question_type_id from question_pool qp where qp.id= %s" % (question_pool_id)
        records = self.db_conn.processquery(query=query, fetch=True)
        return records

    def get_student_assignment_solution(self, assignment_id: int, student_id: int):
        query = "select question_pool_id, answer , response_sheet_link from quiz_response where question_pool_id in" \
                " (select id from question_pool where assignment_id= %s) and student_id=%s" % (
                    assignment_id, student_id)
        records = self.db_conn.processquery(query=query, fetch=True)

        return records

    def get_student_teacher_name(self,student_id: int):
        query = "select emp.name from employee emp inner join " \
                "(select t.employee_emp_id, tcm.teacher_id, tcm.class_id from teacher_class_mapping tcm " \
                "inner join teachers t on t.teacher_id=tcm.teacher_id) as gol on " \
                "gol.employee_emp_id=emp.emp_id where class_id in (select class_id from student_class_mapping " \
                "where student_id=%s)" % (student_id)
        records = self.db_conn.processquery(query=query, fetch=True)
        return records

    def get_student_assignment_count(self, student_id: int):
        query = "select sub.name, gol.no_of_assignments from subject sub left outer join " \
                "(select a.subject_id, count(sam.student_id) as no_of_assignments from student_assignment_map sam " \
                "inner join assignment a on a.assignment_id=sam.assignment_id where student_id=%s group by" \
                " a.subject_id) as gol on gol.subject_id=sub.subject_id where sub.subject_id in " \
                "(select subject_id from teacher_class_mapping where class_id in " \
                "(select class_id from student_class_mapping where student_id=%s))" %(student_id,student_id)
        records = self.db_conn.processquery(query=query, fetch=True)
        return records

    def get_student_subject_list(self, student_id: int):
        query = "select s.name, tcm.subject_id,e.name as teacher_name, count(gol.subject_id) as number_of_assignments" \
                " from teacher_class_mapping tcm " \
                "left outer join (select subject_id from assignment) as gol on tcm.subject_id=gol.subject_id " \
                "inner join subject s on s.subject_id=tcm.subject_id inner join " \
                "(select teachers.teacher_id, employee.name from teachers inner join employee" \
                " on employee.emp_id=teachers.employee_emp_id) as e on e.teacher_id=tcm.teacher_id " \
                " where tcm.class_id in (select class_id from student_class_mapping where student_id=%s) " \
                "GROUP by tcm.subject_id" % (student_id)
        records = self.db_conn.processquery(query=query, fetch=True)
        return records

    def get_student_late_assignments(self, student_id: int):
        query = "select sub.name, count(gol.late_submission) as late_submission from subject sub" \
                " left outer join (select s.name, count(sam.assignment_id) as late_submission from " \
                "student_assignment_map sam inner join assignment a on a.assignment_id=sam.assignment_id " \
                "inner join subject s on s.subject_id=a.subject_id where" \
                " date(sam.submission_datetime) > a.submission_date and sam.student_id=%s " \
                "group by a.subject_id,sam.assignment_id) as gol on gol.name=sub.name " \
                "where sub.subject_id in (select subject_id from teacher_class_mapping where " \
                "class_id in (select class_id from student_class_mapping where student_id=%s))" \
                " group by sub.subject_id" % (student_id, student_id)
        records = self.db_conn.processquery(query=query, fetch=True)
        return records

    def get_student_average_marks(self, student_id: int):
        query = "select sub.name, gol.average_marks from subject sub left outer join " \
                "(select sam.student_id,a.subject_id, qp.assignment_id, (sum(qr.marks_awarded)/sam.marks)*100 " \
                "as average_marks from quiz_response qr inner join question_pool qp " \
                "on qp.id=qr.question_pool_id inner join assignment a on a.assignment_id= qp.assignment_id " \
                "inner join student_assignment_map sam on sam.student_id=qr.student_id " \
                "and sam.assignment_id=a.assignment_id where sam.student_id=%s group by 2)" \
                " as gol on gol.subject_id=sub.subject_id where sub.subject_id " \
                "in (select subject_id from teacher_class_mapping where class_id in " \
                "(select class_id from student_class_mapping where student_id=%s))" % (student_id,student_id)
        records = self.db_conn.processquery(query=query, fetch=True)
        return records

    def get_assignment_status(self, student_id: int):
        query = "select sub.name, gol.is_evaluated from subject sub left OUTER join " \
                "(select a.subject_id, sam.is_evaluated, sam.student_id from student_assignment_map sam " \
                "inner JOIN assignment a on a.assignment_id=sam.assignment_id where sam.student_id=%s " \
                "and sam.is_evaluated=0 group by a.subject_id)" \
                " as gol on gol.subject_id=sub.subject_id where sub.subject_id in (select subject_id " \
                "from teacher_class_mapping where class_id in (select class_id from student_class_mapping " \
                "where student_id=%s)) " % (student_id,student_id)
        records = self.db_conn.processquery(query=query, fetch=True)
        return records


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
