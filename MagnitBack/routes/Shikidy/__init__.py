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
from decorators import is_logged, insert_checker


shikidy_route = Blueprint('shikidy', __name__, subdomain='shikidy')
CORS(shikidy_route,  supports_credentials=True)
db = DbWorker('magnit')

#region Login
@shikidy_route.route('/role')
def get_role():
    return jsonify({'role' : session['role']})
@shikidy_route.route('/login')
@insert_checker('login', 'password')
def login():
    login = request.args.get('login')
    password = request.args.get('password')

    user = db.get_user_by_log_pas(login, password)
    print(session)
    if not user:
        return jsonify({
                'is_error' : True,
                'error_texts' : ['Login or password invalid']
            })
    session.clear()
    session['logged'] = user['id']
    session['role'] = user['role']
    session.permanent = True
    session.modified = True
    return jsonify({
            'is_error' : False,
            'error_texts' : [],
            'role' : user['role']
        })
#endregion

#region projects
@shikidy_route.route("/projects", methods=['GET'])
def get_project_list():
    projects = db.get_projects()
    to_json = []
    for el in projects:
        to_json.append(dict(
            id=el['id'],
            name=el['name']
        ))
    return jsonify(to_json)

@shikidy_route.route('/project_add', methods=['GET'])
@insert_checker('name')
def add_project():
    db.create_project(0, request.args.get('name'))
    return jsonify({
            'is_error' : False,
            'error_texts' : []
        })

@shikidy_route.route('/project_remove', methods=['GET'])
@insert_checker('id')
def del_project():
    db.delete_project(request.args.get('id'))
    return jsonify({
            'is_error' : False,
            'error_texts' : []
        })



#endregion

#region Area
@shikidy_route.route("/areas", methods=['GET'])
@insert_checker('project_id')
def get_areas_list():
    areas = db.get_areas_by_project(request.args.get('project_id'))
    to_json = []
    for el in areas:
        to_json.append(dict(
            id=el['id'],
            name=el['name']
        ))
    return jsonify(to_json)


@shikidy_route.route("/create_area", methods=['GET'])
@insert_checker('project_id', 'name')
def add_area():
    db.create_area(request.args.get('project_id'), request.args.get('name'))
    return jsonify({
            'is_error' : False,
            'error_texts' : []
        })

@shikidy_route.route("/area_remove", methods=['GET'])
@insert_checker('id')
def dek_area():
    db.delete_area(request.args.get('id'))
    return jsonify({
            'is_error' : False,
            'error_texts' : []
        })
#endregion

#region Lines
@shikidy_route.route("/lines", methods=['GET'])
@insert_checker('area_id')
def get_lines_list():
    lines = db.get_lines_by_area(request.args.get('area_id'))
    to_json = []
    for el in lines:
        to_json.append(dict(**el
        ))
    return jsonify(to_json)
#endregion

#region Points
@shikidy_route.route('/points', methods=['GET'])
@is_logged
@insert_checker('line_id')
def points_list():
    points = db.get_points_by_line(request.args.get('line_id'))
    to_json = []
    for el in points:
        to_json.append(dict(**el
        ))
    return jsonify(to_json)
#endregion



#region Poin_Result
@shikidy_route.route('/result_points', methods=['GET'])
@is_logged
@insert_checker('point_id')

def point_list():
    points = db.result_by_point(request.args.get('point_id'))
    to_json = []
    for el in points:
        to_json.append(dict(**el
        ))
    return jsonify(to_json)

@shikidy_route.route('/points_by_area', methods=['GET'])
@insert_checker('area_id')
def all_points():
    points = db.get_all_points_by_area(request.args.get('area_id'))
    res = []
    for el in points:
        res.append(el)
    return jsonify(res)
#endregion