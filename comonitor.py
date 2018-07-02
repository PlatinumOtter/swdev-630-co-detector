from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine

db_connect = create_engine('sqlite:///comonitor.db')
app = Flask(__name__)
api = Api(app)


class Alerts(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from alerts")
        return {'rules': [i for i in query.cursor.fetchall()]}

    def post(self):
        conn = db_connect.connect()
        print(request.json)
        Users = request.json['User']
        for user in Users:
            EnvParam = request.json['EnvParam']
            Threshold = request.json['Threshold']
            query = conn.execute("insert into alerts values('{0}','{1}','{2}', null, null)"
                                 .format(user, EnvParam, Threshold))
        return {'status': 'success'}

    def delete(self):
        conn = db_connect.connect()
        print(request.json)
        Users = request.json['User']
        for user in Users:
            EnvParam = request.json['EnvParam']
            Threshold = request.json['Threshold']
            query = conn.execute("delete from alerts where User='{0}' and EnvParam='{1}' and Threshold='{2}'"
                                 .format(user, EnvParam, Threshold))
        return {'status': 'success'}


class User_Alerts(Resource):
    def get(self, username):
        conn = db_connect.connect()
        query = conn.execute(
            "select EnvParam, RegValue, Threshold, Timestamp from alerts where User = \'" + username + "\';")
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)


class Update_Alerts(Resource):
    def post(self, param):
        conn = db_connect.connect()
        print(request.json)
        Reading = request.json['RegValue']
        query = conn.execute(
            "update alerts set RegValue='{0}', Timestamp=datetime() where EnvParam='{1}';".format(Reading, param))
        return {'status': 'success'}


api.add_resource(Alerts, '/alerts')
api.add_resource(User_Alerts, '/alerts/<username>')
api.add_resource(Update_Alerts, '/update/<param>')

if __name__ == '__main__':
    app.run(port=5000)
