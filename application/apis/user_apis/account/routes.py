# application/apis/user_apis/account/routes.py
from .. import user_apis_blueprint
from .... import db, login_manager
from ....models.user_models.models import Account, Roles
from flask import make_response, request, jsonify
from flask_login import current_user, login_user, logout_user

from passlib.hash import sha256_crypt

import uuid

from flask_cors import cross_origin

import gc

from ....utils import AppMessageException, get_wib_date, set_attr, get_default_list_param, exception_handler, success_handler
# from ....utils import get_bucket_name, gcs_upload, check_file_image, check_file_pdf, get_token
from ....utils import send_mailgun_message



SERVICE_SLUG = 'user_account'

@login_manager.user_loader
def load_user(user_id):
    return Account.query.filter_by(id=user_id).first()


@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        user = Account.query.filter_by(api_key=api_key).first()
        if user:
            if user.api_key_expires > get_wib_date():
                return user
    return None

# def access_user_addroles_access(known_account):
#     known_access_roles = []
    
#     known_access_roles = AccessRoles.query.filter_by(roles_id=known_account.roles_id,allow=True).all()

#     access_user_lists = []
    
#     if known_access_roles:
#         for access_roles in known_access_roles:
#             access_user = AccessUser.query.filter_by(account_id=known_account.id, web_menu_id=access_roles.web_menu_id, action_id=access_roles.action_id).first()
#             if access_user:
#                 access_user.allow = True if known_account.rowstatus else False
#             else:
#                 access_user = AccessUser()
#                 access_user.account_id = 0 # dummy
#                 access_user.web_menu_id = access_roles.web_menu_id
#                 access_user.action_id = access_roles.action_id
#                 access_user.allow = True if known_account.rowstatus else False
            
#             access_user_lists.append(access_user)
    
#     return access_user_lists

@user_apis_blueprint.route('/account', methods=['GET'])
@cross_origin()
def getdata_account():
    try:
        
        if not (current_user.is_authenticated):
            return make_response(jsonify(exception_handler('not logged in', 401)), 401)
        
        attr = set_attr(request.args.get('attr'))

        if not current_user.is_admin:
            attr = None

        uid = request.args.get('uid')
        if not uid:
            raise AppMessageException('please provide uid')

        known_account = Account.query.filter_by(uid=uid).first()
        if not known_account:
            raise AppMessageException('invalid account uid: data not found')
        if not known_account.rowstatus:
            raise AppMessageException('data with given uid has been deleted')
        
        results = {
            'data': known_account.to_json(attr=[] if not attr else attr)
        }
        return make_response(jsonify(success_handler(results)), 200)
    except Exception as e:
        return make_response(jsonify(exception_handler(e)), 500)

