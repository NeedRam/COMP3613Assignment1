from App.database import db
from App.models.user import User
from App.models.accolades import Accolade, student_accolades
from App.models.hourRecord import HourRecord

class Student(User):
    __tablename__ = "students"
    __mapper_args__ = {"polymorphic_identity": "student"}

    id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)

    user = db.relationship("User", back_populates="student")
    hourRecords = db.relationship("HourRecord", back_populates="student", cascade="all, delete-orphan")
    accolades = db.relationship("Accolade", secondary=student_accolades, backref="students")

    @property
    def totalHours(self):
        return sum(hr.hours for hr in self.hour_records if hr.status == "Approved")

    def submitHours(self, hours, date):
        record = HourRecord(studentID=self.id, hours=hours, date=date, status="Pending")
        db.session.add(record)
        db.session.commit()
        return record

    def viewHours(self):
        return self.hour_records

    def viewAccolades(self):
        return self.accolades

    def check_and_unlock_milestones(self):
        all_accolades = Accolade.query.all()
        unlocked_ids = {a.accoladeID for a in self.accolades}
        new_accolades = []
        for accolade in all_accolades:
            if self.totalHours >= accolade.milestoneHours and accolade.accoladeID not in unlocked_ids:
                self.accolades.append(accolade)
                print(f"Congratulations {self.userName}! You unlocked the '{accolade.title}' milestone.")
                new_accolades.append(accolade)
        if new_accolades:
            db.session.commit()
        return new_accolades
    
    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'totalHours': self.totalHours     
        }

    def __repr__(self):
        return f"<ID: {self.id}, Username: {self.username}, Email: {self.email}, Password: {self.password}, Total Hours: {self.totalHours}>"