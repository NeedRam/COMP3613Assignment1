import click, pytest, sys, unittest
from datetime import date
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate, create_db
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )
from App.models import ( User, Student, Staff, HourRecord, Accolade, Leaderboard )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    Rimmothy = Staff(userID="30010001", userName="Rimmothy", userEmail="rimmothy@example.com", userPassword="timmothywithanR")
    Bartoldamew = Staff(userID="30010002", userName="Bartoldamew", userEmail="bartoldamew@example.com", userPassword="PASSrelTense")
    Mandoes = Staff(userID="30010003", userName="Mandoes", userEmail="mandoes@example.com", userPassword="mandoeswhatmendez")

    Capking = Student(userID="816010001", userName="Capking", userEmail="capking@example.com", userPassword="PLZSTOPSHOUTING")
    Ladiator = Student(userID="816010002", userName="Ladiator", userEmail="ladiator@example.com", userPassword="GladLad2")
    Ohlysith = Student(userID="816010003", userName="Ohlysith", userEmail="ohlysith@example.com", userPassword="Ohlysith419")
    Kevin = Student(userID="816010004", userName="Kevin", userEmail="kevin@example.com", userPassword="kevin")
    Mark = Student(userID="816010005", userName="Mark", userEmail="mark@example.com", userPassword="ohhi")
    db.session.add_all([Rimmothy, Bartoldamew, Mandoes, Capking, Ladiator, Ohlysith, Kevin, Mark])

    rec1 = HourRecord(studentID=816010001, hours=200000.1, date=date(2023, 10, 5), status="Rejected", staffID=30010001)
    rec2 = HourRecord(studentID=816010001, hours=0.01, date=date(2023, 10, 1), status="Approved", staffID=30010001)
    rec3 = HourRecord(studentID=816010002, hours=41.5, date=date(2023, 10, 5), status="Approved", staffID=30010001)
    rec4 = HourRecord(studentID=816010003, hours=6.8, date=date(2023, 10, 3), status="Approved", staffID=30010002)
    rec5 = HourRecord(studentID=816010004, hours=33.333, date=date(2023, 10, 2), status="Approved", staffID=30010003)
    rec6 = HourRecord(studentID=816010005, hours=2.0, date=date(2023, 10, 4), status="Pending", staffID=30010001)
    db.session.add_all([rec1, rec2, rec3, rec4, rec5, rec6])

    accolade1 = Accolade(title="Newcommer", milestoneHours=10)
    accolade2 = Accolade(title="Beginner", milestoneHours=25)
    accolade3 = Accolade(title="Rookie", milestoneHours=50)
    accolade4 = Accolade(title="Novice", milestoneHours=100)
    accolade5 = Accolade(title="Him", milestoneHours=420)
    db.session.add_all([accolade1, accolade2, accolade3, accolade4, accolade5])

    db.session.commit()

    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)

