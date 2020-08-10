import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random
import sys

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def format_objects(objects):
    return [obj.format() for obj in objects]


def paginate_questions(request, questions):
    page = request.args.get('page', 1, type=int)

    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    current_questions = questions[start:end]

    return format_objects(current_questions)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    '''
    @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    setup_db(app)

    '''
    @DONE: Use the after_request decorator to set Access-Control-Allow
    '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    '''
    @DONE: 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''

    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()

        if len(categories) == 0:
            abort(404)

        categories = {
            category.id: category.type
            for category in categories
        }

        return jsonify({
            'success': True,
            'categories': categories
        })

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
    def get_questions():
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, questions)

        if len(current_questions) == 0:
            abort(404)

        categories = Category.query.order_by(Category.id).all()
        categories = {
            category.id: category.type.lower()
            for category in categories
        }

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions),
            'categories': categories,
            'current_category': True
        })

    '''
    @DONE: 
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        question = Question.query.get_or_404(id)

        try:
            question.delete()

            return jsonify({
                'success': True,
                'deleted': id
            })
        except:
            Question.rollback()
            abort(422)

    '''
    @DONE: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''

    '''
    @DONE: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    @app.route('/questions', methods=['POST'])
    def create_question():
        data = request.get_json()

        question = data.get('question', None)
        answer = data.get('answer', None)
        difficulty = data.get('difficulty', None)
        category = data.get('category', None)
        search = data.get('searchTerm', None)

        try:
            if search:
                questions = Question.query.order_by(Question.id)\
                    .filter(Question.question.ilike(f'%{search}%')).all()

                if len(questions) == 0:
                    abort(404)

                return jsonify({
                    'success': True,
                    'questions': format_objects(questions),
                })
            else:
                new_question = Question(
                    question=question,
                    answer=answer,
                    difficulty=difficulty,
                    category=category
                )
                new_question.insert()

                return jsonify({
                    'success': True,
                    'created': new_question.id,
                })
        except:
            Question.rollback()
            abort(422)

    '''
    @DONE: 
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    @app.route('/categories/<int:id>/questions')
    def get_questions_by_category(id):
        questions = Question.query.filter(Question.category == id)\
            .order_by(Question.id).all()

        if len(questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': format_objects(questions),
            'current_category': id,
        })

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

    @app.route('/quizzes', methods=['POST'])
    def get_quiz_questions():
        data = request.get_json()

        previous_questions = data.get('previous_questions', None)
        quiz_category = data.get('quiz_category', None)

        query = Question.query
        if quiz_category['id']:
            query = query.filter(
                Question.category == str(quiz_category['id'])
            )

        if previous_questions:
            query = query.filter(
                Question.id.notin_(previous_questions)
            )

        questions = query.all()
        choice = random.choice(questions).format() if questions else None

        return jsonify({
            'success': True,
            'question': choice
        })

    '''
    @DONE: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
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
            "message": "bad request"
        }), 400
    return app
