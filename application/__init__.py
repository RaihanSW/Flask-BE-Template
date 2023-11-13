# application/__init__.py
import config
import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    cors = CORS(app)
    environment_configuration = os.environ['CONFIGURATION_SETUP']
    app.config.from_object(environment_configuration)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['RESTX_MASK_SWAGGER'] = False

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        # from .apis import api_blueprint
        # app.register_blueprint(api_blueprint, url_prefix='/' if os.environ.get('DEPLOY_PLATFORM') != 'DEV' else '/api')
        
        
        # from .apis.karyawan_apis import karyawan_apis_blueprint
        # app.register_blueprint(karyawan_apis_blueprint, url_prefix='/karyawan')
        
        from .apis.user_apis import user_apis_blueprint
        app.register_blueprint(user_apis_blueprint, url_prefix='/users')

        from .apis.master_apis import master_apis_blueprint
        app.register_blueprint(master_apis_blueprint, url_prefix='/masters')

        return app


# # application/__init__.py
# import config
# import os
# from flask import Flask
# from flask_login import LoginManager
# from flask_sqlalchemy import SQLAlchemy

# from flask_cors import CORS

# db = SQLAlchemy()
# login_manager = LoginManager()

# def create_app():
#     app = Flask(__name__)
#     cors = CORS(app)
#     environment_configuration = os.environ['CONFIGURATION_SETUP']
#     app.config.from_object(environment_configuration)
#     app.config['CORS_HEADERS'] = 'Content-Type'
#     app.config['RESTX_MASK_SWAGGER'] = False

#     db.init_app(app)
#     login_manager.init_app(app)

#     with app.app_context():
#         # Register blueprints
#         from .apis.user_apis import user_apis_blueprint
#         app.register_blueprint(user_apis_blueprint, url_prefix='/users')
#         # app.register_blueprint(user_apis_blueprint, url_prefix='/' if os.environ.get('DEPLOY_PLATFORM') != 'DEV' else '/users')

#         from .apis.master_apis import master_apis_blueprint
#         app.register_blueprint(master_apis_blueprint, url_prefix='/masters')

#         from .apis.auction_apis import auction_apis_blueprint
#         app.register_blueprint(auction_apis_blueprint, url_prefix='/auctions')

#         from .apis.email_apis import email_apis_blueprint
#         app.register_blueprint(email_apis_blueprint, url_prefix='/emails')

#         return app
