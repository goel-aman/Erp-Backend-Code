from flask import request
from flask_restful import Resource


class StudentAttendance(Resource):
    """This resource will be responsible for CRUD operations on attendance for a specific student."""
    def get(self):
        """
        Gets a student attendance given a date range, class and student_id.
        Request: 
            path: api/v0/attendance/student
            body: {
                "student_id": "1",
                "start_date": "16-05-2020",
                "end_date": "18-05-2020",
            },
            accept: application/json
        Response:
            return  {
                attendance: [{"name": "Shivam Kapoor", "date": "16-05-2020", "status": "P"},],
            }, 200 
            content-type: application/json
        """
        pass
    
    def post(self):
        """
        Creates a student attendance given a date range, class and student_id.
        Request: 
            path: api/v0/attendance/student
            body: {
                "student_id": "1",
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

    def put(self):
        """
        Updates a student attendance given a date range, class and student_id.
        Request: 
            path: api/v0/attendance/student
            body: {
                "student_id": "1",
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

    def delete(self):
        """
        Deletes attendance given a date range, class and student_id.
        Request: 
            path: api/v0/attendance/student
            body: {
                "student_id": "1",
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
    def get(self):
        """
        Gets students attendance given a date and class.
        Request: 
            path: api/v0/attendance/class
            body: {
                "class": "6th B" || "5" class entity id,
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

    def post(self):
        """
        Posts students attendance given a date and class.
        Request: 
            path: api/v0/attendance/class
            body: {
                "class": "6th B" || "5" class entity id,
                "attendance": [
                    {"name": "Shivam Kapoor", "roll_no: "1", "status": "P"},
                    {"name": "Tiwari Seth", "roll_no: "2", "status": "A"},
                ],
                "date": "16-05-2020"
            },
        Response:
            None, 202
        """
        pass

    def update(self):
        """
        Updates students attendance given a date and class.
        Request: 
            path: api/v0/attendance/class
            body: {
                "class": "6th B" || "5" class entity id,
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

    def delete(self):
        """
        Deletes students attendance given a date and class.
        Request: 
            path: api/v0/attendance/class
            body: {
                "class": "6th B" || "5" class entity id,
                "date": "16-05-2020"
            }
        Response:
            None, 200
        """
        pass