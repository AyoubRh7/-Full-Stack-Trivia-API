import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# Function handles questions pagination
def get_questions_pagination(request,all_questions):
  page = request.args.get('page',1,type=int)
  start = (page-1)*QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  questions = [question.format() for question in all_questions]
  selected_questions = questions[start:end]

  return selected_questions

''' Function return new question for quiz
 using list of questions and list of previous questions'''
def randomize_questions(questions,previous_questions):
  # getting the number of questions
  questions_len= len(questions)
  # getting random question from questions list 
  random_question=questions[random.randint(0,questions_len-1)]
  ''' keep generating random question
   until a new question(do not exists in previous question list) generated '''
  while True:
    if(random_question.id not in previous_questions):
      break
    else:
      random_question = questions[random.randint(0,questions_len-1)]
  # return the new question 
  return random_question


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app,resources={'/':{'origings':'*'}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    #setting access control
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,True')
    response.headers.add('Access-Control-Allow-Methods','GET,POST,DELETE,PATCH,OPTIONS')

    return response


  

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories_data={}
    try:
      # Bringing all categories data
      categories=Category.query.all()
      # Add  formatted categories data to dictionary to be suitable for frontend 
      for category in categories:
        categories_data[category.id]=category.type
      # return jsonified success response with categories data
      return jsonify({
        'success':True,
        'categories':categories_data
      }),200
    except:
      # return Internal Server Error if something went wrong
      abort(500)


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_question():
    allcategories={}
    # Getting all questions and categories
    questions = Question.query.all()
    categories = Category.query.all()
    # calculate number of questions 
    total_questions=len(questions)
    # Get 10 questions using get_questions_pagination method for pagination
    paginated_questions = get_questions_pagination(request,questions)
    #if the questions selected successfully :
    if(len(paginated_questions) != 0):
      #formatting categories 
      for categorie in categories:
        allcategories[categorie.id]=categorie.type
      #rertun required data as json 
      return jsonify({
        'success':True,
        'questions':paginated_questions,
        'total_questions' : total_questions,
        'categories':allcategories,
        """I did not understand what current_categorie means
         it's the category realted to the maximum questions in page ?
        """
        'current_categorie': 'null'
        
      }),200
    else:
      # return Internal Server Error if something went wrong 
      abort(500)
  

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      # Getting targeted question using id 
      question = Question.query.filter(Question.id == question_id).first()
      # try to delete the question
      question.delete()
      return jsonify({
        'success':True,
        'deleted_question':question_id,
        'message' : 'deleted successfully'
      }),200
    except:
      # in error case returning Unprocessable Entity Error
      abort(422)
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions',methods=['POST'])
  def create_question():
    try:
    # getting data from request
      question_data=request.get_json()

      lquestion = question_data.get('question','')
      lanswer = question_data.get('answer','')
      ldifficulty = question_data.get('difficulty','')
      lcategory = question_data.get('category','')

    
      # try to insert new question
      question = Question(question=lquestion,answer=lanswer,difficulty=ldifficulty,category=lcategory)
      question.insert()
      # return success and created status code 201
      return jsonify({
        'success':True,
      }),201
    except :
      # in error case returning Unprocessable Entity Error
      abort(422)
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search',methods=['POST'])
  def search_question():
    # getting search term from request
    question_data=request.get_json()
    search_term =question_data.get('searchTerm','')

    try:
      # getting questions based on the search term
      questions = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()
      # if there is at least one question based on the search term
      if(len(questions)!=0):
        #getting  total number of questions 
        total_questions = len(Question.query.all())
        # paginate the the result of questions
        paginated_questions = get_questions_pagination(request,questions)
        # return required data
        return jsonify({
          'success' : True,
          'questions' : paginated_questions,
          'totalQuestions' : total_questions,
          """I did not understand what current_categorie means
              it's the category realted to the maximum questions in page ?
          """
        'current_categorie': 'null'
        })
      else:
        #if there is no question based on the search term return not found error
        abort(404)
    except :
      #in error case returning not found error
      abort(404)



  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id_category>/questions')
  def get_category_questions(id_category):

      # getting the targeted category
      categoryy = Category.query.get(id_category)
      # getting the  targeted category questions
      if (categoryy is None):
          abort(404)
      questions = Question.query.filter(Question.category == str(categoryy.id)).all()
      # getting the total number of category questions
      total_questions = len(questions)
      # paginate the the result of questions
      try:
        paginated_questions = get_questions_pagination(request,questions)
        # return required data
        return jsonify({
          'success' : True,
          'questions' : paginated_questions,
          'totalQuestions': total_questions,
          'currentCategory' : categoryy.type
        }),200
      except :
      #in error case returning not found error
        abort(404)

      

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes',methods=['POST'])
  def play_quiz():
    try:  
      # getting data from request
      quiz_data = request.get_json()
      previous_questions = quiz_data.get('previous_questions')
      quiz_category = quiz_data.get('quiz_category')
      # checking if data not empty

      quiz_category_id = int(quiz_category['id'])
      # checking if the quiz category id is specified
      if(quiz_category_id != 0):
        #getting only question related to that specified category
        questions = Question.query.filter(Question.category ==quiz_category['id']).all()
      else:
        # getting all questions
        questions = Question.query.all()
       
      # Check if questions length = previous question length to avoid repeated question
      if (len(questions) == len(previous_questions)):
        new_question = None 
      # getting the new question using randomize_questions function (on top of the file) 
      new_question = randomize_questions(questions,previous_questions)
      #return required data with success statut code
      return jsonify({
        'success' : True,
        'question' : new_question.format()
      }),200
    except : 
      abort(404)
  



  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  # Not found error handler 404
  app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success':False,
      'error':404,
      'message':'Not found'
    }),404

  # Unprocessable entity error handler 422
  app.errorhandler(422)
  def unprocessable_entity(error):
    return jsonify({
      'success':False,
      'error':422,
      'message':'Unprocessable entity'
    }),422

  # Unprocessable entity error handler 422
  app.errorhandler(500)
  def not_found(error):
    return jsonify({
      'success':False,
      'error':500,
      'message':'Internal server error'
    }),500
  
  return app

    