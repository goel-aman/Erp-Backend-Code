import datetime

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

    def post_leave(self, user_id: int, start_date: str, end_date: str, type_of_leave: str, reason: str):
        """to post the leave request for any employee. made for the teacher leave request."""

        query = "insert into leave_record (user_map_id,start_date,end_date,type_of_leave,reason) " \
                "values (%s,'%s','%s','%s','%s')" % (user_id, start_date, end_date, type_of_leave, reason)
        self.db_conn.processquery(query=query, fetch=False)
        query = "select id, date_of_leave_request from leave_record where user_map_id=%s and start_date='%s'" \
                " and end_date='%s'" % (user_id, start_date, end_date)
        leave_map_id = self.db_conn.processquery(query=query, fetch=True)
        query = "insert into leave_status_record (leave_map_id, status, created_timestamp) " \
                "values (%s,'%s','%s')" % (leave_map_id[0]['id'], 'Pending', leave_map_id[0]['date_of_leave_request'])
        self.db_conn.processquery(query=query, fetch=False)

    def get_leave(self, user_id: int):

        """to get leave records given the user_id"""

        query = "select elr.start_date, elr.end_date, datediff( elr.end_date, elr.start_date) as no_of_days," \
                "elr.type_of_leave, elsr.status from leave_record elr inner join leave_status_record" \
                " elsr on elsr.leave_map_id= elr.id where elr.user_map_id = %s " % (user_id)
        records = self.db_conn.processquery(query=query, fetch=True)
        return records

    def post_leave_status_admin(self, leave_id: int, status: str):
        """to post the status of the leave on the admin page given the leave id. """

        query = "update leave_status_record set status = '%s' where leave_map_id = %s" % (status, leave_id)
        self.db_conn.processquery(query=query, fetch=False)

    def get_leave_record_admin(self, leave_id: int):
        """ to get the leave record for the employee given the leave id. works for the admin page"""

        query = "select user_map_id from leave_record where id= %s" % (leave_id)
        user_id = self.db_conn.processquery(query=query, fetch=True)
        print(user_id)
        query = "select elr.start_date, elr.end_date, datediff( elr.end_date, elr.start_date) as no_of_days," \
                "elr.type_of_leave, elsr.status from leave_record elr inner join leave_status_record" \
                " elsr on elsr.leave_map_id= elr.id where elr.user_map_id = %s " % (user_id[0]['user_map_id'])
        records = self.db_conn.processquery(query=query, fetch=True)
        return records

    def get_leave_history_record_teacher(self, employee_id: int):
        query = "select temp.attendance_date, lr.type_of_leave from (select e.user_id, ear.attendance_date from " \
                "employee_attendance_map ear inner join employee e on e.emp_id=ear.emp_id where ear.emp_id=%s and " \
                "ear.status!='P') as temp" \
                " left outer join leave_record lr on lr.user_map_id=temp.user_id and " \
                "temp.attendance_date>=lr.start_date and temp.attendance_date<=lr.end_date " \
                "" % (employee_id)
        records = self.db_conn.processquery(query=query, fetch=True)
        return records

    def get_leave_category_record_teacher(self, employee_id):
        query = "select e.user_id, ear.attendance_date from employee_attendance_map ear " \
                "inner join employee e on e.emp_id=ear.emp_id where ear.emp_id=%s" % (employee_id)
        records = self.db_conn.processquery(query=query, fetch=True)
        query = "select type_of_leave, count(*) as count from leave_record where user_map_id=%s GROUP by 1" % (records[0]['user_id'])
        records = self.db_conn.processquery(query=query, fetch=True)
        return records


    def UpdateStudentLeaves(self, student_id, leave_date, remarks):
        ack_link = ''
        ack_timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        query = "UPDATE student_attendance_map " \
                "SET parent_remarks=%s, ack_doc_link='', parent_acknowledged_timestamp='%s', parent_acknowledged=1 " \
                "WHERE attendance_date=%s AND status='A' " \
                "AND student_class_map_id=%s;" % (remarks, ack_timestamp, leave_date, student_id)
        records = self.db_conn.processquery(query=query, fetch=False)
        print('---------------------')
        print(records)
        return records

