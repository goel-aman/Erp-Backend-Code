from datetime import datetime, date
from flask import request, jsonify
from flask_restful import Resource
import os
from werkzeug.utils import secure_filename

import utils
from services.assignment.middleware.assignment_handler import AssignmentHandler


class UploadAssignmentByEmployee(Resource):
    """This resource will be responsible for uploading, processing and submitting assignments by employee or students."""

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
            accept: application/json
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
        assignment_type = eval(assignment_type)

        import pdb; pdb.set_trace()
        # Check if employee exists
        check_emp = AssignmentHandler().checkEmployee(employee_id)
        if check_emp[1] == False:
            return jsonify(check_emp[0])

        if utils.checkForAllFields(title=title, description=description, deadline=deadline, subject=subject, section=section, class_=class_, assignment_type=assignment_type):
            try:
                deadline = datetime.strptime(deadline, "%Y-%m-%d")
            except ValueError:
                return jsonify("Improper date string")

            # First save the files
            list_of_files = list()
            if len(assignment_type) == len(request.files):
                random = datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")
                for i in range(len(request.files)):
                    fh = request.files.get("file" + str(i+1))
                    assignment_file = random + "_file" + str(i+1) + "__" + assignment_type.get("file"+str(i+1)).lower() + "__" + secure_filename(fh.filename)
                    fh.save(assignment_file)
                    list_of_files.append(assignment_file)
            else:
                return jsonify("Missing some files, mentioned in the types")

            # Check for file types, if fails delete all of them,
            for file in list_of_files:
                if not utils.checkFileType(file):
                    for f in list_of_files:
                        os.remove(f)
                    return jsonify("Accepted file types are .pdf, .docx, .doc, .xlsx file")

            assignment_handler = AssignmentHandler()
            return_val = assignment_handler.uploadAssignment(employee_id, title, description, deadline, subject, class_, section, list_of_files)

            return jsonify("File saved" + return_val)
        else:
            return jsonify("Some fields are missing")


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
        assignment_handler = AssignmentHandler()
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
        assignment_handler = AssignmentHandler()
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
        assignment_handler = AssignmentHandler()
        return jsonify(assignment_handler.get_completed_assignment_handler(student_id, subject_id))