@user_apis_blueprint.route('/account/register', methods=['POST'])
@cross_origin()
def register_account():
    try:
        # data = request.form

        if not request.is_json:
            raise AppMessageException('please provide json data')
        
        form = request.get_json()


        first_name = form.get('first_name')
        print(first_name)
        last_name = form.get('last_name')
        print(last_name)
        email = form.get('email')
        roles_id = form.get('roles_id')

        # country_code = data.get('country_code')
        # city = data.get('city')

        # phone_number = data.get('phone_number')
        # company_name = data.get('company_name')
        # company_position = data.get('company_position')
        # proof_file = request.files.get('proof_file')

        # linkedin_url = data.get('linkedin_url')
        # facebook_url = data.get('facebook_url')

        if not first_name:
            raise AppMessageException('please input: first_name (text mandatory)')
        if not email:
            raise AppMessageException('please input: email (text mandatory)')
        if '@' not in email:
            raise AppMessageException('invalid format input: email')
        
        # if not country_code:
        #     raise AppMessageException('please input: country_code (string mandatory)')
        # if not city:
        #     raise AppMessageException('please input: city (string mandatory)')
        
        # if not phone_number:
        #     raise AppMessageException('please input: phone_number (text mandatory)')
        # if len(phone_number) > 16:
        #     raise AppMessageException('invalid format input: phone number max length is 16.')
        # if not company_name:
        #     raise AppMessageException('please input: company_name (text mandatory)')
        # if not company_position:
        #     raise AppMessageException('please input: company_position (text mandatory)')
        # if not proof_file:
        #     raise AppMessageException('please provide company proof files (proof_file), we accept jpg/jpeg/pdf formats')
        
        username = first_name.split('@')[0]
        # password = sha256_crypt.hash(str(uuid.uuid4()))
        password = sha256_crypt.hash(str(username))

        
        # Cek email is exists
        known_account = Account.query.filter_by(email=email, rowstatus=1).first()
        if known_account:
            raise AppMessageException('email has been registered')
        
        known_account = Account.query.filter(Account.username.op('rlike')('^{}[0-9][0-9]*[0-9]*[0-9]*$'.format(username)))
        total_account = known_account.count()
        if known_account:
            username = '{}{}{}'.format(username, '-', total_account+1)
        
        known_account = Account()
        known_account.uid = str(uuid.uuid4())

        known_account.first_name = first_name
        known_account.last_name = last_name
        known_account.email = email

        known_account.username = username
        known_account.password = password

        known_account.is_active = 1

        # known_account.country_code = country_code
        # known_account.city = city

        # known_account.phone_number = phone_number
        # known_account.company_name = company_name
        # known_account.company_position = company_position

        # known_account.linkedin_url = linkedin_url
        # known_account.facebook_url = facebook_url

        known_account.roles_id = roles_id # client
        
        known_account.customer_uid = ''
        known_account.customer_code = ''
        known_account.rowstatus = 1
        known_account.created_by = known_account.uid
        known_account.created_date = get_wib_date()

        # proof_file_type = check_file_image(proof_file)
        # if not proof_file_type:
        #     proof_file_type = check_file_pdf(proof_file)
        # if not proof_file_type:
        #     raise AppMessageException('invalid proof file format, please provide jpg/jpeg/pdf file format. ')
        # proof_file.seek(0)
        # uploaded = gcs_upload('OPH5lKVympUwUM6V2vYn/', '{}/{}'.format(known_account.uid, proof_file.filename), proof_file, proof_file_type)
        # known_supporting_documents = f_saveupdate_supporting_documents({
        #     'reference_uid': known_account.uid,
        #     'reference_type': 'user account company proof',
        #     'name': proof_file.filename,
        #     'content_type': proof_file_type,
        #     'public_url': uploaded.get('public_url'),
        #     'created_by': known_account.username
        # })

        db.session.add(known_account)
        # db.session.add(known_supporting_documents)
        db.session.commit()

        return make_response(jsonify(success_handler({'data': known_account.to_json(attr=['uid', 'username'])})), 200)
    except Exception as e:
        return make_response(jsonify(exception_handler(e)), 500)
    

