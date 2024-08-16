from flask import Blueprint, request, jsonify
from models import User, Organisation, Member, db

organisation_bp = Blueprint('organisation', __name__)

@organisation_bp.route('/invite_member', methods=['POST'])
def invite_member():
    data = request.get_json()
    email = data.get('email')
    organisation_id = data.get('organisation_id')
    role = data.get('role')

    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({'error': 'User does not exist'}), 404

    new_member = Member(user_id=user.id, organisation_id=organisation_id, role=role)
    db.session.add(new_member)
    db.session.commit()

    return jsonify({'message': 'Member invited successfully'}), 201

@organisation_bp.route('/delete_member', methods=['DELETE'])
def delete_member():
    data = request.get_json()
    member_id = data.get('member_id')

    member = Member.query.get(member_id)
    if member is None:
        return jsonify({'error': 'Member not found'}), 404

    db.session.delete(member)
    db.session.commit()

    return jsonify({'message': 'Member deleted successfully'}), 200
