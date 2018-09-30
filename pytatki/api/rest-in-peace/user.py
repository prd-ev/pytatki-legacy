from passlib.utils import unicode
from passlib.hash import sha256_crypt
from src.api.v1.auth import auth
from flask import jsonify, request, abort
from pytatki.main import APP, DB
from src.models import User

@APP.route('/api/user/<username>/', methods=["GET"])
@auth.login_required
def api_get_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        user_info = {
            "username": user.username,
            "email": user.email,
            "confirm_email": user.confirm_mail,
            "access": {
            "ban": user.ban,
            "mod": user.ban,
            "admin": user.admin,
            "superuser": user.superuser
            }
        }
        return jsonify(user_info)
    else:
        return jsonify({"data": "User doesn't exist!"})

@APP.route('/api/user/', methods=["GET"])
@auth.login_required
def api_users():
    users_json = dict()
    users = User.query.order_by(User.id.asc()).all()
    for index, user in enumerate(users):
        user_dict = {index+1: {
            "username": user.username,
            "email": user.email,
            "confirm_email": user.confirm_mail,
            "access": {
                "ban": user.ban,
                "mod": user.ban,
                "admin": user.admin,
                "superuser": user.superuser
            }
        }}
        users_json.update(user_dict)
    return jsonify(users_json)

@APP.route('/api/user/', methods=["POST"])
@APP.route('/api/user', methods=["POST"])
def api_add_user():
    json = request.get_json()
    if len(request.json['username']) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'username' in request.json and type(request.json['username']) is not unicode:
        abort(400)
    if 'password' in request.json and type(request.json['password']) is not unicode:
        abort(400)
    if 'email' in request.json and type(request.json['email']) is not unicode:
        abort(400)
    username = str(json.get('username'))
    password = sha256_crypt.encrypt(str(json.get('password')))
    email = str(json.get('email'))
    user = User(username=username, password=password, email=email)
    json_access = json.get("access")
    if json_access:
        if json_access.get("admin"):
            user.admin = json_access.get("admin")
        if json_access.get("ban"):
            user.ban = json_access.get("ban")
        if json_access.get("mod"):
            user.modderator = json_access.get("mod")
        if json_access.get("superuser"):
            user.superuser = json_access.get("superuser")
    DB.session.add(user)
    DB.session.commit()
    user = User.query.filter_by(username=username).first()
    if user:
        user_info = {
            "username": user.username,
            "email": user.email,
            "confirm_email": user.confirm_mail,
            "access": {
                "ban": user.ban,
                "mod": user.ban,
                "admin": user.admin,
                "superuser": user.superuser
            }
        }
        return jsonify(user_info)
    else:
        return jsonify({"data": "Cannot add user"})

@APP.route('/api/user/<username>/', methods=["DELETE"])
@auth.login_required
def api_delete_user(username):
    if not User.query.filter_by(username=username).first().superuser:
        if username == User.query.filter_by(username=auth.username()).first().username or User.query.filter_by(
                username=auth.username()).first().admin:
            user = User.query.filter_by(username=username).first()
            if user:
                DB.session.delete(user)
                DB.session.commit()
                return jsonify({"data": "User " + username + " deleted"})
            else:
                return jsonify({"data": "User doesn't exist"})
        else:
            return jsonify({"data": "Permission denied"})
    else:
        return jsonify({"data": "Permission denied"})