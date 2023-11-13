# application/apis/user_apis/account/__init__.py
from flask import request
from flask_restx import Namespace, Resource, fields, reqparse
import werkzeug

api = Namespace('account', 'user account related endpoints.')

register_parser = api.parser()
register_parser.add_argument('first_name', type=str, required=True, help="first name, sample: John", location="form")
register_parser.add_argument('last_name', type=str, required=False, help="last name, sample: Doe", location="form")
register_parser.add_argument('email', type=str, required=True, help="email, sample: john_doe@mail.com", location="form")
# register_parser.add_argument('country_code', type=str, required=True, help="country_code, sample: ID", location="form")
# register_parser.add_argument('city', type=str, required=True, help="city, sample: Jakarta", location="form")
# register_parser.add_argument('phone_number', type=str, required=True, help="phone number, sample: 67329176310, max 16 length", location="form")
# register_parser.add_argument('company_name', type=str, required=True, help="company name, sample: John Inc", location="form")
# register_parser.add_argument('company_position', type=str, required=True, help="company position, sample: CEO", location="form")
# register_parser.add_argument('proof_file', type=werkzeug.datastructures.FileStorage, help="company proof files", required=True, location="files")
# register_parser.add_argument('linkedin_url', type=str, required=False, help="linkedin url, sample: https://linkedin.com", location="form")
# register_parser.add_argument('facebook_url', type=str, required=False, help="facebook url, sample: https://facebook.com", location="form")

uid_parser = api.parser()
uid_parser.add_argument('uid', type=str, required=True, help="account uid, sample: 7abdfa91-f7f5-40b3-ba98-446df477a337", location="json")

reject_parser = api.parser()
reject_parser.add_argument('uid', type=str, required=True, help="account uid, sample: 7abdfa91-f7f5-40b3-ba98-446df477a337", location="json")
reject_parser.add_argument('reason', type=str, required=True, help="reason uid, sample: <ul>test</ul>", location="json")

token_parser = api.parser()
token_parser.add_argument('token', type=str, required=True, help="account token, sample: -HUE_8GA50kHYkstUkmiCieDhW8amdoXaMns4pG3EvqdM93UzRMCbP5khe6_sWIWb7hz3-nCwMLdzuy6I1pRwg", location="json")
token_parser.add_argument('password', type=str, required=True, help="account password", location="json")

login_parser = api.parser()
login_parser.add_argument('username', type=str, required=True, help="account username, sample: john_doe, john_doe@mail.com", location="json")
login_parser.add_argument('password', type=str, required=True, help="account password, sample: P@ssw0rd", location="json")

put_parser = api.parser()
put_parser.add_argument('uid', type=str, required=False, help="account uid, sample: 7abdfa91-f7f5-40b3-ba98-446df477a337", location="form")
put_parser.add_argument('first_name', type=str, required=False, help="first name, sample: John", location="form")
put_parser.add_argument('last_name', type=str, required=False, help="last name, sample: Doe", location="form")
put_parser.add_argument('email', type=str, required=False, help="email, sample: john_doe@mail.com", location="form")
put_parser.add_argument('country_code', type=str, required=True, help="country_code, sample: ID", location="form")
put_parser.add_argument('city', type=str, required=True, help="city, sample: Jakarta", location="form")
put_parser.add_argument('phone_number', type=str, required=True, help="phone number, sample: 67329176310, max 16 length", location="form")
put_parser.add_argument('company_name', type=str, required=False, help="company name, sample: John Inc", location="form")
put_parser.add_argument('company_position', type=str, required=False, help="company position, sample: CEO", location="form")
put_parser.add_argument('proof_file', type=werkzeug.datastructures.FileStorage, help="company proof files", required=False, location="files")
put_parser.add_argument('linkedin_url', type=str, required=False, help="linkedin url, sample: https://linkedin.com", location="form")
put_parser.add_argument('facebook_url', type=str, required=False, help="facebook url, sample: https://facebook.com", location="form")

post_parser = api.parser()
post_parser.add_argument('username', type=str, required=False, help="username, sample: artaa", location="json")
post_parser.add_argument('password', type=str, required=False, help="password, sample: pass@word1", location="json")
post_parser.add_argument('first_name', type=str, required=False, help="first name, sample: John", location="json")
post_parser.add_argument('email', type=str, required=False, help="email, sample: john_doe@mail.com", location="json")
post_parser.add_argument('roles_id', type=int, required=True, help="roles, sample: 6", location="json")

delete_parser = api.parser()
delete_parser.add_argument("uid", type=str, required=True, help="unique identifier", location="json")

change_password_parser = api.parser()
change_password_parser.add_argument("current_password", type=str, required=True, help="current password", location="json")
change_password_parser.add_argument("password", type=str, required=True, help="new password", location="json")

roles_model = api.model('Roles', {
    'id': fields.Integer,
    'name': fields.String,
})

