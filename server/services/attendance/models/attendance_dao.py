class AttendanceDao():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def GetAttendanceByStudentId(self, student_id: int, start_date: str = None, end_date: str = None):
        """Get student attendance within the start date and end date range."""
        query = "select status, attendance_date from student_attendance_map " \
                "where student_id= %s and attendance_date >= %s and attendance_date <= %s;"
        arguments = [student_id, start_date, end_date]
        records = self.db_conn.processquery(query=query, arguments=arguments, fetch=True)
        return records
    