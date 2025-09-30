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
        print(f"User with id {id} not found")
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
        print(f"User {id} updated")
    else:
        print("No changes given")

@user_cli.command("delete", help="Deletes a user by ID")
@click.argument("id")
def delete_user_command(id):
    user = User.query.get(id)
    if not user:
        print(f"User with id {id} not found")
        return
    db.session.delete(user)
    db.session.commit()
    print(f"User {id} deleted")

@user_cli.command("dropTable", help="Clears the users table")
def drop_user_table_command():
    num_deleted = User.query.delete()
    db.session.commit()
    print(f"Deleted {num_deleted} users from the users table")

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
        print(f"Student with id {id} not found")
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
        print(f"Student {id} updated")
    else:
        print("No changes provided")

@student_cli.command("delete", help="Deletes a student by ID")
@click.argument("id")
def delete_student_command(id):
    student = Student.query.get(id)
    if not student:
        print(f"Student with id {id} not found")
        return
    db.session.delete(student)
    db.session.commit()
    print(f"Student {id} deleted")

@student_cli.command("dropTable", help="Clears the students table")
def drop_student_table_command():
    num_deleted = Student.query.delete()
    db.session.commit()
    print(f"Deleted {num_deleted} students from the students table")

@student_cli.command("submitHours", help="Submits hours for a student")
@click.argument("id")
@click.argument("hours", type=float)
@click.argument("date")
def submit_hours_command(id, hours, date):
    student = Student.query.get(id)
    if not student:
        print(f"Student with id {id} not found")
        return
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        print("Date must be in YYYY-MM-DD format")
        return
    record = student.submitHours(hours, date_obj)
    print(f"Submitted {hours} hours for student {id} on {date} (record id: {record.id})")

@student_cli.command("viewHours", help="Views all hour records for a student")
@click.argument("id")
def view_hours_command(id):
    student = Student.query.get(id)
    if not student:
        print(f"Student with id {id} not found")
        return
    records = student.viewHours()
    if not records:
        print(f"No hour records found for student {id}")
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
        print(f"Student with id {id} not found")
        return
    accolades = student.viewAccolades()
    if not accolades:
        print(f"No accolades found for student {id}")
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
        print(f"Staff with id {id} not found")
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
        print(f"Staff {id} updated")
    else:
        print("No changes givenn")

@staff_cli.command("delete", help="Deletes a staff member by ID")
@click.argument("id")
def delete_staff_command(id):
    staff = Staff.query.get(id)
    if not staff:
        print(f"Staff with id {id} not found")
        return
    db.session.delete(staff)
    db.session.commit()
    print(f"Staff {id} deleted")

@staff_cli.command("dropTable", help="Clears the staff table")
def drop_staff_table_command():
    num_deleted = Staff.query.delete()
    db.session.commit()
    print(f"Deleted {num_deleted} staff members from the staff table")

@staff_cli.command("logHours", help="Logs hours for a student")
@click.argument("staffID")
@click.argument("studentID")
@click.argument("hours", type=float)
@click.argument("date")
def log_hours_command(staffID, studentID, hours, date):
    staff = Staff.query.get(staffID)
    if not staff:
        print(f"Staff with id {staffID} not found")
        return
    student = Student.query.get(studentID)
    if not student:
        print(f"Student with id {studentID} not found")
        return
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        print("Date must be in YYYY-MM-DD format")
        return
    record = staff.logHours(student, hours, date_obj)
    print(f"Logged {hours} hours for student {studentID} on {date} (record ID: {record.id})")

@staff_cli.command("approveHours", help="Approves a student's hour record")
@click.argument("staffID")
@click.argument("recordID", type=int)
def approve_hours_command(staffID, recordID):
    staff = Staff.query.get(staffID)
    if not staff:
        print(f"Staff with id {staffID} not found")
        return
    record = HourRecord.query.get(recordID)
    if not record:
        print(f"Hour record with id {recordID} not found")
        return
    if record.status == "Approved":
        print(f"Hour record {recordID} is already approved")
        return
    staff.approveHours(record)
    print(f"Hour record {recordID} approved by staff {staffID}")

