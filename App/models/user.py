from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    student = db.relationship("Student", uselist=False, back_populates="user")
    staff = db.relationship("Staff", uselist=False, back_populates="user")

    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

    

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password       
        }
    
    def __repr__(self):
        return f"<ID {self.id}, Username: {self.username}, Email: {self.email}, Password: {self.password}>"

