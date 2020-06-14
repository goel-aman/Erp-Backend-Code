"""
Transaction manager : This is used for all achieving the transactional behaviour accross multiple
medium like databases, files, web service connection, etc. If any one of the medium fails, this will
rollback remaining all medium which are involved.

"""

import sys
import inspect
from datetime import datetime
from core.lib.dbmanager import MySqlDBManager


class TransactionalManager(object):
    """
        :Note: Performs transaction behaviour which involves database, files and webservice
                 transaction

    """

    def __init__(self, cursor_type=None):
        self.storage_mapping = {
            "MYSQL": MySqlDBManager
        }
        self.modes = ["READWRITE", "READ", "SECONDARY_DB"]
        self.cursor_type = cursor_type
        self.__database_conn_objects = {}

    def GetDatabaseConnection(self, mode):
        """
        :Note: Get new connection if the given section is not participated yet else returns
                 old connection

        :Args:
            section : LOAN/ACCOUNT/..
            mode : READ / READWRITE

        :Returns:
            database wrapper object
        """
        # logger.info("Inside TransactionalManager.get_database_connection ")
        server_mode = None
        if mode not in self.modes:
            # logger.debug("Given mode value is not exists - section : %s, mode = %s", section, mode)
            raise ValueError("Database Mode not exists")

        else:
            server_mode = mode

        # storage = ConfigManager.getConfigManager(section='DBCREDENTIALS',
        #        
        old_db_con_obj = self.__database_conn_objects.get(mode)
        if old_db_con_obj and old_db_con_obj.is_connected():
            # logger.debug("Returning already participated database connection object for the \
            #               section : %s, mode : %s ", section, mode)
            return old_db_con_obj
        # logger.debug("creating the database connection object for the section : %s, mode : %s, \
        #               storage : %s ", section, mode, storage)
        new_db_con_obj = self.storage_mapping['MYSQL'](server_mode, cursor_type=self.cursor_type)
        self.__database_conn_objects[mode] = new_db_con_obj
        # logger.debug("Returning New database connection object for the section : %s, mode : %s",
        #              section, mode)
        # Getting details of Caller which create a new db connection
        # parentframe = sys._getframe(1)
        # method_name = parentframe.f_code.co_name
        # module = inspect.getmodule(parentframe).__name__
        # if 'self' in parentframe.f_locals:
        #     class_name = parentframe.f_locals['self'].__class__.__name__
        # else:
        #     class_name = None
        conn_id = new_db_con_obj.connection_id
        # logger.debug("Module:Class:Method <--> connection_id :: %s:%s:%s <--> %s", module,class_name,method_name, conn_id)
        return new_db_con_obj

    def end(self):
        """
        :Note: Ends the transactions - database, file, webservice
        :Args:
            self.__database_conn_objects
            self.__file_obj_list
            self.__webservice_conn_obj_list
        :Returns:
            None
        """
        # logger.info("Inside TransactionalManager.end")
        # close the database connection objects
        for mode, db_conn_obj in self.__database_conn_objects.items():
            # logger.sensitive("Closing database connection object for the section : %s", section)
            db_conn_obj.close()
        self.__database_conn_objects = {}

    def save(self):
        """
        :Note: It commits all transaction

        :Args:
            self.__database_conn_objects
            self.__file_obj_list
            self.__webservice_conn_obj_list
        :Returns:
            None
        """
        # logger.info("Inside TransactionalManager.save")
        # commit the database transaction
        for mode, db_conn_obj in self.__database_conn_objects.items():
            # logger.debug("Committing the database connection object for the section : %s", section)
            db_conn_obj.commit()

    def revertback(self):
        """
        :Note: It rollback all transaction

        :Args:
            self.__database_conn_objects
            self.__file_obj_list
            self.__webservice_conn_obj_list
        :Returns: None

        """
        # logger.info("Inside TransactionalManager.revertback")
        # rollback the database transaction
        for section, db_conn_obj in self.__database_conn_objects.items():
            # logger.debug("Rollbacking the database connection object for the section : %s", section)
            db_conn_obj.rollback()
            
    def __del__(self):
        self.end()


if __name__ == '__main__':
    pass
