import click, pytest, sys, unittest
from datetime import date
from flask.cli import with_appcontext, AppGroup
from rich.console import Console
from rich.table import Table

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
    Rimmothy = Staff(id="30010001", username="Rimmothy", email="rimmothy@example.com", password="timmothywithanR")
    Bartoldamew = Staff(id="30010002", username="Bartoldamew", email="bartoldamew@example.com", password="PASSrelTense")
    Mandoes = Staff(id="30010003", username="Mandoes", email="mandoes@example.com", password="mandoeswhatmendez")

    Capking = Student(id="816010001", username="Capking", email="capking@example.com", password="PLZSTOPSHOUTING")
    Ladiator = Student(id="816010002", username="Ladiator", email="ladiator@example.com", password="GladLad2")
    Ohlysith = Student(id="816010003", username="Ohlysith", email="ohlysith@example.com", password="Ohlysith419")
    Kevin = Student(id="816010004", username="Kevin", email="kevin@example.com", password="kevin")
    Mark = Student(id="816010005", username="Mark", email="mark@example.com", password="ohhi")
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
@click.argument("id", default=123456789)
@click.argument("username", default="rob")
@click.argument("email", default="rob@example.com")
@click.argument("password", default="robpass")
def create_user_command(id, username, email, password):
    create_user(id, username, email, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        users = get_all_users_json()  # Should return a list of dicts
        table = Table(title="User List")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Username", style="magenta")
        table.add_column("Email", style="green")
        table.add_column("Password", style="red")
        for user in users:
            table.add_row(str(user['id']), user['username'], user['email'], user['password'])
        console = Console()
        console.print(table)
    else:
        print(get_all_users_json())


@user_cli.command("searchALL", help="Searches ID, username, email or password for a match")
@click.argument("query")
def search_all_users(query):
    users = get_all_users_json()
    results = []
    for user in users:
        if (
            query.lower() in str(user['id']).lower()
            or query.lower() in user['username'].lower()
            or query.lower() in user['email'].lower()
            or query.lower() in user['password'].lower()
        ):
            results.append(user)
    table = Table(title=f"User Search Results for '{query}'")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Username", style="magenta")
    table.add_column("Email", style="green")
    table.add_column("Password", style="red")
    for user in results:
        table.add_row(str(user['id']), user['username'], user['email'], user['password'])
    console = Console()
    if results:
        console.print(table)
    else:
        console.print(f"[bold red]No users found matching '{query}'.[/bold red]")


@user_cli.command("update", help="Updates user info using ID")
@click.argument("id")
@click.option("--username", default=None, help="New username")
@click.option("--email", default=None, help="New email")
@click.option("--password", default=None, help="New password")
def update_user_command(id, username, email, password):
    user = User.query.get(id)
    if not user:
        print(f"User with id {id} not found.")
        return
    updated = False
    if username:
        user.username = username
        updated = True
    if email:
        user.email = email
        updated = True
    if password:
        user.set_password(password)
        updated = True
    if updated:
        db.session.commit()
        print(f"User {id} updated.")
    else:
        print("No changes provided.")

@user_cli.command("delete", help="Deletes a user by ID")
@click.argument("id")
def delete_user_command(id):
    user = User.query.get(id)
    if not user:
        print(f"User with id {id} not found.")
        return
    db.session.delete(user)
    db.session.commit()
    print(f"User {id} deleted.")

@user_cli.command("dropTable", help="Clears the users table")
def drop_user_table_command():
    num_deleted = User.query.delete()
    db.session.commit()
    print(f"Deleted {num_deleted} users from the users table.")


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

