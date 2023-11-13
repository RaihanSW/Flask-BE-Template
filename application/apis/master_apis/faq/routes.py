# application/apis/master_apis/routes.py
from flask import jsonify, request, make_response
from flask_login import current_user
from sqlalchemy.exc import IntegrityError
from .. import master_apis_blueprint
from .... import db
from ....models.master_models.models import FAQ, FAQDetail

from flask_cors import cross_origin

import json
import random
import gc
import time

from ....utils import (
    AppMessageException,
    get_wib_date,
    set_attr,
    get_default_list_param,
    exception_handler,
    success_handler,
)

@master_apis_blueprint.route("/faq", methods=["GET"])
@cross_origin()
def list_topic():
    try:
        param = get_default_list_param(request.args, nullify_size=True)

        select_field = {
                "id": FAQ.id,
                "name": FAQ.name,
            }
        
        items = []                     
        data = (
            FAQ.query.filter(
                FAQ.rowstatus == 1,
            )
            .with_entities(*[select_field[n] for n in select_field.keys()])
            .order_by(db.asc(FAQ.id))
        )
        
        for row in data.paginate(param.get("page_index"), param.get("page_size"), False).items:
            obj = dict(zip(select_field.keys(), row))
            items.append(obj)

        results = {"data": items}
        return make_response(jsonify(success_handler(results)), 200)
    except Exception as e:
        return make_response(jsonify(exception_handler(e, default_data=[])), 500)


@master_apis_blueprint.route("/faq", methods=["POST", "PUT"])
@cross_origin()
def saveupdate_topic():
    try:
        if not (current_user.is_authenticated):
            return make_response(jsonify(exception_handler("not logged in", 401)), 401)
        if current_user.roles_id != 1:
            return make_response(jsonify(exception_handler('Forbidden access', 403)), 403)

        if not request.is_json:
            raise AppMessageException('please provide json data')

        data = request.get_json()

        topic = data.get("topic")

        if not topic:
            raise AppMessageException("please provide topic")

        topic_id = data.get("id")
        
        # check if name is already available but rowstatus 0
        available_topic = FAQ.query.filter_by(name=topic,rowstatus=0).first()
        if available_topic:
            known_faq = available_topic
            known_faq.rowstatus = 1
            known_faq.modified_by = current_user.username
            known_faq.modified_date = get_wib_date()
            db.session.add(known_faq)
            db.session.commit()
            
            results = {
                "name": known_faq.name,
                "restored_data": True
            }
            
            return make_response(
            jsonify(success_handler({"data": results})), 200
        )
            
        known_faq = FAQ.query.filter_by(id=topic_id).first() if topic_id else FAQ()
        if not known_faq:
            raise AppMessageException("invalid Topic id: data not found")
               
        known_faq.name = topic
        known_faq.modified_by = current_user.username
        known_faq.modified_date = get_wib_date()
        
        if not topic_id:
            known_faq.rowstatus = 1
            known_faq.created_by = current_user.username
            known_faq.created_date = get_wib_date()

        db.session.add(known_faq)
        db.session.commit()

        # Change FAQDetail faq_name if update is succeed
        if topic_id:
            query = FAQDetail.query.filter_by(rowstatus=1, faq_id=topic_id)
            for row in query:
                row.faq_name = known_faq.name
                row.modified_by = current_user.username
                row.modified_date = get_wib_date()
                db.session.add(row)
                db.session.commit()
        
        results = {
                "name": known_faq.name,
                "restored_data": False
            }
        
        return make_response(
            jsonify(success_handler({"data": results})), 200
        )
    except IntegrityError as e:
        duplicate_error = {
        'express21': {
            'status': {
                'message': "IntegrityError: Cannot add duplicated data",
                'status_code': 500
                },
                'results': {
                'data': {}
                }
            }
         }  
        return make_response(jsonify(duplicate_error), 500)
    except Exception as e:
        return make_response(jsonify(exception_handler(e)), 500)
    

@master_apis_blueprint.route("/faq", methods=["DELETE"])
@cross_origin()
def delete_topic():
    try:
        if not (current_user.is_authenticated):
            return make_response(jsonify(exception_handler("not logged in", 401)), 401)
        if current_user.roles_id != 1:
            return make_response(jsonify(exception_handler('Forbidden access', 403)), 403)
        
        id = request.args.get("id")
        if not id:
            raise AppMessageException("Please provide id to be deleted")

        
        known_faq = FAQ.query.filter_by(id=id).first()
        if not known_faq:
            raise AppMessageException('invalid topic id: data not found')
        if not known_faq.rowstatus:
            raise AppMessageException('data with given id has been deleted')
        known_faq.rowstatus = 0
        known_faq.modified_by = current_user.username
        known_faq.modified_date = get_wib_date()

        db.session.add(known_faq)
        db.session.commit()
        
        # cascade on delete FAQDetail connected to the FAQ
        query = FAQDetail.query.filter_by(rowstatus=1,faq_id=id)
        for row in query:
            row.rowstatus = 0
            row.modified_by = current_user.username
            row.modified_date = get_wib_date()
            db.session.add(row)
            db.session.commit()
        
        return make_response(jsonify(success_handler({'data': {}})), 200)
    except Exception as e:
        return make_response(jsonify(exception_handler(e, default_data=[])), 500)
    

