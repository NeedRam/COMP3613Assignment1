![Tests](https://github.com/uwidcit/flaskmvc/actions/workflows/dev.yml/badge.svg)

# Flask MVC Template
A template for flask applications structured in the Model View Controller pattern [Demo](https://dcit-flaskmvc.herokuapp.com/). [Postman Collection](https://documenter.getpostman.com/view/583570/2s83zcTnEJ)


# Dependencies
* Python3/pip3
* Packages listed in requirements.txt

# Installing Dependencies
```bash
$ pip install -r requirements.txt
```

# Configuration Management


Configuration information such as the database url/port, credentials, API keys etc are to be supplied to the application. However, it is bad practice to stage production information in publicly visible repositories.
Instead, all config is provided by a config file or via [environment variables](https://linuxize.com/post/how-to-set-and-list-environment-variables-in-linux/).

## In Development

When running the project in a development environment (such as gitpod) the app is configured via default_config.py file in the App folder. By default, the config for development uses a sqlite database.

default_config.py
```python
SQLALCHEMY_DATABASE_URI = "sqlite:///temp-database.db"
SECRET_KEY = "secret key"
JWT_ACCESS_TOKEN_EXPIRES = 7
ENV = "DEVELOPMENT"
```

These values would be imported and added to the app in load_config() function in config.py

config.py
```python
# must be updated to inlude addtional secrets/ api keys & use a gitignored custom-config file instad
def load_config():
    config = {'ENV': os.environ.get('ENV', 'DEVELOPMENT')}
    delta = 7
    if config['ENV'] == "DEVELOPMENT":
        from .default_config import JWT_ACCESS_TOKEN_EXPIRES, SQLALCHEMY_DATABASE_URI, SECRET_KEY
        config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        config['SECRET_KEY'] = SECRET_KEY
        delta = JWT_ACCESS_TOKEN_EXPIRES
...
```

## In Production

When deploying your application to production/staging you must pass
in configuration information via environment tab of your render project's dashboard.

![perms](./images/fig1.png)

# Flask Commands

wsgi.py is a utility script for performing various tasks related to the project. You can use it to import and test any code in the project. 
You just need create a manager command function, for example:

```python
# inside wsgi.py

user_cli = AppGroup('user', help='User object commands')

@user_cli.cli.command("create-user")
@click.argument("username")
@click.argument("password")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

app.cli.add_command(user_cli) # add the group to the cli

```

Then execute the command invoking with flask cli with command name and the relevant parameters

```bash
$ flask user create bob bobpass
```


# Running the Project

_For development run the serve command (what you execute):_
```bash
$ flask run
```

_For production using gunicorn (what the production server executes):_
```bash
$ gunicorn wsgi:app
```

# Deploying
You can deploy your version of this app to render by clicking on the "Deploy to Render" link above.

# Initializing the Database
When connecting the project to a fresh empty database ensure the appropriate configuration is set then file then run the following command. This must also be executed once when running the app on heroku by opening the heroku console, executing bash and running the command in the dyno.

```bash
$ flask init
```

# Database Migrations
If changes to the models are made, the database must be'migrated' so that it can be synced with the new models.
Then execute following commands using manage.py. More info [here](https://flask-migrate.readthedocs.io/en/latest/)

```bash
$ flask db init
$ flask db migrate
$ flask db upgrade
$ flask db --help
```

# Testing

## Unit & Integration
Unit and Integration tests are created in the App/test. You can then create commands to run them. Look at the unit test command in wsgi.py for example

```python
@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "User"]))
```

You can then execute all user tests as follows

```bash
$ flask test user
```

You can also supply "unit" or "int" at the end of the comand to execute only unit or integration tests.

You can run all application tests with the following command

```bash
$ pytest
```

## Test Coverage

You can generate a report on your test coverage via the following command

```bash
$ coverage report
```

You can also generate a detailed html report in a directory named htmlcov with the following comand

```bash
$ coverage html
```

# Troubleshooting

## Views 404ing

If your newly created views are returning 404 ensure that they are added to the list in main.py.

```python
from App.views import (
    user_views,
    index_views
)

# New views must be imported and added to this list
views = [
    user_views,
    index_views
]
```

## Cannot Update Workflow file

If you are running into errors in gitpod when updateding your github actions file, ensure your [github permissions](https://gitpod.io/integrations) in gitpod has workflow enabled ![perms](./images/gitperms.png)

## Database Issues

If you are adding models you may need to migrate the database with the commands given in the previous database migration section. Alternateively you can delete you database file.

# User Commands

### Create a user
```bash
$ flask user create <id> <username> <email> <password>
```

### List all users
```bash
$ flask user list
```

### Search users by ID, username, email, or password
```bash
$ flask user searchALL <query>
```

### Update a user by ID (any combination of fields)
```bash
$ flask user update <id> [--username <new_username>] [--email <new_email>] [--password <new_password>]
```

### Delete a user by ID
```bash
$ flask user delete <id>
```

### Drop (clear) the users table
```bash
$ flask user dropTable
```


# Student Commands

### Create a student
```bash
$ flask student create <id> <username> <email> <password>
```

### List all students
```bash
$ flask student list
```

### Search students by ID, username, email, or password
```bash
$ flask student searchALL <query>
```

### Update a student by ID (any combination of fields)
```bash
$ flask student update <id> [--username <new_username>] [--email <new_email>] [--password <new_password>]
```

### Delete a student by ID
```bash
$ flask student delete <id>
```

### Drop (clear) the students table
```bash
$ flask student dropTable
```

### Submit hours for a student, date format: YYYY-MM-DD
```bash
$ flask student submitHours <id> <hours> <date>
```

### View all hour records for a student
```bash
$ flask student viewHours <id>
```

### View all accolades for a student
```bash
$ flask student viewAccolades <id>
```


# Staff Commands

### Create a staff member
```bash
$ flask staff create <id> <username> <email> <password>
```

### List all staff
```bash
$ flask staff list
```

### Search staff by ID, username, email, or password
```bash
$ flask staff searchALL <query>
```

### Update a staff member by ID (any combination of fields)
```bash
$ flask staff update <id> [--username <new_username>] [--email <new_email>] [--password <new_password>]
```

### Delete a staff member by ID
```bash
$ flask staff delete <id>
```

### Drop (clear) the staff table
```bash
$ flask staff dropTable
```

### Log hours for a student (by staff)
```bash
$ flask staff logHours <staff_id> <student_id> <hours> <date>
```

### Approve a student's hour record
```bash
$ flask staff approveHours <staff_id> <record_id>
```

### Reject a student's hour record
```bash
$ flask staff rejectHours <staff_id> <recordID>
```

### Manage (edit) a student's hour record
```bash
$ flask staff manageHours <staff_id> <recordID> [--hours <hours>] [--date <date>] [--status <status>]
```


# Hour Record Commands

### Create an hour record, date format: YYYY-MM-DD
```bash
$ flask hourRecord create <student_id> <hours> <date> <status> [--staff_id <staff_id>]
```

### List all hour records
```bash
$ flask hourRecord list
```

### Search hour records by student ID
```bash
$ flask hourRecord searchByStudentID <student_id>
```

### Search hour records by staff ID
```bash
$ flask hourRecord searchByStaffID <staff_id>
```

### Search hour records by date, date format: YYYY-MM-DD
```bash
$ flask hourRecord searchByDate <date> 
```

### Search hour records by status
```bash
$ flask hourRecord searchByStatus <status>
```

### Approve an hour record by ID (as staff)
```bash
$ flask hourRecord approve <id> <staff_id>
```

### Reject an hour record by ID (as staff)
```bash
$ flask hourRecord reject <id> <staff_id>
```

### Update an hour record by ID (any combination of fields)
```bash
$ flask hourRecord update <id> [--student_id <student_id>] [--hours <hours>] [--date <date>] [--status <status>] [--staff_id <staff_id>]
```

### Delete an hour record by ID
```bash
$ flask hourRecord delete <id>
```

### Drop (clear) the hour records table
```bash
$ flask hourRecord dropTable
```


# Accolade Commands

### Create an accolade
```bash
$ flask accolade create <title> <milestone_hours>
```

### List all accolades
```bash
$ flask accolade list
```

### Update an accolade by ID
```bash
$ flask accolade update <id> [--title <title>] [--milestone_hours <hours>]
```

### Delete an accolade by ID
```bash
$ flask accolade delete <id>
```

### Delete all accolades from the table.
```bash
$ flask accolade dropTable
```


# Leaderboard Commands

### List all students in leaderboard
```bash
$ flask leaderboard list
```

### Refresh leaderboard rankings
```bash
$ flask leaderboard refresh
```

### Search leaderboard by student ID or username
```bash
$ flask leaderboard searchALL <query>
```

### Delete all entries from the leaderboard table
```bash
$ flask leaderboard dropTable
```



