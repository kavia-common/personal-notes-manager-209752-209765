from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from marshmallow import Schema, fields, validate

from ..models import db, User

blp = Blueprint(
    "Auth",
    "auth",
    url_prefix="/api/auth",
    description="User authentication and session management routes",
)


class SignupSchema(Schema):
    email = fields.Email(required=True, description="User email")
    password = fields.String(required=True, validate=validate.Length(min=8), description="Password (min 8 chars)")


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class UserResponseSchema(Schema):
    id = fields.Integer()
    email = fields.Email()
    created_at = fields.String()


class TokenResponseSchema(Schema):
    access_token = fields.String(description="JWT access token")


@blp.route("/signup")
class Signup(MethodView):
    """Create a new user account."""

    @blp.response(201, UserResponseSchema)
    @blp.arguments(SignupSchema, location="json")
    def post(self, data):
        """
        summary: User signup
        description: Create a new user with a unique email and hashed password.
        responses:
          201:
            description: User created
          400:
            description: Validation error or duplicate email
        """
        email = data["email"].strip().lower()
        password = data["password"]

        if User.query.filter_by(email=email).first():
            abort(400, message="Email is already registered.")

        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user.to_dict()


@blp.route("/login")
class Login(MethodView):
    """Authenticate a user and obtain JWT."""

    @blp.response(200, TokenResponseSchema)
    @blp.arguments(LoginSchema, location="json")
    def post(self, data):
        """
        summary: User login
        description: Authenticate with email and password to receive a JWT access token.
        responses:
          200:
            description: JWT token returned
          401:
            description: Invalid credentials
        """
        email = data["email"].strip().lower()
        password = data["password"]

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            abort(401, message="Invalid email or password.")

        token = create_access_token(identity=str(user.id))
        return {"access_token": token}


@blp.route("/me")
class Me(MethodView):
    """Return current authenticated user info."""

    @jwt_required()
    @blp.response(200, UserResponseSchema)
    def get(self):
        """
        summary: Get current user
        description: Return the profile of the authenticated user using the JWT token.
        responses:
          200:
            description: User details
          401:
            description: Unauthorized
        """
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id)) if user_id is not None else None
        if not user:
            abort(401, message="Unauthorized.")
        return user.to_dict()
