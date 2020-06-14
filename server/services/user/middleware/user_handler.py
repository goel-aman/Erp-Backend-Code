from mysql.connector import DatabaseError
from services.user.models.user_dao import UserDao, UserNotRegisteredError
from core.lib.transactional_manager import TransactionalManager


class UserHandler():
    """Handles user related functions."""
    def GetUserBasicInformation(username, password):
        """Get basic user information."""
        user_id = None
        transaction_mgr = TransactionalManager()
        db_conn = transaction_mgr.GetDatabaseConnection("READ")
        user_dao = UserDao(db_conn)
        try:
            user = user_dao.GetUserByUsername(username)
        except UserNotRegisteredError:
            # log error
            raise
        except DatabaseError:
            # log error
            raise
        
        if not user.password == password:
            raise AuthenticationFailedError("Either username or password is incorrect.")
    
        user_basic_info = user_dao.GetUserBasicInformation(user_role)
        if user_role == 'Teacher':
            is_class_teacher = user_dao.CheckClassTeacherFlag()

        user_basic_info['is_class_teacher'] = is_class_teacher
        return user_basic_info

        # Login the user, return Username or password incorrect if it fails.
        # Set the jwt token as cookie.
        # Get the basic information of user.