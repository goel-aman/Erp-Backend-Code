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

        if not student_id:
            return {"error": "Mandatory parameter student id not supplied"}, 400
        request_payload = request.json
        start_date = request_payload['start_date']
        end_date = request_payload['end_date']
        status = request_payload['status']
        updated_by = request_payload['updated_by']
        attendance_handler = AttendanceHandler()
        print('Making request to the handler to post the students data')
        attendance_handler.PostStudentAttendance(
            student_id, updated_by, start_date, end_date, status)

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
        if not student_id:
            return {"error": "Mandatory parameter student id not supplied"}, 400
        request_payload = request.json
        start_date = request_payload['start_date']
        end_date = request_payload['end_date']
        status = request_payload['status']
        attendance_handler = AttendanceHandler()
        print('Making request to the handler to post the students data')
        attendance_handler.PutStudentAttendance(
            student_id, start_date, end_date, status)

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
        if not student_id:
            return {"error": "Mandatory parameter student id not supplied"}, 400
        request_payload = request.json
        start_date = request_payload['start_date']
        end_date = request_payload['end_date']
        attendance_handler = AttendanceHandler()
        print('Making request to the handler to post the students data')
        attendance_handler.DeleteStudentAttendance(
            student_id, start_date, end_date)


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
        if not class_id:
            return {"error": "Mandatory parameter class id not supplied"}, 400
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        attendance_handler = AttendanceHandler()
        print('Making request to the handler to get the students data')
        return jsonify(attendance_handler.GetStudentsAttendance(class_id, **request.args))

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
        if not class_id:
            return {"error": "Mandatory parameter class id not supplied"}, 400
        request_payload = request.json
        for attendance_record in request_payload:
            roll_no = attendance_record['roll_no']
            start_date = attendance_record['start_date']
            end_date = attendance_record['end_date']
            status = attendance_record['status']
            updated_by = attendance_record['updated_by']
            attendance_handler = AttendanceHandler()
            print('Making request to the handler to post the students data')
            attendance_handler.PostStudentsAttendance(
                class_id, updated_by, roll_no, start_date, end_date, status)

    def put(self, class_id):
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
        if not class_id:
            return {"error": "Mandatory parameter class id not supplied"}, 400
        request_payload = request.json
        for attendance_record in request_payload:
            roll_no = attendance_record['roll_no']
            start_date = attendance_record['start_date']
            end_date = attendance_record['end_date']
            status = attendance_record['status']
            attendance_handler = AttendanceHandler()
            print('Making request to the handler to post the students data')
            attendance_handler.UpdateStudentsAttendance(
                class_id, roll_no, start_date, end_date, status)

    def delete(self, class_id):
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
        if not class_id:
            return {"error": "Mandatory parameter class id not supplied"}, 400
        request_payload = request.json
        start_date = request_payload['start_date']
        end_date = request_payload['end_date']
        attendance_handler = AttendanceHandler()
        print('Making request to the handler to post the students data')
        attendance_handler.DeleteStudentsAttendance(
            class_id, start_date, end_date)


class StudentDashboardCard1(Resource):
    """
        get request for the donut chart values in student login dashboard

        path: "api/v0/studentdashboardcard1/<int : student_id>"

    """

    def get(self, student_id):
        if not student_id:
            return {"error": "Mandatory parameter class id not supplied"}, 400
        attendance_handler = AttendanceHandler()
        print("making request to the handler to get the dashboard data")
        print(student_id)
        card1 = attendance_handler.DashboardDataCard1(student_id)

        return jsonify({"attendance": card1})


class StudentDashboardCard2(Resource):
    """
        get request for the leave record in student login dashboard

        path: "api/v0/studentdashboardcard2/<int : student_id>"

    """

    def get(self, student_id):
        if not student_id:
            return {"error": "Mandatory parameter class id not supplied"}, 400
        attendance_handler = AttendanceHandler()
        print("making request to the handler to get the dashboard data")
        print(student_id)
        card2 = attendance_handler.DashboardDataCard2(student_id)
        return jsonify({"leave record": card2})


