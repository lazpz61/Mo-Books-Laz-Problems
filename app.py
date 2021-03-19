from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://uawixqerjzcvxm:42fa8cf6bc4355ad730d9c8e897fa13d91299ab79591903dad18a65faa9331df@ec2-3-91-127-228.compute-1.amazonaws.com:5432/dao4f5kujs1tas"

db = SQLAlchemy(app)
ma = Marshmallow(app)
heroku = Heroku(app)
CORS(app)
bcrypt = Bcrypt(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username")

user_schema = UserSchema()
multiple_user_schema = UserSchema(many=True)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    review = db.Column(db.String, nullable=False)
    recommend = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def __init__(self, title, author, review, recommend):
        self.title = title
        self.author = author
        self.review = review
        self.recommend = recommend
        self.user_id = user_id

class BookSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "author", "review", "recommend", "user_id")


@app.route("/user/add", methods=["POST"])
def add_user():
    if request.content_type != "application/json":
        return jsonify("Error: Data must be sent as JSON.")

    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")

    existing_user = db.session.query(User).filter(User.username == username).first()
    if existing_user is not None:
        return jsonify("Error: Username taken.")

    encrypted_password = bcrypt.generate_password_hash(password).decode("utf-8")

    record = User(username, encrypted_password)
    db.session.add(record)
    db.session.commit()

    return jsonify("User added")

@app.route("/user/verification", methods=["POST"])
def verify_user():
    if request.content_type != "application/json":
        return jsonify("Error verifying user")

    post_data = request.get_json()
    user_password = post_data.get("password")

    password_hash = db.session.query(User.password).filter(User.username == post_data.get("username")).first()
    if password_hash is None:
        return jsonify("User NOT Verified")

    valid_password = bcrypt.check_password_hash(password_hash[0], user_password)
    if valid_password:
        return jsonify("User Verified")

    return jsonify("User NOT Verified")

@app.route("/user/get", methods=["GET"])
def get_all_users():
    all_users = db.session.query(User).all()
    return jsonify(multiple_user_schema.dump(all_users))


if __name__ == "__main__":
    app.run(debug = True)