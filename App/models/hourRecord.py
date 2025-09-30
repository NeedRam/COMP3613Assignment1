from App.database import db
import datetime

class HourRecord(db.Model):
    __tablename__ = "hour_records"

    recordID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, default=datetime.date.today, nullable=False)
    hours = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="Pending", nullable=False)

    studentID = db.Column(db.Integer, db.ForeignKey("students.userID"), nullable=False)
    staffID = db.Column(db.Integer, db.ForeignKey("staff.userID"), nullable=True)  # Staff who approved/logged

    student = db.relationship("Student", back_populates="hour_records")
    staff = db.relationship("Staff", back_populates="hour_records")

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

    def __repr__(self):
        return f"<HourRecord ID={self.recordID}, Student={self.studentID}, Hours={self.hours}, Status={self.status}>"