import datetime
import pandas as pd


class AssignmentDao:

    def __init__(self, db_conn, **kwargs):
        self.db_conn = db_conn
        self.class_ = kwargs.get("class_", "")
        self.section = kwargs.get("section", "")
        self.subject = kwargs.get("subject", "")
        self.comma_files = kwargs.get("comma_files", "")
        self.title = kwargs.get("title", "")
        self.description = kwargs.get("description", "")
        self.deadline = kwargs.get("deadline", "")
        self.user_id = kwargs.get("user_id", "")

        # Fetch class Id,
        self.class_ids = list()
        if self.section != "" and self.class_ != "":
            if len(self.section) > 0:
                for i in self.section:
                    query = "select class_id from class where standard=%s and section='%s';" % (self.class_, i)
                    records = self.db_conn.processquery(query=query, fetch=True)
                    if len(records) > 0:
                        self.class_ids.append(records[0].get("class_id"))

        # Fetch subject Id,
        if self.subject != "":
            self.subject_id = None
            query = "select subject_id from subject where name='%s';" % (self.subject)
            records = self.db_conn.processquery(query=query, fetch=True)
            if len(records) > 0:
                self.subject_id = records[0].get("subject_id")

        # Initiation Date,
        self.today = datetime.datetime.now().strftime("%Y-%m-%d")

        """
            Insert Assignment records, and should be done for only one time for all the Uploads,
            This function also handles manual document uploading, as there is no questions to them,
        """

        if self.title != "" and self.comma_files != "" and self.description != "" and self.deadline != "" and self.subject_id != "" \
                and self.class_ids != "" and self.user_id != "" and self.title != "":
            for c_id in self.class_ids:
                query = "insert into assignment (title, file_link, description, initiation_date, " \
                        "submission_date, subject_id, class_id, uploaded_by) values " \
                        "('%s', '%s', '%s', '%s', '%s', %s, %s, %s);" % (
                            self.title, self.comma_files, self.description, self.today, self.deadline, self.subject_id,
                            c_id, self.user_id)
                records = self.db_conn.processquery(query=query, fetch=False)

    def upload_manual(self, file, list_of_files, mark, ques_type):
        return_val = None
        # Query Question Type to fetch the Id with the type,
        query = "select id from question_type where question_type='%s';" % ques_type
        records = self.db_conn.processquery(query=query, fetch=True)
        type_id = None
        if len(records) > 0:
            type_id = records[0].get("id")

        # Get Assignment Ids for the all sections,
        assign_ids = list()

        for c_id in self.class_ids:
            query = "select assignment_id from assignment where file_link='%s' and class_id=%s;" % (list_of_files, c_id)
            records = self.db_conn.processquery(query=query, fetch=True)
            if len(records) == 1:
                assign_ids.append(records[0].get("assignment_id", ""))

        # Insert into question_pool with manual file link,
        for assign_id in assign_ids:
            query = "insert into question_pool (question_type_id, assignment_id, marks, manual_link) " \
                    "values (%s, %s, %s, '%s');" % (type_id, assign_id, mark, file)
            records = self.db_conn.processquery(query=query, fetch=False)

        return_val = "Inserted Manual document"
        return return_val, True

    def upload_subjective(self, file, list_of_files, ques_type):
        # try:
        # Query Question Type to fetch the Id with the type,
        query = "select id from question_type where question_type='%s';" % ques_type
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
            return return_val, False

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
                        "values (%s, '%s', %s, %s, '', %s);" \
                        % (type_id, ques_list[i], assign_id, marks_list[i], expected_no_of_words[i])
                records = self.db_conn.processquery(query=query, fetch=False)
        return_val = "Inserted Subjective document"
        return return_val, True
        # except:
        #     return "Some error happened!"

    def upload_MCQ(self, file, list_of_files, type):
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

    def delete_assignment_dao(self, user_id, assignment_id):
        """
        :param employee_id: employee who is deleting
        :param assignment_id: which assignment she is deleting
        :return: tuple(str, bool)
        """
        return_val = None

        # Check if assignment exists
        query = "select is_deleted from assignment where assignment_id=%s;" % assignment_id
        records = self.db_conn.processquery(query=query, fetch=True)
        if len(records) <= 0:
            return_val = ("Assignment doesn't exists!", False)
            return return_val
        elif records[0].get("is_deleted"):
            return_val = ("Assignment deleted!", True)
            return return_val

        # Update assignment table,
        query = "update assignment set is_deleted=1, modified_by=%s where assignment_id=%s;" \
                % (user_id, assignment_id)
        self.db_conn.processquery(query=query, fetch=False)

        # Update question_pool table,
        query = "update question_pool set is_deleted=1 where assignment_id=%s;" \
                % assignment_id
        self.db_conn.processquery(query=query, fetch=False)

        return_val = ("Assignment deleted!", True)
        return return_val

    def active_assignment_by_userid(self, user_id):
        """
        :param user_id:
        :return:
        """
        return_val = dict()
        return_val['mcq'] = dict()
        return_val['subjective'] = dict()
        return_val['manual'] = dict()

        # Fetch all the assignments,
        query = "select * from assignment where uploaded_by=%s and is_deleted=0;" % user_id
        records = self.db_conn.processquery(query=query, fetch=True)

        if len(records) > 0:
            for record in records:
                return_dict = dict()
                return_dict["id"] = record.get("assignment_id")
                return_dict["topic"] = record.get("title")
                return_dict["subject"] = None
                query = "select name from subject where subject_id=%s" % record.get("subject_id", "")
                subject_records = self.db_conn.processquery(query=query, fetch=True)
                return_dict["subject"] = subject_records[0].get("name", "")
                return_dict["standard"] = None
                query = "select standard, section from class where class_id=%s" % record.get("class_id", "")
                class_records = self.db_conn.processquery(query=query, fetch=True)
                return_dict["standard"] = str(class_records[0].get("standard")) + "-" + \
                                          str(class_records[0].get("section"))
                return_dict["deadline"] = record.get("submission_date")
                query = "select question_type from question_type where id in " \
                        "(select question_type_id from question_pool where assignment_id=%s " \
                        "group by question_type_id);" % record.get("assignment_id")
                question_type_records = self.db_conn.processquery(query=query, fetch=True)
                import pdb; pdb.set_trace()
                # Make separate dictionaries for individual question types,
                for types in question_type_records:
                    if types.get("question_type", "") == "mcq":
                        return_val["mcq"][record.get("assignment_id")] = return_dict
                    elif types.get("question_type", "") == "subjective":
                        return_val["subjective"][record.get("assignment_id")] = return_dict
                    elif types.get("question_type", "") == "manual":
                        return_val["manual"][record.get("assignment_id")] = return_dict

            return return_val, True
        else:
            return "Invalid assignment", False


