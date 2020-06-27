
import datetime
import calendar


class AttendanceDao():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def GetAttendanceByStudentId(self, student_id: int, start_date: str = None, end_date: str = None):
        """Get student attendance within the start date and end date range."""
        query = "select status, attendance_date, updated_by from student_attendance_map " \
                "where student_class_map_id = %s and attendance_date >= %s and attendance_date <= %s;" % (
                    student_id, start_date, end_date)
        # arguments = [student_id, start_date, end_date]
        records = self.db_conn.processquery(query=query, fetch=True)
        return records

    def PostAttendanceByStudentId(self, student_id: int, updated_by: int, start_date: str = None, end_date: str = None,
                                  status: str = None):
        """Post student attendance within the start date and end date range and student id and status"""
        query = "select id from student_class_mapping where student_id=%s" % (student_id)
        records = self.db_conn.processquery(query=query, fetch=True)
        student_map_id = records[0]['id']
        print(start_date, status, student_map_id, updated_by)
        query = "insert into student_attendance_map (attendance_date,status,student_class_map_id, updated_by) values" \
                "('%s','%s',%s,%s)" % (start_date, status, student_map_id, updated_by)
        self.db_conn.processquery(query=query, fetch=False)

    def PutAttendanceByStudentId(self, student_id: int, start_date: str = None, end_date: str = None,
                                 status: str = None):
        """update student attendance given student id , start date, end date, status."""
        query = "update student_attendance_map set status = '%s' where student_class_map_id in " \
                "(select id from student_class_mapping where student_id=%s) and " \
                "attendance_date >= '%s' and attendance_date <= '%s' " % (status, student_id, start_date, end_date)
        self.db_conn.processquery(query=query, fetch=False)
        # arguments = [student_id, start_date, end_date]

    def DeleteAttendanceByStudentId(self, student_id: int, start_date: str = None, end_date: str = None):
        """update student attendance given student id , start date, end date, status."""
        query = "select id from student_class_mapping where student_id=%s" % (student_id)
        records = self.db_conn.processquery(query=query, fetch=True)
        student_map_id = records[0]['id']
        query = "delete from student_attendance_map where student_class_map_id = %s and attendance_date >= '%s'" \
                "and attendance_date <='%s'" % (student_map_id, start_date, end_date)
        self.db_conn.processquery(query=query, fetch=False)

        # arguments = [student_id, start_date, end_date]

    def GetAttendanceByClassId(self, class_id: int, start_date: str = None, end_date: str = None):
        """Get student attendance within the start date and end date range."""
        query = "select s.student_fname,s.student_lname, c.roll_no, stu.status from student_class_mapping c " \
                "INNER JOIN students s on c.student_id=s.student_id INNER JOIN student_attendance_map stu " \
                "on stu.student_class_map_id=c.id where stu.attendance_date>=%s and " \
                "stu.attendance_date<=%s and c.class_id=%s;" % (
                    start_date, end_date, class_id)
        # arguments = [student_id, start_date, end_date]
        records = self.db_conn.processquery(query=query, fetch=True)
        for x in range(0,len(records)):
            student = dict()
            if records[x]['status'] == 'P':
                student['student_name'] = records[x]['student_fname'] + ' ' + records[x]['student_lname']
                student['parent_mobile'] = records[x]['mobile']
                student['roll_no'] = records[x]['roll_no']
                student['present_days'] = records[x]['count']
                student['working_days'] = records[x+1]['count']
                return_list.append(student)
        return return_list

    def PostAttendanceByClassId(self, class_id: int, updated_by: int, roll_no: int = None, start_date: str = None,
                                end_date: str = None,
                                status: str = None):
        """Get student attendance within the start date and end date range."""
        query = "select id from student_class_mapping where class_id= %s and roll_no = %s" % (class_id, roll_no)
        records = self.db_conn.processquery(query=query, fetch=True)
        student_map_id = records[0]['id']
        query = "insert into student_attendance_map (attendance_date,status,student_class_map_id, updated_by) values" \
                "('%s','%s',%s,%s)" % (start_date, status, student_map_id, updated_by)
        self.db_conn.processquery(query=query, fetch=False)
        # arguments = [student_id, start_date, end_date]

    def UpdateAttendanceByClassId(self, class_id: int, roll_no: int, start_date: str = None, end_date: str = None,
                                  status: str = None):
        """update student attendance within the start date and end date range."""
        query = "update student_attendance_map set status = '%s' where attendance_date >= '%s'" \
                "and attendance_date <= '%s' and student_class_map_id in" \
                " (select id from student_class_mapping where class_id = %s and roll_no = %s)" % (
                    status, start_date, end_date, class_id, roll_no)
        # arguments = [student_id, start_date, end_date]
        records = self.db_conn.processquery(query=query, fetch=False)

    def DeleteAttendanceByClassId(self, class_id: int, start_date: str = None, end_date: str = None):
        """delete student attendance within the start date and end date range."""
        query = "delete from student_attendance_map where student_class_map_id in (select id from student_class_mapping" \
                " where class_id= %s) and attendance_date >= '%s'" \
                "and attendance_date <= '%s'" % (class_id, start_date, end_date)
        self.db_conn.processquery(query=query, fetch=False)
        # arguments = [student_id, start_date, end_date]

    def DashboardCard1(self, student_id: int):
        """gives the values for the donut graph in student login dashboard"""

        today = datetime.date.today()
        month_name = str(today.year) + str(today.month)
        print(month_name)
        query = "select * from (select month_name,(car.cumulative_present/car.cumulative_working)*100 " \
                "as attendance_percent, (car.cumulative_absent/car.cumulative_working)*100 as " \
                "absent_percent, (car.cumulative_late/car.cumulative_working)*100 as late_percent " \
                "from student_class_mapping scm join cumulative_attendance_records_final car on " \
                "scm.id=car.student_class_map_id where scm.student_id=%s) as gol where month_name='20205' " % (
                    student_id)
        records = self.db_conn.processquery(query=query, fetch=True)
        return records

    def DashboardCard2(self, student_id: int):
        """ list of all leaves taken by the student for student login dashboard"""
        query = "SELECT  sam.attendance_date,sam.status,sam.parent_acknowledged from " \
                "student_attendance_map sam inner join student_class_mapping scm on " \
                "scm.id=sam.student_class_map_id where sam.status!='P' and scm.student_id=%s" % (
                    student_id)
        records = self.db_conn.processquery(query=query, fetch=True)
        print(records)
        return records

    def dashboard_card3_absent_days(self, student_id: int):
        """list of all absent and late days in calendar in student login dashboard"""

        query = "select sam.attendance_date from student_attendance_map sam inner join " \
                "student_class_mapping scm on scm.id=sam.student_class_map_id where sam.status='A'" \
                " and scm.student_id=%s" % (
                    student_id)
        records = self.db_conn.processquery(query=query, fetch=True)
        return records

    def dashboard_card3_late_days(self, student_id: int):
        """list of all absent and late days in calendar in student login dashboard"""

        query = "select sam.attendance_date from student_attendance_map sam inner join " \
                "student_class_mapping scm on scm.id=sam.student_class_map_id where sam.status='L' " \
                "and scm.student_id=%s" % (
                    student_id)
        records = self.db_conn.processquery(query=query, fetch=True)
        return records

    def DashboardCard4your_attendance(self, student_id: int):
        """ line graph values for the student login dashboard"""

        query = "select car.month_name, (car.cumulative_present/car.cumulative_working)*100 as" \
                " attendance_percent from cumulative_attendance_records_final car inner join" \
                " student_class_mapping scm on scm.id=car.student_class_map_id where scm.student_id=%s" % (
                    student_id)
        records = self.db_conn.processquery(query=query, fetch=True)
        return records

    def dashboard_card4_highest_attendance(self, student_id: int):
        """ line graph values for the student login dashboard"""

        query = "select car.student_class_map_id from student_class_mapping scm join " \
                "cumulative_attendance_records_final car on scm.id=car.student_class_map_id " \
                "where scm.class_id in (select class_id from student_class_mapping where student_id=%s)" \
                " and car.month_name in (select max(month_name) from cumulative_attendance_records_final)" \
                " order by cumulative_present desc limit 1" % (student_id)
        records = self.db_conn.processquery(query=query, fetch=True)
        best_student_class_map_id = records[0]['student_class_map_id']
        print(best_student_class_map_id)
        query = "select month_name,(cumulative_present/cumulative_working)*100 as attendance_percent from" \
                " cumulative_attendance_records_final where student_class_map_id in (%s)" % (
                    best_student_class_map_id)
        records = self.db_conn.processquery(query=query, fetch=True)
        return records

    def teacher_dashboard_highest_attendance(self, class_id: int):
        """ line graph values for the teacher login dashboard"""

        query = "select car.student_class_map_id from student_class_mapping scm join " \
                "cumulative_attendance_records_final car on scm.id=car.student_class_map_id " \
                "where scm.class_id in (%s)" \
                " and car.month_name in (select max(month_name) from cumulative_attendance_records_final)" \
                " order by cumulative_present desc limit 1" % (class_id)
        records = self.db_conn.processquery(query=query, fetch=True)
        best_student_class_map_id = records[0]['student_class_map_id']
        print(best_student_class_map_id)
        query = "select month_name,(cumulative_present/cumulative_working)*100 as attendance_percent from" \
                " cumulative_attendance_records_final where student_class_map_id in (%s)" % (
                    best_student_class_map_id)
        records = self.db_conn.processquery(query=query, fetch=True)
        return records

    def teacher_dashboard_worst_attendance(self, class_id: int):
        """ line graph values for the teacher login dashboard"""

        query = "select car.student_class_map_id from student_class_mapping scm join " \
                "cumulative_attendance_records_final car on scm.id=car.student_class_map_id " \
                "where scm.class_id in (%s)" \
                " and car.month_name in (select max(month_name) from cumulative_attendance_records_final)" \
                " order by cumulative_present limit 1" % (class_id)
        records = self.db_conn.processquery(query=query, fetch=True)
        best_student_class_map_id = records[0]['student_class_map_id']
        print(best_student_class_map_id)
        query = "select month_name,(cumulative_present/cumulative_working)*100 as attendance_percent from" \
                " cumulative_attendance_records_final where student_class_map_id in (%s)" % (
                    best_student_class_map_id)
        records = self.db_conn.processquery(query=query, fetch=True)
        return records

    def teacher_dashboard_average_attendance(self, class_id: int):
        """ line graph values for the teacher login dashboard"""

        query = "select month_name,avg((cumulative_present/cumulative_working)*100) as attendance_percent from " \
                "student_class_mapping scm join cumulative_attendance_records_final car on " \
                "scm.id=car.student_class_map_id " \
                "where scm.class_id in (%s) " \
                "group by 1" % (
                    class_id)
        records = self.db_conn.processquery(query=query, fetch=True)
        return records

    def dashboard_card4_average_attendance(self, student_id: int):
        """ line graph values for the student login dashboard"""

        query = "select month_name,avg((cumulative_present/cumulative_working)*100) as attendance_percent from " \
                "student_class_mapping scm join cumulative_attendance_records_final car on " \
                "scm.id=car.student_class_map_id " \
                "where scm.class_id in (select class_id from student_class_mapping where student_id=%s) " \
                "group by 1" % (
                    student_id)
        records = self.db_conn.processquery(query=query, fetch=True)
        return records

    def GetStudentLatestDateAttendance(self):
        query = "select status,count(*) as count from student_attendance_map " \
                "where attendance_date = (select attendance_date from student_attendance_map " \
                "order by attendance_date desc limit 1)" \
                " group by 1 with rollup"
        status_count = self.db_conn.processquery(query=query, fetch=True)
        return status_count

    def GetStudentLatestDateAttendanceDetails(self):
        query = "select student_fname, student_lname, standard, section, roll_no, status, parent_notified, parent_acknowledged " \
                "from students, class, student_class_mapping, student_attendance_map " \
                "where students.student_id = student_class_mapping.student_id " \
                "and class.class_id = student_class_mapping.class_id " \
                "and student_class_mapping.id = student_attendance_map.student_class_map_id " \
                "and attendance_date = (select attendance_date from student_attendance_map " \
                "order by attendance_date desc limit 1)"
        attendance_details = self.db_conn.processquery(query=query, fetch=True)
        return attendance_details

    def GetStudentsLowAttendance(self):
        query = "select student_fname, student_lname, standard, section, sum(at.present_days) as present, sum(at.working_days) as working," \
                "if(exists(select * from student_attendance_map where student_attendance_map.student_class_map_id = student_class_mapping.id and (student_attendance_map.parent_acknowledged = 0 or student_attendance_map.parent_acknowledged is null)), 'Yes', 'No') as unacknowledged " \
                "from cumulative_attendance_records_final, students, class, student_class_mapping " \
                "where students.student_id = student_class_mapping.student_id " \
                "and class.class_id = student_class_mapping.class_id " \
                "and student_class_mapping.id = cumulative_attendance_records_final.student_class_map_id " \
                "and month_name = (select max(month_name) from cumulative_attendance_records_final) " \
                "order by `sum(at.present_days)` limit 10"
        low_attendance = self.db_conn.processquery(query=query, fetch=True)

        print(low_attendance)
        return low_attendance

    def GetStudentAttendanceByName(self, student_fname: str, student_lname: str):
        student_fname = f'"{student_fname}"'
        student_lname = f'"{student_lname}"'

        query = "select student_fname, student_lname, attendance_date, parent_acknowledged, status, `sum(at.present_days)` as present, `sum(at.working_days)` as working " \
                "from students, student_class_mapping, student_attendance_map, cumulative_attendance_records_final " \
                "where students.student_id = student_class_mapping.student_id " \
                "and student_class_mapping.id = student_attendance_map.student_class_map_id " \
                "and student_class_mapping.id = cumulative_attendance_records_final.student_class_map_id " \
                "and cumulative_attendance_records_final.month_name = (select max(month_name) from cumulative_attendance_records_final) " \
                "and student_fname = %s and student_lname = %s " \
                "and status = 'A' order by attendance_date desc" % (student_fname, student_lname)

        attendance_by_name = self.db_conn.processquery(query=query, fetch=True)
        return attendance_by_name

    def PostTeacherAttendance(self, form):
        # print(form)

        for record in form['attendance']:
            print(record)
            record['name'] = f"""'{record['name']}'"""
            record['status'] = f"""'{record['status']}'"""
            record['attendance_date'] = f"""'{form['date']}'"""
            record['updated_by'] = f"""'{form['updated_by']}'"""
            record['updated_on'] = f'"{datetime.now().strftime("%Y-%m-%d")}"'
            record['remarks'] = f"""'{record['remarks']}'"""

            query = "insert into employee_attendance_map (emp_id, attendance_date, status, updated_on, remarks, updated_by) " \
                    "values ((select emp_id from employee where name = %s), %s, %s, %s, %s, %s)" \
                    % (record['name'], record['attendance_date'], record['status'], record['updated_on'],
                       record['remarks'], record['updated_by'])

            self.db_conn.processquery(query=query, fetch=False)

    def GetTeacherLatestDateAttendance(self):
        query = "select status,count(*) as count from employee_attendance_map " \
                "where attendance_date = (select max(attendance_date) from employee_attendance_map) " \
                " group by 1 with rollup"
        status_count = self.db_conn.processquery(query=query, fetch=True)

        return status_count

    def GetTeacherLatestDateAttendanceDetails(self):
        query = "select name, status from employee, employee_attendance_map " \
                "where employee.emp_id = employee_attendance_map.emp_id " \
                "and attendance_date = (select max(attendance_date) from employee_attendance_map) " \
                "and status in ('A','L')"
        attendance_details = self.db_conn.processquery(query=query, fetch=True)

        return attendance_details

    def GetTeacherAttendanceByName(self, name: str):
        name = f'"{name}"'

        query = "select name, attendance_date from employee, employee_attendance_map " \
                "where employee.emp_id = employee_attendance_map.emp_id " \
                "and name = %s and status = 'A' order by attendance_date desc" % (name,)

        attendance_by_name = self.db_conn.processquery(query=query, fetch=True)
        return attendance_by_name

    def GetTeacherAttendanceReport(self):

        query = "select distinct(employee.emp_id), name, mobile, " \
                "(select count(*) from employee_attendance_map where emp_id = employee.emp_id and status = 'P') as present, " \
                "(select count(*) from employee_attendance_map where emp_id = employee.emp_id) as working "\
                "from employee, employee_attendance_map "\
                "where employee.emp_id = employee_attendance_map.emp_id"
                #"and working = (select count(*) from employee_attendance_map where emp_id = e_a_m.emp_id) "\

        attendance_report = self.db_conn.processquery(query=query, fetch=True)
        return attendance_report

    def GetTeacherAttendanceReportByName(self, emp_id):

        #emp_id = f"'emp_id'"

        query = "select attendance_date, status from employee_attendance_map where emp_id = %s" %(emp_id)
        attendance_report_by_name = self.db_conn.processquery(query=query, fetch=True)
        return attendance_report_by_name
