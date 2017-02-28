# Test 项目 -- 大米

## Setup
With Python3 installed
virtualenv or venv module in Python3 is recommended.
In the root directory of project:
```
$ python3 -m venv venv
$ source venv/bin/activate
(venv)$ pip install -r requirements.txt
```

## Environment Variable

### `FLASK_CONFIG`
Configuration name for Rice app.
```
- development
- testing
- production
- default (alias for development)
```

### `DATABASE_URL`
Database connection URL.

### `DEV_DATABASE_URL`
Development database connection URL.

### `TEST_DATABASE_URL`
Test database connection URL.

## `manage.py` command

```
# Running development server on http://localhost:5000/
$ python manage.py runserver

# Enter python shell with preload global variables (see in manage.py)
$ python manage.py shell

# Apply migration to databases
$ python manage.py db upgrade

# Run unittest in tests directory
$ python manage.py test

# Create a test admin account
$ python manage.py create_admin username password phone_number

# For help
$ python manage.py --help
```

## Development

For frontend web development consuming backend API, put static file in `rice/static` directory.
After `python manage.py runserver`, go to http://localhost:5000 can see the web page.
