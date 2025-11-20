from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields, validate

from ..models import db, Note

blp = Blueprint(
    "Notes",
    "notes",
    url_prefix="/api/notes",
    description="CRUD endpoints for managing personal notes",
)


class NoteCreateSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1, max=255))
    content = fields.String(required=False, allow_none=True)


class NoteUpdateSchema(Schema):
    title = fields.String(required=False, validate=validate.Length(min=1, max=255))
    content = fields.String(required=False, allow_none=True)


class NoteResponseSchema(Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    title = fields.String()
    content = fields.String(allow_none=True)
    created_at = fields.String()
    updated_at = fields.String()


@blp.route("")
class NotesList(MethodView):
    """List or create notes for the authenticated user."""

    @jwt_required()
    @blp.response(200, NoteResponseSchema(many=True))
    def get(self):
        """
        summary: List notes
        description: Retrieve all notes for the current authenticated user.
        responses:
          200:
            description: List of notes
        """
        user_id = int(get_jwt_identity())
        notes = Note.query.filter_by(user_id=user_id).order_by(Note.created_at.desc()).all()
        return [n.to_dict() for n in notes]

    @jwt_required()
    @blp.arguments(NoteCreateSchema, location="json")
    @blp.response(201, NoteResponseSchema)
    def post(self, data):
        """
        summary: Create note
        description: Create a new note for the current authenticated user.
        responses:
          201:
            description: Note created
          400:
            description: Validation error
        """
        user_id = int(get_jwt_identity())
        note = Note(user_id=user_id, title=data["title"].strip(), content=data.get("content") or "")
        db.session.add(note)
        db.session.commit()
        return note.to_dict()


@blp.route("/<int:note_id>")
class NoteDetail(MethodView):
    """Retrieve, update, or delete a specific note owned by the user."""

    @jwt_required()
    @blp.response(200, NoteResponseSchema)
    def get(self, note_id: int):
        """
        summary: Get note by ID
        description: Retrieve a single note by ID for the authenticated user.
        responses:
          200:
            description: Note details
          404:
            description: Note not found
        """
        user_id = int(get_jwt_identity())
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        if not note:
            abort(404, message="Note not found.")
        return note.to_dict()

    @jwt_required()
    @blp.arguments(NoteUpdateSchema, location="json")
    @blp.response(200, NoteResponseSchema)
    def put(self, data, note_id: int):
        """
        summary: Update note
        description: Update title and/or content of a note owned by the authenticated user.
        responses:
          200:
            description: Updated note
          404:
            description: Note not found
        """
        user_id = int(get_jwt_identity())
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        if not note:
            abort(404, message="Note not found.")

        if "title" in data and data["title"] is not None:
            note.title = data["title"].strip()
        if "content" in data:
            note.content = data.get("content") or ""
        db.session.commit()
        return note.to_dict()

    @jwt_required()
    @blp.response(204)
    def delete(self, note_id: int):
        """
        summary: Delete note
        description: Delete a note owned by the authenticated user.
        responses:
          204:
            description: Note deleted
          404:
            description: Note not found
        """
        user_id = int(get_jwt_identity())
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        if not note:
            abort(404, message="Note not found.")
        db.session.delete(note)
        db.session.commit()
        return ""
