#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

AUTH_TYPE = os.getenv("AUTH_TYPE")

# check the Auth_TYPE
if AUTH_TYPE == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()


@app.before_request
def before_request():
    """
        _summary_

    Returns:
        _type_: _description_
    """
    if auth is None:
        pass
    else:
        excluded_list == ['/api/v1/status/',
                            '/api/v1/unauthorized/', '/api/v1/forbidden/']

        if auth.require_auth(request.path, excluded_list):
            if auth.authorization_header(request) is None:
                abort(401, description ="Unautorized")
            if auth.current_user(request) is None:
                abort(403, description='Forbidden')


@app.errorhandler(401)
def unauthorised(error) -> str:
    """ Unauthorised handler
    """
    return jsonify({"error": "Unauthorized"}), 401


def forbidden(error) -> str:
    """_summary_

    Args:
        error (_type): _description_

    Returns:
        str: _description_
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