@staff_cli.command("manageHours", help="Manages a student's hour record")
@click.argument("staffID")
@click.argument("recordID", type=int)
@click.option("--hours", type=float)
@click.option("--date")
@click.option("--status")
def manage_hours_command(staffID, recordID, hours, date, status):
    staff = Staff.query.get(staffID)
    if not staff:
        print(f"Staff with id {staffID} not found")
        return
    date_obj = None
    if date:
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            print("Date must be in YYYY-MM-DD format")
            return
    record = staff.manageHours(recordID, hours=hours, date=date_obj, status=status)
    if not record:
        print(f"Hour record with id {recordID} not found or you do not have permission to manage it")
        return
    print(f"Hour record {recordID} updated by staff {staffID}")


app.cli.add_command(staff_cli) # add the group to the cli

'''
Hour Record Commands
'''
hourRecord_cli = AppGroup('hourRecord', help='hourRecord object commands')

@hourRecord_cli.command("create", help="Creates an hour record")
@click.argument("studentID")
@click.argument("hours", type=float)
@click.argument("date")
@click.argument("status")
@click.option("--staffID", default=None)
def create_hourrecord_command(studentID, hours, date, status, staffID):
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        print("Date must be in YYYY-MM-DD format")
        return
    record = HourRecord(studentID=studentID, hours=hours, date=date_obj, status=status, staffID=staffID)
    db.session.add(record)
    db.session.commit()
    print(f'Hour record {record.id} created for student {studentID}!')

@hourRecord_cli.command("list", help="Lists hour records in the database")
@click.argument("format", default="string")
def list_hourrecord_command(format):
    if format == 'string':
        records = db.session.scalars(db.select(HourRecord)).all()
        table = Table(title="Hour Record List")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Student ID", style="magenta")
        table.add_column("Date", style="green")
        table.add_column("Hours", style="yellow")
        table.add_column("Status", style="red")
        table.add_column("Staff ID", style="blue")
        for record in records:
            table.add_row(str(record.id), str(record.studentID), record.date.isoformat(), str(record.hours), record.status, str(record.staffID) if record.staffID else "N/A")
        console = Console()
        console.print(table)

@hourRecord_cli.command("searchByStudentID", help="Searches hour records by student ID")
@click.argument("studentID")
def search_hourrecord_by_student_command(studentID):    
    records = db.session.scalars(db.select(HourRecord).where(HourRecord.studentID == studentID)).all()
    if not records:
        print(f"No hour records found for student ID {studentID}")
        return
    table = Table(title=f"Hour Records for Student {studentID}")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Date", style="magenta")
    table.add_column("Hours", style="green")
    table.add_column("Status", style="yellow")
    table.add_column("Staff ID", style="red")
    for record in records:
        table.add_row(str(record.id), record.date.isoformat(), str(record.hours), record.status, str(record.staffID) if record.staffID else "N/A")
    console = Console()
    console.print(table)

@hourRecord_cli.command("searchByStaffID", help="Searches hour records by staff ID")
@click.argument("staffID")
def search_hourrecord_by_staff_command(staffID):    
    records = db.session.scalars(db.select(HourRecord).where(HourRecord.staffID == staffID)).all()
    if not records:
        print(f"No hour records found for staff ID {staffID}")
        return
    table = Table(title=f"Hour Records managed by Staff {staffID}")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Student ID", style="magenta")
    table.add_column("Date", style="green")
    table.add_column("Hours", style="yellow")
    table.add_column("Status", style="red")
    for record in records:
        table.add_row(str(record.id), str(record.studentID), record.date.isoformat(), str(record.hours), record.status)
    console = Console()
    console.print(table)

@hourRecord_cli.command("searchByDate", help="Searches hour records by date")
@click.argument("date")
def search_hourrecord_by_date_command(date):    
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        print("Date must be in YYYY-MM-DD format")
        return
    records = db.session.scalars(db.select(HourRecord).where(HourRecord.date == date_obj)).all()
    if not records:
        print(f"No hour records found for date {date}")
        return
    table = Table(title=f"Hour Records for Date {date}")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Student ID", style="magenta")
    table.add_column("Hours", style="yellow")
    table.add_column("Status", style="red")
    table.add_column("Staff ID", style="blue")
    for record in records:
        table.add_row(str(record.id), str(record.studentID), str(record.hours), record.status, str(record.staffID) if record.staffID else "N/A")
    console = Console()
    console.print(table)

