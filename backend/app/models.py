from app import db
from datetime import datetime, timezone

profile_interests = db.Table('profile_interests',
    db.Column('profile_id', db.Integer, db.ForeignKey('profiles.id'), primary_key=True),
    db.Column('interest_id', db.Integer, db.ForeignKey('interests.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    is_active = db.Column(db.Boolean, default=True)

    profile = db.relationship('Profile', back_populates='user', uselist=False)
    sent_matches = db.relationship('Match', back_populates='sender', foreign_keys='Match.sender_id')
    received_matches = db.relationship('Match', back_populates='receiver', foreign_keys='Match.receiver_id')
    sent_messages = db.relationship('Message', back_populates='sender', foreign_keys='Message.sender_id')
    received_messages = db.relationship('Message', back_populates='receiver', foreign_keys='Message.receiver_id')

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at,
            'is_active': self.is_active
        }
    
class Profile(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    #Personal information
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    age = db.Column(db.Integer)
    bio = db.Column(db.Text)
    gender = db.Column(db.String(20))
    looking_for = db.Column(db.String(20))

    #Location information
    location = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    #Preferences
    preferred_age_min = db.Column(db.Integer, default=18)
    preferred_age_max = db.Column(db.Integer, default=100)
    distance_preference_km = db.Column(db.Integer, default=50)

    #Additional fields
    relationship_goal = db.Column(db.String(255))
    occupation = db.Column(db.String(255))
    education = db.Column(db.String(255))

    is_public = db.Column(db.Boolean, default=True)

    photo_url = db.Column(db.String(255))

    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    user = db.relationship('User', back_populates='profile')
    interests = db.relationship('Interest', secondary=profile_interests, back_populates='profiles')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'bio': self.bio,
            'gender': self.gender,
            'looking_for': self.looking_for,
            'location': self.location,
            'relationship_goal': self.relationship_goal,
            'occupation': self.occupation,
            'education': self.education,
            'is_public': self.is_public,
            'photo_url': self.photo_url,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'interests': [interest.name for interest in self.interests]
        }
    
class Interest(db.Model):
    __tablename__ = 'interests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    profiles = db.relationship('Profile', secondary=profile_interests, back_populates='interests')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
    
class Match(db.Model):
    __tablename__ = 'matches'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_mutual = db.Column(db.Boolean, default=False) #both users have liked each other
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    action = db.Column(db.String(20), nullable=False) #like, dislike, superlike

    __table_args__ = (
        db.UniqueConstraint('sender_id', 'receiver_id', name='unique_match'),
        db.Index('idx_sender_receiver', 'sender_id', 'receiver_id')
    )

    sender = db.relationship('User', back_populates='sent_matches', foreign_keys=[sender_id])
    receiver = db.relationship('User', back_populates='received_matches', foreign_keys=[receiver_id])

    def to_dict(self):
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'is_mutual': self.is_mutual,
            'created_at': self.created_at,
            'action': self.action
        }
    
class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    sender = db.relationship('User', back_populates='sent_messages', foreign_keys=[sender_id])
    receiver = db.relationship('User', back_populates='received_messages', foreign_keys=[receiver_id])

    def to_dict(self):
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'content': self.content,
            'created_at': self.created_at
        }
    
