from logging import FileHandler, WARNING

from flask import Flask, jsonify
from models import User, Stories, db, StoriesSchema, UserSchema

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_task_1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


if not app.debug:
    log_file = FileHandler('errorlog.txt')
    log_file.setLevel(WARNING)
    app.logger.addHandler(log_file)

@app.route('/user/<int:user_id>/')
def user(user_id):
    """
    http://localhost:5000/user/{userId}/ This will print json of all stories related to userId
    """
    rez_db = db.session.query(Stories).filter(Stories.user_id == user_id).all()
    user = db.session.query(User).filter(User.user_id == user_id).first()
    if len(rez_db) == 0 and user is None:
        return {"message": "User could not be found."}, 400
    stories_schema = StoriesSchema(many=True)
    user_data = UserSchema()
    result = {'user': user_data.dump(user), 'stories': stories_schema.dump(rez_db)}
    return jsonify(result)



@app.route('/story/<int:id>/')
def story(id):
    """
    http://localhost:5000/story/{id}/ This will print json of specific story id.
    """
    rez_db = db.session.query(Stories).get(id)
    if rez_db is None:
        return {"message": "Story could not be found."}, 400
    else:
        stories_schema = StoriesSchema()
        return jsonify(stories_schema.dump(rez_db))


@app.route('/title/<data>/')
def title(data):
    """
    http://localhost:5000/title/{title}/ This will return all titles containing the data in the title.
    """
    rez_db = [i for i in db.session.query(Stories).all() if data in i.title]
    if len(rez_db) == 0:
        return {"message": "Title could not be found."}, 400
    else:
        stories_schema = StoriesSchema(many=True)
    return jsonify(stories_schema.dump(rez_db))


if __name__ == "__main__":
    app.run()
