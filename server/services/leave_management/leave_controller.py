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
        if not request.args.get('roll_no') and not request.args.get('student_id') and not request.args.get('admission_id'):
            return {"error": "Kindly send either admission no or student's rollno."}, 400
        leave_handler = LeaveHandler()
        return jsonify(leave_handler.GetStudentLeaves(**request.args))
