# application/apis/user_apis/roles/__init__.py
from flask import request
from flask_restx import Namespace, Resource, fields, reqparse
from ..account import roles_model, blank_model, status_model, blank_results_object_model, blank_results_list_model
from ..account import blank_arta_object_model, blank_arta_list_model, blank_response_object_model, blank_response_list_model

api = Namespace('roles', 'user roles related endpoints.')

post_parser = api.parser()
post_parser.add_argument("name", type=str, required=True, help="name, sample: 'Marketing'", location="json")

put_parser = api.parser()
put_parser.add_argument("id", type=int, required=True, help="id, sample: 1", location="json")
put_parser.add_argument("name", type=str, required=True, help="name, sample: 'Marketing'", location="json")

delete_parser = api.parser()
delete_parser.add_argument("id", type=int, required=True, help="identifier", location="json")

# roles results
results_object_model = api.model('ResObjRoles', {
    'data': fields.Nested(roles_model),
})
results_list_model = api.model('ResLisRoles', {
    'data': fields.List(fields.Nested(roles_model)),
    'total_records': fields.Integer,
})
arta_object_model = api.model('ArtaObjRoles', {
    'status': fields.Nested(status_model, skip_none=True),
    'results': fields.Nested(results_object_model, skip_none=True),
})
arta_list_model = api.model('ArtaLisRoles', {
    'status': fields.Nested(status_model, skip_none=True),
    'results': fields.Nested(results_list_model, skip_none=True),
})
response_object_model = api.model('RespObjRoles', {
    'arta': fields.Nested(arta_object_model, skip_none=True),
})
response_list_model = api.model('RespLisRoles', {
    'arta': fields.Nested(arta_list_model, skip_none=True),
})


@api.route('')
class Roles(Resource):

    @api.response(200, 'Success', model=response_object_model)
    @api.response(401, 'Unauthorized, please provide api key', model=blank_response_object_model)
    @api.response(500, 'Internal Server error, refer to the error code and messages status.', model=blank_response_object_model)
    @api.param('id', 'identifier')
    def get(self):
        pass

    @api.response(200, 'Success', model=response_object_model)
    @api.response(401, 'Unauthorized, please provide api key', model=blank_response_object_model)
    @api.response(500, 'Internal Server error, refer to the error code and messages status.', model=blank_response_object_model)
    @api.doc(parser=post_parser)
    def post(self):
        pass
    
    @api.response(200, 'Success', model=response_object_model)
    @api.response(401, 'Unauthorized, please provide api key', model=blank_response_object_model)
    @api.response(500, 'Internal Server error, refer to the error code and messages status.', model=blank_response_object_model)
    @api.doc(parser=put_parser)
    def put(self):
        pass
    
    @api.response(200, 'Success', model=blank_response_object_model)
    @api.response(401, 'Unauthorized, please provide api key', model=blank_response_object_model)
    @api.response(500, 'Internal Server error, refer to the error code and messages status.', model=blank_response_object_model)
    @api.doc(parser=delete_parser)
    def delete(self):
        pass

@api.route('/list')
class ListRoles(Resource):
    @api.response(200, 'Success', model=response_list_model)
    @api.response(401, 'Unauthorized, please provide api key', model=blank_response_list_model)
    @api.response(500, 'Internal Server error, refer to the error code and messages status.', model=blank_response_list_model)
    @api.param('page_index', 'page index')
    @api.param('page_size', 'page size')
    @api.param('search_by', 'search by')
    @api.param('keywords', 'keywords')
    @api.param('filter_by_col', 'available filter: name')
    @api.param('filter_by_text', 'text for every filter')
    @api.param('order_by_col', 'available order: id, name')
    @api.param('order_by_type', 'sample type: asc, asc')
    def get(self):
        pass