@user_apis_blueprint.route('/account', methods=['POST'])
@cross_origin()
def saveupdate_account():
    try:
        if not current_user.is_authenticated:
            return make_response(jsonify(exception_handler('not logged in', 401)), 401)
        
        if not current_user.is_admin:
            return make_response(jsonify(exception_handler('you dont have permission to do this', 401)), 401)
        
        if not request.is_json:
            raise AppMessageException('please provide json data')
        
        data = request.get_json()

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')

        roles_id = data.get('roles_id')

        if not first_name:
            raise AppMessageException('please input: first_name (text mandatory)')
        if not email:
            raise AppMessageException('please input: email (text mandatory)')
        if '@' not in email:
            raise AppMessageException('invalid format input: email')
        
        if not roles_id:
            raise AppMessageException('please input: roles_id (int mandatory)')
        known_roles = Roles.query.filter_by(id=roles_id).first()
        if not known_roles:
            raise AppMessageException('roles data not found: invalid roles_id')
        if not known_roles.rowstatus:
            raise AppMessageException('roles with given id {} has been deleted'.format(known_roles.id))
        
        uid = data.get('uid')
        if not uid: #bikin
            username = email.split('@')[0]
            # password = sha256_crypt.hash(str(uuid.uuid4()))
            
            password = sha256_crypt.hash(str(username))
            
            known_account = Account.query.filter_by(email=email, rowstatus=1).first()
            if known_account:
                raise AppMessageException('email has been registered')
            
            known_account = Account.query.filter(Account.username.op('rlike')('^{}[0-9][0-9]*[0-9]*[0-9]*$'.format(username)))
            total_account = known_account.count()
            if total_account:
                username = '{}{}{}'.format(username, '-', total_account+1)
            
            known_account = Account()
            known_account.uid = str(uuid.uuid4())

            known_account.username = username
            known_account.password = password

            known_account.is_active = 1

            known_account.customer_uid = ''
            known_account.customer_code = ''
        else: #update
            known_account = Account.query.filter_by(uid=uid).first()
            if not known_account.rowstatus:
                raise AppMessageException('account has been deleted, cannot be modified')
            if not known_account.is_active:
                raise AppMessageException('account has been deactivated, cannot be modified')
            
        known_account.first_name = first_name
        known_account.last_name = last_name
        known_account.email = email

        known_account.roles_id = roles_id

        known_account.rowstatus = 1
        known_account.created_by = current_user.username
        known_account.created_date = get_wib_date()


        db.session.add(known_account)
        db.session.flush()
        db.session.refresh(known_account)

        db.session.commit()

        return make_response(jsonify(success_handler({'data': known_account.to_json(attr=['uid', 'username'])})), 200)
    except Exception as e:
        return make_response(jsonify(exception_handler(e)), 500)
    
##################### TRIAL #######################
# @user_apis_blueprint.route('/accounttest', methods=['POST'])
# @cross_origin()
def register_account_customer(customer_data):
    try:
        # if not current_user.is_authenticated:
        #     return make_response(jsonify(exception_handler('not logged in', 401)), 401)
        
        # if not current_user.is_admin:
        #     return make_response(jsonify(exception_handler('you dont have permission to do this', 401)), 401)
        
        # if not request.is_json:
        #     raise AppMessageException('please provide json data')
        
        data = customer_data

        customer_username = data.get('customer_username')
        customer_code = data.get('customer_code')
        last_name = data.get('last_name')
        email = data.get('email')
        customer_uid = data.get('customer_uid')
        customer_code = data.get('customer_code')

        # first_name = data.get('first_name')
        # last_name = data.get('last_name')
        # email = data.get('email')

        # roles_id = data.get('roles_id')

        # if not first_name:
        #     raise AppMessageException('please input: first_name (text mandatory)')
        # if not email:
        #     raise AppMessageException('please input: email (text mandatory)')
        # if '@' not in email:
        #     raise AppMessageException('invalid format input: email')
        
        # if not roles_id:
        #     raise AppMessageException('please input: roles_id (int mandatory)')
        # known_roles = Roles.query.filter_by(id=roles_id).first()
        # if not known_roles:
        #     raise AppMessageException('roles data not found: invalid roles_id')
        # if not known_roles.rowstatus:
        #     raise AppMessageException('roles with given id {} has been deleted'.format(known_roles.id))


        # username = customer_code.replace(" ","_")
        clean_customer_code = customer_code.replace(" ","_")
        # password = sha256_crypt.hash(str(username))

        # print('########################################################################################## INI GENERATED PASSNYA')
        # print(password)
        account = Account.query.filter_by(username=customer_username, rowstatus=1).first()
        if not account: #create
            known_account = Account.query.filter_by(email=email, rowstatus=1).first()
            if known_account:
                raise AppMessageException('email has been registered')

            known_account = Account.query.filter(Account.username.op('rlike')('^{}[0-9][0-9]*[0-9]*[0-9]*$'.format(clean_customer_code)))
            total_account = known_account.count()
            if known_account:
                clean_customer_code = '{}{}{}'.format(clean_customer_code, '-', total_account+1)
        
            username = clean_customer_code
            password = sha256_crypt.hash(str(username))

            known_account = Account()
            known_account.uid = str(uuid.uuid4())

            known_account.username = username
            known_account.password = password
        else: #update
            known_account = account
            if not known_account.rowstatus:
                raise AppMessageException('account has been deleted, cannot be modified')
            if not known_account.is_active:
                raise AppMessageException('account has been deactivated, cannot be modified')

        known_account.first_name = customer_code
        known_account.last_name = last_name
        known_account.email = email

        known_account.customer_uid = customer_uid
        known_account.customer_code = customer_code

        known_account.roles_id = 2 # Partner
        known_account.is_active = 1
        known_account.rowstatus = 1
        known_account.created_by = current_user.username
        known_account.created_date = get_wib_date()

        db.session.add(known_account)
        db.session.flush()
        db.session.refresh(known_account)

        db.session.commit()

        return make_response(jsonify(success_handler({'data': known_account.to_json(attr=['uid', 'username'])})), 200)
    except Exception as e:
        return make_response(jsonify(exception_handler(e)), 500)
    

