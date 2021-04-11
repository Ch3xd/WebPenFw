from App.ext import db


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(16))
    cookie = db.Column(db.String(2300))