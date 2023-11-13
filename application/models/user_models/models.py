# application/models/user_models/models.py
from ... import db
from datetime import datetime
from flask_login import UserMixin
from passlib.hash import sha256_crypt
import uuid

import os

from datetime import timedelta
from ...utils import get_wib_date, map_attr

class Account(UserMixin, db.Model):
    __tablename__ = 'user_account'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(36), unique=True, default=uuid.uuid4)
    first_name = db.Column(db.String(256), nullable=False)
    last_name = db.Column(db.String(256), nullable=True)
    email = db.Column(db.String(128), nullable=False, index=True)
    
    username = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256), unique=False, nullable=False)

    roles_id = db.Column(db.Integer, db.ForeignKey('user_roles.id'))
    # roles_name = db.Column(db.String(256), db.ForeignKey('user_roles_id'))
    roles = db.relationship('Roles', back_populates='account')

    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)
    # is_verified = db.Column(db.Integer, default=0)
    authenticated = db.Column(db.Boolean, default=False)

    customer_uid = db.Column(db.String(256), index=True, nullable=False)
    customer_code = db.Column(db.String(20), index=True, nullable=False)

    # is_active = db.Column(db.Boolean, default=True)

    # country_code = db.Column(db.String(5), nullable=False)
    # city = db.Column(db.String(128), nullable=False)

    # phone_number = db.Column(db.String(16), nullable=False)
    # company_name = db.Column(db.String(256), nullable=False)
    # company_position = db.Column(db.String(256), nullable=False)

    # linkedin_url = db.Column(db.String(256), nullable=True)
    # facebook_url = db.Column(db.String(256), nullable=True)

    api_key = db.Column(db.String(255), unique=True, nullable=True)
    api_key_expires = db.Column(db.DateTime, default=get_wib_date)

    reject_reason = db.Column(db.Text(64000), nullable=True)

    rowstatus = db.Column(db.Integer, default=1)
    created_by = db.Column(db.String(100), nullable=True)
    created_date = db.Column(db.DateTime, default=get_wib_date)
    modified_by = db.Column(db.String(100), nullable=True)
    modified_date = db.Column(db.DateTime, onupdate=get_wib_date)

    # pp_url = db.Column(db.String(1000), nullable=True)

    # access_user = db.relationship('AccessUser', back_populates='account')
    # auction_account = db.relationship('AuctionAccount', back_populates='account')

    def encode_api_key(self):
        self.api_key = sha256_crypt.hash(self.username + str(get_wib_date))
        self.api_key_expires = datetime.utcnow() + timedelta(hours=7) + timedelta(hours=24)

    def encode_password(self):
        self.password = sha256_crypt.hash(self.password)

    def __repr__(self):
        return '<User %r>' % (self.username)

    def to_json(self, attr=[]):
        if attr:
            return map_attr(self, attr, nullify=['password', 'is_admin', 'authenticated', 'api_key'])
        
        return {
            'uid': self.uid,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            
            'username': self.username,

            'roles_id': self.roles_id,
            'roles': self.roles.to_json(attr=['name']),

            'is_admin': self.is_admin,
            'is_active': self.is_active,
            # 'is_verified': self.is_verified,
            'authenticated': self.authenticated,

            'customer_uid': self.customer_uid,
            'customer_code': self.customer_code,
            # 'is_active': self.is_active,

            # 'country_code': self.country_code,
            # 'city': self.city,

            # 'phone_number': self.phone_number,
            # 'company_name': self.company_name,
            # 'company_position': self.company_position,

            # 'linkedin_url': self.linkedin_url,
            # 'facebook_url': self.facebook_url,

            # 'pp_url': self.pp_url,

            'reject_reason': self.reject_reason,
        }

class Roles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    account = db.relationship('Account', back_populates='roles')
    # access_roles = db.relationship('AccessRoles', back_populates='roles')

    rowstatus = db.Column(db.Integer, default=1)
    created_by = db.Column(db.String(100), nullable=True)
    created_date = db.Column(db.DateTime, default=get_wib_date)
    modified_by = db.Column(db.String(100), nullable=True)
    modified_date = db.Column(db.DateTime, onupdate=get_wib_date)

    def to_json(self, attr=[]):
        if attr:
            return map_attr(self, attr)
        
        return {
            'id': self.id,
            'name': self.name,
        }

# class AccessUser(db.Model):
#     __tablename__ = 'user_access_user'
#     id = db.Column(db.Integer, primary_key=True)
    
#     account_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=False, index=True)
#     account = db.relationship('Account', back_populates='access_user')

#     # services_id = db.Column(db.Integer, db.ForeignKey('master_services.id'), nullable=False, index=True)
#     # services = db.relationship('Services', back_populates='access_user')

#     web_menu_id = db.Column(db.Integer, db.ForeignKey('menu_web_menu.id'), nullable=False, index=True)
#     web_menu = db.relationship('WebMenu', back_populates='access_user')
    
#     action_id = db.Column(db.Integer, db.ForeignKey('master_dictionary.id'), nullable=False, index=True)
#     action = db.relationship('Dictionary', back_populates='access_user')

#     allow = db.Column(db.Boolean, default=False)

#     def to_json(self, attr=[]):
#         if attr:
#             return map_attr(self, attr)
        
#         return {
#             'id': self.id,

#             'account_id': self.account_id,
#             'account': self.account.to_json(attr=['uid', 'first_name', 'last_name', ]),

#             # 'services_id': self.services_id,
#             # 'services': self.services.to_json(attr=['uid', 'code', 'name']),
            
#             'web_menu_id': self.web_menu_id,
#             'web_menu': self.web_menu.to_json(attr=['id', 'name', 'slug', 'url', 'parent.id', 'parent.name']),

#             'action_id': self.action_id,
#             'action': self.action.to_json(attr=['id', 'code', 'name']),
            
#             'allow': self.allow,

#         }

# class AccessRoles(db.Model):
#     __tablename__ = 'user_access_roles'
#     id = db.Column(db.Integer, primary_key=True)
    
#     roles_id = db.Column(db.Integer, db.ForeignKey('user_roles.id'), nullable=False, index=True)
#     roles = db.relationship('Roles', back_populates='access_roles')

#     # services_id = db.Column(db.Integer, db.ForeignKey('master_services.id'), nullable=False, index=True)
#     # services = db.relationship('Services', back_populates='access_roles')

#     web_menu_id = db.Column(db.Integer, db.ForeignKey('menu_web_menu.id'), nullable=False, index=True)
#     web_menu = db.relationship('WebMenu', back_populates='access_roles')
    
#     action_id = db.Column(db.Integer, db.ForeignKey('master_dictionary.id'), nullable=False, index=True)
#     action = db.relationship('Dictionary', back_populates='access_roles')

#     allow = db.Column(db.Boolean, default=False)

#     def to_json(self, attr=[]):
#         if attr:
#             return map_attr(self, attr)
        
#         return {
#             'id': self.id,

#             'roles_id': self.roles_id,
#             'roles': self.roles.to_json(attr=['id', 'name', ]),

#             # 'services_id': self.services_id,
#             # 'services': self.services.to_json(attr=['uid', 'code', 'name']),

            
#             'web_menu_id': self.web_menu_id,
#             'web_menu': self.web_menu.to_json(attr=['id', 'name', 'slug', 'url', 'parent.id', 'parent.name']),

#             'action_id': self.action_id,
#             'action': self.action.to_json(attr=['id', 'code', 'name']),
            
#             'allow': self.allow,

#         }

