from flask import Flask
from flask import jsonify
from flask import make_response
from flask import session
from flask_cors import CORS
from flask import flash, redirect, request
from functools import wraps



def is_logged(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # if not 'logged' in session.keys():
        #     flash('Login Expired')
        #     return jsonify({'is_error': True, 'error_texts': ['Login Expired']}), 403
        return func(*args, **kwargs)
    return decorated_function    


def insert_checker(*values_tags: tuple):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            err_response = {
                'is_error' : False,
                'error_texts' : []
            }
            for value in values_tags:
                if not value in request.args.keys():
                    err_response['error_texts'].append(f'{value} expected')
                elif len(request.args.get(value)) == 0:
                    err_response['error_texts'].append(f'{value} empty value')
                elif len(request.args.get(value)) > 10:
                    err_response['error_texts'].append(f'{value} more than 10')
                
            if err_response['error_texts']:
                err_response['is_error'] = True
                return jsonify(err_response), 400
            try:
                return  function(*args, **kwargs)
            except Exception as err:
                print(err)
                return jsonify({'is_error': True, 'error_texts': ['Error on request']}), 400
        return wrapper
    return decorator


def role_checker(role: str):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            err_response = {
                'is_error' : False,
                'error_texts' : []
            }
        
            if not 'role' in session.keys():
                err_response['error_texts'].append('Login error')
            
            elif session['role'] != role:
                err_response['error_texts'].append('Role doesnt match')

            if err_response['error_texts']:
                err_response['is_error'] = True
                return jsonify(err_response), 403
            try:
                return  function(*args, **kwargs)
            except:
                return jsonify({'is_error': True, 'error_texs': ['Unknown err']})
        return wrapper
    return decorator
