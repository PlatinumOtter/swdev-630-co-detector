from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

db_connect = create_engine('sqlite:///comonitor.db')
app = Flask(__name__)
api = Api(app)


class Rules(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from alerts")
        return {'rules': [i for i in query.cursor.fetchall()]}

    def post(self):
        conn = db_connect.connect()
        print(request.json)
        User = request.json['User']
        EnvParam = request.json['EnvParam']
        Threshold = request.json['Threshold']
        query = conn.execute("insert into alerts values(null,'{0}','{1}','{2}')"
                             .format(User, EnvParam, Threshold))
        return {'status': 'success'}


class User_Alerts(Resource):
    def get(self, username):
        conn = db_connect.connect()
        query = conn.execute("select EnvParam, RegValue, Threshold, Timestamp from alerts where User = \'" + username + "\';")
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)


api.add_resource(Rules, '/rules')
api.add_resource(User_Alerts, '/rules/<username>')

if __name__ == '__main__':
    app.run(port=5002)