account_model = api.model('Account', {
    'uid': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'username': fields.String,
    'roles_id': fields.Integer,
    'roles': fields.Nested(roles_model, skip_none=True),
    'is_verified': fields.Integer,
    'country_code': fields.String,
    'city': fields.String,
    'phone_number': fields.String,
    'company_name': fields.String,
    'company_position': fields.String,
    'linkedin_url': fields.String,
    'facebook_url': fields.String,
    'rowstatus': fields.Boolean,
    'created_by': fields.String,
    'created_date': fields.DateTime(dt_format='rfc822'),
    'modified_by': fields.String,
    'modified_date': fields.DateTime(dt_format='rfc822'),
    'pp_url': fields.String,
})

access_user_model = api.model('AccessUser', {
    'account_uid': fields.String,
    'account_first_name': fields.String,
    'services_id': fields.Integer,
    'services_name': fields.String,
    'action_id': fields.Integer,
    'action_name': fields.String,
    'allow': fields.Boolean,
})

access_roles_model = api.model('AccessRoles', {
    'roles_id': fields.Integer,
    'roles_name': fields.String,
    'services_id': fields.Integer,
    'services_name': fields.String,
    'action_id': fields.Integer,
    'action_name': fields.String,
    'allow': fields.Boolean,
})

api_response_model = api.model('ApiResponse', {
    'api_key': fields.String,
    'api_key_expired': fields.DateTime(dt_format='rfc822'),
    'account': fields.Nested(account_model, skip_none=True),
})

account_reset_model = api.model('AccountReset', {
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'company_name': fields.String,
    'company_position': fields.String,
})

approve_model = api.model('Approve', {
    'token': fields.String,
})

register_model = api.model('Register', {
    'uid': fields.String,
    'username': fields.String,
})

blank_model = api.model('BlankObject', {})

status_model = api.model('ErrorStatus', {
    'message': fields.String,
    'status_code': fields.Integer,
    'error_message': fields.String,
    'error_code': fields.Integer,
})

# blank results
blank_results_object_model = api.model('BlankResultsObject', {
    'data': fields.Nested(blank_model),
})
blank_results_list_model = api.model('BlankResultsList', {
    'data': fields.List(fields.Nested(blank_model)),
    'total_records': fields.Integer,
})

blank_arta_object_model = api.model('BlankArtaObject', {
    'status': fields.Nested(status_model, skip_none=True),
    'results': fields.Nested(blank_results_object_model, skip_none=True),
})
blank_arta_list_model = api.model('BlankArtaList', {
    'status': fields.Nested(status_model, skip_none=True),
    'results': fields.Nested(blank_results_list_model, skip_none=True),
})

blank_response_object_model = api.model('BlankResponseObject', {
    'express21': fields.Nested(blank_arta_object_model, skip_none=True),
})
blank_response_list_model = api.model('BlankResponseList', {
    'express21': fields.Nested(blank_arta_list_model, skip_none=True),
})

# account results
results_object_model = api.model('ResObjAccount', {
    'data': fields.Nested(account_model),
})
results_list_model = api.model('ResLisAccount', {
    'data': fields.List(fields.Nested(account_model)),
    'total_records': fields.Integer,
})
arta_object_model = api.model('ArtaObjAccount', {
    'status': fields.Nested(status_model, skip_none=True),
    'results': fields.Nested(results_object_model, skip_none=True),
})
arta_list_model = api.model('ArtaLisAccount', {
    'status': fields.Nested(status_model, skip_none=True),
    'results': fields.Nested(results_list_model, skip_none=True),
})
response_object_model = api.model('RespObjAccount', {
    'express21': fields.Nested(arta_object_model, skip_none=True),
})
response_list_model = api.model('RespLisAccount', {
    'express21': fields.Nested(arta_list_model, skip_none=True),
})

# api response results
apiresponse_results_model = api.model('ApiResponseResults', {
    'data': fields.Nested(api_response_model),
})
apiresponse_arta_model = api.model('ApiResponseArta', {
    'status': fields.Nested(status_model, skip_none=True),
    'results': fields.Nested(apiresponse_results_model, skip_none=True),
})
apiresponse_response_model = api.model('ApiResponseResponse', {
    'express21': fields.Nested(apiresponse_arta_model, skip_none=True),
})

# account reset results
accountreset_results_model = api.model('AccountResetResults', {
    'data': fields.Nested(account_reset_model),
})
accountreset_arta_model = api.model('AccountResetArta', {
    'status': fields.Nested(status_model, skip_none=True),
    'results': fields.Nested(accountreset_results_model, skip_none=True),
})
accountreset_response_model = api.model('AccountResetResponse', {
    'express21': fields.Nested(accountreset_arta_model, skip_none=True),
})

# approve results
approve_results_model = api.model('ApproveResults', {
    'data': fields.Nested(approve_model),
})
approve_arta_model = api.model('ApproveArta', {
    'status': fields.Nested(status_model, skip_none=True),
    'results': fields.Nested(approve_results_model, skip_none=True),
})
approve_response_model = api.model('ApproveResponse', {
    'express21': fields.Nested(approve_arta_model, skip_none=True),
})

