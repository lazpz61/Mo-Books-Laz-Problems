from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://uawixqerjzcvxm:42fa8cf6bc4355ad730d9c8e897fa13d91299ab79591903dad18a65faa9331df@ec2-3-91-127-228.compute-1.amazonaws.com:5432/dao4f5kujs1tas"

db = SQLAlchemy(app)
ma = Marshmallow(app)
heroku = Heroku(app)
CORS(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullible=False)
    password = db.Column(db.String, nullible=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserSchema(ma.Schema):
    class Meta:
        fields = (id, username)

user_schema = UserSchema()
multiple_user_schema = UserSchema(many=True)


if __name__ == "__main__":
    app.run(debug = True)