from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields, Namespace
from app.data import db_session
from app.data.users import User
from app.data.competitions import Comps

# Настройка приложения и Swagger
app = Flask(__name__)
app.config['SECRET_KEY'] = 'RETRACTED'

# Настройка Swagger через Flask-RESTX
api = Api(app, version='1.0', title='Competition API', description='User registration, login, competition management', doc='/swagger')

# Пространство имен для маршрутов
ns = Namespace('api', description='User registration and competition management')

# Описание моделей для Swagger
register_model = api.model('RegisterUser', {
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'name': fields.String(required=True, description='Nickname of the user')
})

login_model = api.model('LoginUser', {
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

competition_model = api.model('CreateCompetition', {
    'name': fields.String(required=True, description='Competition name'),
    'prize': fields.String(required=True, description='Prize'),
    'participantsCount': fields.Integer(required=True, description='Participants count'),
    'location': fields.String(required=True, description='Competition location'),
    'sport': fields.String(required=True, description='Sport type'),
    'nickname': fields.String(required=True, description='Organizer\'s nickname')
})

response_model = api.model('Response', {
    'success': fields.String(description='Success message'),
    'error': fields.String(description='Error message')
})

competition_response = api.model('Competition', {
    'id': fields.Integer(description='Competition ID'),
    'title': fields.String(description='Competition title'),
    'prize': fields.String(description='Prize'),
    'participantsCount': fields.Integer(description='Number of participants'),
    'place': fields.String(description='Location'),
    'sport': fields.String(description='Sport type')
})

api.add_namespace(ns)

@ns.route('/reg')
class RegisterUser(Resource):
    @ns.expect(register_model)
    @ns.response(200, 'Success', response_model)
    def post(self):
        dict_obj = request.json
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter_by(email=dict_obj['email']).first()
        if user:
            return {'error': 'user with such email already exist'}, 400
        user = db_sess.query(User).filter_by(nickname=dict_obj['name']).first()
        if user:
            return {'error': 'user with such nickname already exist'}, 400
        user = User(
            email=dict_obj['email'],
            hashed_password=hash(dict_obj['password']),
            is_admin=False,
            nickname=dict_obj['name']
        )
        db_sess.add(user)
        db_sess.commit()
        return {'success': 'OK'}, 200

@ns.route('/sign')
class LoginUser(Resource):
    @ns.expect(login_model)
    @ns.response(200, 'Success', response_model)
    def post(self):
        dict_obj = request.json
        if not dict_obj:
            return {'error': 'email and password are required'}, 400
        elif 'email' not in dict_obj:
            return {'error': 'email is required'}, 400
        elif 'password' not in dict_obj:
            return {'error': 'password is required'}, 400
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter_by(email=dict_obj['email']).first()
        if not user or not user.hashed_password == hash(dict_obj['password']):
            return {'error': 'invalid email or password'}, 400
        return {'success': 'OK'}, 200


@ns.route('/makecompete')
class CreateCompetition(Resource):
    @ns.expect(competition_model)
    @ns.response(200, 'Success', response_model)
    def post(self):
        dict_obj = request.json
        db_sess = db_session.create_session()
        comp = Comps(
            title=dict_obj['name'],
            prize=dict_obj['prize'],
            participantsCount=dict_obj['participantsCount'],
            place=dict_obj['location'],
            sport=dict_obj['sport']
        )
        user = db_sess.query(User).filter_by(nickname=dict_obj['nickname']).first()
        if not user:
            return {'error': 'user is not authorized'}, 400
        db_sess.add(comp)
        db_sess.commit()
        return {'success': 'OK'}, 200

@ns.route('/comps')
class GetCompetitions(Resource):
    @ns.marshal_list_with(competition_response)
    def get(self):
        db_sess = db_session.create_session()
        comps = db_sess.query(Comps).all()
        return comps, 200


@app.route('/champs')
def kokui():
    competitions = {
        "sport": "Бокс Строитель",
        "first": "Петр Иванов",
        "second": "Сергей Грушев"
    }
    return {'data': competitions}

def main():
    db_session.global_init("db/database.db")
    app.run(host="0.0.0.0", port=8000)

if __name__ == '__main__':
    main()
