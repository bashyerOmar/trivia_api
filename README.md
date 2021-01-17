

## Trivia API

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out. 

The application's Features:

1) Display questions - both all questions and by category. Questions show all questions list, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 





#### Backend 

The `./backend` directory contains Flask and SQLAlchemy server.

## Getting Started / Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql db_name < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 



###Getting Started
Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/ or localhost:5000 , which is set as a proxy in the frontend configuration.
Authentication: This version of the application does not require authentication or API keys.

Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 404,
    "message":Resource Not Found
}
```
The API will return five error types when requests fail:

400: Bad Request
404: Resource Not Found
500: Server error
422: Not Processable
405:method not allwoed


### API Endpoints

GET '/categories'
General:
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Return success value and list of categories formmated as JSON 
Sample: ```curl http://127.0.0.1:5000/categories ```
```

{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```

GET '/questions'
General:
- return success value , list of all questions stored in database as JSON format , number of all questions , current category of each question and return all categories ``` /categories```
- show all questions paginated as 10 questions per page, start from page 1 
Sample: ```curl http://127.0.0.1:5000/questions?page=1 ```
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": {
    "answer": "Lake Victoria",
    "category": "3",
    "difficulty": 2,
    "id": 13,
    "question": "What is the largest lake in Africa?"
  },
  "questions": [
    {
      "answer": "ss",
      "category": "2",
      "difficulty": 2,
      "id": 30,
      "question": "whats the colour of bannana "
    },
    {
      "answer": "tst",
      "category": "2",
      "difficulty": 2,
      "id": 31,
      "question": "test"
    },
    {
      "answer": "final ",
      "category": "1",
      "difficulty": 1,
      "id": 32,
      "question": "final"
    },
    {
      "answer": "George Washington Carver",
      "category": "4",
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": "3",
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": "3",
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": "3",
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": "2",
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": "2",
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": "2",
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }
  ],
  "success": true,
  "total_questions": 19
}

```

DELETE '/questions/<int:question_id>'
General:
- return success value and ID of the deleted question
- delete question based on given ID
Sample:``` curl http://127.0.0.1:5000/questions/12     ```
```
{
  "success": true,
  "deleted": 12
}
```

POST '/questions' 
General:
- Return success value and values of question , category , difficulty and answer
- Fetch data from the form as JSON  
- Add new question to the database 
Sample: ```curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"what is the biggest animal?", "answer":"Blue Whale", "category":"4", "difficulty":"1"}' ```
```
{
    "success": True,
    "question": "what is the biggest animal?",
    "answer": "Blue Whale",
    "difficulty": 1,
    "category": "4"
}
```

POST '/questions/search'
General:
- insensitive and partial search for questions based on given SearchTerm 
- return success value , found questions and number of the found questions
Sample:``` curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"search_term":"peanut"}' ```
```
{
  "questions": [{
    "id": 12,
    "question": "Who invented Peanut Butter?",
    "answer": "George Washington Carver",
    "category": "4",
    "difficulty": 2
  }],
  "total_questions": 1,
  "success":true
}
```

GET '/categories/<int:category_id>/questions'
General:
- get all questions based on specific category using (category_id)
- return success value , questions of the given category, number of the questions and given category ID
Sample:``` curl http://127.0.0.1:5000/categories/1/questions```
```
{
  "current_category": 1,
  "questions": [
  
    {
      "answer": "The Liver",
      "category": "1",
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": "1",
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": "1",
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "rr",
      "category": "1",
      "difficulty": 1,
      "id": 24,
      "question": "test"
    }
  ],
  "success": true,
  "total_questions": 4
}

```

POST '/playquiz' 
General: 
- take a chosen category ID to fetch all questions of that category 
- check if the entire question was a previous question to prevent duplicate 
- the number of questions per paly depend on on number of questions of the chosen category
- questions pick randomly 
- return success value and random question  
Sample: ```curl http://127.0.0.1:5000/playquiz -X POST -H "Content-Type: application/json" -d '{"quiz_category": "1","previous_questions": [20,21]}```



## Testing
To run the tests, go to backend directory and open termianl and then run this command
```
python test_flaskr.py
```


### Frontend

The `./frontend` directory contains a complete React frontend to consume the data from the Flask server. 

##Installing Dependencies

Installing Node and NPM
This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from https://nodejs.com/en/download.


This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the frontend directory, open your terminal and run:
```
npm install // only once to install dependencies
npm start 
```
By default, the frontend will run on localhost:3000.

