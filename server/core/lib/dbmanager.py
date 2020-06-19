import abc
import datetime
import sys
import mysql.connector
import re
import time
import traceback
import core.lib.config_dev as config

#from mysql.connector import DBConnectionError


class DBManager(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.conn = None

    @abc.abstractmethod
    def createConnection(self):
        pass

    @abc.abstractmethod
    def getcursor(self):
        print('getting cursor')
        pass

    @abc.abstractmethod
    def processquery(self):
        print("executeQuery from DBManager")
        pass

    def commit(self):
        """
            Committing the changes
        """
        if self.conn:
            self.conn.commit()

    def rollback(self):
        """
            Rollback the changes
        """
        if self.conn:
            self.conn.rollback()

    def close(self):
        """Closing the Connection."""
        if self.conn:
            self.conn.close()


class MySqlDBManager(DBManager):

    def __init__(self, mode, cursor_type=None):
        self.mode = mode
        self.cursor_type = cursor_type
        super(MySqlDBManager, self).__init__()
        self.connection_id = None
        self.conn = self.createConnection()

    def createConnection(self):
        """Getting MySQL Connection."""

        # Getting Configuration Parameters
        try:
            db_config = config.LOCAL_DATABASE_CONFIGURATION
            database = db_config['dbname']
            user = db_config['user']
            passwd = db_config['password']
            host = db_config['host']
            port = db_config['port']
            retry = db_config['retry']

        except Exception as e:
            # logger.exception("exception while fetching config variable.")
            raise
        connection_start_time = datetime.datetime.now()
        for trial in range(retry):
            try:
                # Creating MySQL Connection
                self.conn = mysql.connector.connect(host=host,
                                                    user=user,
                                                    passwd=passwd,
                                                    db=database,
                                                    port=port,
                                                    autocommit=False)
                connection_end_time = datetime.datetime.now()
                time_taken_to_acquire_connection = connection_end_time - connection_start_time
                # logger.debug("User :: " + str(user) + " took " + str(time_taken_to_acquire_connection) + 
                #              " time to acquire connection")
                #Retrieving connection id from MySQL server
                self.connection_id = self.conn.connection_id
                return self.conn

            except (mysql.connector.DatabaseError,
                    mysql.connector.IntegrityError,
                    mysql.connector.InterfaceError,
                    mysql.connector.InternalError,
                    mysql.connector.OperationalError,
                    mysql.connector.PoolError,
                    mysql.connector.DataError,
                    mysql.connector.NotSupportedError,
                    mysql.connector.ProgrammingError) as ex:
                # logger.exception(
                #     " Exception Occurred in creating Connection")
                if trial == retry:
                    raise DBConnectionError(ex.errno, "Database Connection Error : %s", ex)

    def getcursor(self):
        '''
           Creating cursor from the connection.
        '''
        if self.conn:
            if self.cursor_type == "TUPLE_CURSOR":
                return self.conn.cursor()
            return self.conn.cursor(dictionary=True)

    def is_connected(self):
        if self.conn.is_connected():
            return True
        else:
            return False

    def ping(self,reconnect = False):
        self.conn.ping(reconnect)

    def __formatargs(self, query, arguments):
        if isinstance(arguments, tuple):
            arguments = list(arguments)
        if isinstance(arguments, list):
            find_idx = 0
            end_idx = 0
            query = re.sub('\([ ]*%[ ]*s[ ]*\)', '(%s)', query)
            for i, value in enumerate(arguments):
                if (isinstance(value, tuple) or isinstance(value, list)):
                    len_ = len(value)
                    find_idx = query.index('(%s)', end_idx)
                    end_idx = find_idx + len("(%s)")
                    query = list(query)
                    query[find_idx:end_idx] = '(%s' + ', %s' * (len_ - 1) + ')'
                    query = ''.join(query)
                    arguments.remove(value)
                    for ele in value:
                        arguments.insert(i, ele)
                        i += 1
        else:
            pass
        return query, arguments
    
    def split_list(self, data, chunk_size):
        """
        :Notes: Splits the list into chunks of data
        :Args data: Data to be split
        :Args chunk_size: Chunk size
        """
        if isinstance(data, list):
            for i in range(0, len(data), chunk_size):
                yield data[i:i+chunk_size]
        else:
            raise Exception("Argument passed is not of type List")
        
    
    def processquery_paginate(self, query, count=0, arguments=None, fetch=False, returnprikey=0, insert_limit = 1000):
        """
        :Notes: execute the given query respective of given argument.
        :Args: query: query to execute
        :Args: insert_limit - limit for number of inserts to be done in a single shot
        :Args: count: if select query, howmany rows to return
        :Args: arguments: arguments for the query.
        :Args: fetch: select query - True , update/insert query - False
        :Args: returnprikey: insert query - 1, update query - 0
        :returns: total_rowcount - total number of rows inserted
        """
        
        try:
            dao_info = "%s-%s" %(str(sys._getframe().f_back.f_code.co_name), str(sys._getframe().f_back.f_lineno))
        except Exception as e:
            dao_info = query
        query_success = True
        try:
            if arguments:
                logger.debug("Processing the Bulk insert with insert limit :: %s rows "%insert_limit )
                total_rowcount = 0
                curs = self.getcursor()
                processed_arguments = self.split_list(arguments, insert_limit)
                for query_arguments in processed_arguments:
                    try:
                        query_start_time = datetime.datetime.now()
                        curs.executemany(query, query_arguments)
                        rowcount = curs.rowcount
                        total_rowcount = total_rowcount + rowcount
                    except Exception as e:
                        query_success = False
                        rowcount = None
                        raise e
                    finally:
                        query_end_time = datetime.datetime.now()
                        query_execution_time = self.logQueryExecutionTime(query_start_time, query_end_time, query, query_arguments, result_set=None, row_count=rowcount)
                        # log_trace_query(dao_info, query_execution_time, query_success)
                curs.close()
                return total_rowcount
            raise Exception("Arguments not passed for Bulk insert")
        except (mysql.connector.DataError,
                mysql.connector.IntegrityError,
                mysql.connector.NotSupportedError,
                mysql.connector.ProgrammingError) as ex:
            # logger.exception("ConnectionID :: " +
            #                  str(self.connection_id) +
            #                  " Exception Occurred while executing the query")
            raise DBQueryError(ex.errno, 'Exception while executing the Query')
        except (mysql.connector.DatabaseError,
                mysql.connector.InterfaceError,
                mysql.connector.InternalError,
                mysql.connector.OperationalError,
                mysql.connector.PoolError) as ex:
            # logger.exception("ConnectionID :: " +
            #                  str(self.connection_id) +
            #                  " Exception Occurred in creating Connection")
            raise DBConnectionError(ex.errno, 'DB Connection creation Error')
        except ValueError as ex:
            # logger.exception("ConnectionID :: " +
            #                  str(self.connection_id) +
            #                  " Value Error Occurred while executing the query")
            raise DBQueryError(None, 'Exception while executing the Query')
        except Exception as ex:
            # logger.exception("ConnectionID :: " +
            #                  str(self.connection_id) +
            #                  " Un-handled exception in DB Manager processquery")
            raise DBConnectionError(None, 'Un-handled exception in DB Manager processquery paginate')
    
    def processquery(self, query, count=0, arguments=None, fetch=True, returnprikey=0, do_not_log_resultset=0):
        '''
        :Notes: execute the given query respective of given argument.
        :Args: query: query to execute
        :Args: count: if select query, howmany rows to return
        :Args: arguments: arguments for the query.
        :Args: fetch: select query - True , update/insert query - False
        :Args: returnprikey: insert query - 1, update query - 0
        '''
        # try:
            # dao_info = "%s-%s" %(str(sys._getframe().f_back.f_code.co_name), str(sys._getframe().f_back.f_lineno))
        # except Exception as e:
        # dao_info = query
        query_success = False
        query_start_time = None
        query_end_time = None
        query_execution_time = None
        try:
            res = None
            result_set = None
            curs = self.getcursor()
            if arguments:
                query, arguments = self.__formatargs(query, arguments)
            #Calculate query execution time
            print('query', query)
            query_start_time = datetime.datetime.now()
            curs.execute(query, arguments)
            query_success = True
            
            if fetch:
                result_set = curs.fetchall()
                if count == 1 and len(result_set) >= count:
                    res = result_set[0]
                elif count > 1 and len(result_set) >= count:
                    res = result_set[0:count]
                else:
                    res = result_set
                query_end_time = datetime.datetime.now()
                query_execution_time = self.logQueryExecutionTime(query_start_time, query_end_time, query, arguments, result_set=res, row_count=None, do_not_log_resultset=do_not_log_resultset)
            else:
                if returnprikey:
                    res = curs.lastrowid
                else:
                    res = curs.rowcount
                query_end_time = datetime.datetime.now()
                query_execution_time = self.logQueryExecutionTime(query_start_time, query_end_time, query, arguments, result_set=None, row_count=res, do_not_log_resultset=do_not_log_resultset)
            curs.close()
            return res
        except (mysql.connector.DataError,
                mysql.connector.IntegrityError,
                mysql.connector.NotSupportedError,
                mysql.connector.ProgrammingError) as ex:
            # logger.exception("ConnectionID :: " +
            #                  str(self.connection_id) +
            #                  " Exception Occurred while executing the query")
            raise DBQueryError(ex.errno, 'Exception while executing the Query::%s'%ex)
        except (mysql.connector.DatabaseError,
                mysql.connector.InterfaceError,
                mysql.connector.InternalError,
                mysql.connector.OperationalError,
                mysql.connector.PoolError) as ex:
            # logger.exception("ConnectionID :: " +
            #                  str(self.connection_id) +
            #                  " Exception Occurred in creating Connection")
            raise DBConnectionError(ex.errno, 'DB Connection creation Error::%s'%ex)
        except ValueError as ex:
            # logger.exception("ConnectionID :: " +
            #                  str(self.connection_id) +
            #                  " Value Error Occurred while executing the query")
            raise DBQueryError(None, 'Exception while executing the Query::%s'%ex)
        except Exception as ex:
            # logger.exception("ConnectionID :: " +
            #                  str(self.connection_id) +
            #                  " Un-handled exception in DB Manager processquery")
            raise DBConnectionError(None, 'Un-handled exception in DB Manager processquery::%s'%ex)
        finally:
            if not query_success:
                if not query_start_time:
                    query_execution_time = None
                else:
                    query_end_time = datetime.datetime.now()
                    query_execution_time = (query_end_time - query_start_time).total_seconds()
            # log_trace_query(dao_info, query_execution_time, query_success)

    
    def logQueryExecutionTime(self, query_start_time, query_end_time, query, arguments, 
                              result_set=None, row_count=None, do_not_log_resultset=0):
        """
        @summary: This method logs the execution time of the query.
        @param query_start_time: The time before the query is executed.
        @param query_end_time: The time after the query is executed.
        @param query: The actual query which was executed.
        """
        query_execution_time = (query_end_time - query_start_time).total_seconds()
        #log_params = (self.connection_id, query,row_count, query_execution_time)
        #if do_not_log_resultset:
        #    result_set = None
        #13187#sense_log_params = (arguments,result_set)
        #logger.info("ConnectionID :: %s :: Query :: %s ::  Row count/Last row id :: %s"
        #            " :: Query Execution time :: %s "%log_params)
        #13187#logger.sensitive("Arguments:: %s :: Result set :: %s"%sense_log_params)
        return query_execution_time
    
if __name__ == "__main__":
    pass
    # dbManager = MySqlDBManager('loan', 'READ')

    # dbManager.processquery(
    #     'select * from loan',
    #     count=0,
    #     arguments=None,
    #     fetch=True,
    #     returnprikey=0)

    # up_query = "update loan set name=%s where loan_id =%s"
    # dbManager.processqueryandcommit(query=up_query, arguments=('maha', 1), fetch=False)

    # ins_query = "insert into loan values(%s,%s)"
    # res = dbManager.processqueryandcommit(query=ins_query, arguments=(10, 'krishna'),
    #                                       fetch=False, returnprikey=1)
    # print('sdfsfsdfsdfdfsdf', res

    # dbManager.processqueryandcommit('select * from t1',
    #                                 count=0,
    #                                 arguments=None,
    #                                 fetch=True,
    #                                 returnprikey=0)

    # dbManager.commit()
    # dbManager.rollback()
    # dbManager.close()

    # dbManager1 = PostgresDBManager('application')
    # dbManager1.processquery('select * from loan_info', count=0, fetch=True)

    # up_query = "update loan_info set name=%s where loan_id =%s"
    # dbManager1.processqueryandcommit(query=up_query, arguments=('maha', 1), fetch=False)

    # ins_query = "insert into loan_info values(%s,%s)"
    # dbManager1.processqueryandcommit(query=ins_query, arguments=(10, 'krishna'), fetch=False)

    # dbManager1.processqueryandcommit('select * from loan', count=0, fetch=True)
    # dbManager1.commit()
    # dbManager1.rollback()
    # dbManager1.close()