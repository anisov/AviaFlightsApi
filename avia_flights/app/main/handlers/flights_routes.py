from flask import request, jsonify
from flask.views import MethodView

from app.errors.handlers.exceptions import ApiException
from app.main.utils.helpers import convert_to_dict
from app.main.storage.parser import CreateStorage


class SearchRoutes(MethodView):
    def get(self):
        """
        /api/v1/routes/?source=DXB&destination=BKK&sort=fastest
        /api/v1/routes/?source=DXB&destination=BKK&sort=fastest&limit=3
        :return: json
        """
        get_params = request.args
        source = get_params.get("source")
        destination = get_params.get("destination")
        sort = get_params.get("sort")
        limit = get_params.get("limit", default=1, type=int)
        if not source or not destination:
            raise ApiException(
                message=u"Укажите верные параметры запроса", status_code=400
            )
        storage = CreateStorage.execute()
        routes = storage.get_route(
            source, destination, sort_attr=sort, limit=limit
        )
        data = convert_to_dict(routes)
        return jsonify(data)


class DiffRoutes(MethodView):
    def get(self):
        """
        /api/v1/routes/diff_routes
        :return: json
        """
        storage = CreateStorage.execute()
        routes = storage.get_diff()
        data = convert_to_dict(routes)
        return jsonify(data)


class DiffRoutes(MethodView):
    def get(self):
        """
        /api/v1/diff_request/
        :return: json
        """
        storage = CreateStorage.execute()
        routes = storage.get_diff()
        data = convert_to_dict(routes)
        return jsonify(data)
