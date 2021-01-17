  import os
  from flask import Flask, request, abort, jsonify
  from flask_sqlalchemy import SQLAlchemy
  from flask_cors import CORS
  import random
  from models import setup_db, Question, Category , db

  QUESTIONS_PER_PAGE = 10




  def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)  #, resources={r"*/api/*": {origins:'*'}}


    def after_request(response):
       response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization')
       response.headers.add('Access-Control-Allow-Methods','GET,PATCH,POST,DELETE,OPTIONS')
       #response.headers.add("Access-Control-Allow-Origin", "*")
       return response
    


    @app.route('/categories') # methods=['GET'] by default 
    def get_categories():
        #fetch categories from db order by id 
        all_categories =db.session.query(Category).order_by(Category.id).all() 
        
        # check if there is data in categories or not 
        if all_categories==None:      
           abort(404)  
        else:
          return jsonify ({
            'success': True,
            'categories':Category.format(all_categories)
            })  

        
    
    @app.route('/questions') #methods=['GET']
    def get_questions():

        try:

          page = request.args.get('page', 1, type=int)
          #start = (page - 1) * QUESTIONS_PER_PAGE
          # end = start + QUESTIONS_PER_PAGE

          #fetch all questions from db 
          all_questions=db.session.query(Question).all()

          #pagination and retrieve data (items) 
          paginated_questions= Question.query.paginate(per_page=QUESTIONS_PER_PAGE, page=page).items
          
          #check if all_questions list is empty 
          if all_questions == None:
             abort(404)
          else:
             #fetch all categories 
             categories=db.session.query(Category).all()
             #format categories to JSON 
             all_categories=Category.format(categories)
             #format questions to JSON 
             formatted_questions= [Question.format(question) for question in paginated_questions]
             
             #return data 
             return jsonify ({
              'success': True,
              'questions':formatted_questions,#[start:end]
              'total_questions':len(all_questions), # all_questions.count() 
              'current_category':formatted_questions[4],
              'categories':all_categories
              })
        
        except Exception:
          abort(404)
         

         
          

    @app.route('/questions/<int:question_id>' , methods=['DELETE'])
    def remove_question(question_id):
        try:
          #fetch question which will remove
          question_to_del = db.session.query(Question).filter(question_id==Question.id).one_or_none()
          
          #check if the question exist or not
          if question_to_del == None:
             abort(404)
          else:
            #delete question from db 
             Question.delete(question_to_del)
             #question_to_del.delete()
             return jsonify({
              'success':True,
              'deleted':question_id
              })

        except Exception:
          abort(422) # unprocessable

    
    @app.route('/questions' , methods=['POST']) 
    def add_new_question():
        try:
          #fetch the data from the form as JSON format
          new_question_data = request.json
          question = new_question_data["question"]
          answer = new_question_data["answer"]
          difficulty = new_question_data["difficulty"]
          category =new_question_data["category"]
          
          #check if any filed missing (none)
          if ((question == None) or (answer == None) 
            or (difficulty == None) or (str(category) == None)):
              abort(400)

          else:
              #create new question object 
              new_question = Question(question=question,answer=answer,difficulty=difficulty,category=category)
              #insert question in db 
              Question.insert(new_question)
              #return data for frontend in JSON format 
              return jsonify ({
                  'success': True,
                  'question': question,
                  'answer': answer,
                  'difficulty': difficulty,
                  'category': category
              })

        except Exception:
          abort(400) # or 405 method not allowed
        
   

    @app.route('/questions/search' , methods=['POST'])
    def search_for_questions():

	      try:
	        question_search_of= request.json
	        search_term=question_search_of["searchTerm"]

	        #used ilike method cause its case-insensitive and enable partial search 
	        results = db.session.query(Question).filter(Question.question.ilike(f'%{search_term}%')).all()
	        if len(results) == 0 : #no results found of the search 
	            abort(404)
	        else:
	            formmated_results=[Question.format(question) for question in results]
	            print(formmated_results)
	            return jsonify({
	                  'success': True,
	                  'questions': formmated_results,
	                  'total_questions': len(results),
	                  #'currentCategory':results[4] 
	            })
	      except Exception:
	        abort(404)
    

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_based_on_category(category_id):
        
          try:
            #pagination
            page = request.args.get('page', 1, type=int)
            start= (page - 1) * QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE

            questions_based_category = db.session.query(Question).filter(Question.category == str(category_id)).all()
            if (len(questions_based_category) == 0): #(questions_based_category) == None
                abort(404)
            else:
                formatted_questions= [Question.format(question) for question in questions_based_category]
                return jsonify({
                    'success': True,
                    'questions': formatted_questions[start:end],
                    'total_questions': len(questions_based_category),
                    'current_category':category_id 
                })
          except Exception:
              abort(404)

   
    @app.route('/playquiz' , methods=['POST'])
    def play_quiz():
        
          quiz_data = request.json
          given_category = quiz_data["quiz_category"]
          prev_questions = quiz_data["previous_questions"]
          all_questions = None
          selected_questions =[]
          formmated_question=None
          question_counter=0
         
          

          if given_category["id"] == 0 : #All category selected 
            all_questions = db.session.query(Question).all()

          else: #specific category selected 
            all_questions = db.session.query(Question).filter(Question.category==given_category["id"])#str(given_category)

          
          #loop for all questions either All categories or specific one (based on prev step)
          for question in all_questions:
            '''check if the entire question in previous question list 
            if yes try another question (to prevent duplicate) 
            if not, format the question as JSON and then add it to selected_questions list '''
            if question.id in prev_questions:
                continue
            #else:
            formmated_question=Question.format(question)
            selected_questions.append(formmated_question)
          '''check if the selected questions list empty thats mean all of the question previous (used)
            so force end should be True to end the game (quiz)
            if the given category is 'All' the game only be 5 questions 
          '''
          if (len(selected_questions) == 0 ):
             return jsonify({
              'forceEnd':True
              })

          if (given_category["id"] == 0): #if given category is 'All' choose only 5 questions to play quiz
             if (question_counter < 6 ):
                random_question=random.choice(selected_questions)
                question_counter += 1
                print(question_counter)
             else:
                return jsonify({
                'forceEnd':True
                })
          #select random question 
          random_question=random.choice(selected_questions)
          #print(prev_questions)
             

          return jsonify({
                'success':True,
                'question':random_question 

              })


    #errors handling 
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
          "success": False, 
          "error": 404,
          "message": "Not found"
          }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
          "success": False, 
          "error": 422,
          "message": "unprocessable"
          }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
          "success": False, 
          "error": 400,
          "message": "Bad Request"
          }), 400

    @app.errorhandler(500)
    def internal_server_error(error):
          return jsonify ({
              'success': False,
              'error': 500,
              'message':"internal server error"
          }), 500

    @app.errorhandler(405)
    def method_not_allowed(error):
          return jsonify ({
              'success': False,
              'error': 405,
              'message':"Method Not Allowed"
          }),405
    
    return app

      