# Heroku deployment

You need a Procfile and a requirements.txt file to deploy to Heroku.

```
# Procfile
web: uvicorn main:app --host=0.0.0.0 --port=$PORT
```

If you you Alembic, add this:

```
release: alembic upgrade head
```

This project uses `uv` to manage depenencies so to generate the requirements.txt file for Herou, use: `uv export --no-dev --no-hashes >| requirements.txt`.

Then the usual Heroku commands:

```
$ heroku create
# provision a Postgres database
$ heroku addons:create heroku-postgresql
$ git push heroku main
$ heroku open
-> go to /docs
```

One tricky thing was `sqlalchemy.exc.NoSuchModuleError: Can't load plugin: sqlalchemy.dialects:postgres` for which I added [this workaround](https://github.com/PyBites-Open-Source/affirmations-api/commit/d7da6387d000de2ca2ae89c0a8935c727084262f).
