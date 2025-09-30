from App.database import db
from App.models.user import User
from App.models.hourRecord import HourRecord

class Staff(User):
    __tablename__ = "staff"
    __mapper_args__ = {"polymorphic_identity": "staff"}

    id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    
    user = db.relationship("User", back_populates="staff")
    hourRecord = db.relationship("HourRecord", back_populates="staff")

    def logHours(self, student, hours, date):
        record = HourRecord(studentID=student.id, staffID=self.id, hours=hours, date=date, status="Approved")
        db.session.add(record)
        db.session.commit()
        return record

    def approveHours(self, record):
        record.status = "Approved"
        db.session.commit()

    def manageHours(self):
        return self.hourRecord
    
    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password       
        }

    def __repr__(self):
        return f"<ID: {self.id}, Username: {self.username}, Email: {self.email}, Password: {self.password}>"
