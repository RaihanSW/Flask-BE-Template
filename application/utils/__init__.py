from flask import render_template
from datetime import timedelta
from string import ascii_lowercase, digits
from sqlalchemy.orm.collections import InstrumentedList
from datetime import datetime
from google.cloud import storage
from PyPDF2 import PdfFileReader
from secrets import token_urlsafe

import os
import imghdr
import requests
import json, yaml
import pytz
import magic

from .handler import *

BASE_URL = os.environ.get('BASE_URL')

def get_wib_date():
    # return (datetime.utcnow() + timedelta(hours=7)).replace(tzinfo=pytz.timezone('Asia/Jakarta'))
    # return datetime.utcnow() + timedelta(hours=7)
    return datetime.utcnow()

def map_attr(data, map, nullify=[]):
    j = {}
    for n in map:
        if n in nullify: # jika ingin nullify user.password berarti input nullify user dan user.password
            continue
        s = []
        if '.' in n:
            s = n.split('.')
        if s:
            fmt = 'j{}'
            for d in range(len(s)):
                q = fmt.format(''.join(['''['{}']'''.format(s[x]) for x in range(d+1)]))
                vq = fmt.format(''.join(['''.get('{}')'''.format(s[x]) for x in range(d+1)]))
                if not eval(vq):
                    exec('{}{}'.format(q, ' = {}'))
                if d == len(s)-1:
                    exec('{}{}'.format(q, ' = {}'.format('data.{}'.format(n))))
        else:
            j[n] = eval('data.{}'.format(n))
            if type(j[n]) == InstrumentedList:
                j[n] = eval('[i.to_json() for i in data.{} if i.rowstatus==1] if data.{} else []'.format(n, n))
            elif type(j[n]) == datetime:
                j[n] = eval('(data.{}.isoformat() + ".000Z") if data.{} else None'.format(n, n))
    return j

def set_attr(attr):
    if not attr:
        return None
    a = ascii_lowercase + digits + '.,_'
    if all([n in a for n in set(attr)]):
        return [n.strip() for n in attr.split(',')]
    return None

def get_default_list_param(args, nullify_size=False):
    page_index = args.get('page_index')
    page_size = args.get('page_size')
    search_by = args.get('search_by') if args.get('search_by') else ''
    keywords = args.get('keywords') if args.get('keywords') else ''
    order_by_col = args.get('order_by_col') if args.get('order_by_col') else ''
    order_by_type = args.get('order_by_type') if args.get('order_by_type') else ''
    filter_by_col = args.get('filter_by_col') if args.get('filter_by_col') else ''
    filter_by_text = args.get('filter_by_text') if args.get('filter_by_text') else ''
    
    try:
        int(page_index)
        int(page_size)
    except:
        page_index = 1
        page_size = 9999
    
    page_index = int(page_index)
    page_size = int(page_size)

    return {
        'page_index': page_index,
        'page_size': page_size,
        'search_by': search_by[:1000],
        'keywords': keywords[:1000],
        'order_by_col': order_by_col[:1000],
        'order_by_type': order_by_type[:1000],
        'filter_by_col': filter_by_col[:1000],
        'filter_by_text': filter_by_text[:1000],
    }

def get_bucket_name():
    return os.environ.get('GCS_BUCKET_NAME')

def serialize_blob(blob):
    return {
        'blob': blob.name,
        # 'storage_class': blob.storage_class,
        # 'id': blob.id,
        'size': blob.size,
        'updated': blob.updated,
        'generation': blob.generation,
        'metageneration': blob.metageneration,
        
        # 'etag': blob.etag,
        # 'owner': blob.owner,
        'cache_control': blob.cache_control,
        'content-disposition': blob.content_disposition,
        'content-encoding': blob.content_encoding,
        'content-language': blob.content_language,
        'metadata': blob.metadata,
        'custom_time': blob.custom_time,
        
        'content-type': blob.content_type,
        'public_url': blob.public_url,
    }

