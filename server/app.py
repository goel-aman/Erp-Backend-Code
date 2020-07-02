from flask import Flask
from flask_restful import Api
from services.leave_management.leave_controller import StudentLeaves, SubmitLeave, ManageLeavesAdmin, \
    TeacherDashboardLeaveHistory, TeacherDashboardLeaveCategoryRecord
from services.attendance.attendance_controller import StudentAttendance, StudentsAttendance, \
    StudentLatestDateAttendance, StudentLatestAttendanceDetails, StudentsLowAttendance, StudentAttendanceByName, \
    TeacherDashboardLineGraph
from services.attendance.attendance_controller import StudentAttendance, StudentsAttendance, StudentLatestDateAttendance, StudentLatestAttendanceDetails, StudentsLowAttendance, StudentAttendanceByName, TeacherAttendance, TeacherLatestDateAttendance, TeacherLatestAttendanceDetails, TeacherAttendanceByName, TeacherAttendanceReport, TeacherAttendanceReportByName
from services.attendance.attendance_controller import StudentAttendance, StudentsAttendance, StudentDashboardCard1, \
    StudentDashboardCard2, StudentDashboardCard3, StudentDashboardCard4
from services.leave_management.leave_controller import StudentLeaves, SubmitLeave, ManageLeavesAdmin
from services.attendance.attendance_controller import StudentAttendance, StudentsAttendance, StudentLatestDateAttendance, StudentLatestAttendanceDetails, StudentsLowAttendance, StudentAttendanceByName
from services.leave_management.leave_controller import StudentLeaves

from services.assignment.assignment_controller import UploadAssignmentByEmployee, AssignmentSubmit

app = Flask(__name__)
api = Api(app)

# app.config['UPLOAD_FOLDER'] = "uploads/"


api.add_resource(StudentAttendance, "/attendance/student/<int:student_id>")
"""
    get -> teacher login (class attendance -> upload attendance)
    post -> teacher login (class attendance -> upload attendance)
    put -> teacher login (class attendance -> upload attendance)
    delete -> teacher login (class attendance -> upload attendance)
"""
api.add_resource(StudentDashboardCard1, "/studentdashboardcard1/<int:student_id>")
"""
    get -> student login  attendance dashboard 
"""
api.add_resource(StudentDashboardCard2, "/studentdashboardcard2/<int:student_id>")
"""
    get -> student login  attendance dashboard 
"""
api.add_resource(StudentDashboardCard3, "/studentdashboardcard3/<int:student_id>")
"""
    get -> student login  attendance dashboard 
"""
api.add_resource(StudentDashboardCard4, "/studentdashboardcard4/<int:student_id>")
"""
    get -> student login  attendance dashboard 
"""
api.add_resource(StudentLeaves, "/leaves/student")
"""
    put -> for parent to acknowledge student leave
    # parent login 
"""
api.add_resource(StudentLatestDateAttendance, "/attendance/daily")
"""
    get -> student donut chart
    # admin login
"""
api.add_resource(StudentLatestAttendanceDetails, "/attendance/details")
"""
get #admin login
"""
api.add_resource(StudentsLowAttendance, "/attendance/low")
"""
get #admin login
"""
api.add_resource(StudentAttendanceByName, "/attendance/name/<student_name>")
"""
get #admin login
"""
api.add_resource(TeacherAttendance, "/attendance/teacher")
"""
 get teacher attendance dashboard # admin login
"""
api.add_resource(TeacherLatestDateAttendance, "/attendance/teacher/daily")
"""
 get teacher attendance dashboard # admin login
"""
api.add_resource(TeacherLatestAttendanceDetails, "/attendance/teacher/details")
"""
 get teacher attendance dashboard # admin login 
"""
api.add_resource(TeacherAttendanceByName, "/attendance/teacher/name/<teacher_name>")
api.add_resource(TeacherAttendanceReport, "/attendance/teacher/report")
api.add_resource(TeacherAttendanceReportByName, "/attendance/teacher/report/<int:emp_id>")


api.add_resource(SubmitLeave, "/submitleave/<int:user_id>")
"""
    get -> teacher login (leave -> apply leave)
    post -> teacher login (leave -> apply leave)
"""
api.add_resource(ManageLeavesAdmin, "/leavestatusadmin/<int:leave_id>")
"""
    get -> admin login (attendance -> manage leaves)
    post -> admin login (attendance -> manage leaves)
"""
api.add_resource(TeacherDashboardLineGraph, "/teacherdashboardlinegraph/<int:class_id>")
"""
    get -> teacher login (class attendance -> attendance dashboard)
"""
api.add_resource(TeacherDashboardLeaveHistory, "/teacherdashboardleavehistory/<int:employee_id>")
"""
    get -> teacher login (leave -> leave dashboard)
"""
api.add_resource(TeacherDashboardLeaveCategoryRecord, "/teacherdashboardleavecategory/<int:employee_id>")
"""
    get -> teacher login (leave -> leave dashboard)
"""

"""
    ASSIGNMENT - related APIs
"""

api.add_resource(UploadAssignmentByEmployee, "/assignment/employee/<int:employee_id>")
"""
    post -> teacher or admin assignment upload
"""
api.add_resource(AssignmentSubmit, "/assignmentsubmit/<int:student_id>")
"""
    post -> student login assignment submit responses
"""

if __name__ == "__main__":
    app.run(port=5000, debug=True)
