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
        print(start_date)
        print(end_date)
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
        
        if not student_id:
            
            return {"error": "Mandatory parameter student id not supplied"}, 400
        

        data_input=request.json
        
        start_date=data_input['start_date']
        end_date=data_input['end_date']
        status=data_input['status']
        #return jsonify({"student_id": student_id, "start_date": start_date, "end_date": end_date, "status": status})

        attendance_handler = AttendanceHandler()
        print('Making request to the handler to post the students data')

        attendance_handler.PostStudentAttendance(student_id,start_date,end_date,status)
        # SHREESH WORK ENDS HERE

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
        

        data_input=request.json
        
        start_date=data_input['start_date']
        end_date=data_input['end_date']
        status=data_input['status']
        #return jsonify({"student_id": student_id, "start_date": start_date, "end_date": end_date, "status": status})

        attendance_handler = AttendanceHandler()
        print('Making request to the handler to post the students data')

        attendance_handler.PutStudentAttendance(student_id,start_date,end_date,status)


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
        if not student_id:
            
            return {"error": "Mandatory parameter student id not supplied"}, 400
        

        data_input=request.json
        
        start_date=data_input['start_date']
        end_date=data_input['end_date']
        
        #return jsonify({"student_id": student_id, "start_date": start_date, "end_date": end_date, "status": status})

        attendance_handler = AttendanceHandler()
        print('Making request to the handler to post the students data')

        attendance_handler.DeleteStudentAttendance(student_id,start_date,end_date)


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
        print(start_date)
        print(end_date)
        print(request.args)
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
        data_input=request.json
        for i in data_input:
            roll_no=i['roll_no']
            start_date=i['start_date']
            end_date=i['end_date']
            status=i['status']
            #return jsonify({"student_id": student_id, "start_date": start_date, "end_date": end_date, "status": status})

            
            attendance_handler = AttendanceHandler()
            print('Making request to the handler to post the students data')

            attendance_handler.PostStudentsAttendance(class_id,roll_no,start_date,end_date,status)

        #pass

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
        data_input=request.json
        for i in data_input:
            roll_no=i['roll_no']
            start_date=i['start_date']
            end_date=i['end_date']
            status=i['status']
            #return jsonify({"student_id": student_id, "start_date": start_date, "end_date": end_date, "status": status})

            attendance_handler = AttendanceHandler()
            print('Making request to the handler to post the students data')

            attendance_handler.UpdateStudentsAttendance(class_id,roll_no,start_date,end_date,status)
        #pass

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
        
        data_input=request.json
        start_date=data_input['start_date']
        end_date = data_input['end_date']
        attendance_handler = AttendanceHandler()
        print('Making request to the handler to post the students data')

        attendance_handler.DeleteStudentsAttendance(class_id,start_date,end_date)
        
        #pass