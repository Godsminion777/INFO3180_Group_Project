from flask import Blueprint, current_app, request, jsonify, session
from app import db
from app.models import User, Profile, Interest
import os
from werkzeug.utils import secure_filename

profiles_bp = Blueprint('profiles', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@profiles_bp.route('', methods=['GET'])
@login_required
def get_all_profiles():
    profiles = Profile.query.filter_by(is_public=True).all()
    return jsonify({'profiles': [profile.to_dict() for profile in profiles]}), 200

@profiles_bp.route('/<int:profile_id>', methods=['GET'])
@login_required
def get_profile(profile_id):
    profile = Profile.query.get(profile_id)
    if not profile:
        return jsonify({'error': 'Profile not found'}), 404
    if not profile.is_public and profile.user_id != session['user_id']:
        return jsonify({'error': 'Profile is private'}), 403
    return jsonify({'profile': profile.to_dict()}), 200

@profiles_bp.route('/<int:profile_id>', methods=['PUT'])
@login_required
def update_profile(profile_id):
    profile = Profile.query.get(profile_id)
    if not profile:
        return jsonify({'error': 'Profile not found'}), 404
    if profile.user_id != session['user_id']: #if not the owner then you cant update
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    for key in ['first_name', 'last_name', 'age', 'bio', 'gender', 'looking_for',
                'location', 'latitude', 'longitude', 'preferred_age_min',
                'preferred_age_max', 'distance_preference_km', 'relationship_goal',
                'occupation', 'education', 'is_public']:
        if key in data:
            setattr(profile, key, data[key])

    if 'interests' in data:
        interest_obj = []
        for name in data['interests']:
            name = name.strip().lower()
            interest = Interest.query.filter_by(name=name).first()
            if not interest:
                interest = Interest(name=name)
                db.session.add(interest)
            interest_obj.append(interest)
        profile.interests = interest_obj

    db.session.commit()
    return jsonify({'message': 'Profile updated successfully', 'profile': profile.to_dict()}), 200

@profiles_bp.route('/<int:profile_id>/photo', methods=['POST'])
@login_required
def upload_photo(profile_id):
    profile = Profile.query.get(profile_id)
    if not profile:
        return jsonify({'error': 'Profile not found'}), 404
    if profile.user_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if 'photo' not in request.files:
        return jsonify({'error': 'No photo uploaded'}), 400
    
    file = request.files['photo']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(f"user_{profile.user_id}_{file.filename}")
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        profile.photo_url = f'/uploads/{filename}'
        db.session.commit()
        return jsonify({'message': 'Photo uploaded successfully', 'photo_url': profile.photo_url}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400
