# Coffee Shop Backend


## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Testing

To run the tests, follow these steps:
1. Register 2 users - assign the Barista role to one and Manager role to the other.
2. Sign into each account and make note of the JWT.
3. Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
4. Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
5. Run the collection and check the results.
