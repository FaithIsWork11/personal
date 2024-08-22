"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Blueprint, request, jsonify, url_for, redirect, render_template,send_from_directory
import logging
from api.models import db, UserAccount, Contact, Photo,Profile, Like, Message
from api.utils import generate_sitemap, APIException
from flask_cors import CORS, cross_origin
import json
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies, unset_jwt_cookies
from werkzeug.utils import secure_filename
import os
import re

logging.basicConfig(level=logging.DEBUG)
#import requests

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api, supports_credentials=True)


CORS(api, resources={r"api/*": {"origins": "http://localhost:3001"}})

# Define the path where profile pictures will be stored
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    allowed_extensions = {'jpg', 'jpeg', 'png', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

@api.route('/user', methods=['POST'])
@cross_origin()  
def create_user():
    email = request.form.get('email')
    password = request.form.get('password')
    dog_name = request.form.get('dog_name')
    owner_name = request.form.get('owner_name')
    dog_age = request.form.get('dog_age')
    location = request.form.get('location')
    breed = request.form.get('breed')
    dog_sex = request.form.get('dog_sex')
    bio = request.form.get('bio')
    traits = request.form.get('traits')
    profile_picture = request.files.get('profile_picture')
    
    profile_picture_filename = None
    if profile_picture:
        profile_picture_filename = secure_filename(profile_picture.filename)
        profile_picture.save(os.path.join(UPLOAD_FOLDER, profile_picture_filename))
    
    userAccount = UserAccount(
        email=email,
        password=password,  # Ideally, you should hash this password before saving
        dog_name=dog_name,
        owner_name=owner_name,
        dog_age=dog_age,
        location=location,
        breed=breed,
        dog_sex=dog_sex,
        bio=bio,
        traits=traits,
        profile_picture=profile_picture_filename
    )
    userAccount.set_password(password)

    db.session.add(userAccount)
    db.session.commit()
    
    response_body = {
        "result": userAccount.serialize()
    }

    return jsonify(response_body), 200





@api.route('/contact', methods=['GET'])
@cross_origin()
def get_contacts():
    contacts = Contact.query.all()
    serialized_contacts = [contact.serialize() for contact in contacts]
    return jsonify(serialized_contacts), 200

@api.route('/contact', methods=['POST'])
@cross_origin()
def contact():
    data = request.get_json()

    if not re.match(r'^[A-Za-z\s]+$', data['name']):
        return jsonify({"error": "Name must contain only alphabetic characters"}), 400

    if '@' not in data['email']:
        return jsonify({"error": "Invalid email address"}), 400

    if data.get('phone') and not re.match(r'^\d{10,15}$', data['phone']):
        return jsonify({"error": "Phone number must contain 10-15 digits"}), 400

    if len(data['subject']) < 5:
        return jsonify({"error": "Subject must be at least 5 characters long"}), 400
    if len(data['message']) < 10:
        return jsonify({"error": "Message must be at least 10 characters long"}), 400

    new_contact = Contact(
        name=data['name'],
        email=data['email'],
        phone=data.get('phone'),
        subject=data['subject'],
        message=data['message']
    )

    db.session.add(new_contact)
    db.session.commit()

    return jsonify({"message": "Contact information saved!"}), 201



@api.route("/token", methods=["POST"])
def create_token():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = UserAccount.query.filter_by(email=email).first()
    if user and user.password == password:
        access_token = create_access_token(identity=user.email)
        response = jsonify({ "access_token": access_token })
        set_access_cookies(response, access_token)
        return response
    else:
        return jsonify({"msg": "Bad email or password"}), 401

@api.route('/private', methods=['GET'])
@jwt_required()
def private_hello():
    user_id = get_jwt_identity()
    userAccount = UserAccount.query.get(user_id)
    response_body = {
        "section": "Private",
        "message": "Logged in as " + str(userAccount.email)
    }
    return jsonify(response_body), 200



# Other route definitions...

@api.route('/form')
def serve_form():
    return render_template('form.html')

@api.route('/search_user', methods=['GET'])
@cross_origin()
def search_user():
    # Retrieve form data from the query parameters
    owner_name = request.args.get('owner_name')
    email = request.args.get('useremail')

    # Log the search parameters
    logging.debug(f"Searching for owner_name: {owner_name}, email: {email}")

    # Start building the query
    query = db.session.query(UserAccount)
    
    if owner_name:
        query = query.filter(UserAccount.owner_name == owner_name)
    if email:
        query = query.filter(UserAccount.email == email)
    
    # Get the first user that matches the criteria
    user = query.first()
    
    # Log the query result
    logging.debug(f"Query result: {user}")
    
    if user:
        # Generate URL for the profile picture if it exists
        profile_pic_url = None
        if user.profile_picture:
            profile_pic_url = url_for('serve_uploads', filename=user.profile_picture, _external=True)

        # Serialize the user data if found
        user_data = {
            'owner_name': user.owner_name,
            'dog_name': user.dog_name,
            'email': user.email,
            'profile_pic': profile_pic_url
        }
        response = {
            'result': user_data,
            'message': 'User found!'
        }
    else:
        # Return a message if no user is found
        response = {
            'result': None,
            'message': 'User does not exist'
        }
    
    # Log the final response
    logging.debug(f"Response: {response}")
    
    return jsonify(response)

@api.route('/profile/<int:profile_id>', methods=['GET'])
@cross_origin()
def get_profile(profile_id):
    profile = Profile.query.get(profile_id)
    
    if not profile:
        return jsonify({"error": "Profile not found"}), 404
    
    return jsonify(profile.serialize()), 200

@api.route('/profile', methods=['POST'])
@cross_origin()
def create_profile():
    data = request.json
    user_id = data.get('user_id')
    full_name = data.get('full_name')
    location = data.get('location')
    bio = data.get('bio')
    profile_picture = data.get('profile_picture', None)
    
    profile = Profile(
        user_id=user_id,
        full_name=full_name,
        location=location,
        bio=bio,
        profile_picture=profile_picture
    )

    db.session.add(profile)
    db.session.commit()

    return jsonify(profile.serialize()), 201

@api.route('/profile/<int:profile_id>', methods=['PUT'])
@cross_origin()
def update_profile(profile_id):
    data = request.json
    profile = Profile.query.get(profile_id)
    
    if not profile:
        return jsonify({"error": "Profile not found"}), 404
    
    profile.full_name = data.get('full_name', profile.full_name)
    profile.location = data.get('location', profile.location)
    profile.bio = data.get('bio', profile.bio)
    profile.profile_picture = data.get('profile_picture', profile.profile_picture)

    db.session.commit()

    return jsonify(profile.serialize()), 200

@api.route('/profile/<int:profile_id>', methods=['DELETE'])
@cross_origin()
def delete_profile(profile_id):
    profile = Profile.query.get(profile_id)
    
    if not profile:
        return jsonify({"error": "Profile not found"}), 404
    
    try:
        # Remove the profile picture file if it exists
        if profile.profile_picture:
            photo_path = os.path.join(UPLOAD_FOLDER, profile.profile_picture)
            if os.path.exists(photo_path):
                os.remove(photo_path)
        
        db.session.delete(profile)
        db.session.commit()

        return jsonify({"message": "Profile deleted successfully"}), 200
    except Exception as e:
        logging.error(f"Error deleting profile: {e}")
        return jsonify({"error": "Failed to delete the profile"}), 500


# Route to serve uploaded profile pictures
@api.route('/uploads/<filename>')
def serve_uploads(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
@api.route('/users', methods=['GET'])
def get_users():
    users = UserAccount.query.all()
    response_body = {
        "users": [user.serialize() for user in users]
    }
    return jsonify(response_body), 200

@api.route('/user', methods=['DELETE'])
@jwt_required()
def delete_user():
    user_id = get_jwt_identity()
    userAccount = UserAccount.query.get(user_id)
    
    if userAccount:
        try:
            db.session.delete(userAccount)
            db.session.commit()
            response = jsonify({"msg": "User account deleted"})
            unset_jwt_cookies(response)
            return response, 200
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting user: {e}")  # Print error to server log
            return jsonify({"msg": "Error deleting account", "error": str(e)}), 500
    return jsonify({"msg": "User not found"}), 404

@api.route('/user/email', methods=['POST'])
@jwt_required()
def update_email():
    user_id = get_jwt_identity()
    userAccount = UserAccount.query.get(user_id)
    if userAccount:
        data = request.json  # Expect JSON body
        new_email = data.get('newEmail')
        if new_email:
            userAccount.email = new_email
            db.session.commit()
            return jsonify({"msg": "Email updated", "user": userAccount.serialize()}), 200
        return jsonify({"msg": "No new email provided"}), 400
    return jsonify({"msg": "User not found"}), 404

@api.route('/user/password', methods=['POST'])
@jwt_required()
def update_password():
    user_id = get_jwt_identity()
    userAccount = UserAccount.query.get(user_id)
    if userAccount:
        data = request.json  # Expect JSON body
        current_password = data.get('currentPassword')
        new_password = data.get('newPassword')
        if userAccount.check_password(current_password):
            if new_password:
                userAccount.set_password(new_password)
                db.session.commit()
                return jsonify({"msg": "Password updated", "user": userAccount.serialize()}), 200
            return jsonify({"msg": "No new password provided"}), 400
        return jsonify({"msg": "Current password is incorrect"}), 401
    return jsonify({"msg": "User not found"}), 404

@api.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"message": "logout successful"})
    unset_jwt_cookies(response)
    return response

@api.route("/userChat", methods=['POST'])
def create_user_chat():
    name = request.json.get("name", None)
    resp = requests.post("https://api.chatengine.io/users",
                        headers={"PRIVATE-KEY": "your_private_key"},
                        data={
                            "username": name,
                            "first_name": name,
                            "last_name": ' ',
                            "secret": "123456"
                        })
    return jsonify(resp.json())

@api.route("/privateChat", methods=['PUT'])
def create_private_chat():
    name = request.json.get("name", None)
    guest = request.json.get("guest", None)
    resp = requests.put("https://api.chatengine.io/chats",
                        headers={"Project-ID": "your_project_id",
                                 "User-Name" : name,
                                 "User-Secret" : "123456"},
                        data={
                            "usernames": [guest],
                            "is_direct_chat": True
                        })
    return jsonify(resp.json())
