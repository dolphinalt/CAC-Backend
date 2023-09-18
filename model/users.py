""" database dependencies to support sqliteDB examples """
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id=db.Column(db.Integer, primary_key=True)
    _uid = db.Column(db.String, unique=True, nullable=False)
    _name = db.Column(db.String, unique=False, nullable=False)
    _pfp = db.Column(db.String, unique=False, nullable=True)
    _about = db.Column(db.String, unique=False, nullable=True)
    _password = db.Column(db.String, unique=False, nullable=False)
    _allergies = db.Column(db.String, unique=False, nullable=True)
    _isResturuant = db.Column(db.Boolean, unique=False, nullable=False)

    def __init__(self, id, name, isResturuant, password, pfp="", about="", allergies=""):
        self._uid = id
        self._name = name
        self._pfp = pfp
        self._about = about
        self._password = password
        self._allergies = allergies
        self._isResturuant = isResturuant
    
    @property
    def uid(self):
        return self._uid
    @property
    def name(self):
        return self._name
    @property
    def pfp(self):
        return self._pfp
    @property
    def about(self):
        return self._about
    @property
    def password(self):
        return self._password[0:3] + "..."
    @property
    def allergies(self):
        return self._allergies
    @property
    def isResturuant(self):
        return self._isResturuant
    
    @uid.setter
    def uid(self, uid):
        self._uid = uid
    @name.setter
    def name(self, name):
        self._name = name
    @pfp.setter
    def pfp(self, pfp):
        self._pfp = pfp
    @about.setter
    def about(self, about):
        self._about = about
    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password, method='sha256')
    @allergies.setter
    def allergies(self, allergies):
        self._allergies = allergies
    @isResturuant.setter
    def isResturuant(self, isResturuant):
        self._isResturuant = isResturuant
    
    ### UTILITIES ###
    def is_uid(self, uid):
        return self._uid == uid
    def is_password(self, password):
        """Check against hashed password."""
        result = check_password_hash(self._password, password)
        return result
    ### UTILITIES ###

    def __str__(self):
        return json.dumps(self.read())

    ### CREATE ###
    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None
    ### CREATE ###

    ### READ ###
    def read(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "name": self.name,
            "pfp": self.pfp,
            "about": self.about,
            "allergies": self.allergies,
            "isResturuant": self.isResturuant
        }
    ### READ ###

    ### UPDATE ###
    def update(self, name="", pfp="", about="", password="", allergies=""):
            """only updates values with length"""
            if len(name) > 0:
                self.name = name
            if len(pfp) > 0:
                self.pfp = pfp
            if len(about) > 0:
                self.about = about
            if len(password) > 0:
                self.set_password(password)
            if len(allergies) > 0:
                self.allergies = allergies
            db.session.commit()
            return self
    ### UPDATE ###

    ### DELETE ###
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None
    ### DELETE ###

def initAllergyUsers():
    db.create_all()
    u1=User(id=1, name="John", about="John is a cool guy", isResturuant=False, password="password")
    u2=User(id=2, name="Jacob", about="Jacob is a cool guy", isResturuant=False, password="password")
    u3=User(id=3, name="Tea Station", about="Tea Station is a cool resturuant", isResturuant=True, password="TeaStationPassword")

    users = [u1, u2, u3]

    for user in users:
        try:
            user.create()
        except IntegrityError:
            db.session.remove()
            print(f"User already exists {user.uid}")