from datetime import datetime, date
from flask import request, jsonify
from flask_restful import Resource
import os, re
from werkzeug.utils import secure_filename

import utils
from services.assignment.middleware.assignment_handler import AssignmentHandler, AssignmentViewHandler


class AssignmentByEmployee(Resource):
    """
        This resource will be responsible for uploading,
        processing and submitting assignments by employee or students.
    """
    def get(self, employee_id):
        # Check for employee existence,
        check_emp = AssignmentHandler().check_user(employee_id=employee_id)
        if check_emp[1] == False:
            return jsonify("Invalid User")

        assign_handler = AssignmentHandler()
        return_val = assign_handler.active_assignments(check_emp[0])
        return jsonify(return_val)

    def post(self, employee_id):
        """
            Creates a new assignment either by teacher or admin.
            Param:
                employee_id: employee id.
            Request:
            path: api/v0/assignment/employee
            body: {
                "title": "Title of the assignment",
                "description": "Assignment guidelines",
                "deadline": "Last submission date",
                "subject_id": "subject id",
                "class_id": "class id",
                "assignment_type": "MCQ or Subjective"
                "level_id": "Section of the class",
                "fille": "Assignment file as an Excel sheet (.xlsx)",
            },
            Example Form data Format:

            title:Assignment 1
            description:This is your first assignment.
            deadline:2020-07-10
            subject:Science
            class:4
            section:A,B,C
            assignment_type:{"file1": "MCQ", "file2": "Subjective", "file3": "Manual", "file4": "Manual"}
            manual_marks:{"file3": 50, "file4": 25}
            // finally, actual files should have the name "file1, file2, file3, file4, ..."
        Response:
            return  None, 201
            content-type: application/json
        """
        request_payload = request.form
        title = request_payload.get("title", "")
        description = request_payload.get("description", "")
        deadline = request_payload.get("deadline", "")
        subject = request_payload.get("subject", "")
        class_ = request_payload.get("class", "")
        section = request_payload.get("section", "")
        assignment_type = request_payload.get("assignment_type", "")
        manual_marks = request_payload.get("manual_marks", "")
        try:
            assignment_type = eval(assignment_type)
        except:
            return "Invalid Assignment Type"

        # Check manual marks if manual type is present
        for value in assignment_type.values():
            if value == "manual" and manual_marks == "":
                manual_marks = False
                return "Invalid Marks"

        # Check if employee exists
        check_emp = AssignmentHandler().check_user(employee_id=employee_id)
        if check_emp[1] == False:
            return jsonify("Invalid User")
        user_id = check_emp[0]

        if utils.check_for_all_fields(title=title, description=description, deadline=deadline, subject=subject,
                                      section=section, class_=class_, assignment_type=assignment_type, user_id=user_id):
            try:
                deadline = datetime.strptime(deadline, "%Y-%m-%d")
            except ValueError:
                return jsonify("Improper date string")

            # First save the files
            list_of_files = list()
            if len(assignment_type) == len(request.files):
                random = datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")
                for i in range(len(request.files)):
                    fh = request.files.get("file" + str(i + 1))
                    assignment_file = random + "_file" + str(i + 1) + "__" + assignment_type.get(
                        "file" + str(i + 1)).lower() + "__" + secure_filename(fh.filename)
                    fh.save(assignment_file)
                    list_of_files.append(assignment_file)
            else:
                return jsonify("Missing some files, mentioned in the types")

            # Check for file types, if fails delete all of them,
            for file in list_of_files:
                if not utils.check_file_type(file):
                    for f in list_of_files:
                        os.remove(f)
                    return jsonify("Accepted file types are .pdf, .docx, .doc, .xlsx file")

            assignment_handler = AssignmentHandler()
            return_val = assignment_handler.upload_assignment(user_id, title, description, deadline, subject, class_,
                                                              section, list_of_files, manual_marks)

            return jsonify("File saved" + return_val)
        else:
            return jsonify("Some fields are missing")

    def delete(self, employee_id):
        """
        Example
        api endpoint: /assignment/employee/730?assignment_id=111
        :param employee_id:
        :return:
        """
        request_payload = request.json
        assignment_id = request_payload.get("assignment_id", "")

        # Check for employee existence
        check_emp = AssignmentHandler().check_user(employee_id=employee_id)
        if check_emp[1] == False:
            return jsonify("Invalid User")
        user_id = check_emp[0]

        # Check for all the field values are present
        if utils.check_for_all_fields(employee_id=employee_id):
            assign_handler = AssignmentHandler()
            return_val = assign_handler.delete_assignment(user_id, assignment_id)
            return jsonify(return_val[0])
        else:
            return jsonify("Some fields are missing!")


class TeacherAssignments(Resource):
    """
        This resource will handle the assignment list for a particular employee,
    """
    def get(self, teacher_id):
        """
        :param teacher_id:
        :return:
        """
        request_payload = request.json
        teacher_id = teacher_id
        class_ = request.json.get("class", "")
        subject = request.json.get("subject", "")

        class_section = re.search(r"^\d{1,2}\-\w{1}$", class_)
        if class_section is None:
            return jsonify("No such Class")
        class_section = class_section.group(0).split("-")
        class_ = class_section[0]
        section = class_section[1]

        if not utils.check_for_all_fields(teacher_id=teacher_id, class_=class_, subject=subject, section=section):
            return jsonify("Some fields are missing")

        # Check if employee exists
        check_emp = AssignmentHandler().check_user(teacher_id=teacher_id)
        if check_emp[1] == False:
            return jsonify("Invalid User")
        user_id = check_emp[0]

        assignment_view = AssignmentViewHandler()
        return_val = assignment_view.teacher_assignment_view(user_id, teacher_id, class_, section, subject)
        print(return_val)

        return jsonify(return_val)


