# Capstone Project: Casting Agency 

## Introduction and Motivation

This project is a web application that stores a database of movies and actors. It allows the Casting Agency workers to *create*, *read*, *update* and *delete* information in the database.

It completes the Full-Stack Web Developer nanodegree. Therefore, this project objective is to apply the main concepts of the course curriculum in the development of a application.

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 

## Getting Started

### Pre-requisites

This project requires [Python3](https://www.python.org/downloads/), [pip](https://pip.pypa.io/en/stable/installing/) and [postgresql](https://www.postgresql.org/download/) to run.

## Local Development

First, install [Python](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python), [pip](https://pip.pypa.io/en/stable/installing/) and [postgresql](https://www.postgresql.org/download/) if you haven't already.

Make sure you are in ` backend` directory, if not:
```
$ cd PROJECT_DIRECTORY_PATH/
```

To start and run the local development server:

1. Initialize and activate a [venv](https://docs.python.org/3.6/library/venv.html#module-venv):
```bash
$ python3 -m venv venv
$ . venv/bin/activate
```

2. Install the dependencies:
```
$ pip install -r requirements.txt
```

3. Create the database:
```bash
createdb <DATABASE_NAME>
```
And setup database config in `config.py`. 
```python
	...
	database_config = {
        "name": "casting",
        "user": "gbrandao",
        "password": None,
        "port": "localhost:5432"
    }
	...
```
Change the `name`, `user`, `password` and `port` to your correspondent database name, your user, password and configured access port.

4. Apply migrations to database:
```bash
python3 manage.py db upgrade
```

5. Setup auth0 config in `config.py`, if you want. 
```python
	...
	auth0_config = {
        "domain": "fsnd-capstone-2020.us.auth0.com",
        "algorithm": ["RS256"],
        "audience": "casting"
    }
	...
```
This step is optional, you can test the API endpoints using the tokens available in `config.py`.


6. Run the development server:
```bash
$ python app.py
```

Now you are ready to go.

### Testing

Be sure you setup the `database_config` in `config.py` correctly. Tests will be executed in the same database configured in that file.

To execute the tests, run:
```bash
python3 test_app.py
```

## API Reference

#### Base URL

The project is hosted on `http://casting-agency-fsnd-2020.herokuapp.com`. 

When running localy it is hosted at `http://127.0.0.1:8080/`.

#### RBAC : Roles and Permissions

The API endpoints have permission requirements that are distributed by the auth0 application into the following roles:

* Casting Assistant: can view actors and movies
    * Permissions: `get:movies` and `get:actors`
* Casting Director: have the same permissions of a Casting Assistant and can also create and delete actors from the database and update actors and movies.
    * Permissions: `get:movies`, `get:actors`, `post:actors`, `delete:actors`, `patch:actors` and `patch:movies`
* Executive Producer: have the same permissions of a Casting Director and can also create and delete movies.
    * Permissions: `get:movies`, `get:actors`, `post:actors`, `post:movies`, `delete:actors`, `delete:movies`, `patch:actors`, `patch:movies`

#### Error handling

Error responses are returned as JSON objects as follows:

```js
{	
	"success": false,
	"error": 404,
	"message": "resource not found"
}
```
Status codes and messages summary:
| code | message |
| ------- | ------------- |
| `400`  | bad request  |
| `404` | resource not found  |
| `405` | method not allowed  |
| `422` | unprocessable |
| `500` | internal server error |

### Endpoints

Summary:

* Movies
	* [GET /movies](#get-movies)
	* [POST /movies](#post-movies)
    * [PATCH /movies/{id}](#patch-movies)
	* [DELETE /movies/{id}](#delete-movies)

* Actors
	* [GET /actors](#get-actors)
	* [POST /actors](#post-actors)
    * [PATCH /actors/{id}](#patch-actors)
	* [DELETE /actors/{id}](#delete-actors)

Notice that it is required to pass an Authorization header containing a valid Bearer Token in the samples `curl` requests. You can find jwts for all roles in the file `config.py` and make then bearer tokens by adding "Bearer " as prefix to those strings.

<a name="get-movies"/>

#### GET /movies

Fetch all movies.

```html
GET http://casting-agency-fsnd-2020.herokuapp.com/movies
```

* Returns json object containing a list of movies and success value.
* Requires `get:movies` permission.

Sample response:

`curl http://casting-agency-fsnd-2020.herokuapp.com/movies`:

```js
{
  "movies": [
    {
      "id": 55, 
      "release_date": "Mon, 02 Oct 2000 00:00:00 GMT", 
      "title": "Cars"
    }
  ], 
  "success": true
}

```
<a name="post-movies"/>

#### POST /movies

Creates a new movie with the given title and release date.

```html
POST http://casting-agency-fsnd-2020.herokuapp.com/movies
```

* Returns json object containing the id of created question and success value.
* Requires `post:movies` permission.

Sample response:

`curl -X POST 'http://casting-agency-fsnd-2020.herokuapp.com/movies' -H "Authorization: <Bearer Token>" -H "Content-Type: application/json" -d '{"title" : "Cars", "release_date":"2000-10-02"}'`

```js
{
  "movies": [
    {
      "id": 55, 
      "release_date": "Mon, 02 Oct 2000 00:00:00 GMT", 
      "title": "Cars"
    }
  ], 
  "success": true
}

```

<a name="patch-movies"/>

#### PATCH /movies/{id}

Update the movie with the given id.

```html
POST http://casting-agency-fsnd-2020.herokuapp.com/movies/<id>
```

* Returns json object containing the modified movie object and success value.
* Requires `patch:movies` permission.

Sample response:

`curl -X PATCH 'http://casting-agency-fsnd-2020.herokuapp.com/movies/55' -H "Authorization: <Bearer Token>" -H "Content-Type: application/json" -d '{"release_date":"2001-10-02"}'`

```js
{
  "movie": [
    {
      "id": 55, 
      "release_date": "Tue, 02 Oct 2001 00:00:00 GMT", 
      "title": "Cars"
    }
  ], 
  "success": true
}

```


<a name="delete-movies"/>

#### DELETE /movies/{id}

Deletes the movie of given id.

```html
DELETE http://127.0.0.1:5000/questions/<id>
```

* Deletes the movie if exists. Returning json object containing the id of deleted movie and success value.
* Requires `delete:movies` permission.

Sample response:

`curl -X DELETE 'http://casting-agency-fsnd-2020.herokuapp.com/movies/55' -H "Authorization: <Bearer Token>"`

```js
{
  "deleted": 55, 
  "success": true
}
```

<a name="get-actors"/>

#### GET /actors

Fetch all actors.

```html
GET http://casting-agency-fsnd-2020.herokuapp.com/actors
```

* Returns json object containing a list of actors and success value.
* Requires `get:actors` permission.

Sample response:

`curl http://casting-agency-fsnd-2020.herokuapp.com/actors`:

```js
{
  "actors": [
    {
      "id": 55, 
      "release_date": "Mon, 02 Oct 2000 00:00:00 GMT", 
      "title": "Cars"
    }
  ], 
  "success": true
}

```
<a name="post-actors"/>

#### POST /actors

Creates a new actor with the given name, age and gender.

```html
POST http://casting-agency-fsnd-2020.herokuapp.com/actors
```

* Returns json object containing the id of created question and success value.
* Requires `post:actors` permission.

Sample response:

`curl -X POST 'http://casting-agency-fsnd-2020.herokuapp.com/actors' -H "Authorization: <Bearer Token>" -H "Content-Type: application/json" -d '{"name":"Emilia Clarke", "age":34, "gender":"Female"}'`

```js
{
  "actors": [
    {
      "age": 34, 
      "gender": "Female", 
      "id": 55, 
      "name": "Emilia Clarke"
    }
  ], 
  "success": true
}

```

<a name="patch-actors"/>

#### PATCH /actors/{id}

Update the actor with the given id.

```html
POST http://casting-agency-fsnd-2020.herokuapp.com/actors/<id>
```

* Returns json object containing the modified actor object and success value.
* Requires `patch:actors` permission.

Sample response:

`curl -X PATCH 'http://casting-agency-fsnd-2020.herokuapp.com/actors/55' -H "Authorization: <Bearer Token>" -H "Content-Type: application/json" -d '{"age":31}'`

```js
{
  "actor": [
    {
      "age": 31, 
      "gender": "Female", 
      "id": 55, 
      "name": "Emilia Clarke"
    }
  ], 
  "success": true
}

```


<a name="delete-actors"/>

#### DELETE /actors/{id}

Deletes the actor of given id.

```html
DELETE http://127.0.0.1:5000/questions/<id>
```

* Deletes the actor if exists. Returning json object containing the id of deleted actor and success value.
* Requires `delete:actors` permission.

Sample response:

`curl -X DELETE 'http://casting-agency-fsnd-2020.herokuapp.com/actors/55' -H "Authorization: <Bearer Token>"`

```js
{
  "deleted": 55, 
  "success": true
}
```

