class LeaveDao():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def GetLeavesByAdmissionNo(self, admission_no: int):
        if not admission_no:
            return 

        student_leaves = []
        query = "select sm.attendance_date, sm.status, sm.parent_acknowledged from students s " \
                "left join student_attendance_map sm on s.student_id = sm.student_id " \
                "where s.admission_no = %s and sm.status IN ('A','L'); "
        arguments = [admission_no]
        student_leaves = self.db_conn.processquery(query=query, arguments=arguments, fetch=True)
        return student_leaves

    def GetLeavesByStudentClassId(self, roll_no: int, class_id: int):
        if not roll_no or not class_id:
            return
        
        student_leaves = []
        query = "select sm.attendance_date, sm.status, sm.parent_acknowledged from student_class_mapping scm " \
                "left join student_attendance_map sm on scm.student_id = sm.student_id " \
                "where scm.roll_no = %s and scm.class_id = %s and sm.status IN ('A', 'L');"
        arguments = [roll_no, class_id]
        student_leaves = self.db_conn.processquery(query=query, arguments=arguments, fetch=True)
        return student_leaves

    def GetStudentLeavesById(self, student_id: int):
        if not student_id:
            return
        
        student_leaves = []
        query = "select attendance_date, status, parent_acknowledged from student_attendance_map " \
                "where student_id = %s and status IN ('A', 'L');"
        arguments = [student_id]
        student_leaves = self.db_conn.processquery(query=query, arguments=arguments, fetch=True)
        return student_leaves