## Local Development

First, install [Python](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python), [pip](https://pip.pypa.io/en/stable/installing/) and [postgresql](https://www.postgresql.org/download/) if you haven't already.

Make sure you are in ` backend` directory, if not:
```
$ cd PROJECT_DIRECTORY_PATH/backend
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

3. Setup database config in  `models.py` and `test_flaskr.py`.
```python
	...
	database_name = "<DATABASE_NAME>"
	database_host = "<DATABASE_HOST_AND_PORT>"
	...
```

4. If desired, restore a database using the trivia.psql file provided.
```bash
$ dropdb DATABASE_NAME && createdb DATABASE_NAME  
$ psql DATABASE_NAME < trivia.psql
```

5. Run the development server:
```bash
$ export FLASK_APP=flaskr FLASK_ENV=development
$ flask run
```

Now you are ready to go. If frontend server is not running yet, go to `frontend` directory and follow the instructions.

### Testing

Be sure you setup the TEST_DATABASE_NAME in `test_flaskr.py` correctly. To run the tests:
```bash
dropdb TEST_DATABASE_NAME && createdb TEST_DATABASE_NAME
psql TEST_DATABASE_NAME < trivia.psql
python3 test_flaskr.py
```

## API Reference

#### Base URL

Since this project only runs locally, it is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.

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
| `422` | unprocessable |
| `500` | internal server error |

### Endpoints

Summary:

* Questions
	* [GET /questions](#get/questions)
	* [POST /questions](#post/questions)
	* [DELETE /questions/<id>](#delet/questions)

* Categories
	* [GET /categories](#get/categories)
	* [GET /categories/<id>/questions](#get/categories/questions)

* Quizzes
	* [POST /quizzes](#post/quizzes)


<a name="get/questions"/>

#### GET /questions

Get paginated questions.

```html
GET http://127.0.0.1:5000/questions?page=<page>
```

* Returns json object containing a list of questions, number of total questions, current category, categories available and success value.

* Questions are paginated in groups of 10. Argument **page** is optional, default value is set to 1.

Sample request:

`curl http://127.0.0.1:5000/questions?page=1`:

```js
{
  "categories": {
    "1": "science", 
    "2": "art", 
    "3": "geography", 
    "4": "history", 
    "5": "entertainment", 
    "6": "sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
	...
  ], 
  "success": true, 
  "total_questions": 19
}

```
<a name="post/questions"/>

#### POST /questions

Creates a new question with the given question, answer, difficulty and category.

```html
POST http://127.0.0.1:5000/questions
```

* Returns json object containing the id of created question and success value.

Sample request:

`curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"question":"Who invented the airplane?", "answer":"Santos Dumont", "difficulty":3, "category":"4"}'`

```js
{
	"created": 24,
	"success": true
}
```

If argument `searchTerm` is provided returns questions for whom the search term is a substring of the question instead.

* Returns json object containing a list of all matching questions and success value.

Sample request:

`curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"searchTerm":"soccer"}'`

```js
{
  "questions": [
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ], 
  "success": true
}
```
<a name="delete/questions"/>

#### DELETE /questions/<id>

Deletes the question of given id.

```html
DELETE http://127.0.0.1:5000/questions/<id>
```

* Deletes the question if exists. Returning json object containing the id of deleted question and success value.

Sample request:

`curl -X DELETE http://127.0.0.1:5000/questions/23`

```js
{
	"deleted": 23,
	"success": true
}
```

<a name="get/categories"/>

#### GET /categories

Get all categories available.

```html
GET http://127.0.0.1:5000/categories
```

* Returns a json object containing categories available (object with `{id, type}` key-value pairs) and success value.

Sample request:

`curl http://127.0.0.1:5000/categories`

```js
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

<a name="get/categories/questions"/>

#### GET /categories/<id>/questions

Get all questions from given category.

```html
GET http://127.0.0.1:5000/categories/<id>/questions
```

* Returns a json object containing a list of questions, current category and success value.

Sample request:

`curl http://127.0.0.1:5000/categories/1/questions`

```js
{
  "current_category": 1, 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "success": true
}
```
<a name="post/quizzes"/>

#### POST /quizzes

Get questions to play the quiz.

```html
POST http://127.0.0.1:5000/quizzes
```

* Recieve arguments category and previous questions, a list of question ids.

* Returns a random questions within the given category, if provided, and that is not one of the previous questions.

Sample request:

`curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"quiz_category":{"id":"4", "type":"History"}}'`

```js
{
  "question": {
    "answer": "Muhammad Ali", 
    "category": 4, 
    "difficulty": 1, 
    "id": 9, 
    "question": "What boxer's original name is Cassius Clay?"
  }, 
  "success": true
}
```