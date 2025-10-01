from App.database import db
from App.models.user import User
from App.models.hourRecord import HourRecord

class Staff(User):
    __tablename__ = "staff"
    __mapper_args__ = {"polymorphic_identity": "staff"}

    id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    
    hourRecord = db.relationship("HourRecord", back_populates="staff")

    def logHours(self, student, hours, date):
        record = HourRecord(student_id=student.id, staff_id=self.id, hours=hours, date=date, status="Approved")
        db.session.add(record)
        db.session.commit()
        return record

    def approveHours(self, record):
        record.status = "Approved"
        db.session.commit()
    
    def rejectHours(self, record):
        record.status = "Rejected"
        db.session.commit()

    def manageHours(self, record_id, hours=None, date=None, status=None):
        record = HourRecord.query.get(record_id)
        if not record or record.staff_id != self.id:
            return None
        if hours is not None:
            record.hours = hours
        if date is not None:
            record.date = date
        if status is not None:
            record.status = status
        db.session.commit()
        return record
    
    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password       
        }

    def __repr__(self):
        return f"<ID: {self.id}, Username: {self.username}, Email: {self.email}, Password: {self.password}>"
