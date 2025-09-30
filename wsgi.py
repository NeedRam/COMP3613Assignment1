import click, pytest, sys, unittest
from datetime import date
from flask.cli import with_appcontext, AppGroup
from rich.console import Console
from rich.table import Table
from datetime import datetime

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
user_cli = AppGroup('user', help='User object commands') 

@user_cli.command("create", help="Creates a user")
@click.argument("id")
@click.argument("username")
@click.argument("email")
@click.argument("password")
def create_user_command(id, username, email, password):
    user = User(id=id, username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    print(f'{username} created!')

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        users = get_all_users_json() 
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
@click.option("--username")
@click.option("--email")
@click.option("--password")
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
Student Commands
'''
student_cli = AppGroup('student', help='Student object commands') 

@student_cli.command("create", help="Creates a user")
@click.argument("id")
@click.argument("username")
@click.argument("email")
@click.argument("password")
def create_student_command(id, username, email, password):
    student = Student(id=id, username=username, email=email, password=password)
    db.session.add(student)
    db.session.commit()
    print(f'{username} created!')

@student_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_student_command(format):
    if format == 'string':
        students = db.session.scalars(db.select(Student)).all()
        table = Table(title="Student List")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Username", style="magenta")
        table.add_column("Email", style="green")
        table.add_column("Password", style="red")
        table.add_column("Total Hours", style="yellow")
        for student in students:
            table.add_row(str(student.id), student.username, student.email, student.password, str(student.totalHours))
        console = Console()
        console.print(table)

@student_cli.command("searchALL", help="Searches ID, username, email or password for a match")
@click.argument("query")
def search_all_students(query):
    students = db.session.scalars(db.select(Student)).all()
    results = []
    for student in students:
        if (
            query.lower() in str(student.id).lower()
            or query.lower() in student.username.lower()
            or query.lower() in student.email.lower()
            or query.lower() in student.password.lower()
        ):
            results.append(student)
    table = Table(title=f"Student Search Results for '{query}'")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Username", style="magenta")
    table.add_column("Email", style="green")
    table.add_column("Password", style="red")
    table.add_column("Total Hours", style="yellow")
    for student in results:
        table.add_row(str(student.id), student.username, student.email, student.password, str(student.totalHours))
    console = Console()
    if results:
        console.print(table)
    else:
        console.print(f"[bold red]No students found matching '{query}'.[/bold red]")

@student_cli.command("update", help="Updates student info using ID")
@click.argument("id")
@click.option("--username")
@click.option("--email")
@click.option("--password")
def update_student_command(id, username, email, password):
    student = Student.query.get(id)
    if not student:
        print(f"Student with id {id} not found.")
        return
    updated = False
    if username:
        student.username = username
        updated = True
    if email:
        student.email = email
        updated = True
    if password:
        student.set_password(password)
        updated = True
    if updated:
        db.session.commit()
        print(f"Student {id} updated.")
    else:
        print("No changes provided.")

@student_cli.command("delete", help="Deletes a student by ID")
@click.argument("id")
def delete_student_command(id):
    student = Student.query.get(id)
    if not student:
        print(f"Student with id {id} not found.")
        return
    db.session.delete(student)
    db.session.commit()
    print(f"Student {id} deleted.")

@student_cli.command("dropTable", help="Clears the students table")
def drop_student_table_command():
    num_deleted = Student.query.delete()
    db.session.commit()
    print(f"Deleted {num_deleted} students from the students table.")

@student_cli.command("submitHours", help="Submits hours for a student")
@click.argument("id")
@click.argument("hours", type=float)
@click.argument("date")
def submit_hours_command(id, hours, date):
    student = Student.query.get(id)
    if not student:
        print(f"Student with id {id} not found.")
        return
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        print("Date must be in YYYY-MM-DD format.")
        return
    record = student.submitHours(hours, date_obj)
    print(f"Submitted {hours} hours for student {id} on {date} (record id: {record.id}).")

@student_cli.command("viewHours", help="Views all hour records for a student")
@click.argument("id")
def view_hours_command(id):
    student = Student.query.get(id)
    if not student:
        print(f"Student with id {id} not found.")
        return
    records = student.viewHours()
    if not records:
        print(f"No hour records found for student {id}.")
        return
    table = Table(title=f"Hour Records for Student {id}")
    table.add_column("Record ID", style="cyan", no_wrap=True)
    table.add_column("Date", style="magenta")
    table.add_column("Hours", style="green")
    table.add_column("Status", style="yellow")
    table.add_column("Staff ID", style="red")
    for record in records:
        table.add_row(str(record.id), record.date.isoformat(), str(record.hours), record.status, str(record.staffID) if record.staffID else "N/A")
    console = Console()
    console.print(table)

@student_cli.command("viewAccolades", help="Views all accolades for a student")
@click.argument("id")
def view_accolades_command(id):
    student = Student.query.get(id)
    if not student:
        print(f"Student with id {id} not found.")
        return
    accolades = student.viewAccolades()
    if not accolades:
        print(f"No accolades found for student {id}.")
        return
    table = Table(title=f"Accolades for Student {id}")
    table.add_column("Accolade ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Milestone Hours", style="green")
    for accolade in accolades:
        table.add_row(str(accolade.id), accolade.title, str(accolade.milestoneHours))
    console = Console()
    console.print(table)

app.cli.add_command(student_cli) # add the group to the cli

'''
Staff Commands
'''
staff_cli = AppGroup('staff', help='Staff object commands')

@staff_cli.command("create", help="Creates a staff member")
@click.argument("id")
@click.argument("username")
@click.argument("email")
@click.argument("password")
def create_staff_command(id, username, email, password):
    staff = Staff(id=id, username=username, email=email, password=password)
    db.session.add(staff)
    db.session.commit()
    print(f'{username} created!')

@staff_cli.command("list", help="Lists staff in the database")
@click.argument("format", default="string")
def list_staff_command(format):
    if format == 'string':
        stafvs = db.session.scalars(db.select(Staff)).all()
        table = Table(title="Staff List")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Username", style="magenta")
        table.add_column("Email", style="green")
        table.add_column("Password", style="red")
        for staff in stafvs:
            table.add_row(str(staff.id), staff.username, staff.email, staff.password)
        console = Console()
        console.print(table)

@staff_cli.command("searchALL", help="Searches ID, username, email or password for a match")
@click.argument("query")
def search_all_staff(query):
    stafvs = db.session.scalars(db.select(Staff)).all()
    results = []
    for staff in stafvs:
        if (
            query.lower() in str(staff.id).lower()
            or query.lower() in staff.username.lower()
            or query.lower() in staff.email.lower()
            or query.lower() in staff.password.lower()
        ):
            results.append(staff)
    table = Table(title=f"Staff Search Results for '{query}'")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Username", style="magenta")
    table.add_column("Email", style="green")
    table.add_column("Password", style="red")
    for staff in results:
        table.add_row(str(staff.id), staff.username, staff.email, staff.password)
    console = Console()
    if results:
        console.print(table)
    else:
        console.print(f"[bold red]No staff found matching '{query}'.[/bold red]")

@staff_cli.command("update", help="Updates staff info using ID")
@click.argument("id")
@click.option("--username")
@click.option("--email")
@click.option("--password")
def update_staff_command(id, username, email, password):
    staff = Staff.query.get(id)
    if not staff:
        print(f"Staff with id {id} not found.")
        return
    updated = False
    if username:
        staff.username = username
        updated = True
    if email:
        staff.email = email
        updated = True
    if password:
        staff.set_password(password)
        updated = True
    if updated:
        db.session.commit()
        print(f"Staff {id} updated.")
    else:
        print("No changes provided.")

@staff_cli.command("delete", help="Deletes a staff member by ID")
@click.argument("id")
def delete_staff_command(id):
    staff = Staff.query.get(id)
    if not staff:
        print(f"Staff with id {id} not found.")
        return
    db.session.delete(staff)
    db.session.commit()
    print(f"Staff {id} deleted.")

@staff_cli.command("dropTable", help="Clears the staff table")
def drop_staff_table_command():
    num_deleted = Staff.query.delete()
    db.session.commit()
    print(f"Deleted {num_deleted} staff members from the staff table.")

@staff_cli.command("logHours", help="Logs hours for a student")
@click.argument("staffID")
@click.argument("studentID")
@click.argument("hours", type=float)
@click.argument("date")
def log_hours_command(staffID, studentID, hours, date):
    staff = Staff.query.get(staffID)
    if not staff:
        print(f"Staff with id {staffID} not found.")
        return
    student = Student.query.get(studentID)
    if not student:
        print(f"Student with id {studentID} not found.")
        return
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        print("Date must be in YYYY-MM-DD format.")
        return
    record = staff.logHours(student, hours, date_obj)
    print(f"Logged {hours} hours for student {studentID} on {date} (record ID: {record.id}).")

@staff_cli.command("approveHours", help="Approves a student's hour record")
@click.argument("staffID")
@click.argument("recordID", type=int)
def approve_hours_command(staffID, recordID):
    staff = Staff.query.get(staffID)
    if not staff:
        print(f"Staff with id {staffID} not found.")
        return
    record = HourRecord.query.get(recordID)
    if not record:
        print(f"Hour record with id {recordID} not found.")
        return
    if record.status == "Approved":
        print(f"Hour record {recordID} is already approved.")
        return
    staff.approveHours(record)
    print(f"Hour record {recordID} approved by staff {staffID}.")

flask staff manage-hours <staff_id>
@staff_cli.command("manageHours", help="Manages a student's hour record")
@click.argument("staffID")
@click.argument("recordID", type=int)
@click.option("--hours", type=float)
@click.option("--date")
@click.option("--status")
def manage_hours_command(staffID, recordID, hours, date, status):
    staff = Staff.query.get(staffID)
    if not staff:
        print(f"Staff with id {staffID} not found.")
        return
    date_obj = None
    if date:
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            print("Date must be in YYYY-MM-DD format.")
            return
    record = staff.manageHours(recordID, hours=hours, date=date_obj, status=status)
    if not record:
        print(f"Hour record with id {recordID} not found or you do not have permission to manage it.")
        return
    print(f"Hour record {recordID} updated by staff {staffID}.")


app.cli.add_command(staff_cli) # add the group to the cli




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

