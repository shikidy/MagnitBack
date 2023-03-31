from flask import Flask
from flask import jsonify
from flask import make_response
from flask_cors import CORS
from flask import flash, redirect, request, session
from decorators import is_logged, insert_checker
from functools import wraps

from secret import SECRET_CONFIG, DOMAIN
from routes import shikidy_route


app = Flask(__name__)
app.register_blueprint(blueprint=shikidy_route)
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = SECRET_CONFIG
app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True, SECURE=True)
# app.config['SERVER_NAME'] = DOMAIN
app.config['APPLICATION_ROOT'] = '/'
app.config['SESSION_COOKIE_DOMAIN'] = False



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)