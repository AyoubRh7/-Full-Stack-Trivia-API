import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres','pleaseforgiveme','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        # question test data
        self.new_question = {
            'question' : "who's the best football player of all time",
            'answer' : "Lionel Messi",
            'difficulty' : 2,
            'category' : 1
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # getting all categories test
    def test_get_categories(self):
        # making request and getting response
        res = self.client().get('/categories')
        data = json.loads(res.data)
        
        # verify that response data match succussful getting all categories response data
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['categories'])

    # getting all questions test
    def test_get_questions(self):
        # making request and getting response
        res = self.client().get('/questions')
        data = json.loads(res.data)
        # verify that response data match succussful getting all questions response data
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['questions'])
    # test delete question
    def test_delete_question(self):
        # create qeustion for test
        test_question = Question(
            question = self.new_question['question'] ,answer=self.new_question['answer'] ,
             category=self.new_question['category'] , difficulty=self.new_question['difficulty'] )
        test_question.insert()
        # getting inserted question id 
        test_question_id = test_question.id
        # verify if the question has been added successfully to datbase
        question = Question.query.filter_by(id=test_question_id).one_or_none()
        self.assertNotEqual(question,None)
        

        # making request and getting response
        res = self.client().delete(f'/questions/{question.id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['deleted_question'],test_question_id)
        self.assertEqual(data['message'],'deleted successfully')
    # test delete inexisting question
    def test_failed_delete_question(self):
        res = self.client().delete('/questions/564913289')

        # verify that response data match failed question delete response data
        self.assertEqual(res.status_code,422)
    # test create question
    def test_create_question(self):
        # making request and getting response
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        
        # verify that response data match succussful question creating response data
        self.assertEqual(res.status_code,201)
        self.assertEqual(data['success'],True)


    # test create quetion with lack of data
    def test_failed_question_create(self):

        # create question for test with lack of data
        test_question = self.new_question
        test_question['answer'] = ''
        test_question['difficulty']=''

        res=self.client().post('/questions',json = test_question)

        # verify that response data match question creating failed response data
        self.assertEqual(res.status_code,422)


    # test successfull search for quetion
    def test_search_question(self):
           # create serchTerm dict
        search = {
            'searchTerm': 'a'
        }

        # making request and getting response
        res=self.client().post('/questions/search',json=search)
        data = json.loads(res.data)

        # verify that response data match successful question search response data
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])

    # test unsuccessful search for quetion
    def test_failed_search_question(self):
        # create serchTerm dict
        search = {
            # this string do not match any questions data
            'searchTerm': '7sfregg767hgfdh'
        }

        # making request and getting response
        res=self.client().post('/questions/search',json=search)

        # verify that response data match a failing question search response data
        self.assertEqual(res.status_code,404)

    # test getting questions based on categorie successfully
    def test_get_category_questions(self):
        # making request and getting response
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        # verify that response data match getting question based on category successfully response data
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])

    # test getting questions of an inexisting category
    def test_failed_get_category_questions(self):
        res = self.client().get('/categories/114141414/questions')

        # verify that response data match getting question based on category failed response data
        self.assertEqual(res.status_code,404)

    # test generating new question for quiz successfully
    def test_play_quiz(self):
        # create a quiz data for test
        quiz_data_test = {
            'previous_questions' : [1,2,3],
            'quiz_category' : {
                "type":"sport",
                "id":"1"
                }
        }
        
        # making request and getting response
        res = self.client().post('quizzes', json=quiz_data_test)
        data = json.loads(res.data)

        # verify that response data match generating new question successfully response data
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['question'])

    # test passing empty quiz data to play_quiz function
    def test_failed_play_quiz(self):
        # create empty quiz data for test
        quiz_data_test = {
            'previous_questions' :'',
            'quiz_category' :''
        }
        
        # making request and getting response
        res = self.client().post('quizzes', json=quiz_data_test)


        # verify that response data match failing to generate new question response data
        self.assertEqual(res.status_code,404)











# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()