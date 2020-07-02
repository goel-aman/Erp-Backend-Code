"""
    Before running this script make sure to restore the sql dump, `acedge_dump_02072020.sql`
"""
import datetime

from core.lib.transactional_manager import TransactionalManager


class MarksAward():
    """
    Processing Quiz responses answers and awarding marks
    """
    def __init__(self, db_conn):
        self.question_type_id = None
        self.db_conn = db_conn


    # Fetch MCQ question_type_id from question_type
    def fetch_question_type(self):
        query = "select id from question_type where question_type='mcq';"
        records = self.db_conn.processquery(query=query, fetch=True)
        self.question_type_id = records[0].get("id")


    # Check if any records in quiz_response,
    def check_records_if_any(self):
        query = "select count(*) as count from quiz_response;"
        records = self.db_conn.processquery(query=query, fetch=True)
        if records[0].get("count") <= 0:
            print("No records in quiz_response -- ", datetime.datetime.now())
            return False
        return True


    # Check if all records are awareded,
    def check_marks_awarded(self):
        query = "select * from quiz_response where marks_awarded is null;"
        records = self.db_conn.processquery(query=query, fetch=True)
        if len(records) <= 0:
            print("All records marks are awarded -- ", datetime.datetime.now())
            return False
        self.quiz_responses = records
        return True


    # Fetch MCQ questions from question_pool
    def fetch_mcq_question(self):
        query = "select id, answer, marks from question_pool where question_type_id=1;"
        records = self.db_conn.processquery(query=query, fetch=True)
        self.question_pool_ids = list()
        self.actual_answers = list()
        self.marks = list()
        if len(records) > 0:
            for i in range(0, len(records)):
                self.question_pool_ids.append(records[i].get("id"))
                self.actual_answers.append(records[i].get("answer"))
                self.marks.append(records[i].get("marks"))


    # Compare question_pool answers with quiz_response answers,
    def process_marks_award(self):
        for record in range(0, len(self.quiz_responses)):
            current_id = self.quiz_responses[record].get("question_pool_id")
            if current_id in self.question_pool_ids:
                index = self.question_pool_ids.index(current_id)
                mark_awarded = float(0)
                if self.quiz_responses[record].get("answer") == self.actual_answers[index]:
                    mark_awarded = float(self.marks[index])
                query = "update quiz_response set marks_awarded=%s where " \
                        "question_pool_id=%s;" % (mark_awarded, self.question_pool_ids[index])
                records = self.db_conn.processquery(query=query, fetch=False)



transaction_mgr = TransactionalManager()
db_conn = transaction_mgr.GetDatabaseConnection("READWRITE")

marksAward = MarksAward(db_conn)
if marksAward.check_records_if_any() and marksAward.check_marks_awarded():
    marksAward.fetch_mcq_question()
    marksAward.process_marks_award()
else:
    exit(1)

transaction_mgr.save()
