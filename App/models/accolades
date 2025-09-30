from App.database import db

student_accolades = db.Table(
    "student_accolades",
    db.Column("student_id", db.Integer, db.ForeignKey("students.userID"), primary_key=True),
    db.Column("accolade_id", db.Integer, db.ForeignKey("accolades.accoladeID"), primary_key=True)
)

class Accolade(db.Model):
    __tablename__ = "accolades"
    
    accoladeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    milestoneHours = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)

    def __init__(self, title, milestoneHours):
        self.title = title
        self.milestoneHours = milestoneHours

    def __repr__(self):
        return f"<Accolade {self.title}, Milestone: {self.milestoneHours}>"