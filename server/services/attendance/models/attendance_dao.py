class AttendanceDao():
    def __init__(self, db_conn):
        self.db_conn = db_conn



    def GetAttendanceByStudentId(self, student_id: int, start_date: str = None, end_date: str = None):
        """Get student attendance within the start date and end date range."""
        query = "select status, attendance_date, updated_by from student_attendance_map " \
                "where student_class_map_id = %s and attendance_date >= %s and attendance_date <= %s;"%(student_id, start_date, end_date)
        #arguments = [student_id, start_date, end_date]
        records = self.db_conn.processquery(query=query, fetch=True)
        return records
    
    # SHREESH WORK STARTS HERE

    def PostAttendanceByStudentId(self, student_id: int, start_date: str = None, end_date: str = None, status: str = None):
        """Post student attendance within the start date and end date range and student id and status"""
        #query = ""
        #arguments = [student_id, start_date, end_date]
        #self.db_conn.processquery(query=query, fetch=True)
        #return records
        
        return 'ok'
    
    def PutAttendanceByStudentId(self, student_id: int, start_date: str = None, end_date: str = None, status: str = None):
        """update student attendance given student id , start date, end date, status."""
        #query = ""
        #arguments = [student_id, start_date, end_date]
        #self.db_conn.processquery(query=query, fetch=True)
        #return records
        print("             attendance_dao put working         ")
        print(student_id,start_date,end_date,status)
        return 'ok'

    def DeleteAttendanceByStudentId(self, student_id: int, start_date: str = None, end_date: str = None):
        """update student attendance given student id , start date, end date, status."""
        #query = ""
        #arguments = [student_id, start_date, end_date]
        #self.db_conn.processquery(query=query, fetch=True)
        #return records
        return 'ok'


    def GetAttendanceByClassId(self, class_id: int, start_date: str = None, end_date: str = None):
        """Get student attendance within the start date and end date range."""
        query = "select s.student_fname,s.student_lname, c.roll_no, stu.status from student_class_mapping c INNER JOIN students s on c.student_id=s.student_id INNER JOIN student_attendance_map stu on stu.student_class_map_id=c.id where stu.attendance_date>=%s and stu.attendance_date<=%s and c.class_id=%s;"%(start_date,end_date,class_id)
        #arguments = [student_id, start_date, end_date]
        records = self.db_conn.processquery(query=query, fetch=True)
        return records

    def PostAttendanceByClassId(self, class_id: int, roll_no: int = None, start_date: str = None, end_date: str = None, status: str = None):
        """Get student attendance within the start date and end date range."""
        #query = ""
        #arguments = [student_id, start_date, end_date]
        #records = self.db_conn.processquery(query=query, fetch=True)
        print("          attendance dao class post    ")
        print(class_id,roll_no,start_date,end_date,status)
        return 'ok'

    def UpdateAttendanceByClassId(self, class_id: int, roll_no: int, start_date: str = None, end_date: str = None, status: str = None):
        """Get student attendance within the start date and end date range."""
        #query = ""
        #arguments = [student_id, start_date, end_date]
        #records = self.db_conn.processquery(query=query, fetch=True)
        print("          attendance dao class put    ")
        print(class_id,roll_no,start_date,end_date,status)
        return 'ok'

    def DeleteAttendanceByClassId(self, class_id: int, start_date: str = None, end_date: str = None):
        """Get student attendance within the start date and end date range."""
        #query = ""
        #arguments = [student_id, start_date, end_date]
        #records = self.db_conn.processquery(query=query, fetch=True)
        print("          attendance dao class delete    ")
        print(class_id,start_date,end_date)
        return 'ok'