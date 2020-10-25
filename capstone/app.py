import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import Movie, Actor, setup_db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # API Endpoints
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        """
            GET /movies

            returns status code 200 and json 
                {"success": True, "movies": movies} 
                where movies is the list of movies
                OR appropriate status code indicating reason for failure
        """
        movies = Movie.query.order_by(Movie.id).all()

        if len(movies) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies]
        })

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movies(payload):
        """
            POST /movies

            returns status code 200 and json {"success": True, "created": id}
                    where id is the id of the created movie
                    OR appropriate status code indicating reason for failure
        """
        data = request.get_json()

        if not data:
            abort(400)

        title = data.get('title', None)
        release_date = data.get('release_date', None)

        if None in [title, release_date]:
            abort(422)

        try:
            new_movie = Movie(
                title=title,
                release_date=release_date
            )
            new_movie.insert()

        except:
            Movie.rollback()
            abort(422)

        return jsonify({
            'success': True,
            'created': new_movie.id
        })

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def patch_movies(payload, id):
        """
            PATCH /movies

            returns status code 200 and json {"success": True, "movie": movie}
                where movie is the movie modified attributes
                OR appropriate status code indicating reason for failure
        """
        movie = Movie.query.get_or_404(id)

        data = request.get_json()

        if not data:
            abort(400)

        title = data.get('title', None)
        release_date = data.get('release_date', None)

        try:
            if title:
                movie.title = title
            if release_date:
                movie.release_date = release_date
            movie.update()

        except:
            Movie.rollback()
            abort(422)

        return jsonify({
            'success': True,
            'movie': [movie.format()]
        })

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, id):
        """
            DELETE /movies

            returns status code 200 and json {"success": True, "deleted": id}
                where id is the id of deleted movie
                OR appropriate status code indicating reason for failure
        """

        movie = Movie.query.get_or_404(id)

        try:
            movie.delete()

        except:
            Movie.rollback()
            abort(422)

        return jsonify({
            'success': True,
            'deleted': movie.id
        })

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        """
            GET /actors

            returns status code 200 and json 
                {"success": True, "actors": actors} 
                where actors is the list of actors
                OR appropriate status code indicating reason for failure
        """
        actors = Actor.query.order_by(Actor.id).all()

        if len(actors) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors]
        })

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actors(payload):
        """
            POST /actors

            returns status code 200 and json {"success": True, "created": id}
                    where id is the id of the created actor
                    OR appropriate status code indicating reason for failure
        """
        data = request.get_json()

        if not data:
            abort(400)

        name = data.get('name', None)
        age = data.get('age', None)
        gender = data.get('gender', None)

        if None in [name, age, gender]:
            abort(422)

        try:
            new_actor = Actor(
                name=name,
                age=age,
                gender=gender
            )
            new_actor.insert()

        except:
            Actor.rollback()
            abort(422)

        return jsonify({
            'success': True,
            'created': new_actor.id
        })

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def patch_actors(payload, id):
        """
            PATCH /actors

            returns status code 200 and json {"success": True, "actor": actor}
                where actor is the actor modified attributes
                OR appropriate status code indicating reason for failure
        """
        actor = Actor.query.get_or_404(id)

        data = request.get_json()

        if not data:
            abort(400)

        name = data.get('name', None)
        age = data.get('age', None)
        gender = data.get('gender', None)

        try:
            if name:
                actor.name = name
            if age:
                actor.age = age
            if gender:
                actor.gender = gender
            actor.update()

        except:
            Actor.rollback()
            abort(422)

        return jsonify({
            'success': True,
            'actor': [actor.format()]
        })

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, id):
        """
            DELETE /actors

            returns status code 200 and json {"success": True, "deleted": id}
                where id is the id of deleted actor
                OR appropriate status code indicating reason for failure
        """
        actor = Actor.query.get_or_404(id)

        try:
            actor.delete()

        except:
            Actor.rollback()
            abort(422)

        return jsonify({
            'success': True,
            'deleted': actor.id
        })

    # Error Handling

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

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(AuthError)
    def authentication_error(error):
        if 'description' in error.error:
            message = error.error['description']
        else:
            message = 'authentication error'
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': message
        }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
