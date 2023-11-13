# application/apis/master_apis/__init__.py
from flask import Blueprint, Response, request
from ...utils import get_swagger_yaml

master_apis_blueprint = Blueprint('master_apis', __name__)

from .faq import routes

# restx
from flask_restx import Api
# from application.apis.master_apis.cities import api as docs_cities


authorizations = {
    'api_key': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api_extension = Api(
    master_apis_blueprint,
    authorizations=authorizations,
    title='Masters APIs',
    version='1.0',
    doc='/',
    security='api_key',
)

@master_apis_blueprint.route('/specs.yaml', methods=['GET'])
def swagger_specs():
    return Response(
        get_swagger_yaml(
            str(request.base_url).replace('/specs.yaml', '')
        ), 
        mimetype='text/yaml'
    )

# api_extension.add_namespace(docs_cities)