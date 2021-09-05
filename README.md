# Affirmations API

This API is to keep track of affirmations.

To get a virtual environment running and install the dependencies:

```
make setup
```

You might have to manually enable your virtual environment after this:

```
source venv/bin/activate
```

Next set your `DATABASE_URL` environment variable:

```
cp .env-template .env
# update DATABASE_URL in .env
```

To run the flake8 / mypy / tests:

```
make lint
make typing
make test
```

Or run them all in one:

```
make ci
```

To run `black` upon commit (recommended) install `pre-commit`:

```
make precommit
```

To run the `uvicorn` webserver:

```
make run
```

Then navigate to [http://localhost:8000/docs](http://localhost:8000/docs) - enjoy!
