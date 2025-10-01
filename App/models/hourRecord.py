from App.database import db
import datetime

class HourRecord(db.Model):
    __tablename__ = "hourRecord"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, default=datetime.date.today, nullable=False)
    hours = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="Pending", nullable=False)

    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey("staff.id"), nullable=True)  # Staff who approved/logged

    student = db.relationship("Student", back_populates="hourRecord")
    staff = db.relationship("Staff", back_populates="hourRecord")

    def __init__(self, student_id, hours, date=None, status="Pending", staff_id=None):
        self.student_id = student_id
        self.hours = hours
        self.date = date if date is not None else datetime.date.today()
        self.status = status
        self.staff_id = staff_id

    def approve(self, staff_id):
        self.status = "Approved"
        self.staff_id = staff_id
        db.session.commit()

    def reject(self, staff_id):
        self.status = "Rejected"
        self.staff_id = staff_id
        db.session.commit()

    def get_json(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'hours': self.hours,
            'status': self.status,
            'student_id': self.student_id,
            'staff_id': self.staff_id
        }

    def __repr__(self):
        return f"<ID: {self.id}, student_id: {self.student_id}, Date: {self.date} Hours: {self.hours}, Status: {self.status}, student_id: {self.student_id}, staff_id: {self.staff_id}>"