#!/usr/bin/env python
# coding: utf-8

# # Mental Health in the Tech Industry Data Processing

# Let's create a class for gathering the data, statistical calculation and processing data for presentation and visualization.


import sqlite3
import numpy as np



class DataProcessing:
    ''' Class for gathering the data, statistical calculation and processing data. '''
    
    def __init__(self, path, db_name):
        self.path = path
        self.db_name = db_name
    
    def get_table(self, table):
        ''' Get table content from the database. '''
        conn = sqlite3.connect(f'{self.path}{self.db_name}.sqlite')
        c = conn.cursor()
        c.execute(f"SELECT * FROM {table}")
        table = c.fetchall()
        conn.close()
        return table

    def get_all_answers_per_q(self, q_id):
        ''' Get all unique answers from Answer table for particular question 
            represented by QuestionID number from the Question table. '''
        conn = sqlite3.connect(f'{self.path}{self.db_name}.sqlite')
        c = conn.cursor()
		# SELECT DISTINCT can be used
        c.execute("SELECT AnswerText FROM Answer WHERE QuestionID = ?", (q_id,)) 
#         answers = set(c.fetchall())
        answers = list(dict.fromkeys(c.fetchall())) # let's keep the order
        conn.close()
        return answers
    
    def get_all_years_per_q(self, q_id):
        ''' Get all unique years from Answer table for particular question 
            represented by QuestionID. '''
        conn = sqlite3.connect(f'{self.path}{self.db_name}.sqlite')
        c = conn.cursor()
        c.execute("SELECT SurveyID FROM Answer WHERE QuestionID = ?", (q_id,))
        years = list(dict.fromkeys(c.fetchall()))
        conn.close()
        return years
    
    def get_users_no_per_q(self, q_id):
        ''' Get number of all answers for the question. '''
        conn = sqlite3.connect(f'{self.path}{self.db_name}.sqlite')
        c = conn.cursor()
        c.execute("SELECT count(UserID) FROM Answer WHERE QuestionID = ?", (q_id,))
        user_no = c.fetchone()[0]
        conn.close()
        return user_no
    
    def get_users_no_for_q_and_answer(self, q_id, answer):
        ''' Get number of users from Answer table for particular question number (QuestionID) and answer (AnswerText). '''
        conn = sqlite3.connect(f'{self.path}{self.db_name}.sqlite')
        c = conn.cursor()
        c.execute("SELECT count(UserID) FROM Answer WHERE QuestionID = ? and AnswerText = ?", (q_id, answer))
        user_no = c.fetchone()[0]
        conn.close()
        return user_no
    
    def get_users_no_per_answer(self, q_id):
        ''' Get frequency of the answers for particular question number (QuestionID) in Answer table. '''
        conn = sqlite3.connect(f'{self.path}{self.db_name}.sqlite')
        c = conn.cursor()
        c.execute("SELECT AnswerText, count(UserID) FROM Answer WHERE QuestionID = ? GROUP BY AnswerText", (q_id,))
        user_no = c.fetchall()
        conn.close()
        return user_no
    
    def get_table_based_value_from_column(self, table, column, value):
        ''' Get particular answer from provided table. '''
        conn = sqlite3.connect(f'{self.path}{self.db_name}.sqlite')
        c = conn.cursor()
        c.execute(f"SELECT * FROM {table} WHERE {column} = ?", (value,))
        value = c.fetchall()
        conn.close()
        return value

    def get_answers_for_q_less_occ(self, q_id, qty):
        ''' Get answers for provided question q_id where occurency is less than qty. '''
        q_id, qty = int(q_id), int(qty)
        conn = sqlite3.connect(f'{self.path}{self.db_name}.sqlite')
        c = conn.cursor()
        c.execute(f'SELECT AnswerText, count(UserID) as UNo FROM Answer WHERE QuestionID = ? GROUP BY AnswerText HAVING UNo < ?', 
                  (q_id, qty))
        answers = c.fetchall()
        conn.close()
        return answers

    def get_answers_for_q_greater_occ(self, q_id, qty):
        ''' Get answers for provided question q_id where occurency is greater than qty. '''
        q_id, qty = int(q_id), int(qty)
        conn = sqlite3.connect(f'{self.path}{self.db_name}.sqlite')
        c = conn.cursor()
        c.execute(f'SELECT AnswerText, count(UserID) as UNo FROM Answer WHERE QuestionID = ? GROUP BY AnswerText HAVING UNo > ?', 
                  (q_id, qty))
        answers = c.fetchall()
        conn.close()
        return answers
    
    def get_answers_for_q_in_year(self, q_id, year):
        ''' Get all answers from Answer table for particular question (QuestionID)
            in given year (SurveyID). '''
        conn = sqlite3.connect(f'{self.path}{self.db_name}.sqlite')
        c = conn.cursor()
        c.execute("SELECT AnswerText FROM Answer WHERE QuestionID = ? and SurveyID = ?", (q_id, year))
        answers = set(c.fetchall())
        conn.close()
        return answers
    
    def get_users_no_for_q_and_answer_in_year(self, q_id, answer, year):
        ''' Get number of users from Answer table for particular question number (QuestionID) and answer (AnswerText)
            in given year (SurveyID). '''
        conn = sqlite3.connect(f'{self.path}{self.db_name}.sqlite')
        c = conn.cursor()
        c.execute("SELECT count(UserID) FROM Answer WHERE QuestionID = ? and AnswerText = ? and SurveyID = ?", (q_id, answer, year))
        user_no = c.fetchone()[0]
        conn.close()
        return user_no
    
    def get_users_no_per_q_in_year(self, q_id, year):
        ''' Get number of all answers for the question in given year (SurveyID). '''
        conn = sqlite3.connect(f'{self.path}{self.db_name}.sqlite')
        c = conn.cursor()
        c.execute("SELECT count(UserID) FROM Answer WHERE QuestionID = ? and SurveyID = ?", (q_id, year))
        user_no = c.fetchone()[0]
        conn.close()
        return user_no
    
    def get_answers_for_question(self, q_id):
        ''' Get answers content for given question. '''
        conn = sqlite3.connect(f'{self.path}{self.db_name}.sqlite')
        c = conn.cursor()
        c.execute(f"SELECT AnswerText FROM Answer WHERE QuestionID = ?", (q_id,))
        table = c.fetchall()
        conn.close()
        return table
    
    def get_answers_for_questions(self, q_ids):
        ''' Get answers content for given questions. '''
        values_no = ('?, '*len(q_ids))[:-2]
        conn = sqlite3.connect(f'{self.path}{self.db_name}.sqlite')
        c = conn.cursor()
        c.execute(f"SELECT AnswerText FROM Answer WHERE QuestionID = {values_no}", (*q_ids))
        table = c.fetchall()
        conn.close()
        return table
    
    def get_table_for_questions(self, q_ids):
        ''' Get table content for given questions. '''
        values_no = ('?, '*len(q_ids))[:-2]
        conn = sqlite3.connect(f'{self.path}{self.db_name}.sqlite')
        c = conn.cursor()
        c.execute(f"SELECT * FROM Answer WHERE QuestionID = {values_no}", (*q_ids))
        table = c.fetchall()
        conn.close()
        return table
    
    def get_different_answers_for_2q(self, q_id1, q_id2):
        ''' Get different answers on two questions for the same user. '''
        conn = sqlite3.connect(f'{self.path}{self.db_name}.sqlite')
        c = conn.cursor()
        c.execute(f"""SELECT AnswerText, UserID as uid FROM Answer 
        WHERE QuestionID = ? and AnswerText != (SELECT AnswerText FROM Answer WHERE UserID = uid and QuestionID = ?)""",
                 (q_id1, q_id2))
        table = c.fetchall()
        conn.close()
        return table
    
    def get_different_answers_for_2q_v2(self, q_id1, q_id2):
        ''' Get different answers on two questions for the same user.
            Much faster than get_different_answers_for_2q. '''
        tab_q1 = self.get_answers_ordered_by_uid(q_id1)
        tab_q2 = self.get_answers_ordered_by_uid(q_id2)
        diff_table = self._get_diff_table(tab_q1, tab_q2)
        return self._get_combined_tab_uid_based(diff_table, tab_q1)
        
    def get_answers_ordered_by_uid(self, q_id):
        ''' Get the answers ordered by UserID for given question. '''
        conn = sqlite3.connect(f'{self.path}{self.db_name}.sqlite')
        c = conn.cursor()
        c.execute(f"SELECT AnswerText, UserID FROM Answer WHERE QuestionID = ? Order by UserID", (q_id,))
        table = c.fetchall()
        conn.close()
        return table
    
    @staticmethod
    def _get_diff_table(tab1, tab2):
        ''' Returns the difference between two lists. '''
        table1 = set(tab1)
        table2 = set(tab2)
        return table2.difference(table1)
    
    @staticmethod
    def _get_combined_tab_uid_based(tab1, tab2):
        ''' Returns a list which combine first values from lists of tuples tab1 and tab2
            based on the second values.
            tab1 and tab2 need to have values of tuples of length 2. '''
        result_list = []
        for wc, wuid in list(tab1):
            for lc, luid in list(tab2):
                if luid == wuid:
                    result_list.append((lc, wc, wuid))
        return result_list    
    
    def get_users_no_per_two_q(self, q_id1, q_id2):
        ''' Get number of users who answered for provided two questions. '''
        conn = sqlite3.connect(f'{self.path}{self.db_name}.sqlite')
        c = conn.cursor()
        c.execute(f"""SELECT count(UserID), UserID as uid 
        FROM Answer WHERE QuestionID = ? and 
        EXISTS(SELECT AnswerText FROM Answer WHERE UserID = uid and QuestionID = ?)""",
                 (q_id1, q_id2))
        user_no = c.fetchone()[0]
        conn.close()
        return user_no
    
    def get_all_answers_based_on_answer_and_q(self, q_id, answer):
        ''' Get all answers for all users which answered on given question (q_id) in particular way (answer). '''
        conn = sqlite3.connect(f'{self.path}{self.db_name}.sqlite')
        c = conn.cursor()
        c.execute(f"""SELECT * FROM Answer 
                  WHERE UserID in (SELECT UserID FROM Answer WHERE AnswerText = ? and QuestionID = ?) 
                  Order by UserID""", (answer, q_id))
        table = c.fetchall()
        conn.close()
        return table
    
    def get_some_answers_based_on_answer_and_q(self, q_ids, q_id, answer):
        ''' Get answers on q_ids questions for all users which answered on given question (q_id) in particular way (answer). '''
        values_no = ('?, '*len(q_ids))[:-2]
        conn = sqlite3.connect(f'{self.path}{self.db_name}.sqlite')
        c = conn.cursor()
        c.execute(f"""SELECT * FROM Answer 
                  WHERE QuestionID in ({values_no}) 
                  and UserID in (SELECT UserID FROM Answer WHERE AnswerText = ? and QuestionID = ?) 
                  Order by UserID""", (*q_ids, answer, q_id))
        table = c.fetchall()
        conn.close()
        return table
    
    def get_some_answer_no_based_on_answer_and_q(self, q_id1, q_id2, answer):
        ''' Get number of answers on q_id1 question for all users 
            which answered on given question (q_id2) in particular way (answer). '''
        conn = sqlite3.connect(f'{self.path}{self.db_name}.sqlite')
        c = conn.cursor()
        c.execute(f"""SELECT DISTINCT AnswerText, Count(UserID) OVER (PARTITION BY AnswerText) FROM Answer 
                  WHERE QuestionID = ?
                  and UserID in (SELECT UserID FROM Answer WHERE AnswerText = ? and QuestionID = ?)""", 
                  (q_id1, answer, q_id2))
        table = c.fetchall()
        conn.close()
        return table
    
    def get_answers_distribution_for_q(self, q_id):
        ''' Get users percentage per answer for given question. '''
        answers = self.get_users_no_per_answer(q_id)
        return self._change_total_to_pct(answers)      
        
    def _change_total_to_pct(self, tab):
        ''' Change input table of answers with total occurrence to the percentage representation.
            Only table (answer,..., count) is supported. '''
