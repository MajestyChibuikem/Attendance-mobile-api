from flask import request, Blueprint, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import(
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)

from routes.users import load_users, USERS
auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login', methods=['POST'])
def login():
    """
        method to login users and also generate a jwt key
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'username and password required'}),400
    Users = load_users()
    
    user = next((a_user for a_user in Users if a_user['username'] == username), None)
    if not user:
        return jsonify({'error':'username invalid'}), 401
    
    if not check_password_hash(user['password'],password):
        return jsonify({'error':'invalid password'}), 401
    
    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)

    return jsonify({
        'message':'login was a success',
        'access token': access_token,
        'refresh token': refresh_token
    }), 200


@auth_blueprint.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    """
        generates  new access token using a refresh token
    """
    current_user_id = get_jwt_identity()
    current_user = next((user for user in USERS if user['username'] == current_user_id), None)



    if current_user is None:
        return jsonify({'error':'user not found'}), 404
    new_access_token = create_access_token(identity=current_user['username'])
    return jsonify({'new access token':new_access_token}), 201
