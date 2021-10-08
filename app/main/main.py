from flask import Flask, request, Response
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class Redact(Resource):
    def get(self):
        return {'message': "hello"}, 200  # return data and 200 OK

    def post(self):

        if request.content_type != 'application/pdf':
            return {'message': 'Not a valid document format'}, 415  # return error and 415 Unsupported Media Type
        else:
            pdf = request.data
            return Response(pdf, mimetype='application/pdf')
            #return {"Post Redact": 'You did it'}, 200  # return data with 200 OK


api.add_resource(Redact, '/redact')

if __name__ == '__main__':
    app.run()