class TeacherAssignmentDetailView(Resource):
    """
    Resource to list all the students details,
    who has submitted a particular an assignment,
    """
    def get(self, teacher_id, assignment_id):
        """
        :param teacher_id:
        :param assignment_id:
        :return:
        """
        if not utils.check_for_all_fields(assignment_id=assignment_id, teacher_id=teacher_id):
            return jsonify(teacher_id, assignment_id)

        # Check if employee exists
        check_emp = AssignmentHandler().check_user(teacher_id=teacher_id)
        if check_emp[1] == False:
            return jsonify("Invalid User")

        assignment_view = AssignmentViewHandler()
        return_val = assignment_view.assignment_student_detail_view(assignment_id, teacher_id)

        return jsonify(return_val)


class AssignmentSubmit(Resource):
    def post(self, student_id):
        """
                Post student assignment solutions given student id.
                Param:
                    student_id: Student id.
                Request:
                    path: api/v0/assignmentsubmit
                    body: {

                        question_pool_id : 2,
                        solution : 3,
                    },
                    accept: application/json
                Response:
                    return  None, 201
                    content-type: application/json
        """
        if not student_id:
            return {"error": "mandatory parameter not supplied"}, 404
        assignment_sol = request.json
        assignment_handler = AssignmentHandler()
        print('Making request to the handler to post the students data')
        assignment_handler.assignment_submit(student_id, assignment_sol)


class GetAssignment(Resource):
    """
        Get student assignment solutions in teacher login
        Param: Student Id, Assignment Id
        Request:
            path: api/vo/getstudentassignmentsolutoin/
        Response:
            return [ {question_pool_id : 1, answer: A},{question_pool_id : 1, answer: A}]
            content type: application/json
    """

    def get(self):
        assignment_id = request.args.get('assignment_id')
        student_id = request.args.get('student_id')
        assignment_handler= AssignmentViewHandler()
        print('Making request to the handler to post the students data')
        records = assignment_handler.get_student_assignment_solution(assignment_id, student_id)
        return jsonify(records)


class AssignmentQuestions(Resource):

    def get(self, assignment_id):
        """
        Gets the questions for a particular assignment.
        Param: assignment_id: Assignment ID
        Request:
            path: api/v0/assignment_ques/<int:assignment_id>
            body: {},
            # Date format can be iso or "YYYY-mm-dd"
            accept: application/json
        Response:
            return  {
                  {
                    "choice1": "Charles Babbage",
                    "choice2": "Doug Engelbart",
                    "choice3": "Richard Feynmann",
                    "id": 254,
                    "marks": 2,
                    "question": "Who invented the Computer Mouse?",
                    "question_type": "mcq"
                  },
                  {
                    "id": 265,
                    "marks": 2,
                    "question": "Who invented the telephone? ",
                    "question_type": "subjective"
                  },
            }, 200
            content-type: application/json
        """
        assignment_handler = AssignmentViewHandler()
        return jsonify(assignment_handler.get_assignment(assignment_id))


class PendingAssignment(Resource):

    def get(self, student_id):
        """
        Gets the pending assignments for a particular student.
        Param: student_id: Student ID
        Request:
            path: api/v0/pending_assignment/<int:student_id>
            body: {},
            # Date format can be iso or "YYYY-mm-dd"
            accept: application/json
        Response:
            return  {
                {
                    "assignment_id": 102,
                    "description": "Description of assignment",
                    "initiation_date": "2020-06-30",
                    "name": "English",
                    "submission_date": "2020-07-10",
                    "title": "Fourth Assignment"
                },
            }, 200
            content-type: application/json
        """
        assignment_handler = AssignmentViewHandler()
        return jsonify(assignment_handler.get_pending_assignment_handler(student_id))


class CompletedAssignment(Resource):

    def get(self, student_id, subject_id):
        """
        Gets the completed assignments for a particular student and a particular subject.
        Param:
            student_id: Student ID
            subject_id: Subject ID
        Request:
            path: api/v0/completed_assignment/<int:student_id>/<int:subject_id>
            body: {},
            # Date format can be iso or "YYYY-mm-dd"
            accept: application/json
        Response:
            return  {
                {
                    "assignment_id": 102,
                    "description": "Description of assignment",
                    "initiation_date": "2020-06-30",
                    "name": "English",
                    "submission_date": "2020-07-10",
                    "title": "Fourth Assignment"
                },
            }, 200
            content-type: application/json
        """
        assignment_handler = AssignmentViewHandler()
        return jsonify(assignment_handler.get_completed_assignment_handler(student_id, subject_id))


class AssignmentHistory(Resource):
    """
        get the records of all the assignments submitted by the student
        Param: Student Id
        Request:
            path: "api/v0/assingmenthistory/<int:student_id>
    """

    def get(self, student_id):
        if not student_id:
            return {"error": "mandatory parameter not supplied "}, 404
        assignment_handler = AssignmentViewHandler()
        print('Making request to the handler to post the students data')
        records = assignment_handler.get_assignment_history(student_id)
        return jsonify(records)


class PostAssignmentMarks(Resource):
    """
        post student marks for a assignment given the teacher id
        Param : Teacher_id
        body:{
                {"question_pool_id": 1, "marks_awarded": 2, "student_id" : 1, "evaluated_sheet_link": null}
                }
        Path: "api/vo/postassignmentmarks/<int:teacher_id"

    """
    def post(self, teacher_id):
        if not teacher_id:
            return {"error" : "mandatory parameter not supplied"}
        student_marks = request.json
        assignment_handler = AssignmentHandler()
        print('Making request to the handler to post the students data')
        assignment_handler.post_assignment_marks(teacher_id, student_marks)
