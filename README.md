
# APIs

## Prerequisites
- Python 3.6 or 3.7 (Ignore if using Docker)
- Virtualenv (Ignore if using Docker)
- Postgres 9.6 + (Ignore if using Docker)
- Docker (Optional)
- Docker Compose (Optional)

## virtualenv

```bash
# 1. Create virtual env
python3 -m venv venv
. venv/bin/activate

# 2. copy .env to hr/config/
cp .envexample hr/config/.env

# 3. Install dependency
pip install -r requirements.txt

# 4. Migrate database
# NOTE: we can use docker-compose to create a new database (OPTIONAL)
# docker-compose -f docker-compose.yml up -d db
$ cd hr
$ python ./manage.py migrate
$ python ./manage.py createsuperuser
$ python ./manage.py seed_data

# 5. Start app
$ python manage.py runserver

# GET token:
curl -X POST -H "Content-Type: application/json" -d '{"username": "hung", "password": "123321"}' http://127.0.0.1:8000/api-token-auth/
Response: {"token":"99e62f577188e45652420c8e4c0e8496c0107200"}

# Employee Search API:
curl -X GET -H "Authorization: Token 99e62f577188e45652420c8e4c0e8496c0107200" http://127.0.0.1:8000/api/v1/employee/
## Search: http://127.0.0.1:8000/api/v1/employee/?status=ACTIVE&status=TERMINATED&department_id=1&full_name=test
## You can refer in unit test: hr/employee/tests.py


$$ Use Dockerfile to run app
$ modify host of databse to host of db container in .env:
    DATABASE_URL=postgres://postgres:123321@db:5432/postgres
$ Run docker-compose
    $ docker-compose up --build

## Display Fields configuration
# I add display_feilds in Organization model. we can set it to show location, company, department, contacts
# You can refer seed_data command: hr/employee/management/commands/seed_data.py