# @user_apis_blueprint.route('/account', methods=['DELETE'])
# @cross_origin()
def delete_account_customer(customer_uid):
    try:
        if not (current_user.is_authenticated):
            return make_response(jsonify(exception_handler('not logged in', 401)), 401)

        if not request.is_json:
            raise AppMessageException('please provide json data')

        data = customer_uid

        customer_uid = data.get('customer_uid')

        known_account = Account.query.filter_by(customer_uid=customer_uid).first()
        if not known_account:
            raise AppMessageException('invalid account uid: data not found')
        if not known_account.rowstatus:
            raise AppMessageException('data with given id has been deleted')
        known_account.rowstatus = 0
        known_account.is_active = 0
        known_account.modified_by = current_user.username
        known_account.modified_date = get_wib_date()

        db.session.add(known_account)
        db.session.commit()
        
        return make_response(jsonify(success_handler({'data': {}})), 200)
    except Exception as e:
        return make_response(jsonify(exception_handler(e)), 500)
        
# @user_apis_blueprint.route('/account/reset', methods=['POST'])
# @cross_origin()
# def reset_account():
#     try:
#         if not request.is_json:
#             raise AppMessageException('please provide json data')
        
#         data = request.get_json()

#         token = data.get('token')
#         if not token:
#             raise AppMessageException('please provide token')
        
#         password = data.get('password')
#         if not password:
#             raise AppMessageException('please provide password')
#         if len(password) < 8:
#             raise AppMessageException('invalid format: password minimal length is 8')
        
#         password = sha256_crypt.hash(password)

#         known_account = Account.query.filter_by(id=known_token.account_id).first()
#         known_account.password = password
#         known_account.modified_by = known_account.username
#         known_account.modified_date = get_wib_date()

#         known_token.is_used = 1

#         db.session.add(known_account)
#         db.session.add(known_token)
#         db.session.commit()

#         return make_response(jsonify(success_handler({'data': {}})), 200)
#     except Exception as e:
#         return make_response(jsonify(exception_handler(e)), 500)

# @user_apis_blueprint.route('/account/reset', methods=['GET'])
# @cross_origin()
# def reset_getdata_account():
#     try:
#         attr = set_attr(request.args.get('attr'))

#         token = request.args.get('token')
#         if not token:
#             raise AppMessageException('please provide token')
#         known_token = Key.query.filter_by(key=token).first()
#         if not known_token:
#             raise AppMessageException('invalid token')
#         if not known_token.rowstatus:
#             raise AppMessageException('invalid token')
#         if known_token.is_used:
#             raise AppMessageException('invalid token: token has been used')

#         known_account = Account.query.filter_by(id=known_token.account_id).first()
        
#         results = {
#             'data': known_account.to_json(attr=['first_name', 'last_name', 'email', 'company_name', 'company_position'] if not attr else attr)
#         }
#         return make_response(jsonify(success_handler(results)), 200)
#     except Exception as e:
#         return make_response(jsonify(exception_handler(e)), 500)

