""" database dependencies to support sqliteDB examples """
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


class Resturuant(db.Model):
    __tablename__ = 'Resturuants'
    id=db.Column(db.Integer, primary_key=True)
    _rid = db.Column(db.String, unique=True, nullable=False)
    _name = db.Column(db.String, unique=False, nullable=False)
    _pfp = db.Column(db.String, unique=False, nullable=True)
    _about = db.Column(db.String, unique=False, nullable=True)
    _menu = db.Column(db.String, unique=False, nullable=True)

    def __init__(self, id, name, pfp="", about="", menu=""):
        self._rid = id
        self._name = name
        self._pfp = pfp
        self._about = about
        self._menu = menu
    
    @property
    def rid(self):
        return self._rid
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
    def menu(self):
        return self._menu
    
    @rid.setter
    def rid(self, rid):
        self._rid = rid
    @name.setter
    def name(self, name):
        self._name = name
    @pfp.setter
    def pfp(self, pfp):
        self._pfp = pfp
    @about.setter
    def about(self, about):
        self._about = about
    @menu.setter
    def menu(self, menu):
        self._menu = menu
    
    ### UTILITIES ###
    def is_rid(self, rid):
        return self._rid == rid
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
            "rid": self.rid,
            "name": self.name,
            "pfp": self.pfp,
            "about": self.about,
            "menu": self.menu,
        }
    ### READ ###

    ### UPDATE ###
    def update(self, name="", pfp="", about="", password="", menu=""):
            """only updates values with length"""
            if len(name) > 0:
                self.name = name
            if len(pfp) > 0:
                self.pfp = pfp
            if len(about) > 0:
                self.about = about
            if len(password) > 0:
                self.set_password(password)
            if len(menu) > 0:
                self.menu = menu
            db.session.commit()
            return self
    ### UPDATE ###

    ### DELETE ###
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None
    ### DELETE ###

def initResturuants():
    db.create_all()
    u1=Resturuant(id=3, name="Tea Station", about="Tea Station is a cool resturuant", menu='{"itemName":{"picture":"base64==","description":"testdescription","ingredients":"ing1, ing2, ing3, ing4"}}')

    resturuants = [u1]

    for resturuant in resturuants:
        try:
            resturuant.create()
        except IntegrityError:
            db.session.remove()
            print(f"Resturuant already exists {resturuant.rid}")