#         sum_of_answers = sum([no for _, no in tab]) # works only for (answer, count)
        sum_of_answers = sum([row[-1] for row in tab]) # works for (answer,..., count) 
        table = []
#         for answer, value in tab: # works only for (answer, count) 
#             table.append((answer, self._round_2(100*value/sum_of_answers)))
        for row in tab: # works for (answer,..., count) 
            answer, value = row[0], row[-1]
            if len(row) > 2:
                table.append((answer, *row[1:-1], self._round_2(100*value/sum_of_answers)))
            else:
                table.append((answer, self._round_2(100*value/sum_of_answers)))
        return table
    
    def get_answers_distribution_for_q_by_years(self, q_id):
        ''' Get users percentage per answer for given question. '''
        answers = self.get_users_no_per_answer_by_years(q_id)
        return self._change_total_to_pct_yearly(q_id, answers)      
    
    def get_users_no_per_answer_by_years(self, q_id):
        ''' Get frequency of the answers along the years for particular question number (QuestionID) in Answer table. '''
        conn = sqlite3.connect(f'{self.path}{self.db_name}.sqlite')
        c = conn.cursor()
        c.execute("""SELECT AnswerText, SurveyID, count(UserID) 
        FROM Answer WHERE QuestionID = ? 
        GROUP BY SurveyID, AnswerText""", (q_id,))
        user_no = c.fetchall()
        conn.close()
        return user_no
    
    def _change_total_to_pct_yearly(self, q_id, tab):
        ''' Change input table of answers with total occurrence to the percentage representation.
            The calculation are done year by year.
            Only table (answer, year, ..., count) is supported. '''
        table = []
        years = [year[0] for year in self.get_all_years_per_q(q_id)]
        for year in years:
            answers_no = [row[-1] for row in tab if row[1] == year] 
            for row in tab[:len(answers_no)]:
                answer, value = row[0], row[-1]
                if len(row) > 2:
                    table.append((answer, *row[1:-1], self._round_2(100*value/sum(answers_no))))
                else:
                    table.append((answer, self._round_2(100*value/sum(answers_no))))
            del tab[:len(answers_no)]
        return table
        
    @staticmethod
    def _round_2(x):
        return round(x , 2)
    
    def get_avg_for_quantitative_q(self, q_id):
        ''' Get average for given quantitative question (q_id). '''
        conn = sqlite3.connect(f'{self.path}{self.db_name}.sqlite')
        c = conn.cursor()
        c.execute(f'SELECT avg(AnswerText) FROM Answer WHERE QuestionID = ?', (q_id,))
        avg = c.fetchone()[0]
        conn.close()
        return self._round_2(avg)
    
    def get_hist_for_quantitative_q(self, q_id):
        answers = self.get_answers_for_question(q_id)
        return self._get_hist(answers)
    
    @staticmethod
    def _get_hist(answers):
        data = [int(answer[0]) for answer in answers]
        return np.histogram(data)
    
    def get_question_text(self, q_id):
        ''' Get given question text. '''
        conn = sqlite3.connect(f'{self.path}{self.db_name}.sqlite')
        c = conn.cursor()
        c.execute(f'SELECT questiontext FROM Question WHERE questionid = ?', (q_id,))
        q_text = c.fetchone()[0]
        conn.close()
        return q_text


