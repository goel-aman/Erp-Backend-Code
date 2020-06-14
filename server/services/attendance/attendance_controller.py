from datetime import datetime, date
from flask import request, jsonify
from flask_restful import Resource
from services.attendance.middleware.attendance_handler import AttendanceHandler


class StudentAttendance(Resource):
    """This resource will be responsible for CRUD operations on attendance for a specific student."""
    def get(self, student_id):
        """
        Gets a student attendance given a date range, class and student_id.
        Param:
            student_id: Student id.
        Request: 
            path: api/v0/attendance/student
            body: {
                "start_date": "16-05-2020",
                "end_date": "18-05-2020",
            },
            # Date format can be iso or "dd-m-YYYY"
            accept: application/json
        Response:
            return  {
                attendance: [{"name": "Shivam Kapoor", "date": "2020-06-25", "status": "P"},],
            }, 200 
            content-type: application/json
        """
        if not student_id:
            return {"error": "Mandatory parameter student id not supplied"}, 400
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        print(request.args)
        attendance_handler = AttendanceHandler()
        print('Making request to the handler to get the students data')
        return jsonify(attendance_handler.GetStudentAttendance(student_id, **request.args))
        

    def post(self, student_id):
        """
        Creates a student attendance given a date range, class and student_id.
        Param:
            student_id: Student id.
        Request: 
            path: api/v0/attendance/student
            body: {
                "start_date": "16-05-2020",
                "end_date": "18-05-2020",
                "status": "P",
            },
            accept: application/json
        Response:
            return  None, 201
            content-type: application/json
        """
        pass

    def put(self, student_id):
        """
        Updates a student attendance given a date range, class and student_id.
        Param:
            student_id: Student id.
        Request: 
            path: api/v0/attendance/student
            body: {
                "start_date": "16-05-2020",
                "end_date": "18-05-2020",
                "status": "P",
            },
            accept: application/json
        Response:
            return  None, 201
            content-type: application/json
        """
        pass

    def delete(self, student_id):
        """
        Deletes attendance given a date range, class and student_id.
        Param:
            student_id: Student id.
        Request: 
            path: api/v0/attendance/student
            body: {
                "start_date": "16-05-2020",
                "end_date": "18-05-2020",
            },
            accept: application/json
        Response:
            return  None, 200
            content-type: application/json
        """
        pass


class StudentsAttendance(Resource):
    """This resource will be responsible for CRUD operations on attendance for whole class."""
    def get(self, class_id):
        """
        Gets students attendance given a date and class.
        Param:
            class_id: Class entity id.
        Request: 
            path: api/v0/attendance/class
            body: {
                "date": "16-05-2020"
            },
            accept: application/json
        Response:
            if attendance is there for a date:
                return  {
                    attendance: [{"name": "Shivam Kapoor", "roll_no: "1", "status": "P"},],
                    date: "16-05-2020"
                }, 200
            return "Attendance is not calculated for the date: {date}", 400  
            content-type: application/json
        """
        pass

    def post(self, class_id):
        """
        Posts students attendance given a date and class.
        Param:
            class_id: Class entity id.
        Request: 
            path: api/v0/attendance/class
            body: {
                "attendance": [
                    {"name": "Shivam Kapoor", "roll_no: "1", "status": "P"},
                    {"name": "Tiwari Seth", "roll_no: "2", "status": "A"},
                ],
                "date": "16-05-2020",
            },
        Response:
            None, 202
        """
        pass

    def update(self, class_id):
        """
        Updates students attendance given a date and class.
        Param:
            class_id: Class entity id.
        Request: 
            path: api/v0/attendance/class
            body: {
                "attendance": [
                    {"name": "Shivam Kapoor", "roll_no: "1", "status": "P"},
                    {"name": "Tiwari Seth", "roll_no: "2", "status": "A"},
                ],
                "date": "16-05-2020"
            }
        Response:
            None, 202
        """
        pass

    def delete(self, class_id: int):
        """
        Deletes students attendance given a date and class.
        Param:
            class_id: Class entity id.
        Request: 
            path: api/v0/attendance/class
            body: {
                "date": "16-05-2020"
            }
        Response:
            None, 200
        """
        pass