class StudentDashboardCard3(Resource):
    """
        get request for the calendar details in the student login dashboard
        path: "api/v0/studentdashboardcard3/<int : student_id>"
    """

    def get(self, student_id):
        if not student_id:
            return {"error": "Mandatory parameter class id not supplied"}, 400
        attendance_handler = AttendanceHandler()
        print("making request to the handler to get the dashboard data")
        print(student_id)
        card3 = attendance_handler.dashboard_data_card3(student_id)
        return jsonify({"calendar": card3})



class StudentDashboardCard4(Resource):
    """
        get request for the line graph values in the student login dashboard
        path: "api/v0/studentdashboardcard4/<int : student_id>"
    """

    def get(self, student_id):
        if not student_id:
            return {"error": "Mandatory parameter class id not supplied"}, 400
        attendance_handler = AttendanceHandler()
        print("making request to the handler to get the dashboard data")
        print(student_id)
        card4 = attendance_handler.DashboardDataCard4(student_id)
        return jsonify({"class_attendance": card4})


class StudentLatestDateAttendance(Resource):
    def get(self):
        """
        Gets a percenatge of present, absent and late students for the latest day.
        Param:
        Request:
            path: api/v0/attendance/daily
            body: {},
            # Date format can be iso or "dd-m-YYYY"
            accept: application/json
        Response:
            return  {
                percent: [{"Absent": "33.33", "Late": "16.66", "Present": "50"},],
            }, 200
            content-type: application/json
        """
        attendance_handler = AttendanceHandler()
        return jsonify(attendance_handler.GetStudentLatestDateAttendance())


class StudentLatestAttendanceDetails(Resource):
    def get(self):
        """
        Gets a percenatge of present, absent and late students for the latest day.
        Param:
        Request:
            path: api/v0/attendance/daily
            body: {},
            # Date format can be iso or "dd-m-YYYY"
            accept: application/json
        Response:
            return  {
                percent: [{"Absent": "33.33", "Late": "16.66", "Present": "50"},],
            }, 200
            content-type: application/json
        """
        attendance_handler = AttendanceHandler()

        return jsonify(attendance_handler.GetStudentLatestDateAttendanceDetails())


class StudentsLowAttendance(Resource):
    def get(self):
        attendance_handler = AttendanceHandler()
        return jsonify(attendance_handler.GetStudentsLowAttendance())


class StudentAttendanceByName(Resource):
    def get(self, student_name):
        attendance_handler = AttendanceHandler()
        return jsonify(attendance_handler.GetStudentAttendanceByName(student_name))


class TeacherAttendance(Resource):
    def post(self):
        # body: {
        #         "attendance": [
        #             {"name": "Shivam Kapoor", "status": "P", "remarks": ""},
        #             {"name": "Tiwari Seth", "status": "A", "remarks": ""},
        #         ],
        #         "date": "16-05-2020",
        #         "updated_by": ""
        #     }

        print(request.json)
        attendance_handler = AttendanceHandler()
        attendance_handler.PostTeacherAttendance(request.json)


class TeacherLatestDateAttendance(Resource):
    def get(self):
        attendance_handler = AttendanceHandler()
        return jsonify(attendance_handler.GetTeacherLatestDateAttendance())


class TeacherLatestAttendanceDetails(Resource):
    def get(self):
        attendance_handler = AttendanceHandler()
        return jsonify(attendance_handler.GetTeacherLatestDateAttendanceDetails())


class TeacherAttendanceByName(Resource):
    def get(self, teacher_name):
        attendance_handler = AttendanceHandler()
        return jsonify(attendance_handler.GetTeacherAttendanceByName(teacher_name))


class TeacherDashboardLineGraph(Resource):
    def get(self, class_id):
        if not class_id:
            return {"error": "mandatory parameter not supplied"}, 404
        attendance_handler = AttendanceHandler()
        return jsonify(attendance_handler.TeacherDashboardLineGraph(class_id))



class TeacherAttendanceReport(Resource):
    def get(self):
        attendance_handler = AttendanceHandler()
        return jsonify(attendance_handler.GetTeacherAttendanceReport())

class TeacherAttendanceReportByName(Resource):
    def get(self, emp_id):
        attendance_handler = AttendanceHandler()
        return jsonify(attendance_handler.GetTeacherAttendanceReportByName(emp_id))


