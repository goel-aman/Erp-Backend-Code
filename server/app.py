from flask import Flask
from flask_restful import Api
from services.attendance.attendance_controller import StudentAttendance, StudentsAttendance
from services.leave_management.leave_controller import StudentLeaves

app = Flask(__name__)
api = Api(app)

api.add_resource(StudentAttendance, "/attendance/student/<int:student_id>")
api.add_resource(StudentsAttendance, "/attendance/class/<int:class_id>")
api.add_resource(StudentLeaves, "/leaves/student")

if __name__ == "__main__":
    app.run(port=5000, debug=True)