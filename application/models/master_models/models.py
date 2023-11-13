# application/models/master_models/models.py
from ... import db
from datetime import datetime
import uuid

import os
from ...utils import get_wib_date, map_attr


class FAQ(db.Model):
    __tablename__ = "master_faq"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    faq_detail = db.relationship("FAQDetail", back_populates="faq")

    rowstatus = db.Column(db.Integer, default=1)
    created_by = db.Column(db.String(100), nullable=True)
    created_date = db.Column(db.DateTime, default=get_wib_date)
    modified_by = db.Column(db.String(100), nullable=True)
    modified_date = db.Column(db.DateTime, onupdate=get_wib_date)

    def to_json(self, attr=[]):
        if attr:
            return map_attr(self, attr)

        return {
            "name": self.name,
        }


class FAQDetail(db.Model):
    __tablename__ = "master_faq_detail"
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    faq_name = db.Column(db.String(128), nullable=True)

    faq_id = db.Column(db.Integer, db.ForeignKey("master_faq.id"))
    faq = db.relationship("FAQ", back_populates="faq_detail")

    rowstatus = db.Column(db.Integer, default=1)
    created_by = db.Column(db.String(100), nullable=True)
    created_date = db.Column(db.DateTime, default=get_wib_date)
    modified_by = db.Column(db.String(100), nullable=True)
    modified_date = db.Column(db.DateTime, onupdate=get_wib_date)

    def to_json(self, attr=[]):
        if attr:
            return map_attr(self, attr)

        return {
            "faq_name": self.faq_name,
            "question": self.question,
            "answer": self.answer,
        }


# class Category(db.Model):
#     __tablename__ = "master_category"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(128), unique=True, nullable=False)
    

#     rowstatus = db.Column(db.Integer, default=1)
#     created_by = db.Column(db.String(100), nullable=True)
#     created_date = db.Column(db.DateTime, default=get_wib_date)
#     modified_by = db.Column(db.String(100), nullable=True)
#     modified_date = db.Column(db.DateTime, onupdate=get_wib_date)

#     def to_json(self, attr=[]):
#         if attr:
#             return map_attr(self, attr)

#         return {
#             "name": self.name,
#         }

# class Product(db.Model):
#     __tablename__ = "master_product"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(128), unique=True, nullable=False)

#     rowstatus = db.Column(db.Integer, default=1)
#     created_by = db.Column(db.String(100), nullable=True)
#     created_date = db.Column(db.DateTime, default=get_wib_date)
#     modified_by = db.Column(db.String(100), nullable=True)
#     modified_date = db.Column(db.DateTime, onupdate=get_wib_date)

#     def to_json(self, attr=[]):
#         if attr:
#             return map_attr(self, attr)

#         return {
#             "name": self.name,
#         }