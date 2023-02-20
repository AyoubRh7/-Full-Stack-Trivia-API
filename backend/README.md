# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## ToDo Tasks
These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*


One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 


2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 


3. Create an endpoint to handle GET requests for all available categories. 


4. Create an endpoint to DELETE question using a question ID. 


5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 


6. Create a POST endpoint to get questions based on category. 


7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 


8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 


9. Create error handlers for all expected errors including 400, 404, 422 and 500. 



## Review Comment to the Students
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/api/v1.0/categories'
GET ...
POST ...
DELETE ...

GET '/api/v1.0/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
### API Reference

## Getting started
- Base URL : http://http://127.0.0.1:5000/ (this app hosted locally)
- Authentication : No authentication protocol used in this app

## Errors handling
    In errors cases the app returns a json object in this format :
    {
      'success':False,
      'error':404,
      'message':'Not found'
    }

    List of errors codes used in the app : 
    - 404 : Not found
    - 422 : Unprocessable entity
    - 500 : Internal server error

## Endpoints

# GET /categories

- General: Returns a list of all categories
- Sample : curl http://127.0.0.1:5000/categories
    {
  "categories": {
    "1": "sport", 
    "2": "general"
    }, 
  "success": true
}

# GET /categories

- General: Returns a list of all categories
- Sample : curl http://127.0.0.1:5000/categories
    {
  "categories": {
    "1": "sport", 
    "2": "general"
    }, 
  "success": true
}

# GET /questions

- General: Returns all questions paginated
- Sample : curlhttp://127.0.0.1:5000/questions
    {
  "I did not understand what current_categorie means\n         it's the category realted to the maximum questions in page ?\n        current_categorie": "null", 
  "categories": {
    "1": "sport", 
    "2": "general"
  }, 
  "questions": [
    {
      "answer": "developer", 
      "category": "2", 
      "difficulty": 1, 
      "id": 2, 
      "question": "Whats your job"
    },
    {
      "answer": "Virjil van dijck",
      "category": "1",
      "difficulty": 2,
      "id": 3,
      "question": "Whose the best cb in the world"
    },
    {
      "answer": "Kante",
      "category": "2",
      "difficulty": 5,
      "id": 5,
      "question": "Whose the best cdm in the world"
    }
  ],
  "success": true,
  "total_questions": 4
}

# DELETE /questions/<int:id>

- General: Deletes a question using id passed in URL
- Sample : curl http://127.0.0.1:5000/questions/6 -X DELETE
    {
  "deleted_question": 6,
  "success": true
    }   

# POST /questions

- General: Creates new question using id passed in URL
- Sample : curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d "{ \"question\": \"Whose the best cm in the world?\", \"answer\": \"Frenkie de jong\", \"difficulty\": 1, \"category\": \"6\" }"
    {
  "success": true
    }   

# POST /questions/search

- General: Returns question based on search term
- Sample : curl http://127.0.0.1:5000/questions_search -X POST -H "Content-Type: application/json" -d "{\"searchTerm\": \"a\"}"
    {
  "current_categorie": "null",    
  "questions": [
    {
      "answer": "developer",
      "category": "2",
      "difficulty": 1,
      "id": 2,
      "question": "Whats your job"
    }
  ],
  "success": true,
  "totalQuestions": 4
}

# GET /categories/<int:id_category>/questions

- General: Returns question based on category using the id passed in URL
- Sample : curl http://127.0.0.1:5000/categories/1/questions
    {
  "currentCategory": "sport",
  "questions": [
    {
      "answer": "Virjil van dijck",
      "category": "1",
      "difficulty": 2,
      "id": 3,
      "question": "Whose the best cb in the world"
    }
  ],
  "success": true,
  "totalQuestions": 1
}  

# POST /quizes

- General: Returns a new question not existing in privious questions passed in request  
- Sample : curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d "{\"previous_questions\": [1, 2], \"quiz_category\": {\"type\": \"sport\", \"id\": \"1\"}}"
    {
  "question": {
    "answer": "Virjil van dijck",
    "category": "1",
    "difficulty": 2,
    "id": 3,
    "question": "Whose the best cb in the world"
  },
  "success": true
}


## Authors
Ayoub Rhouttais developed the apis part






















curl http://127.0.0.1:5000/questions_search -X POST -H "Content-Type: application/json" -d "{\"searchTerm\": \"a\"}"

curl http://127.0.0.1:5000/categories/1/questions


curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d "{\"previous_questions\": [1, 2], \"quiz_category\": [{\"type\": \"sport\", \"id\": \"1\"}]}"

curl http://127.0.0.1:5000/quizes -X POST -H "Content-Type: application/json" -d "{\"previous_questions\": [1, 2], \"quiz_category\": {\"type\": \"sport\", \"id\": \"1\"}}"