from App.database import db
from App.models.student import Student

class Leaderboard(db.Model):
    __tablename__ = "leaderboard"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    rank = db.Column(db.Integer, nullable=False)

    student = db.relationship("Student")

    def __init__(self, student_id, rank):
        self.student_id = student_id
        self.rank = rank

    @staticmethod
    def updateRanking():

        # Clear leaderboard
        Leaderboard.query.delete()
        db.session.commit()

        # Get students ordered by hours (descending)
        students = Student.query.order_by(Student.totalHours.desc()).all()

        # Assign new ranks
        rank = 1
        for student in students:
            entry = Leaderboard(student_id=student.id, rank=rank)
            db.session.add(entry)
            rank += 1

        db.session.commit()

    def get_json(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'rank': self.rank
        }

    def __repr__(self):
        return f"<ID: {self.id}, student_id: {self.student_id}, Rank: {self.rank}>"