# register results
register_results_model = api.model('RegisterResults', {
    'data': fields.Nested(register_model),
})
register_arta_model = api.model('RegisterArta', {
    'status': fields.Nested(status_model, skip_none=True),
    'results': fields.Nested(register_results_model, skip_none=True),
})
register_response_model = api.model('RegisterResponse', {
    'express21': fields.Nested(register_arta_model, skip_none=True),
})

@api.route('')
class Account(Resource):

    @api.response(200, 'Success', model=response_object_model)
    @api.response(401, 'Unauthorized, please provide api key', model=blank_response_object_model)
    @api.response(500, 'Internal Server error, refer to the error code and messages status.', model=blank_response_object_model)
    @api.param('uid', 'unique identifier')
    @api.param('attr', 'sample attr: first_name, last_name, phone_no, company_name')
    def get(self):
        pass
    
    @api.response(200, 'Success', model=register_response_model)
    @api.response(401, 'Unauthorized, please provide api key', model=blank_response_object_model)
    @api.response(500, 'Internal Server error, refer to the error code and messages status.', model=blank_response_object_model)
    @api.doc(parser=post_parser)
    def post(self):
        pass
    
    @api.response(200, 'Success', model=blank_response_object_model)
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
class ListAccount(Resource):
    @api.response(200, 'Success', model=response_list_model)
    @api.response(401, 'Unauthorized, please provide api key', model=blank_response_list_model)
    @api.response(500, 'Internal Server error, refer to the error code and messages status.', model=blank_response_list_model)
    @api.param('page_index', 'page index')
    @api.param('page_size', 'page size')
    @api.param('search_by', 'search by')
    @api.param('keywords', 'keywords')
    @api.param('filter_by_col', 'available filter: name, code, slug, is_verified, account_type')
    @api.param('filter_by_text', 'text for every filter, sample: a, b, c, d, e')
    @api.param('order_by_col', 'available order: name, code, slug, description')
    @api.param('order_by_type', 'sample type: asc, asc, desc, desc')
    @api.param('attr', 'sample attr: first_name, last_name, phone_no, company_name')
    def get(self):
        pass

@api.route('/register')
class RegisterAccount(Resource):
    @api.response(200, 'Success', model=register_response_model)
    @api.response(401, 'Unauthorized, please provide api key', model=blank_response_object_model)
    @api.response(500, 'Internal Server error, refer to the error code and messages status.', model=blank_response_object_model)
    @api.doc(parser=register_parser)
    def post(self):
        pass

@api.route('/approve')
class ApproveAccount(Resource):
    @api.response(200, 'Success', model=blank_response_object_model)
    @api.response(401, 'Unauthorized, please provide api key', model=blank_response_object_model)
    @api.response(500, 'Internal Server error, refer to the error code and messages status.', model=blank_response_object_model)
    @api.doc(parser=uid_parser)
    def post(self):
        pass

@api.route('/reject')
class ApproveAccount(Resource):
    @api.response(200, 'Success', model=blank_response_object_model)
    @api.response(401, 'Unauthorized, please provide api key', model=blank_response_object_model)
    @api.response(500, 'Internal Server error, refer to the error code and messages status.', model=blank_response_object_model)
    @api.doc(parser=reject_parser)
    def post(self):
        pass

@api.route('/reset')
class ResetAccount(Resource):
    @api.response(200, 'Success', model=blank_response_object_model)
    @api.response(401, 'Unauthorized, please provide api key', model=blank_response_object_model)
    @api.response(500, 'Internal Server error, refer to the error code and messages status.', model=blank_response_object_model)
    @api.doc(parser=token_parser)
    def post(self):
        pass
    
    @api.response(200, 'Success', model=accountreset_response_model)
    @api.response(401, 'Unauthorized, please provide api key', model=blank_response_object_model)
    @api.response(500, 'Internal Server error, refer to the error code and messages status.', model=blank_response_object_model)
    @api.param('token', 'account token, sample: -HUE_8GA50kHYkstUkmiCieDhW8amdoXaMns4pG3EvqdM93UzRMCbP5khe6_sWIWb7hz3-nCwMLdzuy6I1pRwg')
    def get(self):
        pass

@api.route('/login')
class LoginAccount(Resource):
    @api.response(200, 'Success', model=apiresponse_response_model)
    @api.response(401, 'Unauthorized, please provide api key', model=blank_response_object_model)
    @api.response(500, 'Internal Server error, refer to the error code and messages status.', model=blank_response_object_model)
    @api.doc(parser=login_parser)
    def post(self):
        pass

@api.route('/logout')
class LogoutAccount(Resource):
    @api.response(200, 'Success', model=blank_response_object_model)
    @api.response(401, 'Unauthorized, please provide api key', model=blank_response_object_model)
    @api.response(500, 'Internal Server error, refer to the error code and messages status.', model=blank_response_object_model)
    def post(self):
        pass

@api.route('/change-password')
class ChangePasswordAccount(Resource):
    @api.response(200, 'Success', model=blank_response_object_model)
    @api.response(401, 'Unauthorized, please provide api key', model=blank_response_object_model)
    @api.response(500, 'Internal Server error, refer to the error code and messages status.', model=blank_response_object_model)
    @api.doc(parser=change_password_parser)
    def post(self):
        pass