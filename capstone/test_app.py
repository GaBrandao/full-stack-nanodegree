import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from config import database_config as db_conf
from config import jwt

from app import create_app
from models import setup_db, Movie, Actor

# Fetch database url or local uri
database_host = f'{db_conf["user"]}:{db_conf["password"]}@{db_conf["port"]}'
database_uri = f'postgresql://{database_host}/{db_conf["name"]}'

database_path = os.environ.get("DATABASE_URL", database_uri)


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_uri = database_path
        setup_db(self.app, self.database_uri)

        # Define authorization headers
        self.assistant_header = {
            'Authorization': 'Bearer ' + jwt['casting_assistant']
        }
        self.director_header = {
            'Authorization': 'Bearer ' + jwt['casting_director']
        }
        self.producer_header = {
            'Authorization': 'Bearer ' + jwt['executive_producer']
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        movie = Movie(
            title='The Incredibles',
            release_date='2004-10-27'
        )
        movie.insert()
        self.test_movie_id = movie.id

        actor = Actor(
            name='Emilia Clarke',
            age=34,
            gender='Female'
        )
        actor.insert()
        self.test_actor_id = actor.id

    def tearDown(self):
        """Executed after reach test"""
        movie = Movie.query.get(self.test_movie_id)
        if movie:
            movie.delete()

        actor = Actor.query.get(self.test_actor_id)
        if actor:
            actor.delete()

    '''
        /movies ENDPOINT TESTS 
    '''

    def test_get_movies(self):
        res = self.client().get(
            '/movies',
            headers=self.assistant_header
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['movies'])

    def test_401_get_movies_missing_authorization_header(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_post_movies(self):
        movie = {
            'title': 'The incredibles',
            'release_date': '2004-10-27'
        }
        res = self.client().post(
            '/movies',
            headers=self.producer_header,
            json=movie
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['created'])

        Movie.query.get(data['created']).delete()

    def test_401_post_movies_missing_authorization_header(self):
        movie = {
            'title': 'The Incredibles',
            'release_date': '2004-10-27'
        }
        res = self.client().post(
            '/movies',
            json=movie
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_400_post_movies_empty_json_body(self):
        res = self.client().post(
            '/movies',
            headers=self.producer_header
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_422_post_movies_null_atribute(self):
        movie = {
            'release_date': '2004-10-27'
        }
        res = self.client().post(
            '/movies',
            headers=self.producer_header,
            json=movie
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    def test_patch_movies(self):
        movie_id = self.test_movie_id
        patch = {
            'title': 'The incredibles'
        }
        res = self.client().patch(
            f'/movies/{movie_id}',
            headers=self.director_header,
            json=patch
        )

        data = json.loads(res.data)
        patched_movie = data['movie'][0]
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(patched_movie['title'], patch['title'])

    def test_401_patch_movies_missing_authorization_header(self):
        movie_id = self.test_movie_id
        patch = {
            'title': 'The incredibles'
        }
        res = self.client().patch(
            f'/movies/{movie_id}',
            json=patch
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_400_patch_movies_empty_json_body(self):
        movie_id = self.test_movie_id
        res = self.client().patch(
            f'/movies/{movie_id}',
            headers=self.producer_header
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_404_patch_movies_that_does_not_exist(self):
        res = self.client().patch(
            '/movies/0',
            headers=self.producer_header
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_delete_movies(self):
        movie_id = self.test_movie_id
        res = self.client().delete(
            f'/movies/{movie_id}',
            headers=self.producer_header
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], movie_id)

    def test_404_delete_movies_that_does_not_exist(self):
        res = self.client().delete(
            '/movies/0',
            headers=self.producer_header
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    '''
        /actors ENDPOINT TESTS
    '''

    def test_get_actors(self):
        res = self.client().get(
            '/actors',
            headers=self.assistant_header
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['actors'])

    def test_401_get_actors_missing_authorization_header(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_post_actors(self):
        actor = {
            'name': 'Emilia Clarke',
            'age': 34,
            'gender': 'Female'
        }
        res = self.client().post(
            '/actors',
            headers=self.director_header,
            json=actor
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['created'])

        Actor.query.get(data['created']).delete()

    def test_401_post_actors_missing_authorization_header(self):
        actor = {
            'name': 'Emilia Clarke',
            'age': 34,
            'gender': 'Female'
        }
        res = self.client().post(
            '/actors',
            json=actor
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_400_post_actors_empty_json_body(self):
        res = self.client().post(
            '/actors',
            headers=self.producer_header
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_422_post_actors_null_atribute(self):
        actor = {
            'release_date': '2004-10-27'
        }
        res = self.client().post(
            '/actors',
            headers=self.producer_header,
            json=actor
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    def test_patch_actors(self):
        actor_id = self.test_actor_id
        patch = {
            'age': 30
        }
        res = self.client().patch(
            f'/actors/{actor_id}',
            headers=self.director_header,
            json=patch
        )

        data = json.loads(res.data)
        patched_actor = data['actor'][0]
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(patched_actor['age'], patch['age'])

    def test_401_patch_actors_missing_authorization_header(self):
        actor_id = self.test_actor_id
        patch = {
            'title': 'The incredibles'
        }
        res = self.client().patch(
            f'/actors/{actor_id}',
            json=patch
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_400_patch_actors_empty_json_body(self):
        actor_id = self.test_actor_id
        res = self.client().patch(
            f'/actors/{actor_id}',
            headers=self.director_header
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_404_patch_actors_that_does_not_exist(self):
        res = self.client().patch(
            '/actors/0',
            headers=self.director_header
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_delete_actors(self):
        actor_id = self.test_actor_id
        res = self.client().delete(
            f'/actors/{actor_id}',
            headers=self.producer_header
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], actor_id)

    def test_404_delete_actors_that_does_not_exist(self):
        res = self.client().delete(
            '/actors/0',
            headers=self.producer_header
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    '''
        RBAC TESTS

        every role was already tested for authenticated access
        on endpoints. 
        Now, we test them for forbidden endpoint access 
        (missing required permission)
    '''

    def test_403_post_actors_forbidden_for_assistant(self):
        actor = {
            'name': 'Emilia Clarke',
            'age': 34,
            'gender': 'Female'
        }
        res = self.client().post(
            '/actors',
            json=actor,
            headers=self.assistant_header
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_403_post_movies_forbidden_for_director(self):
        movie = {
            'title': 'The Incredibles',
            'release_date': '2004-10-27'
        }
        res = self.client().post(
            '/movies',
            json=movie,
            headers=self.assistant_header
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