@hourRecord_cli.command("searchByStatus", help="Searches hour records by status")
@click.argument("status")
def search_hourrecord_by_status_command(status):    
    records = db.session.scalars(db.select(HourRecord).where(HourRecord.status.ilike(f"%{status}%"))).all()
    if not records:
        print(f"No hour records found with status matching '{status}'")
        return
    table = Table(title=f"Hour Records with Status matching '{status}'")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Student ID", style="magenta")
    table.add_column("Date", style="green")
    table.add_column("Hours", style="yellow")
    table.add_column("Staff ID", style="blue")
    for record in records:
        table.add_row(str(record.id), str(record.studentID), record.date.isoformat(), str(record.hours), str(record.staffID) if record.staffID else "N/A")
    console = Console()
    console.print(table)

@hourRecord_cli.command("approve", help="Approves an hour record by ID")
@click.argument("id", type=int)
@click.argument("staffID")
def approve_hourrecord_command(id, staffID):
    staff = Staff.query.get(staffID)
    if not staff:
        print(f"Staff with id {staffID} not found")
        return
    record = HourRecord.query.get(id)
    if not record:
        print(f"Hour record with id {id} not found")
        return
    if record.status == "Approved":
        print(f"Hour record {id} is already approved")
        return
    staff.approveHours(record)
    print(f"Hour record {id} approved by staff {staffID}")

@hourRecord_cli.command("reject", help="Rejects an hour record by ID")
@click.argument("id", type=int)
@click.argument("staffID")
def reject_hourrecord_command(id, staffID):   
    staff = Staff.query.get(staffID)
    if not staff:
        print(f"Staff with id {staffID} not found")
        return
    record = HourRecord.query.get(id)
    if not record:
        print(f"Hour record with id {id} not found")
        return
    if record.status == "Rejected":
        print(f"Hour record {id} is already rejected")
        return
    staff.rejectHours(record)
    print(f"Hour record {id} rejected by staff {staffID}")

@hourRecord_cli.command("update", help="Updates an hour record by ID")
@click.argument("id", type=int)
@click.option("--studentID", type=int)
@click.option("--hours", type=float)
@click.option("--date")
@click.option("--status")
@click.option("--staffID", type=int)
def update_hourrecord_command(id, studentID, hours, date, status, staffID):
    record = HourRecord.query.get(id)
    if not record:
        print(f"Hour record with id {id} not found")
        return
    updated = False
    if studentID:
        record.studentID = studentID
        updated = True
    if hours:
        record.hours = hours
        updated = True
    if date:
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            record.date = date_obj
            updated = True
        except ValueError:
            print("Date must be in YYYY-MM-DD format")
            return
    if status:
        record.status = status
        updated = True
    if staffID:
        record.staffID = staffID
        updated = True
    if updated:
        db.session.commit()
        print(f"Hour record {id} updated")
    else:
        print("Invalid, no changes given")

@hourRecord_cli.command("delete", help="Deletes an hour record by ID")
@click.argument("id", type=int)
def delete_hourrecord_command(id):
    record = HourRecord.query.get(id)
    if not record:
        print(f"Hour record with id {id} not found")
        return
    db.session.delete(record)
    db.session.commit()
    print(f"Hour record {id} deleted")

@hourRecord_cli.command("dropTable", help="Clears the hour records table")
def drop_hourrecord_table_command():
    num_deleted = HourRecord.query.delete()
    db.session.commit()
    print(f"Deleted {num_deleted} hour records from the hour records table")

app.cli.add_command(hourRecord_cli) # add the group to the cli

'''
Accolade Commands
'''
accolade_cli = AppGroup('accolade', help='Accolade object commands')

@accolade_cli.command("create", help="Creates an accolade")
@click.argument("title")
@click.argument("milestoneHours", type=float)
def create_accolade_command(title, milestoneHours):
    accolade = Accolade(title=title, milestoneHours=milestoneHours)
    db.session.add(accolade)
    db.session.commit()
    print(f'Accolade {title} created!')

