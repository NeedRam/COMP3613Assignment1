from App.database import db

student_accolades = db.Table(
    "student_accolades",
    db.Column("student_id", db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"), primary_key=True),
    db.Column("accoladeID", db.Integer, db.ForeignKey("accolades.id", ondelete="CASCADE"), primary_key=True)
)

class Accolade(db.Model):
    __tablename__ = "accolades"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    milestone_hours = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)

    def __init__(self, title, milestone_hours):
        self.title = title
        self.milestone_hours = milestone_hours

    def get_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'milestone_hours': self.milestone_hours
        }        

    def __repr__(self):
        return f"<ID: {self.id}, Title: {self.title}, Milestone Hours: {self.milestone_hours}>"