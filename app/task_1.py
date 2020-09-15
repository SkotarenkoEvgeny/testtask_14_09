import requests
import json


from app import app
from models import db, User, Stories

app.app_context().push()
db.init_app(app)
db.create_all()

for id in range(1, 100):
    url = f'https://jsonplaceholder.typicode.com/todos/{id}'
    response = requests.get(url).json()
    user = db.session.query(User).filter(User.user_id == int(response['userId'])).first()
    if response['completed'] is True:
        if user is None:
            db.session.add(User(user_id=int(response['userId'])))
            new_user = db.session.query(User).filter(User.user_id == int(response['userId'])).first()
            db.session.add(Stories(user_id=new_user.id, title=response['title']))
        else:
            user_id = user.id
            db.session.add(Stories(user_id=user_id, title=response['title']))

db.session.commit()
