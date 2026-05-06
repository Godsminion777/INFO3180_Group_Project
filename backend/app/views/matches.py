from flask import Blueprint, request, jsonify, session
from app import db
from app.models import User, Profile, Match
from app.views.utils import login_required

matches_bp = Blueprint('matches', __name__)

@matches_bp.route('/action', methods=['POST'])
@login_required
def create_match():
    data = request.get_json()
    required_fields = ['receiver_id', 'action']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    sender_id = session['user_id']
    receiver_id = data['receiver_id']
    action = data['action']

    if sender_id == receiver_id:
        return jsonify({'error': 'Cannot match with yourself'}), 400
    
    if action not in ['like', 'dislike', 'superlike']:
        return jsonify({'error': 'Invalid action'}), 400
    
    existing_match = Match.query.filter_by(sender_id=sender_id, receiver_id=receiver_id).first()
    if existing_match:
        existing_match.action = action
        db.session.commit()
        return jsonify({'message': 'Match updated successfully', 'match': existing_match.to_dict()}), 200
    
    new_match = Match(sender_id=sender_id, receiver_id=receiver_id, action=action)
    db.session.add(new_match)
    
    reciprocal_match = Match.query.filter_by(sender_id=receiver_id, receiver_id=sender_id).first()
    if reciprocal_match and reciprocal_match.action in ['like', 'superlike'] and action in ['like', 'superlike']:
        new_match.is_mutual = True
        reciprocal_match.is_mutual = True
        db.session.commit()
        return jsonify({'message': 'It\'s a match!', 'match': new_match.to_dict()}), 201
    
    db.session.commit()
    return jsonify({'message': 'Match created successfully', 'match': new_match.to_dict()}), 201

@matches_bp.route('', methods=['GET'])
@login_required
def get_mutual_matches():
    user_id = session['user_id']
    mutual_matches = Match.query.filter_by(is_mutual=True, sender_id=user_id).all()
    return jsonify({'matches': [match.to_dict() for match in mutual_matches]}), 200

@matches_bp.route('/potential', methods=['GET'])
@login_required
def get_potential_matches():
    #Get profiles the user hasn't acted on yet, scored by compatibility
    user_id = session['user_id']
    current_user = db.session.get(User, user_id)

    if not current_user.profile:
        return jsonify({'error': 'Complete your profile first'}), 400

    current_profile = current_user.profile

    # Get IDs the user has already acted on
    acted_on = db.session.query(Match.receiver_id).filter_by(sender_id=user_id).all()
    acted_ids = [r[0] for r in acted_on] + [user_id]  # exclude self too

    # Get all public profiles not yet acted on
    candidates = Profile.query.filter(
        Profile.is_public == True,
        Profile.user_id.notin_(acted_ids)
    ).all()

    # Score each candidate
    results = []
    for candidate in candidates:
        score = 0

        # Age range match
        if current_profile.preferred_age_min <= candidate.age <= current_profile.preferred_age_max:
            score += 30

        # Shared interests
        current_interests = {i.name for i in current_profile.interests}
        candidate_interests = {i.name for i in candidate.interests}
        shared = current_interests & candidate_interests
        score += len(shared) * 10

        # Gender preference match
        if current_profile.looking_for == 'any' or current_profile.looking_for == candidate.gender:
            score += 20

        # Same location
        if current_profile.location and candidate.location:
            if current_profile.location.lower() == candidate.location.lower():
                score += 20

        results.append({
            'profile': candidate.to_dict(),
            'match_score': score
        })

    # Sort by score descending
    results.sort(key=lambda x: x['match_score'], reverse=True)

    return jsonify({'potential_matches': results}), 200