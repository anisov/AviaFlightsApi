from flask import Blueprint
from app.errors.handlers import exceptions


bp = Blueprint('errors', __name__)

bp.app_errorhandler(exceptions.ApiException)(exceptions.handle_invalid_usage)
