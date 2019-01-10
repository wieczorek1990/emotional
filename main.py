import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from fbmessenger import BaseMessenger

from chatbot import Chatbot
from mood import Mood, MOOD_NEUTRAL


app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/emotional.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    messenger_id = db.Column(db.String(16), unique=True, nullable=False)
    mood = db.Column(db.String(16), nullable=False)

    def __repr__(self):
        return '<User {} {} {}>'.format(self.id, self.messenger_id, self.mood)


db.create_all()


class Messenger(BaseMessenger):
    def __init__(self, page_access_token):
        self.page_access_token = page_access_token
        super(Messenger, self).__init__(self.page_access_token)

    @staticmethod
    def get_current_mood(sender_id):
        user = User.query.filter_by(messenger_id=sender_id).first()
        if user:
            return user.mood
        else:
            return MOOD_NEUTRAL

    @staticmethod
    def get_mood(sender_id, text):
        user = User.query.filter_by(messenger_id=sender_id).first()
        message_mood = Mood().get(text)
        if user:
            next_mood = Mood.get_next(user.mood, message_mood)
            user.mood = next_mood
        else:
            user = User(messenger_id=sender_id, mood=message_mood)
            db.session.add(user)
        db.session.commit()
        return user.mood

    def message(self, message):
        text = message['message']['text']
        sender_id = message['sender']['id']

        if text != 'mood':
            mood = self.get_mood(sender_id, text)
            response_text = Chatbot.get_response(mood)
            self.send({'text': response_text}, 'RESPONSE')
        else:
            mood = self.get_current_mood(sender_id)
            self.send({'text': mood}, 'RESPONSE')

    def delivery(self, message):
        pass

    def read(self, message):
        pass

    def account_linking(self, message):
        pass

    def postback(self, message):
        pass

    def optin(self, message):
        pass


messenger = Messenger(os.environ.get('FB_PAGE_TOKEN'))


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if (request.args.get('hub.verify_token') == os.environ.get('FB_VERIFY_TOKEN')):
            return request.args.get('hub.challenge')
        raise ValueError('FB_VERIFY_TOKEN does not match.')
    elif request.method == 'POST':
        messenger.handle(request.get_json(force=True))
    return ''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