@accolade_cli.command("list", help="Lists accolades in the database")
@click.argument("format", default="string")
def list_accolade_command(format):
    if format == 'string':
        accolades = db.session.scalars(db.select(Accolade)).all()
        table = Table(title="Accolade List")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Title", style="magenta")
        table.add_column("Milestone Hours", style="green")
        for accolade in accolades:
            table.add_row(str(accolade.id), accolade.title, str(accolade.milestoneHours))
        console = Console()
        console.print(table)

@accolade_cli.command("update", help="Updates an accolade by ID")
@click.argument("id", type=int)
@click.option("--title")
@click.option("--milestoneHours", type=float)
def update_accolade_command(id, title, milestoneHours):
    accolade = Accolade.query.get(id)
    if not accolade:
        print(f"Accolade with id {id} not found")
        return
    updated = False
    if title:
        accolade.title = title
        updated = True
    if milestoneHours:
        accolade.milestoneHours = milestoneHours
        updated = True
    if updated:
        db.session.commit()
        print(f"Accolade {id} updated")
    else:
        print("No changes given")

@accolade_cli.command("delete", help="Deletes an accolade by ID")
@click.argument("id", type=int)
def delete_accolade_command(id):
    accolade = Accolade.query.get(id)
    if not accolade:
        print(f"Accolade with id {id} not found")
        return
    db.session.delete(accolade)
    db.session.commit()
    print(f"Accolade {id} deleted")

@accolade_cli.command("dropTable", help="Clears the accolades table")   
def drop_accolade_table_command():
    num_deleted = Accolade.query.delete()
    db.session.commit()
    print(f"Deleted {num_deleted} accolades from the accolades table")

app.cli.add_command(accolade_cli)

'''
Leaderboard Commands
'''
leaderboard_cli = AppGroup('leaderboard', help='Leaderboard object commands')

@leaderboard_cli.command("list", help="Lists the leaderboard")
@click.argument("format", default="string")
def list_leaderboard_command(format):
    if format == 'string':
        leaderboard = db.session.scalars(db.select(Leaderboard)).all()
        table = Table(title="Leaderboard")
        table.add_column("Rank", style="cyan", no_wrap=True)
        table.add_column("Student ID", style="magenta")
        table.add_column("Username", style="green")
        table.add_column("Total Hours", style="yellow")
        for entry in leaderboard:
            student = Student.query.get(entry.studentID)
            username = student.username if student else "N/A"
            table.add_row(str(entry.rank), str(entry.studentID), username, str(entry.totalHours))
        console = Console()
        console.print(table)

@leaderboard_cli.command("refresh", help="Refreshes the leaderboard")
def refresh_leaderboard_command():
    Leaderboard.updateRanking()
    print("Leaderboard refreshed")

@leaderboard_cli.command("searchALL", help="Searches student ID or username for a match in the leaderboard")
@click.argument("query")
def search_all_leaderboard(query):
    leaderboard = db.session.scalars(db.select(Leaderboard)).all()
    results = []
    for entry in leaderboard:
        student = Student.query.get(entry.studentID)
        username = student.username if student else ""
        if (
            query.lower() in str(entry.studentID).lower()
            or query.lower() in username.lower()
        ):
            results.append((entry, username))
    table = Table(title=f"Leaderboard Search Results for '{query}'")
    table.add_column("Rank", style="cyan", no_wrap=True)
    table.add_column("Student ID", style="magenta")
    table.add_column("Username", style="green")
    table.add_column("Total Hours", style="yellow")
    for entry, username in results:
        table.add_row(str(entry.rank), str(entry.studentID), username, str(entry.totalHours))
    console = Console()
    if results:
        console.print(table)
    else:
        console.print(f"[bold red]No leaderboard entries found matching '{query}'.[/bold red]")

@leaderboard_cli.command("dropTable", help="Clears the leaderboard table")
def drop_leaderboard_table_command():
    num_deleted = Leaderboard.query.delete()
    db.session.commit()
    print(f"Deleted {num_deleted} students from the leaderboard table")

app.cli.add_command(leaderboard_cli)

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

