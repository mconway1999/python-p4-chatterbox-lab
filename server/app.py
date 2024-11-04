from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message
import ipdb 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET','POST'])
def messages():
    if request.method == 'GET':
        get_messages = Message.query.all()
        response_body=[message.to_dict() for message in get_messages]
        return response_body
    elif request.method == "POST":
        body_data=request.json.get('body')
        username_data = request.json.get('username')
        new_message = Message(body=body_data, username=username_data)
        db.session.add(new_message)
        db.session.commit()
        response_body = new_message.to_dict()
        return response_body, 201
       
        

   
@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = db.session.get(Message, id)
    if request.method == "PATCH":
        for attr in request.json:
           setattr(message, attr, request.json.get(attr))
        db.session.commit()
        response_body=message.to_dict()
        return response_body, 200
    elif request.method == "DELETE":
        db.session.delete(message)
        db.session.commit()
        return make_response({}, 204)

    

if __name__ == '__main__':
    app.run(port=5555, debug = False)
