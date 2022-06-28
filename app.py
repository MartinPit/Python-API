from flask import Flask, request, jsonify

from database import db, new_id
from models import Post
from validators import valid_id, valid_userId, valid_title, valid_body
from requests import get

external_URL = "https://jsonplaceholder.typicode.com"
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db.init_app(app)


@app.route('/')
def hello_world():  # put application's code here
    return "In progress"


@app.route('/posts', methods=['GET'])
def get_posts():
    args = request.args

    output = []
    if 'id' in args:
        return get_post(args['id'])
    elif 'userId' in args:
        posts = Post.query.filter_by(userId=args['userId']).all()
    else:
        posts = Post.query.all()

    for post in posts:
        output.append(post.__repr__())

    return jsonify(output)


@app.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    if not valid_id(id):
        return {}

    post = Post.query.filter_by(id=id).first()
    if post is None:
        post = get(external_URL + "/posts/" + str(id)).json()
        print(post)
        if post != {}:
            db.session.add(Post(post['id'], post['userId'], post['title'], post['body']))
            db.session.commit()
        return post

    return post.__repr__()


@app.route('/posts', methods=['POST'])
def add_post():
    id = request.json['id']
    userId = request.json['userId']
    title = request.json['title']
    body = request.json['body']

    if not valid_id(id):
        id = new_id()

    if not valid_userId(userId, external_URL) or not valid_title(title) or not valid_body(body):
        return {}

    post = Post(id, userId, title, body)
    db.session.add(post)
    db.session.commit()

    return post.__repr__()


@app.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    if post is None:
        return {}
    db.session.delete(post)
    db.session.commit()
    return {}


@app.route('/posts/<int:id>', methods=['PATCH'])
def update_post(id):
    post_data = request.get_json()
    post = Post.query.filter_by(id=id).first()
    if post is None:
        return "Post not found"
    post.title = post_data['title']
    post.body = post_data['body']
    db.session.commit()
    return "Post updated"


if __name__ == '__main__':
    app.run()
