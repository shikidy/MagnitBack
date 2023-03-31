from flask import Flask
from flask import jsonify
from flask import make_response
from flask import flash, redirect, request
from flask import Blueprint
from flask import session
from flask_cors import CORS
# from flask import session
from functools import wraps

# from app import is_logged, insert_checker
from .db import DbWorker
from decorators import is_logged, insert_checker, role_checker


wl_route = Blueprint('well-logging', __name__, subdomain='well-logging')
CORS(wl_route,  supports_credentials=True)
db = DbWorker('well-logging')

#region Login
@wl_route.route('/login')
@insert_checker('login', 'password')
def login():
    login = request.args.get('login')
    password = request.args.get('password')

    user = db.get_user_by_log_pas(login, password)

    if not user:
        return jsonify({
                'is_error' : True,
                'error_texts' : ['Login or password invalid']
            })
    session.clear()
    session['logged'] = user['id_user']
    session['role'] = user['status_name']
    session.permanent = True
    session.modified = True

    data = db.get_projects_by_user(user['id_user'])
    answer = {
        'is_error' : False,
        'status' : user['status_name'],
        'projects' : []
    }
    for el in data:
        answer['projects'].append(dict(
            id=el['id_project'],
            project_name=el['project_name']
        ))
    return jsonify(answer)
#endregion

#region projects
@wl_route.route("/projects", methods=['GET'])
@is_logged
def get_project_list():
    projects = db.get_projects_by_user(session.get('logged'))
    answer = {
        'is_error' : False,
        'status' : session['role'],
        'projects' : []
    }
    for el in projects:
        answer['projects'].append(dict(
            id=el['id_project'],
            name=el['project_name']
        ))
    return jsonify(answer)

#endregion

#region Area
@wl_route.route("/areas", methods=['GET'])
@insert_checker('project_id')
@is_logged
def get_areas_list():
    areas = db.get_areas_by_project(request.args.get('project_id'))
    to_json = []
    for el in areas:
        to_json.append(dict(
            id=el['id_area'],
            name=el['area_name']
        ))
    return jsonify(to_json)
#endregion

#region Picket
@wl_route.route("/pickets", methods=['GET'])
@insert_checker('area_id')
@is_logged
def get_pickets_list():
    pickets = db.get_pickets_by_area(request.args.get('area_id'))
    to_json = []
    for el in pickets:
        to_json.append(dict(
            id=el['id_picket'],
            X_picket_coord=el['x_coord'],
            Y_picket_coord=el['y_coord'],
            electric_resistance=el['electric_resistance'],
            layer_density=el['layer_density'],
            gamma_ray=el['gamma_ray'],
            magnetic_field=el['magnetic_field']
        ))
    return jsonify(to_json)
#endregion




