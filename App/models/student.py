from App.database import db
from App.models.user import User
from App.models.accolades import Accolade, student_accolades
from App.models.hourRecord import HourRecord

class Student(User):
    __tablename__ = "students"
    __mapper_args__ = {"polymorphic_identity": "student"}

    id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)

    hourRecord = db.relationship("HourRecord", back_populates="student", cascade="all, delete-orphan")
    accolades = db.relationship("Accolade", secondary=student_accolades, backref="students", passive_deletes=True)

    @property
    def totalHours(self):
        return sum(hr.hours for hr in self.hourRecord if hr.status == "Approved")

    def submitHours(self, hours, date):
        record = HourRecord(student_id=self.id, hours=hours, date=date, status="Pending")
        db.session.add(record)
        db.session.commit()
        return record

    def viewHours(self):
        return self.hourRecord

    def check_and_unlock_milestones(self):
        all_accolades = Accolade.query.all()
        unlocked_ids = {a.id for a in self.accolades}
        new_accolades = []
        for accolade in all_accolades:
            if self.totalHours >= accolade.milestone_hours and accolade.id not in unlocked_ids:
                self.accolades.append(accolade)
                print(f"Congratulations {self.username}! You unlocked the '{accolade.title}' milestone.")
                new_accolades.append(accolade)
        if new_accolades:
            db.session.commit()
        return new_accolades
    
    def viewAccolades(self):
        self.check_and_unlock_milestones()
        return self.accolades
    
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