class AssignmentSubmitDao:
    """
    """
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

    def get_student_teacher_name(self, student_id: int):
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
                "(select class_id from student_class_mapping where student_id=%s))" % (student_id, student_id)
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
                "(select sam.student_id,a.subject_id, qp.assignment_id, (sum(qr.marks_awarded)/sum(qp.marks))*100 " \
                "as average_marks from quiz_response qr inner join question_pool qp " \
                "on qp.id=qr.question_pool_id inner join assignment a on a.assignment_id= qp.assignment_id " \
                "inner join student_assignment_map sam on sam.student_id=qr.student_id " \
                "and sam.assignment_id=a.assignment_id where sam.student_id=%s group by 2)" \
                " as gol on gol.subject_id=sub.subject_id where sub.subject_id " \
                "in (select subject_id from teacher_class_mapping where class_id in " \
                "(select class_id from student_class_mapping where student_id=%s))" % (student_id, student_id)
        records = self.db_conn.processquery(query=query, fetch=True)
        return records

    def get_assignment_status(self, student_id: int):
        query = "select sub.name, gol.is_evaluated from subject sub left OUTER join " \
                "(select a.subject_id, sam.is_evaluated, sam.student_id from student_assignment_map sam " \
                "inner JOIN assignment a on a.assignment_id=sam.assignment_id where sam.student_id=%s " \
                "and sam.is_evaluated=0 group by a.subject_id)" \
                " as gol on gol.subject_id=sub.subject_id where sub.subject_id in (select subject_id " \
                "from teacher_class_mapping where class_id in (select class_id from student_class_mapping " \
                "where student_id=%s)) " % (student_id, student_id)
        records = self.db_conn.processquery(query=query, fetch=True)
        return records

    def submit_marks(self, question_pool_id, student_id, marks_awarded):
        query = "update quiz_response set marks_awarded=%s where question_pool_id =%s " \
                "and student_id=%s" % (marks_awarded, question_pool_id, student_id)
        self.db_conn.processquery(query=query, fetch=False)

    def submit_marks_manual(self, question_pool_id, student_id, marks_awarded, evaluated_sheet_link):
        query = "update quiz_response set marks_awarded=%s,evaluated_sheet_link='%s' " \
                "where question_pool_id =%s " \
                "and student_id=%s" % (marks_awarded, evaluated_sheet_link, question_pool_id, student_id)
        self.db_conn.processquery(query=query, fetch=False)

    def submit_marks_in_map(self, total,teacher_id, question_pool_id, student_id):
        query = "select assignment_id from question_pool where id=%s" % (question_pool_id)
        records = self.db_conn.processquery(query=query, fetch=True)
        query = "update student_assignment_map set marks= %s, teacher_id=%s, is_evaluated=1,evaluated_timestamp=now()" \
                " where assignment_id=%s and student_id=%s" %(total, teacher_id, records[0]['assignment_id'], student_id)
        self.db_conn.processquery(query=query, fetch=False)


