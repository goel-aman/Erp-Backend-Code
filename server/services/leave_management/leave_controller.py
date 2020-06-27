from flask import jsonify, request
from flask_restful import Resource
from services.leave_management.middleware.leave_handler import LeaveHandler


class StudentLeaves(Resource):
    """Manages the leave for students."""

    def get(self):
        """
        Gets student leaves.
        Param:
            student_id: Student id.
        Request: 
            path: api/v0/attendance/student
            query_params:
               > roll_no: 46, class_id: 7
               > student_id
               > student_admission_no   
            accept: application/json
        Response:
            return  {
                attendance: [{"name": "Shivam Kapoor", "date": "2020-06-25", "status": "A", "parent_acknowledgment": True, "informed_leave": True},],
            }, 200 
            content-type: application/json
            """
        if not request.args.get('roll_no') and not request.args.get('student_id') and not request.args.get(
                'admission_id'):
            return {"error": "Kindly send either admission no or student's rollno."}, 400
        leave_handler = LeaveHandler()
        return jsonify(leave_handler.GetStudentLeaves(**request.args))

    def put(self):
        """

        :return:
        """
        if not request.args.get('student_id') and not request.args.get('leave_date') and not request.args.get(
                'remarks'):
            return {"error": "student_id, leave_date, remarks is required as json"}
        leave_handler = LeaveHandler()
        status = leave_handler.UpdateStudentLeavesByParent(**request.args)
        if status == 1:
            return jsonify("updated successfully!")
        else:
            return jsonify("Updated failed!")


class SubmitLeave(Resource):
    def get(self, user_id):
        """
        gets all the leave records  given the user id
            Param:
                 leave_id: user id.

            Request:
                path: "api/v0/submitleave/<userid>"
            query_params:
                > user_id
            Response:
                return {
                   date_of_applying: "2020-05-21", date_range: {start_date: "2020-05-21", end_date: "2020-05-22"},
                   no of days: 1, type of leave: "general leave", approval status: "accepted"
                }
                content-type: application/json

        """
        if not user_id:
            return {"error": "mandatory parameter user_id not supplied"}, 404
        print("making request to leave handler to post attendance")
        leave_handler = LeaveHandler()
        records = leave_handler.get_leave_record(user_id)
        return jsonify(records)

    def post(self, user_id):
        """
            Creates a employee leave record given a date range, reason and emp_id.
        Param:
            emp_id: Employee id.
        Request:
            path: api/v0/employeeleave/
            body: {
                "start_date": "16-05-2020",
                "end_date": "18-05-2020",
                "type_of_leave": "General Leave",
                "reason": "some reason",

            },
            accept: application/json
        Response:
            return  None, 201
            content-type: application/json
        """
        if not user_id:
            return {"error": "employee id not given"}, 400
        request_payload = request.json
        start_date = request_payload['start_date']
        end_date = request_payload['end_date']
        type_of_leave = request_payload['type_of_leave']
        reason = request_payload['reason']
        leave_handler = LeaveHandler()
        print("making request to leave handler to post attendance")
        leave_handler.post_leave(user_id, start_date, end_date, type_of_leave, reason)


class ManageLeavesAdmin(Resource):
    def post(self, leave_id):
        """
             updates the status of the leave given the leave id
                Param:
                    leave_id: Leave id.
                Request:
                    path: api/v0/employeeleavestatus/
                    body: {
                        "status": "Approved"
                    },
                    accept: application/json
                Response:
                    return  None, 201
                    content-type: application/json
        """
        if not leave_id:
            return {"error": "mandatory parameter leave_id not supplied"}, 400
        request_payload = request.json
        status = request_payload['status']
        print("making request to leave handler to post attendance")
        leave_handler = LeaveHandler()
        leave_handler.post_leave_status_admin(leave_id, status)

    def get(self, leave_id):
        """
            gets all the leave records of the employee given the leave id
            Param:
                 leave_id: Leave id.

            Request:
                path: "api/v0/employeeleavestatus/"
            query_params:
                > leave_id
            Response:
                return {
                   date_of_applying: "2020-05-21", date_range: {start_date: "2020-05-21", end_date: "2020-05-22"},
                   no of days: 1, type of leave: "general leave", approval status: "accepted"
                }
                content-type: application/json
        """
        if not leave_id:
            return {"error": "mandatory parameter leave_id not supplied"}, 400
        print("making request to leave handler to post attendance")
        leave_handler = LeaveHandler()
        records = leave_handler.get_leave_record_admin(leave_id)
        return jsonify(records)


class TeacherDashboardLeaveHistory(Resource):
    def get(self, employee_id):
        if not employee_id:
            return {"error": "mandatory parameter not supplied"}, 404
        print("making request to leave handler to post attendance")
        leave_handler = LeaveHandler()
        records = leave_handler.get_leave_history_record_teacher(employee_id)
        return jsonify(records)


class TeacherDashboardLeaveCategoryRecord(Resource):
    def get(self, employee_id):
        if not employee_id:
            return {"error": "mandatory parameter not supplied"}, 404
        print("making request to leave handler to post attendance")
        leave_handler = LeaveHandler()
        records = leave_handler.get_leave_category_record_teacher(employee_id)
        return jsonify(records)


