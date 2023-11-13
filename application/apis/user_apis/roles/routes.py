# application/apis/user_apis/roles/routes.py
from .. import user_apis_blueprint
from .... import db
from ....models.user_models.models import Roles
from flask import make_response, request, jsonify, Response
from flask_login import current_user

import uuid
import base64

from flask_cors import cross_origin

import gc

from ....utils import AppMessageException, get_wib_date, set_attr, get_default_list_param, exception_handler, success_handler

@user_apis_blueprint.route('/roles', methods=['GET'])
@cross_origin()
def getdata_roles():
    try:
        if not current_user.is_authenticated:
            return make_response(jsonify(exception_handler('not logged in', 401)), 401)
        
        attr = set_attr(request.args.get('attr'))

        id = request.args.get('id')
        try:
            int(id)
        except:
            raise AppMessageException('please provide correct id')

        known_roles = Roles.query.filter_by(id=id).first()
        if not known_roles:
            raise AppMessageException('invalid roles id: data not found')
        if not known_roles.rowstatus:
            raise AppMessageException('data with given id has been deleted')
        
        results = {
            'data': known_roles.to_json(attr=['id', 'name'] if not attr else attr)
        }
        return make_response(jsonify(success_handler(results)), 200)
    except Exception as e:
        return make_response(jsonify(exception_handler(e)), 500)

@user_apis_blueprint.route('/roles', methods=['POST', 'PUT'])
@cross_origin()
def saveupdate_roles():
    try:
        # if not current_user.is_authenticated:
        #     return make_response(jsonify(exception_handler('not logged in', 401)), 401)

        if not request.is_json:
            raise AppMessageException('please provide json data')
        
        data = request.get_json()

        name = data.get('name')

        if not name:
            raise AppMessageException('please input: name (text mandatory)')
        
        id = data.get('id')

        if id:  # update kalo ngirim id
            known_roles = Roles.query.filter_by(id=id).first()
            if known_roles:
                pass
            else:
                raise AppMessageException('invalid roles id: data not found')
        else:   # create
            known_roles = Roles.query.filter_by(name=name).first()
            if known_roles:
                raise AppMessageException('roles with given name {} already exists'.format(name))
            
            known_roles = Roles()
            known_roles.rowstatus = 1
            known_roles.created_by = current_user.username
            known_roles.created_date = get_wib_date()

        known_roles.name = name

        known_roles.modified_by = current_user.username
        known_roles.modified_date = get_wib_date()

        db.session.add(known_roles)
        db.session.commit()

        return make_response(jsonify(success_handler({'data': known_roles.to_json(attr=['id', 'name'])})), 200)
    except Exception as e:
        return make_response(jsonify(exception_handler(e)), 500)

@user_apis_blueprint.route('/roles', methods=['DELETE'])
@cross_origin()
def delete_roles():
    try:
        if not (current_user.is_authenticated and current_user.is_admin):
            return make_response(jsonify(exception_handler('not logged in', 401)), 401)

        if not request.is_json:
            raise AppMessageException('please provide json data')

        data = request.get_json()

        id = data.get('id')

        known_roles = Roles.query.filter_by(id=id).first()
        if not known_roles:
            raise AppMessageException('invalid roles id: data not found')
        if not known_roles.rowstatus:
            raise AppMessageException('data with given id has been deleted')
        known_roles.rowstatus = 0
        known_roles.modified_by = current_user.username
        known_roles.modified_date = get_wib_date()

        db.session.add(known_roles)
        db.session.commit()
        
        return make_response(jsonify(success_handler({'data': {}})), 200)
    except Exception as e:
        return make_response(jsonify(exception_handler(e)), 500)

@user_apis_blueprint.route('/roles/list', methods=['GET'])
@cross_origin()
def listdata_roles():
    try:
        if not (current_user.is_authenticated):
            return make_response(jsonify(exception_handler('not logged in', 401)), 401)
        
        attr = set_attr(request.args.get('attr'))
        param = get_default_list_param(request.args, nullify_size=True)

        filter_by = []
        if param.get('filter_by_col') and param.get('filter_by_text'):
            for col, text in zip(param.get('filter_by_col').split(','), param.get('filter_by_text').split(',')):
                if col.lower().strip() == 'name' and text:
                    filter_by.append(Roles.name == text)
                    continue

        order_by = []
        if param.get('order_by_col') and param.get('order_by_type'):
            for order_col, order_type in zip(param.get('order_by_col').split(','), param.get('order_by_type').split(',')):
                if order_col.lower().strip() == 'id':
                    order_by.append('user_roles.id ' + ' ' + order_type)
                    continue
                if order_col.lower().strip() == 'code':
                    order_by.append('user_roles.name ' + ' ' + order_type)
                    continue

        order_by = ','.join(order_by)

        items = []
        filters = (
            db.or_(
                db.func.ifnull(Roles.name, '').like('%{}%'.format(param.get('keywords')) if param.get('search_by') == '' or param.get('search_by') == None or param.get('search_by') == 'name' else '\x00'),
            ),
            Roles.rowstatus == 1,
            db.and_(*filter_by)
        )

        data = Roles.query.filter(*filters).order_by(db.desc(Roles.created_date) if not order_by else db.text(order_by))
        total_records = data.count()

        for row in data.paginate(param.get('page_index'), param.get('page_size'), False).items:
            items.append(row.to_json(attr=['id', 'name'] if not attr else attr))
        
        results = {
            'data': items,
            'total_records': total_records
        }
        return make_response(jsonify(success_handler(results)), 200)
    except Exception as e:
        return make_response(jsonify(exception_handler(e, default_data=[])), 500)