from datetime import datetime
from typing import Dict, Any

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# SQLAlchemy instance (initialized in app factory)
db = SQLAlchemy()


class TimestampMixin:
    """Mixin to add created_at and updated_at timestamps."""
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class User(TimestampMixin, db.Model):
    """User model with secure password hashing."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    notes = db.relationship("Note", backref="user", lazy=True, cascade="all, delete-orphan")

    # PUBLIC_INTERFACE
    def set_password(self, password: str) -> None:
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)

    # PUBLIC_INTERFACE
    def check_password(self, password: str) -> bool:
        """Verify a plaintext password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    # PUBLIC_INTERFACE
    def to_dict(self) -> Dict[str, Any]:
        """Serialize user without sensitive fields."""
        return {
            "id": self.id,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Note(TimestampMixin, db.Model):
    """Note model owned by a User."""
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=True)

    # PUBLIC_INTERFACE
    def to_dict(self) -> Dict[str, Any]:
        """Serialize a note to a dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "content": self.content or "",
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