def gcs_upload(dest_path, file_name, file_binary, file_type):
    storage_client = storage.Client()
    bucket = storage_client.bucket(get_bucket_name())
    # yS4mntJcL0 delivery
    # 0fGnyMYxTb customer_received
    blob = bucket.blob('{}{}'.format(dest_path, file_name))
    blob.content_type = '{}'.format(file_type)
    blob.upload_from_file(file_binary)
    blob.cache_control = 'no-cache'
    blob.make_public()
    return serialize_blob(blob)

def gcs_download_stream_images(dest_path, file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(get_bucket_name())
    blob = bucket.blob('{}{}'.format(dest_path, file_name))

    image_stream = blob.download_as_bytes()

    return image_stream

def check_file_pdf(binary):
    try:
        pdf = PdfFileReader(binary)
        info = pdf.getDocumentInfo()
        if info:
            return 'application/pdf'
        else:
            return None
    except:
        return None

def check_file_image(binary):
    accept_type = ['jpg', 'jpeg', 'png']
    file_type = imghdr.what(binary)
    if file_type not in accept_type:
        return None
    return 'image/{}'.format(file_type)

def gcs_list_files(dest_path):
    storage_client = storage.Client()
    blobs = []
    for blob in storage_client.list_blobs(get_bucket_name(), prefix=dest_path):
        blobs.append(blob)
    return blobs

# def gcs_get_latest_file(dest_path):
#     storage_client = storage.Client()
#     blobs = []
#     for blob in storage_client.list_blobs(get_bucket_name(), prefix=dest_path):
#         blobs.append(blob)
#     if blobs:
#         return max(blobs, key=lambda blob: blob.updated)
#     else:
        # return None

# def gcs_get_latest_file(dest_path, filename):
#     storage_client = storage.Client()
#     blobs = storage_client.list_blobs(get_bucket_name(), prefix=dest_path, name_contains=filename)
#     blobs = sorted(blobs, key=lambda blob: blob.time_created, reverse=True)
#     if blobs:
#         return blobs[0]
#     else:
#         return None
    
def gcs_get_latest_file(dest_path, filename):
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(get_bucket_name(), prefix=dest_path)
    # filtered_blobs = [blob for blob in blobs if blob.name.startswith(filename)]
    filtered_blobs = [blob for blob in blobs if filename in blob.name]
    sorted_blobs = sorted(filtered_blobs, key=lambda blob: blob.time_created, reverse=True)
    if sorted_blobs:
        return sorted_blobs[0]
    else:
        return None


# def check_file_excel(binary):
#     try:
#         df = pd.read_excel(files)
#     except Exception as e:
#         print(str(e))
#         raise Exception('wrong file format, please provide excel files.')

def check_file_excel(file):
    mime = magic.Magic(mime=True)
    file_type = mime.from_file(file)
    if file_type == 'application/vnd.ms-excel' or file_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        return file_type
    else:
        return None
    # return file_type == 'application/vnd.ms-excel' or file_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

def get_token(size=64):
    return token_urlsafe(size)

def send_mailgun_simple_message(to, subject, text):
    MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')
    MAILGUN_DOMAIN_NAME = os.environ.get('MAILGUN_DOMAIN_NAME')
    return requests.post(
		"https://api.mailgun.net/v3/{}/messages".format(MAILGUN_DOMAIN_NAME),
		auth=("api", MAILGUN_API_KEY),
		data={"from": "Arta Admin <mailgun@{}>".format(MAILGUN_DOMAIN_NAME),
			"to": [to,],
			"subject": subject,
			"text": text})

def send_mailgun_message(to, subject, template='base.html', data={}):
    MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')
    MAILGUN_DOMAIN_NAME = os.environ.get('MAILGUN_DOMAIN_NAME')
    return requests.post(
		"https://api.mailgun.net/v3/{}/messages".format(MAILGUN_DOMAIN_NAME),
		auth=("api", MAILGUN_API_KEY),
		data={"from": "Arta Admin <mailgun@{}>".format(MAILGUN_DOMAIN_NAME),
			"to": [to,],
			"subject": subject,
			"html": render_template(template, data=data)})

def get_swagger_yaml(request_base_url):
    url = '{}/swagger.json'.format(request_base_url)
    resp = requests.get(url)
    data = json.loads(resp.content)
    return yaml.dump(data, allow_unicode=True)