from App.database import db

class Leaderboard(db.Model):
    __tablename__ = "leaderboard"

    leaderboardID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    studentID = db.Column(db.Integer, db.ForeignKey("students.userID"), nullable=False)
    rank = db.Column(db.Integer, nullable=False)

    student = db.relationship("Student")

    def __init__(self, studentID, rank):
        self.studentID = studentID
        self.rank = rank

    @staticmethod
    def updateRanking():
        from App.models.student import Student

        # Clear leaderboard
        Leaderboard.query.delete()
        db.session.commit()

        # Get students ordered by hours (descending)
        students = Student.query.order_by(Student.totalHours.desc()).all()

        # Assign new ranks
        rank = 1
        for student in students:
            entry = Leaderboard(studentID=student.userID, rank=rank)
            db.session.add(entry)
            rank += 1

        db.session.commit()

    def __repr__(self):
        return f"<Leaderboard Rank={self.studentID}, Rank={self.rank}>"