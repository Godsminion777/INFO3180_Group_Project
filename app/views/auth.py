from flask import Blueprint, request, jsonify, session
from app import db
from app.models import User, Profile
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    required =['email', 'username', 'password', 'first_name', 'last_name', 'age', 'gender', 'looking_for']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
        
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already taken'}), 409
    
    password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    user = User( #create user first to get user_id for profile
        email=data['email'],
        username=data['username'],
        password_hash=password_hash.decode('utf-8')
    )
    db.session.add(user)
    db.session.commit()

    profile = Profile(
        user_id=user.id,
        first_name=data['first_name'],
        last_name=data['last_name'],
        age=data['age'],
        gender=data['gender'],
        looking_for=data['looking_for'],
        bio=data.get('bio', ''),
        location=data.get('location', ''),
        occupation=data.get('occupation', ''),
        relationship_goal=data.get('relationship_goal', '')
    )
    db.session.add(profile)
    db.session.commit()

    return jsonify({'message': 'User registered successfully', 'user': user.to_dict()}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user.password_hash.encode('utf-8')):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    session['user_id'] = user.id #store user session for authentication
    session.permanent = True #make session permanent
    return jsonify({'message': 'Login successful', 'user': user.to_dict()}), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear() #clear user session
    return jsonify({'message': 'Logout successful'}), 200

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'user': user.to_dict()}), 200