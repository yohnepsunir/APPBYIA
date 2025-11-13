from flask import Blueprint

routes = Blueprint('routes', __name__)

from .tasks import tasks_bp

__all__ = ['tasks_bp']