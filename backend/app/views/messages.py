from flask import Blueprint, request, jsonify, session
from app import db
from app.models import User, Message, Match
from app.views.utils import login_required

messages_bp = Blueprint('messages', __name__)

def are_mutual_matches(user1_id, user2_id):
    match1 = Match.query.filter_by(sender_id=user1_id, receiver_id=user2_id, is_mutual=True).first()
    match2 = Match.query.filter_by(sender_id=user2_id, receiver_id=user1_id, is_mutual=True).first()
    return match1 and match2

@messages_bp.route('', methods=['POST'])
@login_required
def send_message():
    data = request.get_json()
    required_fields = ['receiver_id', 'content']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    sender_id = session['user_id']
    receiver_id = data['receiver_id']
    content = data['content']

    if sender_id == receiver_id:
        return jsonify({'error': 'Cannot send message to yourself'}), 400
    
    if not are_mutual_matches(sender_id, receiver_id):
        return jsonify({'error': 'You can only message mutual matches'}), 403
    
    new_message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content)
    db.session.add(new_message)
    db.session.commit()
    return jsonify({'message': 'Message sent successfully', 'data': new_message.to_dict()}), 201

@messages_bp.route('/<int:other_user_id>', methods=['GET'])
@login_required
def get_conversation(other_user_id):
    user_id = session['user_id']
    if not are_mutual_matches(user_id, other_user_id):
        return jsonify({'error': 'You can only view conversations with mutual matches'}), 403
    
    messages = Message.query.filter(
        ((Message.sender_id == user_id) & (Message.receiver_id == other_user_id)) |
        ((Message.sender_id == other_user_id) & (Message.receiver_id == user_id))
    ).order_by(Message.created_at).all()

    return jsonify({'messages': [message.to_dict() for message in messages]}), 200

@messages_bp.route('/conversations', methods=['GET'])
@login_required
def get_conversations():
    user_id = session['user_id']

    sent = db.session.query(Message.receiver_id).filter_by(sender_id=user_id).distinct()
    received = db.session.query(Message.sender_id).filter_by(receiver_id=user_id).distinct()

    other_ids = set([r[0] for r in sent] + [r[0] for r in received])

    conversations = []
    for other_id in other_ids:
        other_user = db.session.get(User, other_id)
        if not other_user:
            continue

        last_message = Message.query.filter(
            ((Message.sender_id == user_id) & (Message.receiver_id == other_id)) |
            ((Message.sender_id == other_id) & (Message.receiver_id == user_id))
        ).order_by(Message.created_at.desc()).first()

        conversations.append({
            'user': other_user.to_dict(),
            'profile': other_user.profile.to_dict() if other_user.profile else None,
            'last_message': last_message.to_dict() if last_message else None
        })

    return jsonify({'conversations': conversations}), 200