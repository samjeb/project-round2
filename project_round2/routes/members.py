from flask import Blueprint, request, jsonify
from models import Member, db

members_bp = Blueprint('members', __name__)

@members_bp.route('/update_member_role', methods=['PUT'])
def update_member_role():
    data = request.get_json()
    member_id = data.get('member_id')
    new_role = data.get('new_role')

    member = Member.query.get(member_id)
    if member is None:
        return jsonify({'error': 'Member not found'}), 404

    member.role = new_role
    db.session.commit()

    return jsonify({'message': 'Member role updated successfully'}), 200
