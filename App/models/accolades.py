from App.database import db

student_accolades = db.Table(
    "student_accolades",
    db.Column("student_id", db.Integer, db.ForeignKey("students.id"), primary_key=True),
    db.Column("accolade_id", db.Integer, db.ForeignKey("accolades.id"), primary_key=True)
)

class Accolade(db.Model):
    __tablename__ = "accolades"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    milestoneHours = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)

    def __init__(self, title, milestoneHours):
        self.title = title
        self.milestoneHours = milestoneHours

    def get_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'milestoneHours': self.milestoneHours
        }        

    def __repr__(self):
        return f"<ID: {self.id}, Title: {self.title}, Milestone Hours: {self.milestoneHours}>"