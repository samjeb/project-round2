from flask import Blueprint, request, jsonify, url_for
from models import User, Organisation, Member, db
from utils.jwt_handler import generate_jwt_token
from utils.email_utils import send_invite_email

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    organisation_name = data.get('organisation_name')
    organisation_details = data.get('organisation_details')

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'User already exists'}), 400

    new_user = User(email=email)
    new_user.set_password(password)

    new_organisation = Organisation(name=organisation_name, details=organisation_details)
    db.session.add(new_organisation)
    db.session.commit()

    new_user.organisation_id = new_organisation.id
    db.session.add(new_user)
    db.session.commit()

    new_member = Member(user_id=new_user.id, organisation_id=new_organisation.id, role='owner')
    db.session.add(new_member)
    db.session.commit()

    # Generate an invite link (could be a tokenized link to an invite page)
    invite_link = url_for('auth.invite', _external=True)

    # Send the invite email
    send_invite_email(email, invite_link)

    return jsonify({'message': 'User created successfully, invite email sent'}), 201


from utils.email_utils import send_login_alert

@auth_bp.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token, refresh_token = generate_jwt_token(user.id)

    # Send login alert email
    send_login_alert(email)

    return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200


from utils.email_utils import send_password_update_alert

@auth_bp.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')
    new_password = data.get('new_password')

    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    user.set_password(new_password)
    db.session.commit()


    send_password_update_alert(email)

    return jsonify({'message': 'Password updated successfully, alert email sent'}), 200
