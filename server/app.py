from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages')
def messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    message_dict =[ message.to_dict() for message in messages]
    response = make_response(
        jsonify(message_dict),
        200,
    )
    return response

@app.route('/messages/<int:id>')
def messages_by_id(id):
    return ''

@app.post('/messages')
def create_message():
    #get the JSON data from the request body
    data = request.get_json()
    
    #create a new Message instance
    New_message = Message(
        body=data['body'],
        username=data['username'],
    )
    try:
        #save the new Message to the database
        db.session.add(New_message)
        db.session.commit()
    except Exception as e:
        db.session.rollback() #rollbakc in case of an error
        return jsonify({"error": "An error occurred while creating the message"}), 500
    
    #return the response with the newly created message
    # response = {
    #     "id": New_message.id,
    #     "body": New_message.body,
    #     "Username": New_message.username,
    #     "created_at": New_message.created_at.isoformat() #isoformat is used to convert the objects into standardized string format
    # }
    return jsonify(New_message.to_dict()), 200

@app.patch('/messages/<int:id>')
def update_message(id):
    
    # message = Message.query.filter(Message.id == id).first()
    message = db.session.get(Message, id)
    
    if message is None:
        return jsonify({"error": "Message not found"}), 400
    
    #get the json data from the request body
    data = request.get_json()
    
    #update the body of the message
    message.body = data['body']
    
    
    try:
        #save the changes to the database
        db.session.commit()
    except Exception as e:
        db.session.rollback() #Rollback if there is an error
        return jsonify({"error": "An error occurred while updating the message body"}), 500
    
    #return the response with the updated message
    return jsonify(message.to_dict()), 200

@app.delete('/messages/<int:id>')
def delete_message(id):
    
    message = db.session.get(Message, id)
    
    if message is None:
        return jsonify({"error": "Message not found"}), 400
    
    try:
        #delete the message from the database
        db.session.delete(message)
        db.session.commit()
    except Exception as e:
        db.session.rollback() #Rollback is there is an error that accuured
        return jsonify({"error": "There was an error trying to delete the message"})
    
    return jsonify({"Success": "The message was successfully deleted"})
    

if __name__ == '__main__':
    app.run(port=5555)
