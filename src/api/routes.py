"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException, generate_token
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }
    return jsonify(response_body), 200


# ============= AUTHENTICATION ENDPOINTS =============

@api.route('/signup', methods=['POST'])
def signup():
    """Register a new user"""
    try:
        # Get data from request
        body = request.get_json()
        
        if not body:
            raise APIException("Request body is required", 400)
        
        email = body.get('email')
        password = body.get('password')
        
        # Validate required fields
        if not email:
            raise APIException("Email is required", 400)
        if not password:
            raise APIException("Password is required", 400)
        
        # Check if user already exists
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            raise APIException("User already exists with this email", 400)
        
        # Create new user
        new_user = User()
        new_user.email = email
        new_user.set_password(password)  # Hash the password
        new_user.is_active = True
        
        # Save to database
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            "message": "User created successfully",
            "user": new_user.serialize()
        }), 201
        
    except APIException as e:
        return jsonify({"error": e.message}), e.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route('/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    try:
        # Get data from request
        body = request.get_json()
        
        if not body:
            raise APIException("Request body is required", 400)
        
        email = body.get('email')
        password = body.get('password')
        
        # Validate required fields
        if not email:
            raise APIException("Email is required", 400)
        if not password:
            raise APIException("Password is required", 400)
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if not user:
            raise APIException("Invalid email or password", 401)
        
        # Check password
        if not user.check_password(password):
            raise APIException("Invalid email or password", 401)
        
        # Check if user is active
        if not user.is_active:
            raise APIException("User account is inactive", 401)
        
        # Generate JWT token
        access_token = generate_token(user.id)
        
        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "user": user.serialize()
        }), 200
        
    except APIException as e:
        return jsonify({"error": e.message}), e.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route('/token/validate', methods=['GET'])
@jwt_required()
def validate_token():
    """Validate if the token is valid and return user info"""
    try:
        # Get user id from token
        current_user_id = get_jwt_identity()
        
        # Get user from database
        user = User.query.get(current_user_id)
        
        if not user:
            raise APIException("User not found", 404)
        
        if not user.is_active:
            raise APIException("User account is inactive", 401)
        
        return jsonify({
            "message": "Token is valid",
            "user": user.serialize()
        }), 200
        
    except APIException as e:
        return jsonify({"error": e.message}), e.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    """Get current user info (requires authentication)"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            raise APIException("User not found", 404)
        
        return jsonify(user.serialize()), 200
        
    except APIException as e:
        return jsonify({"error": e.message}), e.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500