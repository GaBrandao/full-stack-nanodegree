import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random
import sys

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def format_objects(objects):
    '''
    Return a list of formatted objects

    arguments:
    objects -- list of objects
    '''
    return [obj.format() for obj in objects]


def paginate_questions(request, questions):
    '''
    Paginate questions into lists of 10 items

    arguments:
    request -- flask request object
    questions -- list of all questions
    '''
    page = request.args.get('page', 1, type=int)

    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    current_questions = questions[start:end]

    return format_objects(current_questions)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    '''
    @DONE: Set up CORS. Allow '*' for origins.
    '''

    CORS(app)
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
    @DONE: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint return a list of questions, 
    number of total questions, current category, categories.
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
            'current_category': categories
        })

    '''
    @DONE: 
    Create an endpoint to DELETE question using a question ID.
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

    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
    '''

    @app.route('/questions', methods=['POST'])
    def create_or_search_question():
        data = request.get_json()

        if not data:
            abort(400)

        question = data.get('question', None)
        answer = data.get('answer', None)
        difficulty = data.get('difficulty', None)
        category = data.get('category', None)
        search = data.get('searchTerm', None)

        if search:
            questions = Question.query.order_by(Question.id)\
                .filter(Question.question.ilike(f'%{search}%')).all()

            if len(questions) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'questions': format_objects(questions),
            })

        try:
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
    '''

    @app.route('/quizzes', methods=['POST'])
    def get_quiz_questions():
        data = request.get_json()

        previous_questions = data.get('previous_questions', None)
        quiz_category = data.get('quiz_category', None)

        query = Question.query
        if quiz_category and quiz_category.get('id'):
            category = Category.query.get_or_404(quiz_category['id'])
            query = query.filter(
                Question.category == str(category.id)
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

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app