@user_apis_blueprint.route('/account', methods=['PUT'])
@cross_origin()
def update_account():
    try:
        if not (current_user.is_authenticated):
            return make_response(jsonify(exception_handler('not logged in', 401)), 401)

        if not request.is_json:
            raise AppMessageException('please provide json data')
        
        data = request.get_json()

        first_name = data.get('first_name')

        uid = data.get('uid')
        if not uid:
            raise AppMessageException('please provide uid')
        
        known_account = Account.query.filter_by(uid=uid).first()
        if not known_account:
            raise AppMessageException('invalid account uid: data not found')
        
        if first_name:
            known_account.first_name = first_name
        
        known_account.modified_by = current_user.username
        known_account.modified_date = get_wib_date()

        db.session.add(known_account)
        db.commit()

        return make_response(jsonify(success_handler({'data': {}})), 200)
    except Exception as e:
        return make_response(jsonify(exception_handler(e)), 500)

@user_apis_blueprint.route('/account', methods=['DELETE'])
@cross_origin()
def delete_account():
    try:
        if not (current_user.is_authenticated):
            return make_response(jsonify(exception_handler('not logged in', 401)), 401)

        if not request.is_json:
            raise AppMessageException('please provide json data')

        data = request.get_json()

        uid = data.get('uid')

        known_account = Account.query.filter_by(uid=uid).first()
        if not known_account:
            raise AppMessageException('invalid account uid: data not found')
        if not known_account.rowstatus:
            raise AppMessageException('data with given id has been deleted')
        known_account.rowstatus = 0
        known_account.modified_by = current_user.username
        known_account.modified_date = get_wib_date()

        db.session.add(known_account)
        db.session.commit()
        
        return make_response(jsonify(success_handler({'data': {}})), 200)
    except Exception as e:
        return make_response(jsonify(exception_handler(e)), 500)

@user_apis_blueprint.route('/account/activate', methods=['POST'])
@cross_origin()
def activate_account():
    try:
        if not (current_user.is_authenticated):
            return make_response(jsonify(exception_handler('not logged in', 401)), 401)

        if not request.is_json:
            raise AppMessageException('please provide json data')

        data = request.get_json()

        uid = data.get('uid')

        known_account = Account.query.filter_by(uid=uid).first()
        if not known_account:
            raise AppMessageException('invalid account uid: data not found')
        if not known_account.rowstatus:
            raise AppMessageException('data with given id has been deleted')
        known_account.is_active = 1 if not known_account.is_active else 0
        known_account.modified_by = current_user.username
        known_account.modified_date = get_wib_date()

        db.session.add(known_account)
        db.session.commit()
        
        return make_response(jsonify(success_handler({'data': {}})), 200)
    except Exception as e:
        return make_response(jsonify(exception_handler(e)), 500)


