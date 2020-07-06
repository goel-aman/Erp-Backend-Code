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
        check_emp = AssignmentHandler().checkUser(employee_id=employee_id)
        if check_emp[1] == False:
            return jsonify("Invalid User")
        user_id = check_emp[0]

        if utils.checkForAllFields(title=title, description=description, deadline=deadline, subject=subject,
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
                if not utils.checkFileType(file):
                    for f in list_of_files:
                        os.remove(f)
                    return jsonify("Accepted file types are .pdf, .docx, .doc, .xlsx file")

            assignment_handler = AssignmentHandler()
            return_val = assignment_handler.uploadAssignment(user_id, title, description, deadline, subject, class_,
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
        check_emp = AssignmentHandler().checkUser(employee_id=employee_id)
        if check_emp[1] == False:
            return jsonify("Invalid User")
        user_id = check_emp[0]

        # Check for all the field values are present
        if utils.checkForAllFields(employee_id=employee_id):
            assign_handler = AssignmentHandler()
            return_val = assign_handler.deleteAssignment(user_id, assignment_id)
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

        if not utils.checkForAllFields(teacher_id=teacher_id, class_=class_, subject=subject, section=section):
            return jsonify("Some fields are missing")

        # Check if employee exists
        check_emp = AssignmentHandler().checkUser(teacher_id=teacher_id)
        if check_emp[1] == False:
            return jsonify("Invalid User")
        user_id = check_emp[0]

        assignment_view = AssignmentViewHandler()
        return_val = assignment_view.TeacherAssignmentView(user_id, teacher_id, class_, section, subject)
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
        if not utils.checkForAllFields(assignment_id=assignment_id, teacher_id=teacher_id):
            return jsonify(teacher_id, assignment_id)

        # Check if employee exists
        check_emp = AssignmentHandler().checkUser(teacher_id=teacher_id)
        if check_emp[1] == False:
            return jsonify("Invalid User")

        assignment_view = AssignmentViewHandler()
        return_val = assignment_view.AssignmentStudentDetailView(assignment_id, teacher_id)

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
        assignment_handler= AssignmentHandler()
        print('Making request to the handler to post the students data')
        records = assignment_handler.get_student_assignment_solution(assignment_id,student_id)
        return jsonify(records)