class CheckUser:

    def __init__(self, db_conn):
        self.db_conn = db_conn

    def check_employee(self, employee_id):
        """
        :param employee_id:
        :return:
        """
        return_val = None
        # Fetch user_id for the employee_id
        query = "select user_id, is_active from employee where user_id=%s;" % employee_id
        records = self.db_conn.processquery(query=query, fetch=True)

        if len(records) > 0 and records[0].get("is_active") == 1:
            return_val = (records[0].get("user_id", ""), True)
            return return_val
        else:
            teacher_ = self.check_teacher(employee_id)
            if teacher_[1]:
                return_val = (teacher_[0], True)
                return return_val

        return_val = ("User doesn't exist", False)
        return return_val

    def check_teacher(self, teacher_id):
        """
        :param teacher_id:
        :return: (user_id, Bool)
        """
        return_val = None
        query = "select users_user_id from teachers where teacher_id=%s;" % teacher_id
        records = self.db_conn.processquery(query=query, fetch=True)

        if len(records) > 0:
            user_id = records[0].get("users_user_id", "")
            query = "select is_active from users where user_id=%s" % user_id
            records = self.db_conn.processquery(query=query, fetch=True)
            if len(records) > 0 and records[0].get("is_active") == 1:
                return_val = (user_id, True)
                return return_val

        return_val = ("User doesn't exist", False)
        return return_val


