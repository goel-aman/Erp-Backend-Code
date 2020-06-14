_STUDENT_BASIC_INFO_QUERY = """select s.student_fname, s.student_lname, c.standard, c.section 
from students s inner join student_class_mapping scm on s.student_id = scm.student_id
inner join class c on c.class_id = scm.class_id where s.user_id= %s;
"""

_TEACHER_BASIC_INFO_QUERY = """select e.name, tcm.is_class_teacher, c.standard, c.section 
from employee e inner join teachers t on e.emp_id = t.employee_emp_id inner join teacher_class_mapping tcm 
on tcm.teacher_id = t.teacher_id inner join class c on c.class_id = tcm.class_id 
where e.user_id= %s;
"""

_USERROLE_BASIC_INFO_QUERY_MAP = {
    'Student': _STUDENT_BASIC_INFO_QUERY,
    'Teacher': _TEACHER_BASIC_INFO_QUERY,
}


class UserNotRegisteredError(Exception):
    """User is not registered in the system."""


class UserDao():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def GetUserByUsername(self, username):
        """Get user entity based on the username."""
        user_query = "select * from users where username=%s"
        arguments = [username]
        records = self.db_conn.processquery(query=query, arguments=arguments, fetch=True)
        if len(records) < 1:
            raise UserNotRegisteredError("User with username %s not found".format(username))
        return records

    def GetUserBasicInformation(self, user):
        """Get student basic information."""
        query = _USERROLE_BASIC_INFO_QUERY_MAP[user_role]
        arguments = [user_id]
        records = self.db_conn.processquery(query=query, arguments=arguments, fetch=True)
        return records
