from App.database import db
import datetime

class HourRecord(db.Model):
    __tablename__ = "hourRecord"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, default=datetime.date.today, nullable=False)
    hours = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="Pending", nullable=False)

    studentID = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    staffID = db.Column(db.Integer, db.ForeignKey("staff.id"), nullable=True)  # Staff who approved/logged

    student = db.relationship("Student", back_populates="hourRecord")
    staff = db.relationship("Staff", back_populates="hourRecord")

    def __init__(self, studentID, hours, date=None, status="Pending", staffID=None):
        self.studentID = studentID
        self.hours = hours
        self.date = date if date is not None else datetime.date.today()
        self.status = status
        self.staffID = staffID

    def approve(self, staffID):
        self.status = "Approved"
        self.staffID = staffID
        db.session.commit()

    def reject(self, staffID):
        self.status = "Rejected"
        self.staffID = staffID
        db.session.commit()

    def get_json(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'hours': self.hours,
            'status': self.status,
            'studentID': self.studentID,
            'staffID': self.staffID
        }

    def __repr__(self):
        return f"<ID: {self.id}, StudentID: {self.studentID}, Date: {self.date} Hours: {self.hours}, Status: {self.status}, StudentID: {self.studentID}, StaffID: {self.staffID}>"