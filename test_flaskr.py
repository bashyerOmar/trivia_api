import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category , db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')  
        self.DB_USER = os.getenv('DB_USER', 'postgres')  
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', 'zeronyuuki23')  
        self.DB_NAME = os.getenv('DB_NAME', 'trivia_test')  
        self.DB_PATH = 'postgresql+psycopg2://{}:{}@{}/{}'.format(self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_NAME)
        setup_db(self.app, self.DB_PATH)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    ##################### questions based on category testing ####################
    
    #test for successful operation to get questions based in specified category 
    def test_get_questions_based_on_category(self):
        #get endpoint (response) 
        res = self.client().get('/categories/1/questions') #exist 
        #data of the response (loaded in JSON format)
        res_data = json.loads(res.data)
        #make sure satus code is 200 (OK)
        self.assertEqual(res.status_code, 200)
        #make sure succes is True
        self.assertEqual(res_data['success'], True)
        #make sure there is questions retrieved (len != 0)
        self.assertNotEqual(len(res_data['questions']), 0)


    #test for Not Found error (404) for get questions based on specified category 
    def test_404_err_for_get_questions_based_on_category(self):
        res = self.client().get('/categories/1000/questions') #not exist
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data['success'], False)
        #self.assertEqual(len(res_data['questions']), 0)

    ########################## category testing #############################
    def test_get_categories(self):
        res = self.client().get('/categories')
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertNotEqual(len(res_data["categories"]), 0)

    # def test_404_err_get_categories(self):
    #     res = self.client().get('/categories')
    #     res_data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(res_data["success"], False)
    #     self.assertEqual(len(res_data["categories"]) , 0)


    ###################### questions testing ################################

    def test_get_questions(self):
        res = self.client().get('/questions')
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertNotEqual(len(res_data["questions"]) , 0)



    ###################### Pagination testing ################################

    def test_Pagination(self):
        res = self.client().get('/questions?page=1')
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data['success'], True)
        self.assertNotEqual(len(res_data['questions']), 0)

    def test_404_err_for_pagination(self):
        res = self.client().get('/questions?page=1111')
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data['success'], False)
        #self.assertEqual(len(res_data['questions']), 0)


    ###################### search for questions testing ################################
    
    def test_search_for_question(self):
        res = self.client().post('/questions/search', json={'searchTerm': "what"})
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data['success'], True)
        self.assertNotEqual(len(res_data['questions']), 0)

    def test_404_err_search_for_questions(self):
        #in our qestions we have not question included "Bshayer" 
        res = self.client().post('/questions/search', json={'searchTerm':"Bshayer"}) 
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 404) 
        self.assertEqual(res_data['success'], False)
        #self.assertEqual(len(res_data['questions']), 0)
    

    ###################### insert new question testing ################################

    def test_new_question(self):
        #new question will be add to db !!
        new_question={
        'question':"What is biggest animal?!",
        'answer':"blue whale",
        'difficulty':"2",
        'category':"1"

        }
        res = self.client().post('/questions', json=new_question)
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data['success'], True)

    def test_400_err_new_question(self):
        new_question={
        'question':None,
        'answer':"blue whale",
        'difficulty':"2",
        'category':"1"
        }
        res = self.client().post('/questions', json=new_question)
        res_data = json.loads(res.data)
        '''if one of the question field be missed (question or fifficulty or category or answer)
            it should be an error show (400)
            so, i will try put question filed empty'''
        #self.question['question'] = None
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data['success'], False)
    

    ###################### delete question testing ################################
    
    def test_delete_questions(self):
        
        #the question with id=10 will be remove after testing 
        #so we should retrive its data to restore it later 
        
        # question_to_delete=db.session.query(Question).filter(Question.id == 10).all()
        # formmated_question=Question.format(question_to_delete) 
        # question = formatted_questions["question"]
        # answer = formatted_questions["answer"]
        # difficulty = formatted_questions["difficulty"]
        # category =formatted_questions["category"]
        

        res = self.client().delete('/questions/10') 
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data['success'], True)
        self.assertEqual(res_data['deleted'], 10)
        
        # #question object 
        # new_question=Question(question=question,answer=answer,difficulty=difficulty,category=category)
        # #assign question to the same id = 10
        # new_question.id=10
        # #insert to db 
        # Question.insert(new_question)
         


    def test_422_err_delete_questions(self):
        #delete question with ID=1000 (which is invalid)
        res = self.client().delete('/questions/1000')
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(res_data['success'], False)
        #self.assertEqual(res_data['deleted'], 1000)


    ###################### quiz testing ################################


    def test_get_questions_based_on_category_to_play_quiz(self):

        quiz_data={
        'quiz_category': {'type': 'Science', 'id': '1'},
        'previous_questions': []
         }

        res = self.client().post('/playquiz', json=quiz_data)
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data['success'], True)
        self.assertNotEqual((len(res_data['question'])), 0)
        #self.assertEqual(res_data['quiz_category']['id'], 1)    


    #test ensure random question not in previous questions list 
    def test_fail_play_quiz(self): 

        # request with no data (empty)
        res = self.client().post('/playquiz', json={})
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(res_data['success'], False)
        


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()