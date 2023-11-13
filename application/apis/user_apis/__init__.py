# application/apis/user_apis/__init__.py
from flask import Blueprint, Response, request
from ...utils import get_swagger_yaml

user_apis_blueprint = Blueprint('user_apis', __name__)

from .account import routes
from .roles import routes

# restx
from flask_restx import Api
from .account import api as docs_account
from .roles import api as docs_roles

authorizations = {
    'api_key': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api_extension = Api(
    user_apis_blueprint,
    authorizations=authorizations,
    title='Users APIs',
    version='1.0',
    doc='/',
    security='api_key',
)

@user_apis_blueprint.route('/specs.yaml', methods=['GET'])
def swagger_specs():
    return Response(
        get_swagger_yaml(
            str(request.base_url).replace('/specs.yaml', '')
        ), 
        mimetype='text/yaml'
    )

api_extension.add_namespace(docs_account)
api_extension.add_namespace(docs_roles)