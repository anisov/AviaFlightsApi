from flask import Blueprint
from app.main.handlers import flights_routes

bp = Blueprint("main", __name__)
bp.add_url_rule(
    '/routes/', view_func=flights_routes.SearchRoutes.as_view('search_routes')
)
bp.add_url_rule(
    '/diff_request/',
    view_func=flights_routes.DiffRoutes.as_view('diff_request')
)
