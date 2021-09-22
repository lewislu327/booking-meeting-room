from meetingRoomBooking import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    rooms = db.relationship('Room', backref='roomUser', lazy=True)
    role = db.Column(db.String(20), nullable=False, default='User')
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date(), nullable=False)
    roomName = db.Column(db.String(20), nullable=False)
    start_at = db.Column(db.String(20), nullable=False)
    end_at = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return f"Room('{self.roomName}', '{self.date}','{self.start_at}','{self.end_at}')"