@user_apis_blueprint.route('/account/list', methods=['GET'])
@cross_origin()
def listdata_account():
    try:
        if not current_user.is_authenticated:
            return make_response(jsonify(exception_handler('not logged in', 401)), 401)
        
        attr = set_attr(request.args.get('attr'))
        if not current_user.is_admin:
            attr = None
        # param = get_default_list_param(request.args)
        param = get_default_list_param(request.args, nullify_size=True)

        filter_by = []
        if param.get('filter_by_col') and param.get('filter_by_text'):
            for col, text in zip(param.get('filter_by_col').split(','), param.get('filter_by_text').split(',')):
                # if col.lower().strip() == 'company_name' and text:
                #     filter_by.append(Account.company_position == text)
                #     continue
                # if col.lower().strip() == 'company_position' and text:
                #     filter_by.append(Account.company_position == text)
                #     continue
                # if col.lower().strip() == 'country_code' and text:
                #     filter_by.append(Account.country_code == text)
                    # continue
                # if col.lower().strip() == 'city' and text:
                #     filter_by.append(Account.city == text)
                #     continue
                # if col.lower().strip() == 'is_verified' and text:
                #     filter_by.append(Account.is_verified == text)
                #     continue
                if col.lower().strip() == 'account_type' and text:
                    if text == 'admin':
                        filter_by.append(db.or_(
                            Account.roles_id != 6,
                            Account.is_admin == 1
                        ))
                    if text == 'client':
                        filter_by.append(Account.roles_id == 6)
                    continue

        order_by = []
        if param.get('order_by_col') and param.get('order_by_type'):
            for order_col, order_type in zip(param.get('order_by_col').split(','), param.get('order_by_type').split(',')):
                if order_col.lower().strip() == 'first_name':
                    order_by.append('user_account.first_name ' + ' ' + order_type)
                    continue
                if order_col.lower().strip() == 'last_name':
                    order_by.append('user_account.last_name ' + ' ' + order_type)
                    continue
                if order_col.lower().strip() == 'email':
                    order_by.append('user_account.email ' + ' ' + order_type)
                    continue
                # if order_col.lower().strip() == 'company_name':
                #     order_by.append('user_account.company_name ' + ' ' + order_type)
                #     continue
                # if order_col.lower().strip() == 'company_position':
                #     order_by.append('user_account.company_position ' + ' ' + order_type)
                #     continue

        order_by = ','.join(order_by)

        items = []
        filters = (
            db.or_(
                db.func.ifnull(Account.first_name, '').like('%{}%'.format(param.get('keywords')) if param.get('search_by') == '' or param.get('search_by') == None or param.get('search_by') == 'first_name' else '\x00'),
                db.func.ifnull(Account.last_name, '').like('%{}%'.format(param.get('keywords')) if param.get('search_by') == '' or param.get('search_by') == None or param.get('search_by') == 'last_name' else '\x00'),
                db.func.ifnull(Account.email, '').like('%{}%'.format(param.get('keywords')) if param.get('search_by') == '' or param.get('search_by') == None or param.get('search_by') == 'email' else '\x00'),
                # db.func.ifnull(Account.company_name, '').like('%{}%'.format(param.get('keywords')) if param.get('search_by') == '' or param.get('search_by') == None or param.get('search_by') == 'company_name' else '\x00'),
                # db.func.ifnull(Account.company_position, '').like('%{}%'.format(param.get('keywords')) if param.get('search_by') == '' or param.get('search_by') == None or param.get('search_by') == 'company_position' else '\x00'),
                # db.func.ifnull(Account.country_code, '').like('%{}%'.format(param.get('keywords')) if param.get('search_by') == '' or param.get('search_by') == None or param.get('search_by') == 'country_code' else '\x00'),
                # db.func.ifnull(Account.city, '').like('%{}%'.format(param.get('keywords')) if param.get('search_by') == '' or param.get('search_by') == None or param.get('search_by') == 'city' else '\x00'),
            ),
            Account.rowstatus == 1,
            db.and_(*filter_by)
        )

        # data = Account.query.filter(*filters).order_by(db.desc(Account.created_date) if not order_by else db.text(order_by))

        # data = ShipmentStatus.query \
        #         .join(TrackingStatus, TrackingStatus.id==ShipmentStatus.tracking_status_id, isouter=True) \
        #         .join(Branch, Branch.id==ShipmentStatus.branch_id, isouter=True) \
        #         .filter(ShipmentStatus.shipment_id==shipment_id, ShipmentStatus.rowstatus==1) \
        #         .with_entities(
        #             *[select_field[n] for n in select_field.keys()]
        #         )

        data = Account.query \
                .join(Roles, Roles.id==Account.roles_id, isouter=True) \
                .filter(*filters).order_by(db.desc(Account.created_date) if not order_by else db.text(order_by))

        total_records = data.count()

        print("THIS IS DATAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        print(data)

        for row in data.paginate(param.get('page_index'), param.get('page_size'), False).items:
            # items.append(row.to_json(attr=['uid','username', 'first_name', 'last_name', 'email','roles_id',  'is_active', 'reject_reason'] if not attr else attr))
            items.append(row.to_json(attr=[] if not attr else attr))

        results = {
            'data': items,
            'total_records': total_records
        }
        return make_response(jsonify(success_handler(results)), 200)
    except Exception as e:
        return make_response(jsonify(exception_handler(e, default_data=[])), 500)

@user_apis_blueprint.route('/account/login', methods=['POST'])
@cross_origin()
def post_login():
    try:
        if not request.is_json:
            raise AppMessageException('please provide json data')
        form = request.get_json()
        username = form.get('username')
        user = Account.query.filter_by(username=username,  is_active=True).first()
        if not user:
            user = Account.query.filter_by(email=username,  is_active=True).first()
            
        if user:
            if sha256_crypt.verify(str(form.get('password')), user.password):
                if not user.api_key or get_wib_date() > user.api_key_expires:
                    user.encode_api_key()
                db.session.commit()
                login_user(user)
                results = {
                    'data': {
                        'api_key': user.api_key,
                        'api_key_expires': user.api_key_expires.isoformat(),
                        'account': user.to_json(attr=[])
                    }
                }

                gc.collect()
                return make_response(jsonify(success_handler(results)))
            else:
                return make_response(jsonify(exception_handler('Wrong password, please provide correct password', 401)), 401)
        else:
            gc.collect()
            return make_response(jsonify(exception_handler('No Account, please register', 400)), 400)
        
        # return make_response(jsonify(exception_handler('not logged in', 401)), 401)
    except Exception as e:
        return make_response(jsonify(exception_handler(e)), 500)

@user_apis_blueprint.route('/account/logout', methods=['POST'])
@cross_origin()
def post_logout():
    if current_user.is_authenticated:
        current_user.api_key = None
        current_user.api_key_expires = None
        db.session.commit()
        logout_user()
        gc.collect()
        return make_response(jsonify(success_handler({'data': {}})))
    gc.collect()
    return make_response(jsonify(exception_handler('not logged in', 401)), 401)



@user_apis_blueprint.route('/account/change-password', methods=['POST'])
@cross_origin()
def account_change_password():
    try:
        if not current_user.is_authenticated:
            return make_response(jsonify(exception_handler('not logged in', 401)), 401)

        if not request.is_json:
            raise AppMessageException('please provide json data')
        
        data = request.get_json()
        
        current_password = data.get('current_password')
        password = data.get('new_password')
        if not password:
            raise AppMessageException('please provide password')
        if len(password) < 8:
            raise AppMessageException('invalid format: password minimal length is 8')
        if not sha256_crypt.verify(str(current_password), current_user.password):
            raise Exception('wrong password')
        
        password = sha256_crypt.hash(str(password))
        known_account = Account.query.filter_by(uid=current_user.uid).first()
        known_account.password = password
        known_account.modified_by = current_user.username
        known_account.modified_date = get_wib_date()
        db.session.add(known_account)
        db.session.commit()
        
        return make_response(jsonify(success_handler({'data': {}})), 200)
    except Exception as e:
        return make_response(jsonify(exception_handler(e)), 500)


@user_apis_blueprint.route('/account/reset-password', methods=['POST'])
@cross_origin()
def account_reset_password():
    try:
        if not current_user.is_authenticated:
            return make_response(jsonify(exception_handler('not logged in', 401)), 401)
        if current_user.roles_id != 1:
            return make_response(jsonify(exception_handler('Forbidden access', 403)), 403)

        if not request.is_json:
            raise AppMessageException('please provide json data')
        
        data = request.get_json()
        username = data.get('username')
        
        password = sha256_crypt.hash(str(username))
        known_account = Account.query.filter_by(username=username).first()
        if not known_account:
            return make_response(jsonify(exception_handler('Account not found', 400)), 400)
            
        known_account.password = password
        known_account.modified_by = current_user.username
        known_account.modified_date = get_wib_date()
        # print(known_account.username, known_account.password)
        db.session.add(known_account)
        db.session.commit()
        data = {
            'username' : known_account.username,
            'password' : username
        }
        
        return make_response(jsonify(success_handler({'data': data})), 200)
    except Exception as e:
        return make_response(jsonify(exception_handler(e)), 500)
    
    
@user_apis_blueprint.route('/account/info', methods=['GET'])
def getinfo_account():
    try:
        if not current_user.is_authenticated:
            return make_response(jsonify(exception_handler('not logged in', 401)), 401)
        
        attr = set_attr(request.args.get('attr'))

        known_account = Account.query.filter_by(username=current_user.username).first()
        
        results = {
            'data': known_account.to_json(attr=[] if not attr else attr)
        }

        
        return make_response(jsonify(success_handler(results)), 200)
    except Exception as e:
        return make_response(jsonify(exception_handler(e)), 500)