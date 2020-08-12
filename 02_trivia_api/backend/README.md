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

To run the tests:
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