@master_apis_blueprint.route("/faq_detail", methods=["GET"])
@cross_origin()
def faq_list():
    try:
        param = get_default_list_param(request.args, nullify_size=True)
        topic = request.args.get("topic")
        items = []
        select_field = {
            "topic": FAQDetail.faq_name,
            "id": FAQDetail.id,
            "question": FAQDetail.question,
            "answer": FAQDetail.answer,
        }

        filter_by = []
        if topic:
            filter_by.append(FAQDetail.faq_name == topic)
                
        filters = (
            FAQDetail.rowstatus == 1,
            db.and_(*filter_by),
        )
        
        data = (
            FAQDetail.query.filter(*filters)
            .with_entities(*[select_field[n] for n in select_field.keys()])
            .order_by(db.asc(FAQDetail.faq_name))
        )
            
            
        for row in data.paginate(param.get("page_index"), param.get("page_size"), False).items:
            obj = dict(zip(select_field.keys(), row))
            items.append(obj)

        results = {"data": items}
        return make_response(jsonify(success_handler(results)), 200)
    except Exception as e:
        return make_response(jsonify(exception_handler(e, default_data=[])), 500)


@master_apis_blueprint.route("/faq_detail", methods=["POST", "PUT"])
@cross_origin()
def saveupdate_faq():
    try:
        if not (current_user.is_authenticated):
            return make_response(jsonify(exception_handler("not logged in", 401)), 401)
        if current_user.roles_id != 1:
            return make_response(jsonify(exception_handler('Forbidden access', 403)), 403)

        if not request.is_json:
            raise AppMessageException('please provide json data')

        data = request.get_json()

        topic_id = data.get("topic_id")
        question = data.get("question")
        answer = data.get("answer")

        if not topic_id:
            raise AppMessageException("please provide topic_id")
        if not question:
            raise AppMessageException("please provide question")
        if not answer:
            raise AppMessageException("please provide answer")
        
        known_faq = FAQ.query.filter_by(id=topic_id).first()
        if not known_faq:
            raise AppMessageException(f"topic with id:{topic_id} is not found")
        
        id = data.get("id")

        if id:  # update
            known_faqdetail = FAQDetail.query.filter_by(id=id).first()
            if known_faqdetail:
                pass
            else:
                raise AppMessageException("invalid FAQDetail id: data not found")
        else:  # insert
            known_faqdetail = FAQDetail()
            known_faqdetail.rowstatus = 1
            known_faqdetail.created_by = current_user.username
            known_faqdetail.created_date = get_wib_date()

        known_faqdetail.faq_id = topic_id
        known_faqdetail.faq_name = known_faq.name
        known_faqdetail.question = question
        known_faqdetail.answer = answer

        known_faqdetail.modified_by = current_user.username
        known_faqdetail.modified_date = get_wib_date()

        db.session.add(known_faqdetail)
        db.session.commit()

        results = {
            "topic": known_faq.name,
            "question": known_faqdetail.question,
            "answer": known_faqdetail.answer,
        }

        return make_response(
            jsonify(success_handler({"data": results})), 200
        )
    except Exception as e:
        return make_response(jsonify(exception_handler(e)), 500)


@master_apis_blueprint.route("/faq_detail", methods=["DELETE"])
@cross_origin()
def delete_faq():
    try:
        if not (current_user.is_authenticated):
            return make_response(jsonify(exception_handler("not logged in", 401)), 401)
        if current_user.roles_id != 1:
            return make_response(jsonify(exception_handler('Forbidden access', 403)), 403)
        
        id = request.args.get("id")
        if not id:
            raise AppMessageException("Please provide id to be deleted")

        
        known_faqdetail = FAQDetail.query.filter_by(id=id).first()
        if not known_faqdetail:
            raise AppMessageException('invalid FAQ id: data not found')
        if not known_faqdetail.rowstatus:
            raise AppMessageException('data with given id has been deleted')
        known_faqdetail.rowstatus = 0
        known_faqdetail.modified_by = current_user.username
        known_faqdetail.modified_date = get_wib_date()

        db.session.add(known_faqdetail)
        db.session.commit()
        
        return make_response(jsonify(success_handler({'data': {}})), 200)
    except Exception as e:
        return make_response(jsonify(exception_handler(e, default_data=[])), 500)