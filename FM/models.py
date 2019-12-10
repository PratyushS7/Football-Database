from FM import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(club_id):
    return Club.query.get(int(club_id))

class Club(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    clubn = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    manager = db.relationship('Manager', backref='manages', lazy=True)
    player = db.relationship('Player',backref='plays_for',lazy=True)
    stadium= db.relationship('Stadium',backref='belongs_to',lazy=True)
    def __repr__(self):
            return f"Club('{self.club}','{self.manager}','{self.image_file}')"

class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    desc = db.Column(db.Text, nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'), nullable=False)
    def __repr__(self):
        return f"Manager('{self.id}','{self.name}')"


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    age = db.Column(db.String(10), nullable=False)
    country = db.Column(db.String(60),nullable=False)
    position= db.Column(db.String(40),nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'), nullable=False)
    def __repr__(self):
        return f"Player('{self.id}','{self.name}')"

class Stadium(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(100),nullable=False)
    city= db.Column(db.String(100),nullable= False)
    club_id= db.Column(db.Integer,db.ForeignKey('club.id'), nullable=False)
