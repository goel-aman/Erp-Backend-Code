from flask import Flask
from flask_restful import Api

from services.leave_management.leave_controller import StudentLeaves, SubmitLeave, ManageLeavesAdmin, \
                                                    TeacherDashboardLeaveHistory, TeacherDashboardLeaveCategoryRecord
from services.leave_management.leave_controller import StudentLeaves, SubmitLeave, ManageLeavesAdmin

from services.attendance.attendance_controller import StudentAttendance, StudentsAttendance, \
                                                    StudentLatestDateAttendance, StudentLatestAttendanceDetails, \
                                                    StudentsLowAttendance, StudentAttendanceByName
from services.attendance.attendance_controller import TeacherAttendance, TeacherLatestDateAttendance, \
                                                    TeacherLatestAttendanceDetails, TeacherAttendanceByName, \
                                                    TeacherAttendanceReport, TeacherAttendanceReportByName, \
                                                    TeacherDashboardLineGraph
from services.attendance.attendance_controller import StudentDashboardCard1, StudentDashboardCard2, \
                                                    StudentDashboardCard3, StudentDashboardCard4
from services.assignment.assignment_controller import AssignmentQuestions, PendingAssignment, CompletedAssignment, \
                                                    AssignmentByEmployee, TeacherAssignments, \
                                                    TeacherAssignmentDetailView, AssignmentSubmit, \
                                                    GetAssignment, AssignmentHistory, PostAssignmentMarks

app = Flask(__name__)
api = Api(app)


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


api.add_resource(AssignmentByEmployee, "/assignment/employee/<int:employee_id>")
"""
    get     -> employee active assignments
    post    -> employee assignment upload
    delete  -> employee assignment delete
"""
api.add_resource(TeacherAssignments, "/teacher/<int:teacher_id>/assignments")
"""
    post    -> teacher or admin assignment upload 
"""
api.add_resource(TeacherAssignmentDetailView, "/teacher/<int:teacher_id>/assignments/<int:assignment_id>")
"""
    get     -> Teacher assignments list with details
"""
api.add_resource(AssignmentSubmit, "/assignmentsubmit/<int:student_id>")
"""
    post    -> student login assignment submit responses
    get     -> Teacher assignment with student list view
"""
api.add_resource(GetAssignment, "/getstudentassignmentsolution/")
"""
    get     -> teacher login assignment get student assignment solution
"""
api.add_resource(AssignmentQuestions, "/assignment_ques/<int:assignment_id>")
"""
    get -> questions of a particular assignment
"""

api.add_resource(PendingAssignment, "/pending_assignment/<int:student_id>")
"""
    get -> pending assignment of a particular student
"""

api.add_resource(CompletedAssignment, "/completed_assignment/<int:student_id>/<int:subject_id>")
"""
    get -> completed assignment of a particular student of a particular subject 
"""

api.add_resource(AssignmentHistory, "/assignmenthistory/<int:student_id>")
"""
    get -> student login assignment submitted history
"""
api.add_resource(PostAssignmentMarks, "/postassignmentmarks/<int:teacher_id>")
"""
    post-> teacher login to post student assignment marks
"""
if __name__ == "__main__":
    app.run(port=5000, debug=True)
