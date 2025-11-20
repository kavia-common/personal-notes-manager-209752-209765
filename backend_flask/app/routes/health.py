from flask_smorest import Blueprint
from flask.views import MethodView

blp = Blueprint("Health", "health", url_prefix="/", description="Health check route")


@blp.route("/")
class HealthCheck(MethodView):
    """Health check endpoint for uptime monitoring."""
    def get(self):
        """Return a simple health status payload."""
        return {"message": "Healthy"}