class AssignmentView:
    """
        assignment view for the employee or the teacher
    """
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def assignment_by_class_subject_id(self, user_id, teacher_id, class_, section, subject):
        """
        :param teacher_id:
        :param class_id:
        :param subject_id:
        :return:
        """
        return_val = None

        # Check class_id,
        class_id = None
        query = "select class_id from class where standard=%s and section='%s';" % (class_, section)
        records = self.db_conn.processquery(query=query, fetch=True)
        if len(records) <= 0:
            return_val = ("Class or section doesn't exist", False)
            return return_val
        class_id = records[0].get("class_id", "")

        # Check subject_id,
        subject_id = None
        query = "select subject_id from subject where name='%s';" % subject
        records = self.db_conn.processquery(query=query, fetch=True)
        if len(records) <= 0:
            return_val = ("Subject doesn't exist", False)
            return return_val
        subject_id = records[0].get("subject_id", "")

        # Fetch all the students for the particular class and section
        query = "select student_id from student_class_mapping where class_id=%s;" % class_id
        records = self.db_conn.processquery(query=query, fetch=True)
        if len(records) <= 0:
            return_val = ("No students in the Class and section", False)
            return return_val
        all_class_students = list()
        for stud in records:
            all_class_students.append(stud.get("student_id", ""))
        total_students = len(all_class_students)

        # Fetch assignment details of a particular teacher user_id for that class and subject,
        query = "select * from assignment where uploaded_by=%s and class_id=%s and is_deleted=0 " \
                "and subject_id=%s;" % (user_id, class_id, subject_id)
        records = self.db_conn.processquery(query=query, fetch=True)
        if len(records) <= 0:
            return_val = ("No assignments uploaded yet", False)
            return return_val
        all_assignments = dict()
        for assign in records:
            all_assignments[assign.get("assignment_id", "")] = assign

        # Fetch only the students who has submitted the assignment for this class_id,
        all_submitted_assignments = dict()
        for a_id, assignment in all_assignments.items():
            query = "select student_id, is_evaluated from student_assignment_map where teacher_id=%s and class_id=%s " \
                    "and assignment_id=%s;" % (teacher_id, class_id, a_id)
            records = self.db_conn.processquery(query=query, fetch=True)
            all_submitted_assignments[a_id] = records

        # Check all_submitted_assignment has evaluated,
        evaluation_check = dict()
        for a_id, evaluation in all_submitted_assignments.items():
            evaluation_check[a_id] = True
            for eval_ in evaluation:
                if eval_.get("is_evaluated", None) == None or eval_.get("is_evaluated", 0) == 0:
                    evaluation_check[a_id] = False
                    break

        # Create return values,
        return_dict = dict()
        for assign_id, values in all_assignments.items():
            submissions = total_students - len(all_submitted_assignments.get(assign_id))
            topic = values.get("title", "")
            from_ = values.get("initiation_date", "")
            to_ = values.get("submission_date", "")
            status = evaluation_check.get(assign_id, False)
            return_dict[assign_id] = {"topic": topic, "from": from_, "to": to_, "submissions_left": submissions, "status": status}

        if len(return_dict) > 0:
            return (return_dict, True)

        return (return_dict, False)

    def student_submissions_view_by_assignment(self, assignment_id, teacher_id):
        """
        :param assignment_id:
        :return:
        """
        return_val = None

        # Check if the assignment exists
        query = "select is_deleted from assignment where assignment_id=%s;" % assignment_id
        records = self.db_conn.processquery(query=query, fetch=True)

        if len(records) > 0 and records[0].get("is_deleted", "") == 1:
            return_val = ("Assignment doesn't exists", False)
            return return_val

        # Fetch assignment by assignment_id and teacher_id,
        query = "select * from student_assignment_map where teacher_id=%s and assignment_id=%s;" % (teacher_id, assignment_id)
        records = self.db_conn.processquery(query=query, fetch=True)
        all_submissions = records

        # Fetch student_id for getting the student Name,
        for i in range(0, len(all_submissions)):
            stud_id = all_submissions[i].get("student_id", "")
            query = "select student_fname, student_lname from students where student_id=%s;" % (stud_id)
            records = self.db_conn.processquery(query=query, fetch=True)
            student_name = records[0].get("student_fname") + " " + records[0].get("student_lname")
            all_submissions[i]["student_name"] = student_name

        # Fetch total marks from the question_pool for the assignment
        query = "select marks from question_pool where assignment_id=%s;" % assignment_id
        records = self.db_conn.processquery(query=query, fetch=True)
        total_marks = 0.0
        for mark in records:
            total_marks += int(mark.get("marks", 0))

        # Create return dict
        return_dict = dict()

        for rec in all_submissions:
            name = rec.get("student_name", "")
            submitted_date = rec.get("submission_datetime", "")
            status = True
            marks_awarded = rec.get("marks", None)
            if rec.get("is_evaluated", None) == None or rec.get("is_evaluated") == 0:
                status = False
            else:
                if marks_awarded == None:
                    marks_awarded = ""
            if marks_awarded != "":
                try:
                    percentage = (marks_awarded / total_marks) * 100
                except:
                    percentage = None
            return_dict[rec.get("student_id")] = {"student_name": name, "submitted_on": submitted_date, \
                                                 "checked": status, "marks": marks_awarded, "percentage": percentage, "total_marks": total_marks}

        if len(return_dict) > 0:
            return (return_dict, True)

        return (return_dict, False)


class AssignmentQuestionsDao():
    """
    """
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
